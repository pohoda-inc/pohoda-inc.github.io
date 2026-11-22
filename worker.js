// GitHub Pages と同じ URL の形を再現する。ファイルが見つからなかったときだけ呼ばれる。
//   /dir/  -> dir/index.html   /about -> about.html   /dir -> 301 /dir/
// それでも無ければ Pohoda の 404 ページを状態 404 で返す。
// pohoda-site と pohoda-legal で同じファイル。法務側には 404.html が無いので本体のものを借りる。
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
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
