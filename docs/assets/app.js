/* InboxPilot dashboard: reads data/dashboard.json and renders it.
 * If there is no real data yet, it falls back to the fictional demo
 * (data/demo.en.json or data/demo.zh.json).
 * All email-derived text is rendered as plain text (textContent), never HTML.
 */
(() => {
  "use strict";

  const DATA_URL = "data/dashboard.json";
  const demoUrl = (l) => `data/demo.${l}.json`;
  const THEME_KEY = "inboxpilot.theme";
  const LANG_KEY = "inboxpilot.lang";

  /* ---------- i18n ---------- */
  const I18N = {
    en: {
      skip: "Skip to content", title: "Inbox Dashboard", demoFlag: "Demo data", themeAria: "Toggle theme",
      emptyHint: "No data yet. It will appear after the first scheduled run.", viewDemo: "View demo data",
      urgentTitle: "Handle today", next7: "Next 7 days", deadline: "Deadline", meeting: "Meeting", class: "Class",
      todos: "To-dos", newMail: "New mail", mailTabsAria: "Mail categories",
      tracking: "Tracking", trackingNote: "Threads with a status and a deadline: reviews, applications, submissions, orders…",
      thType: "Type", thItem: "Item", thStatus: "Status", thDue: "Due",
      pending: "Waiting for your approval", archived: "Auto-archived today",
      trend: "Mail volume, last 14 days", important: "Important", other: "Other", total: "Total",
      showTable: "Show data table", thDate: "Date",
      suspicious: "Suspicious mail", suspiciousNote: "Not archived — left for you to judge. Don't click links inside.",
      calAdded: "Added to your calendar this run",
      footer: "Updated by your InboxPilot agent on a schedule. All demo content is fictional.",
      dark: "Dark", light: "Light", langBtn: "中文",
      weekdays: ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"],
      today: "Today", tomorrow: "Tomorrow", allDay: "All day", noDue: "No due date",
      updatedAt: (type, when) => `${type || "Update"} · ${when}`, nextAt: (t) => `next at ${t}`,
      reportTypes: { morning: "Morning report", quick: "Quick update", evening: "Evening report" },
      overdueH: (h) => `${h}h overdue`, overdueD: (d) => `${d}d overdue`, minutes: (m) => `${m} min`,
      hoursLeft: (h) => `${h}h left`, days: (d) => `${d} days`, overdueShort: (d) => `${d}d overdue`,
      todayAt: (t) => `Today ${t}`, tomorrowAt: (t) => `Tomorrow ${t}`,
      nothingUrgent: "Nothing needs your attention right now.",
      cTodo: "Open to-dos", cNew: "New today", cPending: "Awaiting approval", cUnread: "Unread in inbox",
      notInCal: "not in calendar", deadlineAt: (t) => `Due ${t}`.trim(),
      todoNote: (l) => `Done? Remove the “${l}” label in Gmail (or just reply) — it's crossed off on the next run.`,
      pendingNote: (l) => `Want to keep one? Remove its “${l}” label in Gmail. The rest is archived tonight.`,
      overdueTag: "! Overdue", doneTag: "✓ Done", noTodos: "No to-dos.",
      all: "All", noSubject: "(no subject)", noMail: "No new mail.", showAll: (n) => `Show all ${n}`, collapse: "Show less",
      noTracking: "Nothing being tracked.", noPending: "Nothing waiting for approval.",
      archivedTotal: (n, l) => `${n} in total, all labelled “${l}” so you can find them again`,
      noArchived: "Nothing auto-archived yet today.", archivedTip: (n) => `${n} auto-archived today`,
      trendEmpty: "The trend appears after a few days of data.", trendAria: "Mail per day over the last 14 days, important vs other",
      demoFail: "Couldn't load the demo data.", loadFail: "Couldn't load data. Refresh to try again.",
      otherCat: "Other",
    },
    zh: {
      skip: "跳到内容", title: "邮件看板", demoFlag: "演示数据", themeAria: "切换深浅色",
      emptyHint: "还没有数据。定时任务第一次运行后这里会自动显示。", viewDemo: "先看演示数据",
      urgentTitle: "今天必须处理", next7: "未来 7 天", deadline: "截止", meeting: "会议", class: "课程",
      todos: "待办", newMail: "新邮件", mailTabsAria: "邮件类别",
      tracking: "进度追踪", trackingNote: "有状态、有期限的邮件线程：审稿、求职、投稿、订单……",
      thType: "类型", thItem: "事项", thStatus: "状态", thDue: "期限",
      pending: "等你批准归档", archived: "今天已自动归档",
      trend: "近 14 天收件量", important: "重要", other: "其他", total: "合计",
      showTable: "查看数据表", thDate: "日期",
      suspicious: "可疑邮件", suspiciousNote: "没有归档，留给你判断。不要点里面的链接。",
      calAdded: "本次新加到日历",
      footer: "由你的 InboxPilot agent 定时更新。演示数据均为虚构。",
      dark: "深色", light: "浅色", langBtn: "EN",
      weekdays: ["周日", "周一", "周二", "周三", "周四", "周五", "周六"],
      today: "今天", tomorrow: "明天", allDay: "全天", noDue: "无期限",
      updatedAt: (type, when) => `${type || "更新"}于 ${when}`, nextAt: (t) => `下次 ${t}`,
      reportTypes: { morning: "晨报", quick: "快报", evening: "晚报" },
      overdueH: (h) => `逾期 ${h} 小时`, overdueD: (d) => `逾期 ${d} 天`, minutes: (m) => `${m} 分钟`,
      hoursLeft: (h) => `还剩 ${h} 小时`, days: (d) => `${d} 天`, overdueShort: (d) => `逾期${d}天`,
      todayAt: (t) => `今天 ${t}`, tomorrowAt: (t) => `明天 ${t}`,
      nothingUrgent: "今天没有必须马上处理的事。",
      cTodo: "待办", cNew: "今天新邮件", cPending: "等你批准归档", cUnread: "收件箱未读",
      notInCal: "日历里还没有", deadlineAt: (t) => `截止 ${t}`.trim(),
      todoNote: (l) => `处理完在 Gmail 里去掉“${l}”标签，或直接回复邮件，下次更新会自动划掉`,
      pendingNote: (l) => `想保留的，在 Gmail 里去掉“${l}”标签；其余今晚统一归档`,
      overdueTag: "! 已逾期", doneTag: "✓ 已完成", noTodos: "没有待办。",
      all: "全部", noSubject: "(无主题)", noMail: "没有新邮件。", showAll: (n) => `显示全部 ${n} 封`, collapse: "收起",
      noTracking: "没有正在追踪的事项。", noPending: "没有等待批准的邮件。",
      archivedTotal: (n, l) => `共 ${n} 封，都打了“${l}”标签，可以回查`,
      noArchived: "今天还没有自动归档。", archivedTip: (n) => `今天自动归档 ${n} 封`,
      trendEmpty: "数据积累几天后这里会出现趋势。", trendAria: "近 14 天每日收件量，分重要和其他两类",
      demoFail: "演示数据加载失败。", loadFail: "数据加载失败，刷新页面再试一次。",
      otherCat: "其他",
    },
  };

  const $ = (sel) => document.querySelector(sel);
  const store = {
    get(k) { try { return localStorage.getItem(k); } catch { return null; } },
    set(k, v) { try { localStorage.setItem(k, v); } catch { /* private mode */ } },
  };

  function pickLang() {
    const q = new URLSearchParams(location.search).get("lang");
    if (q === "zh" || q === "en") return q;
    const saved = store.get(LANG_KEY);
    if (saved === "zh" || saved === "en") return saved;
    return (navigator.language || "").toLowerCase().startsWith("zh") ? "zh" : "en";
  }
  let lang = pickLang();
  const T = () => I18N[lang];

  function applyStaticText() {
    document.documentElement.lang = lang === "zh" ? "zh-CN" : "en";
    for (const n of document.querySelectorAll("[data-i18n]")) {
      const v = T()[n.dataset.i18n];
      if (typeof v === "string") n.textContent = v;
    }
    for (const n of document.querySelectorAll("[data-i18n-aria]")) {
      const v = T()[n.dataset.i18nAria];
      if (typeof v === "string") n.setAttribute("aria-label", v);
    }
    $("#lang-btn").textContent = T().langBtn;
    document.title = `InboxPilot · ${T().title}`;
  }

  /* ---------- helpers ---------- */
  function el(tag, attrs = {}, ...children) {
    const node = document.createElement(tag);
    for (const [k, v] of Object.entries(attrs)) {
      if (v == null || v === false) continue;
      if (k === "class") node.className = v;
      else if (k === "text") node.textContent = v;
      else node.setAttribute(k, v);
    }
    for (const c of children) {
      if (c == null || c === false) continue;
      node.append(c instanceof Node ? c : document.createTextNode(String(c)));
    }
    return node;
  }

  // Only Gmail / Google Calendar links are clickable; anything else renders as text.
  function safeLink(url) {
    try {
      const u = new URL(url);
      if (u.protocol !== "https:") return null;
      if (!/(^|\.)google\.com$/.test(u.hostname)) return null;
      return u.href;
    } catch { return null; }
  }
  function linkOrText(text, url, cls) {
    const href = url && safeLink(url);
    if (!href) return el("span", { class: cls, text });
    return el("a", { class: cls, href, target: "_blank", rel: "noopener noreferrer", text });
  }

  const pad = (n) => String(n).padStart(2, "0");
  function parseDate(s) { if (!s) return null; const d = new Date(s); return isNaN(d) ? null : d; }
  function sameDay(a, b) { return a.getFullYear() === b.getFullYear() && a.getMonth() === b.getMonth() && a.getDate() === b.getDate(); }
  function startOfDay(d) { const x = new Date(d); x.setHours(0, 0, 0, 0); return x; }
  function hm(d) { return `${pad(d.getHours())}:${pad(d.getMinutes())}`; }
  function md(d) { return `${d.getMonth() + 1}/${d.getDate()}`; }
  const wd = (d) => T().weekdays[d.getDay()];

  function countdown(due, now = new Date()) {
    const t = T();
    const ms = due - now, abs = Math.abs(ms);
    const h = Math.floor(abs / 36e5);
    const dDays = Math.round((startOfDay(due) - startOfDay(now)) / 864e5);
    if (ms < 0) {
      if (h < 24) return { big: t.overdueH(Math.max(1, h)), small: `${md(due)} ${hm(due)}` };
      return { big: t.overdueD(Math.abs(dDays)), small: md(due) };
    }
    if (h < 1) return { big: t.minutes(Math.max(1, Math.round(abs / 6e4))), small: t.todayAt(hm(due)) };
    if (h < 24 && dDays === 0) return { big: t.hoursLeft(h), small: t.todayAt(hm(due)) };
    if (dDays === 1) return { big: t.tomorrow, small: hm(due) };
    return { big: t.days(dDays), small: `${md(due)} ${wd(due)}` };
  }

  function dueLabel(due, now = new Date()) {
    const t = T();
    const dDays = Math.round((startOfDay(due) - startOfDay(now)) / 864e5);
    if (dDays < 0) return t.overdueShort(Math.abs(dDays));
    if (dDays === 0) return t.todayAt(hm(due));
    if (dDays === 1) return t.tomorrowAt(hm(due));
    return `${md(due)} ${wd(due)}`;
  }

  async function fetchJSON(url) {
    const res = await fetch(`${url}?t=${Date.now()}`, { cache: "no-store" });
    if (!res.ok) throw Object.assign(new Error(`HTTP ${res.status}`), { status: res.status });
    return res.json();
  }

  const label = (d, key, fallback) => (d.labels && d.labels[key]) || fallback;

  /* ---------- theme ---------- */
  function applyTheme(t) {
    if (t) document.documentElement.setAttribute("data-theme", t);
    else document.documentElement.removeAttribute("data-theme");
    const dark = t ? t === "dark" : window.matchMedia("(prefers-color-scheme: dark)").matches;
    $("#theme-btn").textContent = dark ? T().light : T().dark;
  }

  /* ---------- render ---------- */
  function renderMeta(d) {
    const t = T();
    const gen = parseDate(d.generated_at), next = parseDate(d.next_update);
    const type = t.reportTypes[d.report_type] || d.report_type;
    const parts = [];
    if (gen) parts.push(t.updatedAt(type, `${md(gen)} ${wd(gen)} ${hm(gen)}`));
    if (next) parts.push(t.nextAt(hm(next)));
    $("#meta").textContent = parts.join(lang === "zh" ? "，" : " · ");
  }

  function renderUrgent(d) {
    const box = $("#urgent");
    box.replaceChildren();
    const items = (d.urgent || []).slice(0, 5);
    if (!items.length) { box.append(el("li", {}, el("p", { class: "sign-empty", text: T().nothingUrgent }))); return; }
    for (const it of items) {
      const due = parseDate(it.due);
      const cd = due ? countdown(due) : null;
      box.append(el("li", { class: "sign-item" },
        el("span", { class: "sign-what" }, linkOrText(it.title, it.link)),
        el("span", { class: "sign-detail", text: [it.category, it.detail].filter(Boolean).join(lang === "zh" ? "：" : ": ") }),
        cd ? el("span", { class: "sign-when" }, cd.big, el("small", { text: cd.small })) : null));
    }
  }

  function renderCounts(d) {
    const s = d.stats || {}, t = T();
    const rows = [
      [t.cTodo, s.todo_open, (s.todo_open || 0) > 0],
      [t.cNew, s.new_today],
      [t.cPending, s.pending_archive, (s.pending_archive || 0) > 0],
      [t.cUnread, s.inbox_unread],
    ];
    const box = $("#counts");
    box.replaceChildren();
    for (const [lab, val, alert] of rows) {
      box.append(el("div", { class: `count${alert ? " count--alert" : ""}` },
        el("dt", { text: lab }), el("dd", { text: val ?? "–" })));
    }
  }

  function renderRunway(d) {
    const box = $("#runway"), t = T();
    box.replaceChildren();
    const today = startOfDay(new Date());
    const items = (d.agenda || []).map((a) => ({ ...a, _d: parseDate(a.start) })).filter((a) => a._d);
    for (let i = 0; i < 7; i++) {
      const day = new Date(today); day.setDate(today.getDate() + i);
      const col = el("div", { class: `day${i === 0 ? " day--today" : ""}` },
        el("div", { class: "day-head" },
          el("span", { class: "day-num", text: day.getDate() }),
          el("span", { class: "day-name", text: i === 0 ? t.today : wd(day) })));
      const todays = items.filter((a) => sameDay(a._d, day)).sort((a, b) => a._d - b._d);
      for (const a of todays) {
        const type = ["deadline", "meeting", "class"].includes(a.type) ? a.type : "meeting";
        const time = a.all_day ? t.allDay : hm(a._d);
        const pill = linkOrText("", a.link, `pill pill--${type}`);
        pill.append(el("b", { text: type === "deadline" ? t.deadlineAt(a.all_day ? "" : time) : time }), a.title);
        if (a.in_calendar === false) pill.append(el("span", { class: "pill-flag", text: t.notInCal }));
        col.append(pill);
      }
      box.append(col);
    }
  }

  function renderTodos(d) {
    const t = T();
    $("#todo-note").textContent = t.todoNote(label(d, "todo", "InboxPilot/To-do"));
    let box = $("#todos");
    if (box.tagName !== "UL") { const ul = el("ul", { id: "todos", class: "todo-list" }); box.replaceWith(ul); box = ul; }
    box.replaceChildren();
    const now = new Date();
    const items = (d.todos || []).map((x) => ({ ...x, _d: parseDate(x.due) }));
    const rank = (x) => (x.status === "done" ? 3 : x.status === "overdue" ? 0 : 1);
    items.sort((a, b) => rank(a) - rank(b) || (a._d ? a._d : Infinity) - (b._d ? b._d : Infinity));
    if (!items.length) { box.append(el("li", { class: "empty", text: t.noTodos })); return; }
    for (const x of items) {
      const overdue = x.status === "overdue" || (x.status !== "done" && x._d && x._d < now);
      const soon = !overdue && x.status !== "done" && x._d && x._d - now < 2 * 864e5;
      const cls = ["todo", overdue && "todo--overdue", soon && "todo--soon", x.status === "done" && "todo--done"].filter(Boolean).join(" ");
      const title = el("span", { class: "todo-title" }, linkOrText(x.title, x.link));
      if (overdue) title.append(el("span", { class: "status-tag status-tag--overdue", text: t.overdueTag }));
      if (x.status === "done") title.append(el("span", { class: "status-tag status-tag--done", text: t.doneTag }));
      box.append(el("li", { class: cls },
        el("span", { class: "todo-due", text: x._d ? dueLabel(x._d, now) : t.noDue }),
        title,
        el("span", { class: "todo-meta", text: [x.category, x.source].filter(Boolean).join(lang === "zh" ? "，" : " · ") })));
    }
  }

  let mailCat = null, mailExpanded = false;
  function renderMail(d) {
    const t = T();
    const mails = d.new_mail || [];
    const order = d.category_order || [];
    const counts = new Map();
    for (const m of mails) { const c = m.category || t.otherCat; counts.set(c, (counts.get(c) || 0) + 1); }
    const cats = [...counts.keys()].sort((a, b) => {
      const ia = order.indexOf(a), ib = order.indexOf(b);
      return (ia < 0 ? 99 : ia) - (ib < 0 ? 99 : ib);
    });
    const ALL = "__all__";
    if (mailCat !== ALL && !cats.includes(mailCat)) mailCat = ALL;
    const tabs = $("#mail-tabs");
    tabs.replaceChildren();
    for (const c of [ALL, ...cats]) {
      const n = c === ALL ? mails.length : counts.get(c);
      const b = el("button", { class: "tab", type: "button", role: "tab", "aria-selected": String(c === mailCat) },
        c === ALL ? t.all : c, el("span", { class: "n", text: n }));
      b.addEventListener("click", () => { mailCat = c; mailExpanded = false; renderMail(d); });
      tabs.append(b);
    }
    const list = $("#mail-list");
    list.replaceChildren();
    const shown = mails.filter((m) => mailCat === ALL || (m.category || t.otherCat) === mailCat);
    if (!shown.length) { list.append(el("li", { class: "empty", text: t.noMail })); return; }
    const LIMIT = 6;
    for (const m of mailExpanded ? shown : shown.slice(0, LIMIT)) {
      const r = parseDate(m.received);
      list.append(el("li", { class: "mail" },
        el("div", { class: "mail-top" },
          el("span", { class: "mail-from", text: m.from || "" }),
          el("span", { text: r ? `${md(r)} ${hm(r)}` : "" })),
        linkOrText(m.subject || t.noSubject, m.link, "mail-subject"),
        m.summary ? el("p", { class: "mail-summary", text: m.summary }) : null,
        m.action ? el("p", { class: "mail-action", text: m.action }) : null));
    }
    if (shown.length > LIMIT) {
      const more = el("button", { class: "btn-ghost more-btn", type: "button", text: mailExpanded ? t.collapse : t.showAll(shown.length) });
      more.addEventListener("click", () => { mailExpanded = !mailExpanded; renderMail(d); });
      list.append(el("li", {}, more));
    }
  }

  function renderTracking(d) {
    const t = T();
    const items = d.tracking || [];
    $("#tracking-block").hidden = !items.length;
    const tbody = $("#tracking tbody");
    tbody.replaceChildren();
    for (const r of items) {
      const by = parseDate(r.due);
      const state = ["waiting", "active", "done", "late"].includes(r.state) ? r.state : "active";
      tbody.append(el("tr", {},
        el("td", { class: "tracking-type", text: r.type || "" }),
        el("td", {}, linkOrText(r.item || "", r.link), r.detail ? el("span", { class: "manuscript-title", text: r.detail }) : null),
        el("td", { class: `stage stage--${state}`, text: r.status || "" }),
        el("td", { text: by ? dueLabel(by) : "" })));
    }
  }

  function renderPending(d) {
    const t = T();
    $("#pending-note").textContent = t.pendingNote(label(d, "pending", "InboxPilot/Pending-archive"));
    const box = $("#pending");
    box.replaceChildren();
    const items = d.pending_archive || [];
    if (!items.length) { box.append(el("li", { class: "empty", text: t.noPending })); return; }
    for (const p of items) {
      box.append(el("li", { class: "plain-item" }, el("strong", { text: p.from || "" }), " ", linkOrText(p.subject || "", p.link)));
    }
  }

  function esc(s) { return String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c])); }

  function renderArchived(d) {
    const t = T();
    const a = d.auto_archived || {};
    $("#archived-total").textContent = a.today_total != null ? t.archivedTotal(a.today_total, label(d, "archived", "InboxPilot/Auto-archived")) : "";
    const box = $("#archived-chart");
    box.replaceChildren();
    const rows = (a.by_source || []).slice().sort((x, y) => y.count - x.count).slice(0, 8);
    if (!rows.length) { box.append(el("p", { class: "empty", text: t.noArchived })); return; }
    const max = Math.max(...rows.map((r) => r.count), 1);
    for (const r of rows) {
      const row = el("div", { class: "hbar", tabindex: "0" },
        el("span", { class: "hbar-label", text: r.source }),
        el("div", { class: "hbar-track" }, el("div", { class: "hbar-fill", style: `width:${(r.count / max) * 100}%` })),
        el("span", { class: "hbar-val", text: r.count }));
      bindTip(row, () => `<b>${esc(r.source)}</b><br>${esc(t.archivedTip(r.count))}`);
      box.append(row);
    }
  }

  function renderTrend(d) {
    const t = T();
    const box = $("#trend");
    box.replaceChildren();
    const hist = (d.history || []).slice(-14);
    const tbody = $("#trend-table tbody");
    tbody.replaceChildren();
    if (!hist.length) { box.append(el("p", { class: "empty", text: t.trendEmpty })); return; }

    const W = 720, H = 200, padL = 30, padR = 6, padT = 10, padB = 26;
    const plotW = W - padL - padR, plotH = H - padT - padB;
    const maxV = Math.max(...hist.map((h) => (h.important || 0) + (h.other || 0)), 1);
    const step = niceStep(maxV);
    const top = Math.ceil(maxV / step) * step;
    const colW = plotW / hist.length;
    const barW = Math.min(28, colW * 0.62);
    const NS = "http://www.w3.org/2000/svg";
    const mk = (tag, attrs) => { const n = document.createElementNS(NS, tag); for (const [k, v] of Object.entries(attrs)) n.setAttribute(k, v); return n; };
    const svg = mk("svg", { viewBox: `0 0 ${W} ${H}`, role: "img", "aria-label": t.trendAria });

    for (let v = 0; v <= top; v += step) {
      const y = padT + plotH - (v / top) * plotH;
      svg.append(mk("line", { x1: padL, x2: W - padR, y1: y, y2: y, class: "grid" }));
      const tx = mk("text", { x: padL - 6, y: y + 4, "text-anchor": "end", class: "axis-text" }); tx.textContent = v; svg.append(tx);
    }
    hist.forEach((h, i) => {
      const imp = h.important || 0, oth = h.other || 0;
      const cx = padL + colW * i + colW / 2, x = cx - barW / 2;
      const g = mk("g", { class: "col" });
      g.append(mk("rect", { x: padL + colW * i, y: padT, width: colW, height: plotH, class: "hover-bg", fill: "transparent" }));
      const hImp = (imp / top) * plotH, hOth = (oth / top) * plotH, base = padT + plotH;
      if (imp > 0) g.append(barPath(mk, x, base - hImp, barW, hImp, oth > 0 ? 0 : 4, "bar-s1"));
      if (oth > 0) {
        const gap = imp > 0 ? 2 : 0;
        g.append(barPath(mk, x, base - hImp - gap - hOth, barW, Math.max(hOth, 1), 4, "bar-s2"));
      }
      const dd = parseDate(h.date);
      if (dd && (i % 2 === 0 || i === hist.length - 1)) {
        const tx = mk("text", { x: cx, y: H - 8, "text-anchor": "middle", class: "axis-text" }); tx.textContent = md(dd); svg.append(tx);
      }
      g.append(mk("rect", { x: padL + colW * i, y: padT, width: colW, height: plotH, class: "hit", tabindex: "0" }));
      bindTip(g, () => `<b>${dd ? `${md(dd)} ${wd(dd)}` : ""}</b><br>${t.important} ${imp}<br>${t.other} ${oth}<br>${t.total} ${imp + oth}`, g);
      svg.append(g);
      tbody.append(el("tr", {},
        el("td", { text: dd ? md(dd) : h.date }),
        el("td", { class: "num", text: imp }), el("td", { class: "num", text: oth }), el("td", { class: "num", text: imp + oth })));
    });
    box.append(svg);
  }

  function barPath(mk, x, y, w, h, r, cls) {
    r = Math.min(r, w / 2, h);
    const d = r > 0
      ? `M${x},${y + h} V${y + r} Q${x},${y} ${x + r},${y} H${x + w - r} Q${x + w},${y} ${x + w},${y + r} V${y + h} Z`
      : `M${x},${y + h} V${y} H${x + w} V${y + h} Z`;
    return mk("path", { d, class: cls });
  }
  function niceStep(max) {
    const raw = max / 4, p = Math.pow(10, Math.floor(Math.log10(raw))), n = raw / p;
    return (n <= 1 ? 1 : n <= 2 ? 2 : n <= 5 ? 5 : 10) * p;
  }

  const tip = () => $("#tooltip");
  function bindTip(node, html, activeNode) {
    const show = (x, y) => {
      const tt = tip();
      tt.innerHTML = html();
      tt.hidden = false;
      const r = tt.getBoundingClientRect();
      let left = x + 14, topY = y + 14;
      if (left + r.width > window.innerWidth - 8) left = x - r.width - 14;
      if (topY + r.height > window.innerHeight - 8) topY = y - r.height - 14;
      tt.style.left = `${Math.max(8, left)}px`;
      tt.style.top = `${Math.max(8, topY)}px`;
      activeNode && activeNode.classList.add("is-active");
    };
    const hide = () => { tip().hidden = true; activeNode && activeNode.classList.remove("is-active"); };
    node.addEventListener("pointermove", (e) => show(e.clientX, e.clientY));
    node.addEventListener("pointerleave", hide);
    node.addEventListener("focusin", () => { const r = node.getBoundingClientRect(); show(r.left + r.width / 2, r.top); });
    node.addEventListener("focusout", hide);
  }

  function renderSimpleList(sel, blockSel, items, fmt) {
    const box = $(sel);
    box.replaceChildren();
    $(blockSel).hidden = !items || !items.length;
    for (const it of items || []) box.append(fmt(it));
  }

  function render(d) {
    renderMeta(d); renderUrgent(d); renderCounts(d); renderRunway(d); renderTodos(d);
    renderMail(d); renderTracking(d); renderPending(d); renderArchived(d); renderTrend(d);
    renderSimpleList("#suspicious", "#suspicious-block", d.suspicious, (s) =>
      el("li", { class: "plain-item" }, el("strong", { text: `⚠ ${s.from || ""}` }), " ", el("span", { text: [s.subject, s.reason].filter(Boolean).join(" — ") })));
    renderSimpleList("#calendar-added", "#calendar-block", d.calendar_added, (c) => {
      const w = parseDate(c.when);
      return el("li", { class: "plain-item" }, linkOrText(c.title, c.link), " ", el("span", { text: w ? dueLabel(w) : "" }));
    });
  }

  /* ---------- flow ---------- */
  let current = null; // { data, demo }

  function showApp(data, demo) {
    current = { data, demo };
    $("#empty").hidden = true;
    $("#app").hidden = false;
    $("#demo-flag").hidden = !demo;
    render(data);
  }
  function showEmpty(msg) {
    $("#app").hidden = true;
    $("#empty").hidden = false;
    if (msg) $("#empty-hint").textContent = msg;
  }

  // Demo: shift every date so the demo always looks like "today".
  const DATE_KEYS = new Set(["generated_at", "next_update", "due", "start", "received", "when", "date"]);
  function shiftDates(obj, ms) {
    if (Array.isArray(obj)) return obj.map((x) => shiftDates(x, ms));
    if (obj && typeof obj === "object") {
      const out = {};
      for (const [k, v] of Object.entries(obj)) {
        const d = DATE_KEYS.has(k) && typeof v === "string" ? parseDate(v) : null;
        out[k] = d ? new Date(d.getTime() + ms).toISOString() : shiftDates(v, ms);
      }
      return out;
    }
    return obj;
  }

  async function loadDemo() {
    try {
      const raw = await fetchJSON(demoUrl(lang));
      // Anchor the demo to "now" so every countdown and the 7-day runway look live.
      const base = parseDate(raw.generated_at) || new Date();
      showApp(shiftDates(raw, Date.now() - 5 * 6e4 - base.getTime()), true);
    } catch { showEmpty(T().demoFail); }
  }

  async function loadReal() {
    try { showApp(await fetchJSON(DATA_URL), false); }
    catch (e) {
      if (e && e.status === 404) loadDemo(); // no real data yet → show the demo
      else showEmpty(T().loadFail);
    }
  }

  function init() {
    applyStaticText();
    applyTheme(store.get(THEME_KEY));
    try { window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", () => applyTheme(store.get(THEME_KEY))); } catch { /* old browsers */ }
    const qTheme = new URLSearchParams(location.search).get("theme");
    if (qTheme === "dark" || qTheme === "light") applyTheme(qTheme);

    $("#theme-btn").addEventListener("click", () => {
      const cur = document.documentElement.getAttribute("data-theme")
        || (window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
      const next = cur === "dark" ? "light" : "dark";
      store.set(THEME_KEY, next);
      applyTheme(next);
    });
    $("#lang-btn").addEventListener("click", () => {
      lang = lang === "zh" ? "en" : "zh";
      store.set(LANG_KEY, lang);
      applyStaticText();
      applyTheme(document.documentElement.getAttribute("data-theme"));
      if (current && current.demo) loadDemo();
      else if (current) render(current.data);
    });
    $("#demo-btn").addEventListener("click", loadDemo);

    if (new URLSearchParams(location.search).has("demo")) loadDemo();
    else loadReal();
  }

  document.addEventListener("DOMContentLoaded", init);
})();
