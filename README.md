# AI Principles / AI原則

すべてのAIシステムに共通する基本原則と、自律的に行動するAIエージェントへの追加原則を示します。AIエージェントには、両方の原則が適用されます。

This site presents core principles for all AI systems and additional principles for AI agents that act autonomously. Both sets of principles apply to AI agents.

- [AI Principles / AI原則](https://columuni.github.io/ai-principles/)

人とAIが共通して参照する正式な本文は、以下のHTMLページです。

The HTML pages below contain the official texts and provide a shared reference for people and AI.

## AI三原則 / Three Principles of AI

すべてのAIシステムに共通する基本原則 / Core Principles for All AI Systems

- [日本語](https://columuni.github.io/ai-principles/three-principles-of-ai-ja.html) / [English](https://columuni.github.io/ai-principles/three-principles-of-ai-en.html)

## AIエージェント三原則 / Three Principles for AI Agents

自律的に行動するAIシステムへの追加原則 / Additional Principles for AI Systems That Act Autonomously

AIエージェントには、AI三原則とAIエージェント三原則の両方が適用されます。

Both the Three Principles of AI and the Three Principles for AI Agents apply to AI agents.

- [日本語](https://columuni.github.io/ai-principles/three-principles-of-ai-agents-ja.html) / [English](https://columuni.github.io/ai-principles/three-principles-of-ai-agents-en.html)

## ファイル構成と正本 / Files and source of truth

全5ページのHTMLを正本とし、同名のMarkdown版をHTMLから自動生成します。原則本文は日本語版を意味上の基準文とし、英語版を同じ意味を持つ公式対応版として扱います。READMEには原則本文を転載しません。

The five HTML pages are the source of truth; their Markdown versions are generated from the corresponding HTML files. The Japanese principles define the intended meaning, and the English versions are their official equivalents. This README does not duplicate the full principles.

| ページ / Page | HTML（正本 / Source） | Markdown（自動生成 / Generated） |
| --- | --- | --- |
| インデックス / Index | [HTML](index.html) | [Markdown](index.md) |
| AI三原則 / Three Principles of AI — 日本語 | [HTML](three-principles-of-ai-ja.html) | [Markdown](three-principles-of-ai-ja.md) |
| AI三原則 / Three Principles of AI — English | [HTML](three-principles-of-ai-en.html) | [Markdown](three-principles-of-ai-en.md) |
| AIエージェント三原則 / Three Principles for AI Agents — 日本語 | [HTML](three-principles-of-ai-agents-ja.html) | [Markdown](three-principles-of-ai-agents-ja.md) |
| AIエージェント三原則 / Three Principles for AI Agents — English | [HTML](three-principles-of-ai-agents-en.html) | [Markdown](three-principles-of-ai-agents-en.md) |

本文とナビゲーションは初期HTMLに含め、JavaScriptを実行しなくても利用できます。全5ページで共通の [favicon.svg](favicon.svg) と [favicon.ico](favicon.ico)（16・32・48px）を参照し、フッターに [GitHub](https://github.com/columuni/ai-principles) へのリンクを設けています。

Content and navigation are available in the initial HTML without running JavaScript. All five pages share the SVG and ICO favicons (the ICO contains 16, 32, and 48px images) and include a GitHub link in the footer.

## 構造化データ / Structured data

各HTMLの `<head>` に、機械がページの情報や関係を読み取るためのJSON-LDを記述しています。

Each HTML page includes JSON-LD in its `<head>` to describe the page and its relationships in a machine-readable format.

- `index.html`：`WebSite` と `CollectionPage` で、サイトと入口ページ、本文4ページへの関連リンクを記述します。
- 本文4ページ：`WebPage` で、タイトル・説明・URL・言語・所属サイト・対応する翻訳・関連する原則ページを記述します。

- `index.html`: `WebSite` and `CollectionPage` describe the site, the index page, and links to the four principle pages.
- The four principle pages: `WebPage` describes each page's title, description, URL, language, site membership, translation, and related principle page.

日本語版から英語版への関係は `workTranslation`、英語版から日本語版への関係は `translationOfWork` で示しています。JSON-LDはページの内容に一致する最小限の情報とし、原則本文を複製しません。ブラウザーで実行するJavaScriptではありません。

Japanese pages use `workTranslation` to reference their English versions; English pages use `translationOfWork` to reference their Japanese originals. JSON-LD contains minimal metadata consistent with the page, not a copy of the principles, and is not executable JavaScript.

## Markdown版 / Markdown versions

[生成スクリプト / Generator](scripts/generate_markdown.py) は、上表の5つのHTMLから対応するMarkdownファイルだけを生成します。生成されたMarkdownは直接編集せず、HTMLを修正して再生成します。

The generator creates only the five Markdown files listed above from their corresponding HTML pages. Edit the HTML and regenerate; do not edit the generated Markdown directly.

見出し・原則本文・注意書き・補助定義・ナビゲーション・フッター・固定IDを保持します。CSS、JSON-LD、HTML専用のスキップリンクは含めません。通常のリンク先はHTMLとし、ページ内リンクは `元HTML名#固定ID` に変換します。

Headings, principles, caveats, definitions, navigation, footers, and explicit IDs are preserved. CSS, JSON-LD, and HTML-only skip links are omitted. Links point to HTML pages; fragment-only links become `source-file.html#explicit-id`.

各HTMLは `<link rel="alternate" type="text/markdown">` で対応するMarkdown版を指定しています。例えば `index.html` には次の指定があります。

Each HTML page points to its Markdown version with `<link rel="alternate" type="text/markdown">`. For example, `index.html` contains:

```html
<link rel="alternate" type="text/markdown" href="index.md" />
```

## 更新と確認 / Updating and checking

Python 3.10以上が必要です。追加パッケージは不要です。以下は `python` で対象のPythonを起動できる環境を前提とし、リポジトリのルートで実行します。

Python 3.10 or later is required, with no additional packages. The commands below assume that `python` starts that interpreter; run them from the repository root.

日本語：

1. 日本語の原則本文を変更する場合は、対応する英語版へ反映し、意味・優先順位・適用条件を照合します。入口ページの概要やリンクも必要に応じて更新します。
2. タイトル・説明・URL・言語・ページの関係を変更した場合は、HTMLのメタデータとJSON-LDも一致させます。
3. 本文やフッターを変更したら、次のコマンドでMarkdownを再生成し、生成結果との一致と回帰テストを確認します。

English:

1. When changing the Japanese principles, update the corresponding English version and check meaning, precedence, and conditions of application. Update the index summary and links as needed.
2. When changing titles, descriptions, URLs, languages, or page relationships, keep the HTML metadata and JSON-LD consistent.
3. After changing content or footers, regenerate Markdown and run the consistency check and regression tests:

```console
python scripts/generate_markdown.py
python scripts/generate_markdown.py --check
python -B -m unittest discover -s scripts -p "test_*.py"
```

`--check` はファイルを書き換えず、Markdownの生成漏れやHTMLとの不一致があれば終了コード1を返します。テストは [scripts/test_generate_markdown.py](scripts/test_generate_markdown.py) にあります。

`--check` does not write files. It exits with code 1 if Markdown files are missing or out of date. Regression tests are in `scripts/test_generate_markdown.py`.

最後にローカルで全5ページの表示・リンク・キーボード操作・JavaScript無効時の動作とGit差分を確認します。HTML・生成Markdown・関連ファイルを一緒にコミット・Pushし、公開後にGitHub Pages上で表示・リンク・Markdownの取得・構造化データ・faviconを確認します。

Finally, check all five pages locally for layout, links, keyboard navigation, operation without JavaScript, and Git changes. Commit and push the HTML, generated Markdown, and related files together, then check the deployed pages, links, Markdown availability, structured data, and favicons on GitHub Pages.
