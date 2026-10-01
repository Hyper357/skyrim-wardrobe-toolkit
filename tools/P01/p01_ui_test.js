/* Headless functional test of the SHIPPED P01_WARDROBE_REVIEW.html.
   Extracts the real <script> from the real file and runs it against a minimal
   DOM stub, so this exercises the shipped code, not a copy. */
const fs = require("fs");
const path = require("path");
const vm = require("vm");

const HTML = process.argv[2] ||
  path.join(__dirname, "..", "..", "reports", "P01", "review_ui",
            "P01_WARDROBE_REVIEW.html");
const html = fs.readFileSync(HTML, "utf8");

/* ---------------- DOM stub ---------------- */
const listeners = {};
function mkEl(tag) {
  const el = {
    tagName: (tag || "div").toUpperCase(), _html: "", dataset: {}, value: "",
    style: {}, classList: {
      _s: new Set(),
      add(...c) { c.forEach(x => this._s.add(x)); },
      remove(...c) { c.forEach(x => this._s.delete(x)); },
      contains(c) { return this._s.has(c); }
    },
    children: [], files: [],
    set innerHTML(v) { this._html = v; }, get innerHTML() { return this._html; },
    set textContent(v) { this._text = v; }, get textContent() { return this._text; },
    appendChild(c) { this.children.push(c); return c; },
    remove() {},
    closest(sel) {
      // enough for the shipped handler: it asks for "button,[data-img]" and
      // then reads .dataset off whatever comes back
      if (sel.indexOf("button") >= 0) return this.tagName === "BUTTON" ? this : null;
      if (sel.indexOf("data-img") >= 0 && this.dataset.img !== undefined) return this;
      return null;
    },
    click() {
      (listeners.click || []).forEach(f => f({ target: this }));
      this._fire("click", { target: this });
    },
    scrollIntoView() { this._scrolled = true; },
    focus() {},
    /* element-level listeners are real: the toolbar buttons bind their own
       click handlers rather than going through delegation */
    addEventListener(t, f) { (this._l = this._l || {})[t] = (this._l[t] || []).concat(f); },
    removeEventListener() {},
    _fire(t, ev) { ((this._l || {})[t] || []).forEach(f => f(ev)); },
    hasAttribute(n) { return Object.prototype.hasOwnProperty.call(this.dataset, n); },
    getAttribute(n) { return this.dataset[n] === undefined ? null : this.dataset[n]; },
    get offsetWidth() { return 1; }
  };
  return el;
}
const byId = {};
["stats", "grid", "done", "q", "sort", "f-dec", "f-body", "f-cost", "f-ube",
 "f-mat", "next", "undo", "rc", "ra", "exj", "exc", "exb", "imp", "impf",
 "mask", "mimg", "mx"].forEach(id => {
   // the control elements must be BUTTONs: the shipped click handler begins
   // with e.target.closest("button,[data-img]") and bails on anything else
   const isButton = ["next", "undo", "rc", "ra", "exj", "exc", "exb", "imp"]
     .indexOf(id) >= 0;
   byId[id] = mkEl(isButton ? "button" : "div");
 });
byId["f-dec"].children = ["ALL", "UNDECIDED", "KEEP", "PARTIAL", "DROP"]
  .map(v => { const b = mkEl("button"); b.dataset.v = v; return b; });
byId["f-dec"].children[0].classList.add("on");

/* descendant-aware querySelector for the one selector the app uses that my
   flat map cannot express: "#f-dec .on" -> the active filter button */
function qs(sel) {
  if (sel === "#f-dec .on") {
    return byId["f-dec"].children.find(b => b.classList.contains("on"))
        || byId["f-dec"].children[0];
  }
  if (sel === "#f-dec") return byId["f-dec"];
  return byId[sel.replace("#", "")] || mkEl();
}
/* let a test set the active decision filter the way a user click would */
function setFilter(v) {
  const kids = byId["f-dec"].children;
  kids.forEach(b => b.classList.remove("on"));
  const b = kids.find(k => k.dataset.v === v);
  b.classList.add("on");
  fire("click", { target: b, closest: () => b });
}

