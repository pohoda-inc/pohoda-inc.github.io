/* /nenshu/ の計算機とモデル家計。計算は calc.js（calc.py の移植）、16人のデータは data.json（tiers.py から書き出し） */
(function () {
  const { net, hoiku } = window.NenshuCalc;
  const $ = (id) => document.getElementById(id);
  const yen = (n) => "¥" + Math.round(n).toLocaleString("ja-JP");
  const man = (n) => (Math.round(n / 1000) / 10).toLocaleString("ja-JP") + "万円";
  const pct = (a, b) => (b > 0 ? (Math.round((a / b) * 1000) / 10).toFixed(1) + "%" : "-");
  const num = (el, lo, hi, dflt) => { const v = parseFloat(el.value); return Number.isFinite(v) ? Math.min(hi, Math.max(lo, v)) : dflt; };
  let MODELS = [], hh = "single", modelId = null;

  /* ---------- 計算機 ---------- */
  function calc() {
    const fam = hh === "family", old = $("age40").checked;
    const bm = num($("bonus"), 0, 6, 2);
    let slips, take, bonusTake, yearTake, yearTax, fee = 0, allow = 0, gross, sum;
    if (!fam) {
      gross = num($("inc"), 0, 5000, 0) * 10000;
      const a = net(gross, bm, old ? 40 : 30);
      slips = [a];
    } else {
      const h = num($("inc-h"), 0, 5000, 0), w = num($("inc-w"), 0, 5000, 0);
      gross = (h + w) * 10000;
      const a = net(h * 10000, bm, old ? 40 : 34, w * 10000);
      const b = net(w * 10000, w < 130 ? 0 : 1, old ? 40 : 33);
      slips = [a, b]; allow = 15000; fee = hoiku(a.shotokuwari + b.shotokuwari);
    }
    sum = (k) => slips.reduce((s, x) => s + x[k], 0);
    take = sum("take"); bonusTake = sum("bonus_take"); yearTake = sum("year_take"); yearTax = sum("year_tax");
    const gsum = slips.reduce((s, x) => s + x.gross, 0);
    $("r-take").innerHTML = yen(take) + (fam ? "<small>+ 児童手当 " + yen(allow) + "（月）</small>" : "<small>ボーナスの月を除く</small>");
    $("r-year").innerHTML = yen(yearTake) + "<small>ボーナスの手取り " + yen(bonusTake) + " を含む</small>";
    $("r-tax").innerHTML = yen(yearTax) + "<small>額面の " + pct(yearTax, gsum) + "</small>";
    const rows = [["健康保険（40歳以上は介護保険料を含む）", "hi_y"], ["厚生年金", "pen_y"], ["雇用保険", "emp_y"], ["所得税", "it_y"], ["住民税", "rt_y"]];
    $("r-rows").innerHTML = rows.map(([n, k]) => "<tr><td>" + n + "</td><td class='num'>" + yen(sum(k)) + "</td><td class='num'>" + pct(sum(k), gsum) + "</td></tr>").join("")
      + "<tr class='sum'><td>合計</td><td class='num'>" + yen(yearTax) + "</td><td class='num'>" + pct(yearTax, gsum) + "</td></tr>";
    $("r-fee").hidden = !fam;
    if (fam) $("r-fee").textContent = "保育料（2歳・認可保育所）の目安は月 " + yen(fee) + "。国の上限額の7割で置いた概算で、実際は市区町村で違います。";
    window._ns = { take: take + allow, gross: gsum };
    fixedCalc();
    if (gsum > 0) pickNearest(fam ? "family" : "single", gsum / 10000);
  }
  function fixedCalc() {
    const f = parseFloat($("fixed").value), base = window._ns.take;
    $("fixed-out").textContent = Number.isFinite(f) && f > 0 && base > 0
      ? "固定費 " + yen(f) + " は、月の手取り（" + yen(base) + (hh === "family" ? "・児童手当を含む" : "") + "）の " + pct(f, base) + " です。" : "";
  }

  /* ---------- モデル家計 ---------- */
  function pickNearest(kind, incomeMan) {
    const list = MODELS.filter((m) => (m.fam ? "family" : "single") === kind);
    modelId = list.reduce((b, m) => (Math.abs(m.income - incomeMan) < Math.abs(b.income - incomeMan) ? m : b)).id;
    renderModels(kind);
  }
  function renderModels(kind) {
    const list = MODELS.filter((m) => (m.fam ? "family" : "single") === kind);
    document.querySelectorAll("input[name=mh]").forEach((r) => (r.checked = r.value === kind));
    const chips = $("m-chips"); chips.innerHTML = "";
    list.forEach((m) => {
      const b = document.createElement("button"); b.type = "button"; b.textContent = "年収" + m.income + "万";
      b.setAttribute("aria-pressed", String(m.id === modelId));
      b.onclick = () => { modelId = m.id; renderModels(kind); };
      chips.appendChild(b);
    });
    const m = MODELS.find((x) => x.id === modelId);
    $("m-who").innerHTML = "<strong>" + m.label.replace("子ども2歳", "子ども1人（2歳）") + "</strong>　" + m.job + "　／　" + m.home
      + (m.fam ? "<br>年収" + m.income + "万円は夫婦の合計（夫" + m.husband + "万＋妻" + m.wife + "万）。" : "");
    $("m-grid").innerHTML = [
      ["月の手取り" + (m.fam ? "（児童手当を含む）" : ""), yen(m.inflow)],
      ["月末に残る額", yen(m.left), "家計簿の収支"],
      ["ボーナスの手取り", yen(m.bonus), "年の合計"],
      ["年に引かれる額", yen(m.year_tax), "社会保険料＋税"],
      ["旅行・帰省・冠婚葬祭など", yen(m.special), "年の出費"],
      ["1年で残る額", yen(m.saved), "積立・NISAを含む"],
    ].map(([t, v, s]) => "<div><dt>" + t + "</dt><dd class='num'>" + v + (s ? "<small>" + s + "</small>" : "") + "</dd></div>").join("");
    const fixed = m.rows.filter((r) => r.fixed).reduce((s, r) => s + r.amount, 0);
    $("m-rows").innerHTML = m.rows.map((r) => "<tr><td>" + r.name + (r.fixed ? "<span class='tag-fixed'>固定費</span>" : "") + "</td><td class='num'>" + yen(r.amount) + "</td><td class='num'>" + pct(r.amount, m.inflow) + "</td></tr>").join("")
      + "<tr class='sum'><td>固定費の合計</td><td class='num'>" + yen(fixed) + "</td><td class='num'>" + pct(fixed, m.inflow) + "</td></tr>"
      + "<tr class='sum'><td>支出の合計</td><td class='num'>" + yen(m.spent) + "</td><td class='num'>" + pct(m.spent, m.inflow) + "</td></tr>"
      + "<tr class='sum'><td>月末に残る額</td><td class='num'>" + yen(m.left) + "</td><td class='num'>" + pct(m.left, m.inflow) + "</td></tr>";
    $("m-fixedpct").textContent = "このモデルでは、固定費が月の手取りの " + pct(fixed, m.inflow) + " です。";
  }

  function setHousehold(k) {
    hh = k;
    document.querySelectorAll("input[name=hh]").forEach((r) => (r.checked = r.value === k));
    $("f-single").hidden = k !== "single"; $("f-family").hidden = k !== "family";
    calc();
  }

  function init() {
    document.querySelectorAll("input[name=hh]").forEach((r) => r.addEventListener("change", () => setHousehold(r.value)));
    document.querySelectorAll("#calc input[type=number], #age40").forEach((el) => el.addEventListener("input", calc));
    $("fixed").addEventListener("input", fixedCalc);
    document.querySelectorAll("input[name=mh]").forEach((r) => r.addEventListener("change", () => {
      const list = MODELS.filter((m) => (m.fam ? "family" : "single") === r.value);
      modelId = list[Math.min(1, list.length - 1)].id; renderModels(r.value);
    }));
    setHousehold("single");
  }

  fetch("data.json").then((r) => r.json()).then((d) => { MODELS = d; init(); })
    .catch(() => { $("load-err").hidden = false; });
})();
