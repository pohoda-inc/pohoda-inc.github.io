#!/usr/bin/env python3
"""App Store へのリンク（<a href> だけ）にキャンペーン印を付ける。何度実行しても同じ結果になる。

  python3 tools/appstore_ct.py <サイトのルート> <ct の接頭辞>   例: python3 tools/appstore_ct.py . pj-

ct＝接頭辞＋ページのパス（journal/suimin-kirokuhyo.html → pj-j-suimin-kirokuhyo・guide/ は g-）。
ASC の App Downloads Detailed レポートの Campaign 列に、このページ経由の初回DLとして出る。
pt は ASC のプロバイダID（Keisuke Sugimoto）。JSON-LD など href 以外の URL は触らない。
新しいページを足したら、公開前にこれを流す。
"""
import re
import sys
from pathlib import Path
from urllib.parse import parse_qsl, urlencode

PT = "128987033"
HREF = re.compile(r'href="(https://apps\.apple\.com/[a-z]{2}/app/[^"?#]*id\d+)(?:\?([^"#]*))?"')


def campaign(rel: Path, prefix: str) -> str:
    slug = str(rel.with_suffix(""))
    slug = re.sub(r"^(journal|guide)/", lambda m: m.group(1)[0] + "/", slug).replace("/", "-")  # 40字に収める
    slug = re.sub(r"(^|-)index$", r"\1top", slug)
    return (prefix + slug)[:40]


def tag(html: str, ct: str) -> str:
    def sub(m: re.Match) -> str:
        q = dict(parse_qsl(m.group(2) or "", keep_blank_values=True))
        q.update(pt=PT, ct=ct, mt="8")
        return f'href="{m.group(1)}?{urlencode(q).replace("&", "&amp;")}"'
    # 既存の &amp; は & に戻してから読む（parse_qsl が amp; を名前にしないように）
    return HREF.sub(sub, html.replace("&amp;pt=", "&pt=").replace("&amp;ct=", "&ct=").replace("&amp;mt=", "&mt="))


def main(root: str, prefix: str) -> None:
    base = Path(root)
    changed = 0
    for p in sorted(base.rglob("*.html")):
        if any(part in {"node_modules", "dist", ".git"} for part in p.parts):
            continue
        old = p.read_text(encoding="utf-8")
        new = tag(old, campaign(p.relative_to(base), prefix))
        if new != old:
            p.write_text(new, encoding="utf-8")
            changed += 1
    print(f"{changed} files tagged")


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--selftest":
        h = '<a href="https://apps.apple.com/jp/app/graph/id6785250301">x</a> "downloadUrl": "https://apps.apple.com/jp/app/id1"'
        t = tag(h, "pj-j-a")
        assert 'href="https://apps.apple.com/jp/app/graph/id6785250301?pt=128987033&amp;ct=pj-j-a&amp;mt=8"' in t, t
        assert '"downloadUrl": "https://apps.apple.com/jp/app/id1"' in t
        assert tag(t, "pj-j-a") == t  # 2回目は変わらない
        assert campaign(Path("journal/index.html"), "pj-") == "pj-j-top"
        assert campaign(Path("guide/gakku-shirabekata.html"), "yane-") == "yane-g-gakku-shirabekata"
        assert campaign(Path("index.html"), "yane-") == "yane-top"
        print("ok")
    else:
        main(sys.argv[1], sys.argv[2])
