// GitHub Pages と同じ URL の形を再現する。ファイルが見つからなかったときだけ呼ばれる。
//   /dir/  -> dir/index.html   /about -> about.html   /dir -> 301 /dir/
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
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
  },
};
