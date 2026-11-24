// GitHub Pages と同じ URL の形を再現する。ファイルが見つからなかったときだけ呼ばれる。
//   /dir/  -> dir/index.html   /about -> about.html   /dir -> 301 /dir/
// それでも無ければ Pohoda の 404 ページを状態 404 で返す。
// pohoda-site と pohoda-legal で同じファイル。法務側には 404.html が無いので本体のものを借りる。
// 移した古いページ（0秒で移動する HTML の代わりに 301 で転送する。2026-11-24）。
const MOVED = {
  "/glidwell-story.html": "https://pohoda.jp/glidwell.html#screens-detail",
  "/graph-story.html": "https://pohoda.jp/graph.html#screens-detail",
  "/journal/bukken-hikaku-houhou.html": "https://yane.pohoda.jp/guide/bukken-hikaku-houhou",
  "/journal/chintai-naiken-checklist.html": "https://yane.pohoda.jp/guide/chintai-naiken-checklist",
  "/journal/chintai-shoki-hiyou.html": "https://yane.pohoda.jp/guide/chintai-shoki-hiyou",
  "/journal/chuko-mansion-souba.html": "https://yane.pohoda.jp/guide/chuko-mansion-souba",
  "/journal/gakku-shirabekata.html": "https://yane.pohoda.jp/guide/gakku-shirabekata",
  "/journal/hazardmap-mikata-bukken.html": "https://yane.pohoda.jp/guide/hazardmap-mikata-bukken",
  "/journal/jibun-bunseki-yarikata.html": "https://insight.pohoda.jp/guide/jibun-bunseki-yarikata",
  "/journal/jiko-bunseki-tsuzukanai-riyu.html": "https://insight.pohoda.jp/guide/jiko-bunseki-tsuzukanai-riyu",
  "/journal/jiko-rikai-fukameru.html": "https://insight.pohoda.jp/guide/jiko-rikai-fukameru",
  "/journal/juyo-jiko-setsumei-suigai.html": "https://yane.pohoda.jp/guide/juyo-jiko-setsumei-suigai",
  "/journal/kachikan-shindan.html": "https://insight.pohoda.jp/guide/kachikan-shindan",
  "/journal/kyu-taishin-miwakekata.html": "https://yane.pohoda.jp/guide/kyu-taishin-miwakekata",
  "/journal/morido-ekijoka-shirabekata.html": "https://yane.pohoda.jp/guide/morido-ekijoka-shirabekata",
  "/journal/seikaku-shindan-fukusuu-shiten.html": "https://insight.pohoda.jp/guide/seikaku-shindan-muryo",
  "/journal/seikaku-shindan-muryo.html": "https://insight.pohoda.jp/guide/seikaku-shindan-muryo",
  "/journal/self-disclosure-ai-era.html": "https://insight.pohoda.jp/guide/self-disclosure-ai-era",
  "/journal/shinsui-soutei-chintai.html": "https://yane.pohoda.jp/guide/shinsui-soutei-chintai",
  "/journal/shukatsu-jibun-bunseki-tool.html": "https://insight.pohoda.jp/guide/shukatsu-jibun-bunseki-tool",
  "/journal/strengths-finder-muryo.html": "https://insight.pohoda.jp/guide/strengths-finder-muryo",
  "/journal/youto-chiiki-kenpeiritsu.html": "https://yane.pohoda.jp/guide/youto-chiiki-kenpeiritsu",
  "/katachi-story.html": "https://pohoda.jp/katachi.html#screens-detail",
  "/keep-in-touch-story.html": "https://pohoda.jp/keep-in-touch.html#screens-detail"
};

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (MOVED[url.pathname]) return Response.redirect(MOVED[url.pathname], 301);
    const res = await route(url, request, env);
    if (res.status !== 404) return res;
    let page = await env.ASSETS.fetch(new URL("/404.html", url));
    if (page.status === 404) page = await fetch(url.origin + "/404.html");
    if (!page.ok) return res;
    return new Response(page.body, { status: 404, headers: page.headers });
  },
};

async function route(url, request, env) {
  const path = url.pathname;
  const get = (p) => env.ASSETS.fetch(new URL(p + url.search, url), request);
  if (path.endsWith("/")) return get(path + "index.html");
  const res = await get(path);
  if (res.status !== 404 || /\.[^/]*$/.test(path)) return res;
  const html = await get(path + ".html");
  if (html.status !== 404) return html;
  if ((await get(path + "/index.html")).status !== 404) {
    return Response.redirect(url.origin + path + "/" + url.search, 301);
  }
  return res;
}
