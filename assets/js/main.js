var CHART_DATA = {

  calls: {
    "btc-2023-03": { then: 22000, now: 82660 },
    "btc-2023-10": { then: 28516, now: 82660 },
    "btc-2023-11": { then: 34000, now: 82660 },
    "eth-2023-02": { then: 1687,  now: 2130 },
    "sol-2023-11": { then: 65,    now: 263 }
  },

  bnb: {
    start: ["2020-09-27", 26.25], ath: ["2025-10-13", 1375], startLabel: "$26.25", athLabel: "ATH $1,375",
    months: ["2020-10",28.51,"2020-11",31.49,"2020-12",37.36,"2021-01",44.33,"2021-02",210.21,"2021-03",302.37,"2021-04",622.65,"2021-05",353.33,"2021-06",303.71,"2021-07",332.38,"2021-08",463.9,"2021-09",387.5,"2021-10",524.6,"2021-11",622.5,"2021-12",511.4,"2022-01",374.3,"2022-02",395.6,"2022-03",428.9,"2022-04",377.1,"2022-05",320.9,"2022-06",219.6,"2022-07",283.4,"2022-08",279.2,"2022-09",284.8,"2022-10",325.7,"2022-11",300.6,"2022-12",246.3,"2023-01",312.0,"2023-02",301.4,"2023-03",316.9,"2023-04",337.5,"2023-05",306.8,"2023-06",240.3,"2023-07",241.0,"2023-08",216.7,"2023-09",214.6,"2023-10",226.2,"2023-11",227.6,"2023-12",311.8,"2024-01",300.5,"2024-02",399.4,"2024-03",606.7,"2024-04",578.4,"2024-05",593.7,"2024-06",582.2,"2024-07",576.5,"2024-08",532.9,"2024-09",567.4,"2024-10",576.6,"2024-11",653.43,"2024-12",702.3,"2025-01",677.47,"2025-02",588.07,"2025-03",604.81,"2025-04",599.88,"2025-05",658.01,"2025-06",656.9,"2025-07",783.14,"2025-08",857.65,"2025-09",1008.51]
  },
  eth: {
    start: ["2020-08-06", 394.77], ath: ["2025-08-24", 4957], startLabel: "$394.77", athLabel: "ATH $4,957",
    months: ["2020-08",433.79,"2020-09",359.83,"2020-10",386.46,"2020-11",616.66,"2020-12",736.42,"2021-01",1312.55,"2021-02",1419.18,"2021-03",1919.37,"2021-04",2772.42,"2021-05",2706.15,"2021-06",2275.68,"2021-07",2531.05,"2021-08",3429.2,"2021-09",3000.61,"2021-10",4287.21,"2021-11",4630.26,"2021-12",3676.23,"2022-01",2686.94,"2022-02",2920.95,"2022-03",3281.51,"2022-04",2726.66,"2022-05",1941.9,"2022-06",1071.01,"2022-07",1678.12,"2022-08",1554.1,"2022-09",1328.72,"2022-10",1572.69,"2022-11",1294.46,"2022-12",1196.13,"2023-01",1585.33,"2023-02",1605.23,"2023-03",1821.52,"2023-04",1870.09,"2023-05",1873.63,"2023-06",1933.79,"2023-07",1856.14,"2023-08",1645.76,"2023-09",1670.89,"2023-10",1814.67,"2023-11",2051.96,"2023-12",2281.87,"2024-01",2283.14,"2024-02",3340.09,"2024-03",3645.29,"2024-04",3014.05,"2024-05",3762.29,"2024-06",3438.16,"2024-07",3232.74,"2024-08",2513.01,"2024-09",2602.23,"2024-10",2518.61,"2024-11",3703.6,"2024-12",3337.78,"2025-01",3300.99,"2025-02",2237.59,"2025-03",1822.43,"2025-04",1793.61,"2025-05",2528.06,"2025-06",2485.47,"2025-07",3698.39]
  },

  btf: {
    start: ["2018-01", 260], ath: ["2026-10", 1749], startNote: "Token sale",
    months: ["2020-06", 850], labels: ["$260M", "$850M", "$1.75B"],
    dates: ["Jan 2018", "Jun 2020", "Oct 2026"], ticks: [2020, 2022, 2024]
  }
};

