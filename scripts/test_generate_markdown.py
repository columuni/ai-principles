"""Regression checks: python -B -m unittest discover -s scripts -p "test_*.py"."""

from contextlib import redirect_stdout, redirect_stderr
from html import unescape
from io import StringIO
from pathlib import Path
import re
import unittest
from unittest.mock import patch

import generate_markdown as generator


def fixture(body, extra_head=""):
    return ('<!doctype html><html lang="en"><head>'
            '<link rel="canonical" href="https://example.com/sample.html">'
            + extra_head + '</head><body>' + body + '</body></html>')


def text(node):
    if isinstance(node, str):
        return node
    return "".join(text(child) for child in node.children)


class ConversionTests(unittest.TestCase):
    def convert(self, body):
        return generator.convert_html(fixture(body), "sample.html")

    def test_head_data_and_skip_link_are_excluded(self):
        html = fixture(
            '<a class="skip-link" href="#main-content">Skip to content</a>'
            '<main id="main-content"><h1>Heading</h1><p>Visible</p></main>',
            '<title>Metadata only</title><style>body { color: red; }</style>'
            '<script type="application/ld+json">{"name":"Metadata only"}</script>',
        )
        markdown = generator.convert_html(html, "sample.html")
        self.assertNotIn("Skip to content", markdown)
        self.assertNotIn("Metadata only", markdown)
        self.assertNotIn("color: red", markdown)
        self.assertIn("# Heading\n", markdown)
        self.assertIn('<a id="main-content"></a>', markdown)

    def test_fragment_and_relative_links_target_html(self):
        markdown = self.convert('<h1>Title</h1><p><a href="#scope">Scope</a> / '
                                '<a href="other.html">Other</a></p>')
        self.assertIn("[Scope](sample.html#scope)", markdown)
        self.assertIn("[Other](other.html)", markdown)
        self.assertIn("[HTML](https://example.com/sample.html)", markdown)

    def test_bilingual_labels_and_visible_separator(self):
        markdown = self.convert(
            '<h1>AI三原則<span lang="en">Three Principles of AI</span></h1>'
            '<nav><a href="ja.html">日本語</a>'
            '<span aria-hidden="true">/</span><a href="en.html">English</a></nav>'
        )
        self.assertIn("# AI三原則 Three Principles of AI", markdown)
        self.assertIn("[日本語](ja.html) / [English](en.html)", markdown)

    def test_break_entities_and_literal_markdown(self):
        markdown = self.convert('<p>A &amp; B<br>C &lt; D [x] *literal* _text_</p>')
        self.assertIn(r"A &amp; B<br>C &lt; D \[x\] \*literal\* \_text\_", markdown)

    def test_emphasis_does_not_add_space_before_punctuation(self):
        self.assertIn("**Strong**, *emphasis*.", self.convert(
            '<p><strong>Strong</strong>, <em>emphasis</em>.</p>'))

    def test_lists_restart_and_definition_pairs_remain_together(self):
        markdown = self.convert(
            '<ol><li>One</li><li>Two</li></ol><ol><li>Again</li></ol>'
            '<dl><div><dt>Term A</dt><dd>Definition A</dd></div>'
            '<div><dt>Term B</dt><dd>Definition B</dd></div></dl>'
        )
        self.assertIn("1. One\n2. Two\n\n1. Again", markdown)
        self.assertIn("- **Term A**: Definition A\n- **Term B**: Definition B", markdown)

    def test_unsupported_markup_and_malformed_definitions_fail(self):
        for body in ('<img src="missing.png">', '<dl><dt>Unpaired</dt></dl>',
                     '<section><p>Unclosed</section>',
                     '<h1 id="same">A</h1><p id="same">B</p>'):
            with self.subTest(body=body), self.assertRaises(ValueError):
                self.convert(body)

    def test_unsafe_links_fail_and_url_punctuation_is_encoded(self):
        for href in ("javascript:alert(1)", "//external.example/x", ""):
            with self.subTest(href=href), self.assertRaises(ValueError):
                self.convert(f'<p><a href="{href}">Link</a></p>')
        self.assertEqual(generator.destination("some (page).html#id", "sample.html"),
                         "some%20%28page%29.html#id")