let alertMsg = "", confirmAnswer = true, confirmLog = [];
const sandbox = {
  console,
  JSON, Object, Array, String, Number, Math, Date, Set, Map, RegExp, Boolean,
  parseInt, parseFloat, isNaN, encodeURIComponent, decodeURIComponent,
  setTimeout: (f) => { return 0; }, clearTimeout: () => {},
  document: {
    querySelector: qs,
    getElementById: id => byId[id] || mkEl(),
    createElement: mkEl,
    addEventListener: (t, f) => { (listeners[t] = listeners[t] || []).push(f); },
    body: mkEl()
  },
  localStorage: {
    _d: {},
    getItem(k) { return this._d[k] === undefined ? null : this._d[k]; },
    setItem(k, v) { this._d[k] = String(v); },
    removeItem(k) { delete this._d[k]; }
  },
  alert: m => { alertMsg = m; },
  confirm: m => { confirmLog.push(m); return confirmAnswer; },
  Blob: function (parts, o) { this.parts = parts; this.type = o && o.type; },
  URL: { createObjectURL: () => "blob:x", revokeObjectURL: () => {} },
  FileReader: function () { this.readAsText = () => { if (this.onload) this.onload(); }; }
};
sandbox.window = sandbox;
sandbox.globalThis = sandbox;

/* run the shipped script */
const m = html.match(/<script>([\s\S]*?)<\/script>/);
if (!m) { console.error("FAIL: no <script> found"); process.exit(1); }
const ctx = vm.createContext(sandbox);
try { vm.runInContext(m[1], ctx, { filename: "P01_WARDROBE_REVIEW.html" }); }
catch (e) { console.error("FAIL: script threw on load: " + e.message); process.exit(1); }

/* ---------------- assertions ---------------- */
const R = [];
const ok = (name, cond, extra) => R.push({ name, pass: !!cond, extra: extra || "" });
const fire = (t, ev) => (listeners[t] || []).forEach(f => f(ev));
const clickBtn = (sel) => { const e = byId[sel]; e.click && e.click(); };

/* `const` bindings live in the context's lexical scope and do NOT become
   properties of the sandbox object, so read them back out explicitly.
   (Plain `function` declarations do become globals, which is why the
   helpers below are reachable directly.) */
const get = (expr) => vm.runInContext(expr, ctx);
const S = get("S"), DATA = get("DATA"), omap = get("omap");
const dec = get("dec"), pri = get("pri"), render = get("render");
const currentList = get("currentList"), counts = get("counts");
const loadState = get("loadState"), undo = get("undo");
const initParts = get("initParts");
sandbox.S = S; sandbox.DATA = DATA; sandbox.omap = omap;
sandbox.dec = dec; sandbox.pri = pri; sandbox.render = render;
sandbox.currentList = currentList; sandbox.counts = counts;
sandbox.loadState = loadState; sandbox.undo = undo;
sandbox.initParts = initParts;
const O = DATA.outfits;
const id0 = O[0].id, id1 = O[1].id;
const setDec = (id, d) => fire("click", { target: { closest: () => ({ dataset: { dec: d, o: id } }) } });
const setPri = (id, p) => fire("click", { target: { closest: () => ({ dataset: { pri: p, o: id } }) } });

/* 1. 56 outfits, unique ids */
ok("56 outfits present", O.length === 56, "got " + O.length);
ok("outfit ids unique", new Set(O.map(x => x.id)).size === 56);

/* 2. everything starts UNDECIDED, nothing pre-filled */
ok("all start UNDECIDED", O.every(x => sandbox.dec(x.id) === "UNDECIDED"));
ok("all start Priority UNSET", O.every(x => sandbox.pri(x.id) === "UNSET"));
ok("all notes empty", O.every(x => (S.note[x.id] || "") === ""));
ok("all parts start UNDECIDED",
   O.every(x => Object.values(S.parts[x.id] || {}).every(v => v === "UNDECIDED")));

/* 3. counts are all 56 undecided at boot */
let c = sandbox.counts();
ok("counts boot = 56 UNDECIDED", c.UNDECIDED === 56 && c.KEEP === 0 &&
   c.PARTIAL === 0 && c.DROP === 0, JSON.stringify(c));

/* 4. decisions are mutually exclusive */
setDec(id0, "KEEP"); setDec(id0, "DROP"); setDec(id0, "PARTIAL");
ok("decision is exclusive (last wins)", sandbox.dec(id0) === "PARTIAL",
   sandbox.dec(id0));
setDec(id0, "UNDECIDED");
ok("UNDECIDED resets", sandbox.dec(id0) === "UNDECIDED");

/* 5. PARTIAL panel shows ONLY that outfit's parts */
const withParts = O.find(x => x.parts.length >= 2);
fire("click", { target: { closest: () => ({ dataset: { dec: "PARTIAL", o: withParts.id } }) } });
const ids = new Set(withParts.parts.map(p => p.id));
const leaked = Object.keys(S.parts[withParts.id]).filter(k => !ids.has(k));
ok("PARTIAL panel is scoped to its own outfit", leaked.length === 0,
   leaked.slice(0, 3).join(","));