var TO_EMAIL = "kpwhite330@gmail.com";

var SHORT_BIO = "Kyle White is a Youngstown-based venture investor and accelerator builder. He built the Cointelegraph Accelerator (60 investments, $125M in follow-on), leads investor relations at CoreNest Capital, and is a Techstars All-Star Mentor.";

(function () {
  function money(v) { return "$" + v.toLocaleString("en-US"); }

  function toYear(s) {
    var p = s.split("-"), y = +p[0], m = +p[1];
    return p.length > 2 ? y + (m - 1) / 12 + (+p[2] - 1) / 365 : y + m / 12;
  }

  function whenVisible(el, draw) {
    if (!("IntersectionObserver" in window)) return draw();
    var io = new IntersectionObserver(function (es) {
      if (es[0].isIntersecting) { io.disconnect(); draw(); }
    }, { threshold: 0.3 });
    io.observe(el);
  }

  document.querySelectorAll("canvas[data-call]").forEach(function (cv) {
    var c = CHART_DATA.calls[cv.dataset.call];
    if (!c) return;
    whenVisible(cv, function () {
      new Chart(cv, {
        type: "line",
        data: { labels: ["Then", "Now"], datasets: [{ data: [c.then, c.now], pointRadius: 3,
          pointBackgroundColor: ["var(--chart-ink-2)", "var(--chart-ink)"], pointBorderColor: ["var(--chart-ink-2)", "var(--chart-ink)"] }] },
        options: { events: [], layout: { padding: 6 },
          scales: { x: { display: false }, y: { display: false, min: 0 } },
          plugins: { legend: { display: false }, tooltip: { enabled: false } } }
      });
    });
  });

  document.querySelectorAll("canvas[data-built]").forEach(function (cv) {
    var s = CHART_DATA[cv.dataset.built];
    if (!s) return;
    var pts = [{ x: toYear(s.start[0]), y: s.start[1], d: s.start[0] }];
    for (var i = 0; i < s.months.length; i += 2) pts.push({ x: toYear(s.months[i]), y: s.months[i + 1], d: s.months[i] });
    pts.push({ x: toYear(s.ath[0]), y: s.ath[1], d: s.ath[0] });
    var last = pts.length - 1;

    function isEnd(ctx) { return !!s.labels || ctx.dataIndex === 0 || ctx.dataIndex === last; }
    whenVisible(cv, function () {
      new Chart(cv, {
        type: "line",
        data: { datasets: [{ label: cv.dataset.built.toUpperCase(), data: pts, fill: true,
          backgroundColor: Site.wash("var(--chart-ink)", 0.22),
          pointRadius: pts.map(function (p, k) { return s.labels || k === 0 || k === last ? 3.5 : 0; }) }] },
        options: {

          layout: { padding: { top: 22, left: 30, right: 6 } },
          scales: {
            x: { type: "linear", min: pts[0].x, max: pts[last].x,
              afterBuildTicks: function (ax) { if (s.ticks) ax.ticks = s.ticks.map(function (v) { return { value: v }; }); },
              ticks: { stepSize: 1, autoSkip: false, callback: function (v) { return Number.isInteger(v) ? String(v) : ""; } } },
            y: { display: false, min: 0 }
          },
          plugins: {
            legend: { display: false },
            tooltip: { callbacks: {
              title: function (items) { return s.dates ? s.dates[items[0].dataIndex] : items[0].raw.d; },
              label: function (ctx) { return s.labels ? s.labels[ctx.dataIndex] : money(ctx.raw.y); } } },
            datalabels: Object.assign({}, Site.labels.points, {
              display: isEnd, clamp: true,

              align: function (ctx) { return ctx.dataIndex === last ? 180 : "top"; },
              offset: function (ctx) { return ctx.dataIndex === 0 ? 12 : 10; },
              backgroundColor: function (ctx) { return ctx.dataIndex === 0 ? "rgba(11,31,58,.92)" : null; },
              borderRadius: 3,
              padding: function (ctx) { return ctx.dataIndex === 0 ? { top: 2, bottom: 2, left: 4, right: 4 } : 0; },
              formatter: function (v, ctx) {
                var k = ctx.dataIndex;
                if (s.labels) return k === 0 && s.startNote ? s.labels[0] + "\n" + s.startNote : s.labels[k];
                return k === 0 ? s.startLabel : s.athLabel;
              }
            })
          }
        }
      });
    });
  });

  var fBtns = [].slice.call(document.querySelectorAll(".x-filter button"));
  var score = document.getElementById("score");
  var cards = [].slice.call(score.querySelectorAll(".call"));
  fBtns.forEach(function (b) {
    b.addEventListener("click", function () {
      var f = b.dataset.f;
      fBtns.forEach(function (o) { o.setAttribute("aria-pressed", o === b ? "true" : "false"); });
      cards.forEach(function (c) { c.hidden = !(f === "all" || c.dataset.asset === f); });
      score.scrollLeft = 0;
    });
  });

  function copy(text, btn) {
    if (!btn.dataset.label) btn.dataset.label = btn.textContent;
    var t = document.createElement("textarea");
    t.value = text; t.setAttribute("readonly", ""); t.style.position = "fixed"; t.style.opacity = "0";
    document.body.appendChild(t); t.select();
    try { document.execCommand("copy"); } catch (e) {}
    document.body.removeChild(t); btn.focus();
    try { if (navigator.clipboard) navigator.clipboard.writeText(text).catch(function () {}); } catch (e) {}
    btn.textContent = "Copied"; btn.setAttribute("aria-live", "polite");
    clearTimeout(btn._t); btn._t = setTimeout(function () { btn.textContent = btn.dataset.label; }, 1800);
  }
  document.getElementById("copyBio").addEventListener("click", function () { copy(SHORT_BIO, this); });

  var form = document.getElementById("bookForm"), done = document.getElementById("done"), req = document.getElementById("reqText");
  function val(id) { return document.getElementById(id).value.trim(); }
  function setErr(id, msg) {
    var f = document.getElementById("f-" + id), e = document.getElementById("e-" + id);
    e.textContent = msg || "";
    if (msg) { f.setAttribute("aria-invalid", "true"); f.setAttribute("aria-describedby", "e-" + id); } else { f.removeAttribute("aria-invalid"); }
    return !msg;
  }
  function check() {
    var good = true, first = null;
    [["name", "Add your name."], ["org", "Add your organization or show."], ["type", "Choose a format."], ["msg", "Add a short message."]].forEach(function (p) {
      if (!setErr(p[0], val("f-" + p[0]) ? "" : p[1])) { good = false; first = first || p[0]; }
    });
    var em = val("f-email"), emOk = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(em);
    if (!setErr("email", em ? (emOk ? "" : "Check the email address.") : "Add your email.")) { good = false; first = first || "email"; }
    if (first) document.getElementById("f-" + first).focus();
    return good;
  }
  form.querySelectorAll("input,select,textarea").forEach(function (f) {
    f.addEventListener("input", function () { if (f.getAttribute("aria-invalid") === "true") setErr(f.id.slice(2), ""); });
  });
  form.addEventListener("submit", function (ev) {
    ev.preventDefault();
    if (!check()) return;
    var type = val("f-type"), org = val("f-org");
    var subject = "Booking request: " + type + " | " + org;
    var body = ["Name: " + val("f-name"), "Email: " + val("f-email"), "Organization or show: " + org, "Format: " + type, "Event date: " + (val("f-date") || "Flexible"), "Location or virtual: " + (val("f-loc") || "Not set"), "Audience size: " + (val("f-aud") || "Not set"), "Budget: " + (val("f-budget") || "Not set"), "", "Message:", val("f-msg")].join("\n");
    var url = "mailto:" + TO_EMAIL + "?subject=" + encodeURIComponent(subject) + "&body=" + encodeURIComponent(body);
    try {
      var a = document.createElement("a"); a.href = url; a.target = "_blank"; a.rel = "noopener";
      document.body.appendChild(a); a.click(); document.body.removeChild(a);
    } catch (e) { try { window.location.href = url; } catch (e2) {} }
    req.value = "To: " + TO_EMAIL + "\nSubject: " + subject + "\n\n" + body;
    form.hidden = true; done.hidden = false;
    var h = done.querySelector("h3"); h.setAttribute("tabindex", "-1"); h.focus();
  });
  document.getElementById("copyReq").addEventListener("click", function () { copy(req.value, this); });
  document.getElementById("restart").addEventListener("click", function () {
    form.reset(); ["name", "email", "org", "type", "msg"].forEach(function (id) { setErr(id, ""); });
    done.hidden = true; form.hidden = false; document.getElementById("f-name").focus();
  });

  document.querySelectorAll("a[data-format]").forEach(function (a) {
    a.addEventListener("click", function () {
      var sel = document.getElementById("f-type");
      if (form.hidden) { form.hidden = false; done.hidden = true; }
      sel.value = a.dataset.format;
      setErr("type", "");
    });
  });

  document.getElementById("printSheet").addEventListener("click", function () { window.print(); });

  var navT = document.getElementById("navToggle"), navL = document.getElementById("navLinks");
  function setNav(open) { navT.setAttribute("aria-expanded", open ? "true" : "false"); navL.classList.toggle("is-open", open); }
  navT.addEventListener("click", function () { setNav(navT.getAttribute("aria-expanded") !== "true"); });
  navL.addEventListener("click", function (e) { if (e.target.closest("a")) setNav(false); });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape" && navT.getAttribute("aria-expanded") === "true") { setNav(false); navT.focus(); } });
  document.addEventListener("click", function (e) { if (!e.target.closest(".nav")) setNav(false); });
  window.addEventListener("resize", function () { if (window.innerWidth > 640) setNav(false); });
})();