class RepositoryTests(unittest.TestCase):
    def test_generated_files_match_current_html(self):
        outputs = generator.build_outputs(generator.ROOT)
        self.assertEqual(len(outputs), 5)
        for path, expected in outputs.items():
            with self.subTest(file=path.name):
                self.assertEqual(path.read_bytes(), expected.encode("utf-8"))
                self.assertTrue(expected.startswith(generator.MARKER))
                self.assertEqual(len(re.findall(r"^# ", expected, re.M)), 1)
                self.assertNotIn("\r", expected)
                self.assertNotRegex(expected, r"(?m)^ +<a id=")

    def test_all_explicit_ids_and_links_are_preserved(self):
        for name in generator.PAGES:
            html = (generator.ROOT / name).read_text(encoding="utf-8")
            body, canonical = generator.parse_page(html)
            markdown = (generator.ROOT / Path(name).with_suffix(".md")).read_text(
                encoding="utf-8")
            ids = [node.attrs["id"] for node in body.walk() if "id" in node.attrs]
            self.assertEqual(re.findall(r'<a id="([^"]+)"></a>', markdown), ids)
            links = [generator.destination(node.attrs["href"], name)
                     for node in body.walk() if node.tag == "a"
                     and "skip-link" not in node.attrs.get("class", "").split()]
            self.assertEqual(re.findall(r"\]\(([^)]+)\)", markdown), [canonical] + links)

    def test_all_paragraphs_headings_and_definition_text_remain(self):
        for name in generator.PAGES:
            body, _ = generator.parse_page(
                (generator.ROOT / name).read_text(encoding="utf-8"))
            markdown = (generator.ROOT / Path(name).with_suffix(".md")).read_text(
                encoding="utf-8")
            plain = re.sub(r"<!--[\s\S]*?-->|<[^>]*>", "", markdown)
            plain = re.sub(r"\[([^\]]*)\]\([^)]+\)", r"\1", plain)
            plain = re.sub(r"\\(.)", r"\1", plain).replace("**", "")
            normalized = re.sub(r"\s+", "", unescape(plain))
            for node in body.walk():
                if node.tag in generator.HEADINGS | {"p", "dt", "dd"}:
                    with self.subTest(file=name, tag=node.tag, content=text(node)[:30]):
                        self.assertIn(re.sub(r"\s+", "", text(node)), normalized)
            if "-agents-" in name:
                self.assertEqual(len(re.findall(r"^- \*\*.*?\*\*:", markdown, re.M)), 12)

    def test_check_is_read_only_and_reports_stale_output(self):
        outputs = generator.build_outputs(generator.ROOT)
        with patch.object(Path, "write_bytes") as write, redirect_stdout(StringIO()):
            self.assertEqual(generator.main(["--check"]), 0)
            write.assert_not_called()
        stale = dict(outputs)
        first = next(iter(stale))
        stale[first] += "\nStale content\n"
        with patch.object(generator, "build_outputs", return_value=stale), \
                patch.object(Path, "write_bytes") as write, redirect_stdout(StringIO()):
            self.assertEqual(generator.main(["--check"]), 1)
            write.assert_not_called()

    def test_unchanged_generation_does_not_write(self):
        with patch.object(Path, "write_bytes") as write, redirect_stdout(StringIO()):
            self.assertEqual(generator.main([]), 0)
            write.assert_not_called()

    def test_non_generated_outputs_are_not_overwritten(self):
        output = generator.ROOT / "index.md"
        with patch.object(generator, "build_outputs", return_value={output: "new"}), \
                patch.object(Path, "read_text", return_value="User-written Markdown"), \
                patch.object(Path, "write_bytes") as write, redirect_stderr(StringIO()):
            self.assertEqual(generator.main([]), 1)
            write.assert_not_called()


if __name__ == "__main__":
    unittest.main()
