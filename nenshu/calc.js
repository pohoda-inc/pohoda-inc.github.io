/* 年収→手取りの概算（2026年の制度）。
   ai-video/styles/nenshu/calc.py の net()・hoiku() をそのまま移植したもの（同じ式・同じ丸め）。
   Python の round() は偶数丸めなので pyRound で合わせる。検算: ai-video/styles/nenshu/check_site_calc.mjs */
(function (root) {
  function pyRound(x) {
    const f = Math.floor(x), d = x - f;
    if (d < 0.5) return f;
    if (d > 0.5) return f + 1;
    return f % 2 === 0 ? f : f + 1;
  }
  function salaryDeduction(g) {
    if (g <= 2200000) return 740000;
    if (g <= 3600000) return g * 0.3 + 80000;
    if (g <= 6600000) return g * 0.2 + 440000;
    if (g <= 8500000) return g * 0.1 + 1100000;
    return 1950000;
  }
  const BRACKETS = [[1950000, 0.05, 0], [3300000, 0.10, 97500], [6950000, 0.20, 427500], [9000000, 0.23, 636000], [18000000, 0.33, 1536000], [9e18, 0.40, 2796000]];
  function incomeTax(taxable) {
    const t = Math.max(0, taxable);
    for (const [lim, r, d] of BRACKETS) if (t <= lim) return (t * r - d) * 1.021;
  }
  function spouseDeduction(sp) {
    if (sp <= 1600000) return [380000, 330000];
    if (sp >= 2010000) return [0, 0];
    const r = (2010000 - sp) / 410000;
    return [380000 * r, 330000 * r];
  }
  function net(gross, bonusMonths, age, spouse) {
    if (bonusMonths === undefined) bonusMonths = 2;
    if (age === undefined) age = 30;
    if (spouse === undefined) spouse = null;
    if (!(gross > 0)) return { gross: 0, monthly: 0, bonus: 0, hi: 0, pen: 0, emp: 0, it: 0, rt: 0, take: 0, bonus_take: 0, year_take: 0, year_tax: 0, shotokuwari: 0, hi_y: 0, pen_y: 0, emp_y: 0, it_y: 0, rt_y: 0 };
    const monthly = gross / (12 + bonusMonths);
    const bonus = monthly * bonusMonths;
    const insured = gross >= 1300000;
    const hi = insured ? (0.099 + 0.0023 + (age >= 40 ? 0.0162 : 0)) / 2 : 0;
    const pen = insured ? 0.0915 : 0;
    const mHi = monthly * hi;
    const mPen = Math.min(monthly, 650000) * pen;
    const mEmp = monthly * 0.005;
    const bPen = Math.min(bonus, 1500000 * Math.max(1, bonusMonths / 2) * 2) * pen;
    const bSi = bonus * hi + bPen + bonus * 0.005;
    const si = (mHi + mPen + mEmp) * 12 + bSi;
    const payInc = gross - salaryDeduction(gross);
    const basic = payInc <= 4890000 ? 1040000 : payInc <= 6550000 ? 670000 : 620000;
    const [spIt, spRt] = spouse !== null ? spouseDeduction(spouse) : [0, 0];
    const it = incomeTax(payInc - si - basic - spIt);
    const rtBase = Math.max(0, payInc - si - 430000 - spRt);
    const shotokuwari = rtBase * 0.06;
    const rt = payInc <= 450000 ? 0 : rtBase * 0.10 - 2500 + 5000;
    const mIt = it * monthly / gross;
    const bIt = it - mIt * 12;
    const mRt = rt / 12;
    return {
      gross: pyRound(gross), monthly: pyRound(monthly), bonus: pyRound(bonus),
      hi: pyRound(mHi), pen: pyRound(mPen), emp: pyRound(mEmp), it: pyRound(mIt), rt: pyRound(mRt),
      take: pyRound(monthly - mHi - mPen - mEmp - mIt - mRt),
      bonus_take: pyRound(bonus - bSi - bIt),
      year_take: pyRound(gross - si - it - rt),
      year_tax: pyRound(si + it + rt), shotokuwari: shotokuwari,
      // 以下は画面の内訳用（Python 版の戻り値には無い。年額）
      hi_y: mHi * 12 + bonus * hi, pen_y: mPen * 12 + bPen, emp_y: mEmp * 12 + bonus * 0.005, it_y: it, rt_y: rt
    };
  }
  function hoiku(shotokuwari) {
    const T = [[48600, 19500], [97000, 30000], [169000, 44500], [301000, 61000], [397000, 80000], [9e18, 104000]];
    for (const [lim, fee] of T) if (shotokuwari < lim) return pyRound(fee * 0.7 / 1000) * 1000;
  }
  const api = { net, hoiku, pyRound };
  if (typeof module !== "undefined" && module.exports) module.exports = api; else root.NenshuCalc = api;
})(typeof window !== "undefined" ? window : globalThis);