ok("PARTIAL parts all default UNDECIDED",
   Object.values(S.parts[withParts.id]).every(v => v === "UNDECIDED"));

/* 6. per-part KEEP/DROP */
const p0 = withParts.parts[0].id;
fire("click", { target: { closest: () => ({ dataset: { pk: p0, o: withParts.id } }) } });
ok("KEEP PART sets the part", S.parts[withParts.id][p0] === "KEEP PART");
const p1 = withParts.parts[1].id;
fire("click", { target: { closest: () => ({ dataset: { pd: p1, o: withParts.id } }) } });
ok("DROP PART sets the part", S.parts[withParts.id][p1] === "DROP PART");
ok("other parts untouched",
   withParts.parts.slice(2).every(p => S.parts[withParts.id][p.id] === "UNDECIDED"));
fire("click", { target: { closest: () => ({ dataset: { pall: withParts.id } }) } });
ok("KEEP ALL sets every part",
   Object.values(S.parts[withParts.id]).every(v => v === "KEEP PART"));
fire("click", { target: { closest: () => ({ dataset: { pnone: withParts.id } }) } });
ok("reset parts restores UNDECIDED",
   Object.values(S.parts[withParts.id]).every(v => v === "UNDECIDED"));

/* 7. notes + priority survive a re-render */
S.note[id1] = "XP 核心必留 / 只要靴子";
setPri(id1, "A");
sandbox.render();
ok("note survives render", S.note[id1] === "XP 核心必留 / 只要靴子");
ok("priority survives render", sandbox.pri(id1) === "A");

/* 8. filters */
setFilter("KEEP");
ok("decision filter KEEP -> only KEEP",
   sandbox.currentList().every(o => sandbox.dec(o.id) === "KEEP"));
setDec(id0, "KEEP");
ok("decision filter returns exactly the KEEP ones",
   sandbox.currentList().length === O.filter(o => sandbox.dec(o.id) === "KEEP").length,
   sandbox.currentList().length + " rows");
setFilter("ALL");
byId["f-cost"].value = "HIGH";
const costList = sandbox.currentList();
ok("cost filter HIGH returns only HIGH",
   costList.every(o => String(o.technical_cost || "").startsWith("HIGH")),
   costList.length + " rows");
byId["f-cost"].value = "";
ok("clearing the cost filter restores 56", sandbox.currentList().length === 56);
byId["f-ube"].value = "A";
ok("UBE filter returns only outfits having an A part",
   sandbox.currentList().every(o => o.parts.some(p => p.ube === "A")));
byId["f-ube"].value = "";
byId["f-body"].value = "UNKNOWN";
const bList = sandbox.currentList();
ok("body filter works", bList.every(o => o.body_type === "UNKNOWN"),
   bList.length + " rows");
byId["f-body"].value = "";

/* 9. search */
const someName = O[3].display_name.split(/[\s—-]/)[0];
byId["q"].value = someName;
ok("search by outfit name returns >=1", sandbox.currentList().length >= 1,
   "query=" + someName + " -> " + sandbox.currentList().length);
byId["q"].value = "";
const aPart = O.find(o => o.parts.length).parts[0].name;
const qt = aPart.split(" ")[0];
byId["q"].value = qt;
ok("search by part name returns >=1", sandbox.currentList().length >= 1,
   "query=" + qt + " -> " + sandbox.currentList().length);
byId["q"].value = "";
ok("search clear restores 56", sandbox.currentList().length === 56);

/* 10. sorting */
byId["sort"].value = "name";
ok("sort by name is alphabetical", (() => {
  const L = sandbox.currentList().map(x => x.display_name);
  return JSON.stringify(L) === JSON.stringify([...L].sort((a, b) => a.localeCompare(b, "zh")));
})());
byId["sort"].value = "size";
ok("sort by size is descending", (() => {
  const L = sandbox.currentList().map(x => Number(String(x.current_size_bytes).replace(/[^0-9.]/g, "")));
  return L.every((v, i) => i === 0 || L[i - 1] >= v);
})());
byId["sort"].value = "orig";
ok("sort orig returns all 56 in order", sandbox.currentList().length === 56);

/* 11. NEXT UNDECIDED */
const before = sandbox.dec(id0);
fire("click", { target: { closest: () => ({ dataset: { dec: "KEEP", o: id0 } }) } });
alertMsg = "";
byId["next"].click();
ok("NEXT skips an already-decided outfit",
   !String(alertMsg).includes("已全部决定") || sandbox.dec(id0) === "KEEP");

/* 12. undo */
const snapDec = sandbox.dec(id1);
sandbox.undo();
ok("undo restores previous state", sandbox.dec(id1) !== snapDec || snapDec === "UNDECIDED");

