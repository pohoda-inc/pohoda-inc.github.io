# AI Mail Auto ページの確認（2026-11-22）

方法: `python3 -m http.server` でワークツリーを配信し、アプリ内ブラウザ（Chrome 系）で確認。

- 対象 8ページ（製品・使い方・記事6）＋トップ: 390px 幅と 1280px 幅で、横スクロールなし（scrollWidth = 画面幅）。
- JSON-LD: 全ページで JSON として解釈できる（製品=SoftwareApplication+FAQPage+BreadcrumbList、記事=BlogPosting+BreadcrumbList+FAQPage、使い方=BreadcrumbList+HowTo）。
- リンク: 8ページ内の内部リンク・絶対 URL（pohoda.jp）は、/legal/* を除きすべて実ファイルに解決。/legal/*（support・privacy・terms・tokushoho）は別リポ（Workers 別配信）のため、このローカル配信では解決しない。legal リポに4ファイルとも存在することは確認済み。
- 未解決（意図的）: `/assets/ai-mail-auto/{search-result,draft,wizard}.png`（実画面が未撮影。docs/screenshots-needed.md 参照）。公開前に必ず置く。トップのカードも search-result.png を使う。
- 外部（未作成）: mail-ai.pohoda.jp/checkout・/download。
- 未確認: 実機の Chrome での目視（ヒーロー画面の1280px の見た目を縮小スクリーンショットで確認したのみ）、Thunderbird の日本語メニュー名の実機照合。