(function () {
  if (!window.fetch) return;
  function run() {
  var ctl = window.AbortController ? new AbortController() : null;
  var timer = setTimeout(function () { if (ctl) ctl.abort(); }, 4000);
  fetch("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd", ctl ? { signal: ctl.signal } : {})
    .finally(function () { clearTimeout(timer); })
    .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
    .then(function (j) {
      var px = j && j.bitcoin && +j.bitcoin.usd;
      if (!px || !isFinite(px)) return;
      var asof = "as of " + new Date().toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" });
      document.querySelectorAll('.call[data-asset="btc"]').forEach(function (card) {
        var cv = card.querySelector("canvas[data-call]"), c = cv && CHART_DATA.calls[cv.dataset.call];
        if (!c) return;
        c.now = Math.round(px);
        var gain = Math.round((px / c.then - 1) * 100);
        var now = card.querySelector('[data-btc="now"]'), pct = card.querySelector('[data-btc="pct"]'), when = card.querySelector('[data-btc="asof"]');
        if (now) now.textContent = "$" + Math.round(px).toLocaleString("en-US");
        if (pct) pct.textContent = (gain >= 0 ? "+" : "") + gain + "%";
        if (when) when.textContent = asof;
        var ch = window.Chart && Chart.getChart && Chart.getChart(cv);
        if (ch) { ch.data.datasets[0].data[1] = c.now; ch.update("none"); }
      });
    })
    .catch(function () {});
  }

  var started = false;
  function start() { if (started) return; started = true; setTimeout(run, 0); }
  var score = document.getElementById("score");
  function watch() {
    if (!score || !("IntersectionObserver" in window)) return setTimeout(start, 3000);
    var io = new IntersectionObserver(function (es) {
      if (es[0].isIntersecting) { io.disconnect(); start(); }
    }, { rootMargin: "400px 0px" });
    io.observe(score);
  }
  watch();
})();
