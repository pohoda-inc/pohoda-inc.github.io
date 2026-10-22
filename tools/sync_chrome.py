#!/usr/bin/env python3
"""全ページの共通部品（ヘッダー・フッター・計測タグ・hreflang・サイトマップ）を1か所の定義からそろえる。

ページを足したら、このファイルの NAV / FOOTER（と必要なら EN_PAIRS）を直して
    python3 tools/sync_chrome.py          # 書き換え
    python3 tools/sync_chrome.py --check  # 差分があれば一覧して終了コード1（書き換えない）
を実行する。本文（<main> など）には触らない。

- 日本語ページ: 日本語のヘッダー・フッター。英語ページ（/en/・/about.html）: 英語のもの。
- 他言語の法務ページ（/ko/ /zh-hant/ /es/ /pt-br/ /fr/）: 各言語の切替メニューをそのまま残し、計測タグだけ足す。
- 転送用のページ（meta refresh）は対象外。サイトマップからも外す。
- 日本語の法務ページ（pohoda.jp/legal/）は別リポ pohoda-inc/legal が配信する。`--legal <そのリポのパス>` を付けると
  そちらにも同じ部品を流し、サイトマップにも載せる（付けなければ既存の /legal/ の項目はそのまま残す）。
- ヘッダーにあるページ内リンク（href="#..."、例: 料金）はページごとに残す。
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://pohoda.jp"
BEACON = ("<!-- Cloudflare Web Analytics --><script defer src='https://static.cloudflareinsights.com/beacon.min.js' "
          "data-cf-beacon='{\"token\": \"0edf017e187e4defbdbfdf457f3a7f1a\"}'></script><!-- End Cloudflare Web Analytics -->")

# ---- 日本語
APPS = [("/katachi.html", "KATACHI"), ("/katachi-plus.html", "KATACHI +"), ("/keep-in-touch.html", "Keep In Touch"),
        ("/glidwell.html", "Glidwell"), ("/graph.html", "Graph"), ("/one-crm.html", "One CRM"),
        ("/utility.html", "Utility"), ("/pre-interview.html", "Pre Interview")]
WEB = [("/insight.html", "Insight"), ("/drivescape.html", "DriveScape"), ("/yane.html", "YANE")]
JA_NAV = APPS + WEB + [("/journal/", "読みもの"), ("/news.html", "お知らせ")]
JA_SUPPORT = [("/news.html", "お知らせ"), ("/journal/", "読みもの"), ("/request.html", "要望箱"),
              ("/legal/support.html", "サポート"), ("/legal/privacy.html", "プライバシーポリシー"),
              ("/legal/terms.html", "利用規約"), ("/legal/tokushoho.html", "特定商取引法に基づく表記")]

# ---- 英語（海外でも配信しているアプリだけ）
EN_APPS = [("/en/graph.html", "Graph"), ("/en/katachi.html", "KATACHI"),
           ("/en/keep-in-touch.html", "Keep In Touch"), ("/en/utility.html", "Utility")]
EN_NAV = EN_APPS + [("/about.html", "About"), ("/en/legal/support.html", "Support"), ("/", "日本語")]
EN_SUPPORT = [("/en/legal/support.html", "Support"), ("/en/legal/privacy.html", "Privacy Policy"),
              ("/en/legal/terms.html", "Terms of Use")]
# 日本語ページ ⇔ 英語ページ（hreflang で互いに指す）
EN_PAIRS = {"/": "/en/", "/graph.html": "/en/graph.html", "/katachi.html": "/en/katachi.html",
            "/keep-in-touch.html": "/en/keep-in-touch.html", "/utility.html": "/en/utility.html"}
INTL_LEGAL = ("ko", "zh-hant", "es", "pt-br", "fr")


LEGAL_ROOT: Path | None = None


def url_path(f: Path) -> str:
    if LEGAL_ROOT and LEGAL_ROOT in f.parents:
        p = "/legal/" + f.relative_to(LEGAL_ROOT).as_posix()
    else:
        p = "/" + f.relative_to(ROOT).as_posix()
    return p[: -len("index.html")] if p.endswith("index.html") else p


def links(items, here, indent):
    out = []
    for href, label in items:
        cur = ' style="color:var(--gold)"' if href == here else ""
        lang = ' lang="ja"' if label == "日本語" else ""
        out.append(f'{indent}<a href="{href}"{cur}{lang}>{label}</a>')
    return "\n".join(out)


def header(nav, home, here, anchors):
    extra = "".join(f'\n      <a href="{h}">{t}</a>' for h, t in anchors)
    return (f'<header class="site-header">\n  <div class="wrap">\n'
            f'    <a class="brand" href="{home}"><img src="/assets/brand/pohoda-logo.svg" alt="Pohoda" width="117" height="34"></a>\n'
            f'    <nav class="nav">\n{links(nav, here, "      ")}{extra}\n    </nav>\n  </div>\n</header>')


def col(title, items):
    return (f'      <div class="footer-col">\n        <h4>{title}</h4>\n'
            + links(items, None, "        ") + "\n      </div>")


def ja_footer():
    return ('<footer class="site-footer">\n  <div class="wrap">\n    <div class="footer-cols">\n'
            + "\n".join([col("アプリ", APPS), col("Web サービス", WEB), col("サポート・規約", JA_SUPPORT),
                         '      <div class="footer-col">\n        <h4>お問い合わせ</h4>\n'
                         '        <a href="mailto:pohoda.inc@gmail.com">pohoda.inc@gmail.com</a>\n'
                         '        <a href="/about.html" lang="en">About Pohoda (English)</a>\n'
                         '        <a href="/en/" lang="en">Apps in English</a>\n      </div>'])
            + '\n    </div>\n    <div class="copyright">© 2026 Pohoda（杉本 啓輔）</div>\n  </div>\n</footer>')


def en_footer():
    return ('<footer class="site-footer">\n  <div class="wrap">\n    <div class="footer-cols">\n'
            + "\n".join([col("Apps", EN_APPS), col("Support", EN_SUPPORT),
                         '      <div class="footer-col">\n        <h4>Contact</h4>\n'
                         '        <a href="mailto:pohoda.inc@gmail.com">pohoda.inc@gmail.com</a>\n'
                         '        <a href="/about.html">About Pohoda</a>\n'
                         '        <a href="/" lang="ja">日本語サイト</a>\n      </div>'])
            + '\n    </div>\n    <div class="copyright">© 2026 Pohoda (Keisuke Sugimoto)</div>\n  </div>\n</footer>')


def kind(f: Path, text: str) -> str | None:
    if 'http-equiv="refresh"' in text:
        return None                      # 転送用
    if LEGAL_ROOT and LEGAL_ROOT in f.parents:
        return "ja"
    rel = f.relative_to(ROOT).as_posix()
    if rel.split("/")[0] in INTL_LEGAL:
        return "intl"
    if rel.startswith("en/") or rel == "about.html":
        return "en"
    return "ja"


def nav_here(path: str, nav) -> str | None:
    if path.startswith("/journal/"):
        return "/journal/"
    return path if any(h == path for h, _ in nav) else None


def hreflang(path: str) -> str | None:
    ja = next((j for j, e in EN_PAIRS.items() if path in (j, e)), None)
    if ja is None:
        return None
    en = EN_PAIRS[ja]
    return (f'<link rel="alternate" hreflang="ja" href="{SITE}{ja}">\n'
            f'<link rel="alternate" hreflang="en" href="{SITE}{en}">\n'
            f'<link rel="alternate" hreflang="x-default" href="{SITE}{ja}">')


def sync(f: Path, text: str) -> str:
    k = kind(f, text)
    if k is None:
        return text
    path = url_path(f)
    if k in ("ja", "en"):
        nav, home, foot = (JA_NAV, "/", ja_footer()) if k == "ja" else (EN_NAV, "/en/", en_footer())
        old = re.search(r'<header class="site-header">.*?</header>', text, re.S)
        if old and not path.startswith("/en/legal/"):   # 英語の法務ページは各言語への切替メニューを残す
            anchors = re.findall(r'<a href="(#[^"]+)"[^>]*>([^<]+)</a>', old.group(0))
            text = text.replace(old.group(0), header(nav, home, nav_here(path, nav), anchors), 1)
        text = re.sub(r'<footer class="site-footer">.*?</footer>', lambda m: foot, text, count=1, flags=re.S)
        # hreflang: 日本語⇔英語の組があるページだけ差し替える（法務ページの多言語の hreflang には触らない）
        hl = hreflang(path)
        if hl:
            text = re.sub(r'<link rel="alternate" hreflang="[^"]+" href="[^"]+">\n?', "", text)
            text = re.sub(r'(<link rel="canonical"[^>]*>\n)', lambda m: m.group(1) + hl + "\n", text, count=1)
    text = text.replace('<meta name="theme-color" content="#15130f">', '<meta name="theme-color" content="#ffffff">')
    if "cloudflareinsights" not in text:
        text = text.replace("</body>", BEACON + "\n</body>", 1)
    return text


def pages():
    main = [p for p in ROOT.rglob("*.html") if ".git" not in p.parts and "tools" not in p.parts]
    legal = [p for p in LEGAL_ROOT.glob("*.html")] if LEGAL_ROOT else []
    return sorted(main) + sorted(legal)


def sitemap(live: list[Path]) -> str:
    """既存の項目（lastmod・priority・画像）は残し、無いページを足し、消えた・転送のページを外す。"""
    sm = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    want = {SITE + url_path(p) for p in live}
    blocks = re.findall(r"  <url>.*?</url>\n", sm, re.S)
    def keep(b):
        loc = re.search(r"<loc>(.*?)</loc>", b).group(1)
        return loc in want or (LEGAL_ROOT is None and loc.startswith(SITE + "/legal/"))
    kept = [b for b in blocks if keep(b)]
    have = {re.search(r"<loc>(.*?)</loc>", b).group(1) for b in kept}
    for p in live:
        loc = SITE + url_path(p)
        if loc in have:
            continue
        d = subprocess.run(["git", "log", "-1", "--format=%cs", "--", str(p)], cwd=p.parent,
                           capture_output=True, text=True).stdout.strip() or subprocess.run(
            ["date", "+%Y-%m-%d"], capture_output=True, text=True).stdout.strip()
        kept.append(f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{d}</lastmod>\n  </url>\n")
    head = sm[: sm.index("  <url>")]
    return head + "".join(kept) + "</urlset>\n"


def main() -> int:
    global LEGAL_ROOT
    check = "--check" in sys.argv
    if "--legal" in sys.argv:
        LEGAL_ROOT = Path(sys.argv[sys.argv.index("--legal") + 1]).expanduser().resolve()
    changed, live = [], []
    for f in pages():
        text = f.read_text(encoding="utf-8")
        if kind(f, text) is not None:
            live.append(f)
        new = sync(f, text)
        if new != text:
            changed.append(url_path(f))
            if not check:
                f.write_text(new, encoding="utf-8")
    sm_new = sitemap(live)
    if sm_new != (ROOT / "sitemap.xml").read_text(encoding="utf-8"):
        changed.append("sitemap.xml")
        if not check:
            (ROOT / "sitemap.xml").write_text(sm_new, encoding="utf-8")
    print(("ずれ" if check else "更新") + f" {len(changed)}件" + ("".join(f"\n  {c}" for c in changed)))
    return 1 if (check and changed) else 0


if __name__ == "__main__":
    sys.exit(main())