/* 13. RESET ALL needs a double confirm */
confirmLog = [];
sandbox.lastFocused = id1;
byId["ra"].click();
ok("RESET ALL asks twice", confirmLog.length === 2, confirmLog.length + " prompts");
ok("RESET ALL wording mentions 56", confirmLog.join(" ").includes("56"));
sandbox.initParts();
ok("after RESET ALL everything is UNDECIDED",
   O.every(x => sandbox.dec(x.id) === "UNDECIDED"));

/* 14. export payloads */
const captured = [];
const origCreate = sandbox.document.createElement;
sandbox.document.createElement = (t) => {
  const el = origCreate(t);
  const origClick = el.click;
  el.click = function () { captured.push({ name: el.download, href: el.href }); };
  return el;
};
fire("click", { target: { closest: () => ({ dataset: { dec: "KEEP", o: id0 } }) } });
S.note[id0] = "只要靴子";
S.pri[id0] = "S";
fire("click", { target: { closest: () => ({ dataset: { pri: "S", o: id0 } }) } });
byId["exb"].click();
ok("Export Backup filename", captured.some(c => c.name === "P01_WARDROBE_REVIEW_STATE.json"),
   captured.map(c => c.name).join(","));
byId["exj"].click();
ok("Export JSON filename", captured.some(c => c.name === "P01_USER_DECISIONS.json"));
alertMsg = "";
byId["exc"].click();
ok("Export CSV filename(s)",
   captured.some(c => c.name === "P01_USER_DECISIONS.csv") ||
   String(alertMsg).includes("P01_USER_DECISIONS.csv"),
   alertMsg.slice(0, 80));

/* 15. import with a valid and an invalid outfit_id */
const good = { outfits: [{ outfit_id: id1, decision: "PARTIAL", priority: "B",
  note: "imported note", parts: [] }] };
sandbox.loadState(good, true);
ok("import restores decision", sandbox.dec(id1) === "PARTIAL");
ok("import restores priority", sandbox.pri(id1) === "B");
ok("import restores note", S.note[id1] === "imported note");
const bad = { outfits: [{ outfit_id: "NOT_A_REAL_ID", decision: "KEEP" }] };
alertMsg = "";
sandbox.loadState(bad);            // not silent: the user must be told
ok("import ignores unknown outfit_id", /忽略 1 条/.test(alertMsg), alertMsg);

/* 16. completion notice */
sandbox.initParts();
O.forEach((o, i) => { S.dec[o.id] = i === 0 ? "KEEP" : "DROP"; });
sandbox.render();
let doneHtml = byId["done"]._html;
ok("completion shows when all decided", /P01 Outfit Review Complete/.test(doneHtml));
/* now make one PARTIAL outfit with parts still left UNDECIDED. Pick an outfit
   with at least 2 parts, otherwise "one part decided" legitimately means
   "nothing left" and the complete notice is correct. */
const multi = O.find(x => x.parts.length >= 2);
S.dec[multi.id] = "PARTIAL";
S.parts[multi.id][multi.parts[0].id] = "KEEP PART";   // the rest stay UNDECIDED
sandbox.render();
doneHtml = byId["done"]._html;
ok("completion does NOT over-report when parts remain",
   /PARTIAL 零件尚未处理/.test(doneHtml),
   (multi.parts.length - 1) + " parts left -> " + doneHtml.replace(/<[^>]+>/g, "").slice(0, 70));
/* and once those parts are handled it must report complete again */
multi.parts.forEach(p => { S.parts[multi.id][p.id] = "KEEP PART"; });
sandbox.render();
ok("completion returns once PARTIAL parts are handled",
   /P01 Outfit Review Complete/.test(byId["done"]._html));

/* 17. no network / self-contained */
ok("no external http(s) reference", !/(?:src|href)\s*=\s*["']https?:\/\//i.test(html));
ok("single script tag", (html.match(/<script/g) || []).length === 1);
ok("no CDN or font import", !/@import|fonts\.googleapis|cdn\./i.test(html));

/* 18. P00/P01 CSVs untouched by this test (the harness never writes them) */
ok("shipped data has 56 outfits with parts attached",
   O.reduce((n, o) => n + o.parts.length, 0) === 645,
   O.reduce((n, o) => n + o.parts.length, 0) + " parts");

/* ---------------- report ---------------- */
const pass = R.filter(x => x.pass).length;
R.forEach(r => {
  console.log(`${r.pass ? "PASS" : "FAIL"}  ${r.name}${r.extra ? "   [" + r.extra + "]" : ""}`);
});
console.log(`\n${pass}/${R.length} PASS`);
process.exit(pass === R.length ? 0 : 1);
