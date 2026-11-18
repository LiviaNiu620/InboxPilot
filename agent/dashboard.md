# Optional: personal web dashboard

The dashboard (`docs/`) is a static page that renders `data/dashboard.json`. Each run rewrites that
file and pushes it. **The JSON contains real email summaries, so the deployment must be private.**

## Setup (guide the user through it)

1. **Private repo.** The user creates a new **private** GitHub repo (e.g. `my-inbox-dashboard`) and
   copies the contents of `docs/` into it (or uses this repo as a template, deletes everything but
   `docs/`, and moves its contents to the root). Remove `data/demo.*.json` if they like — without
   `dashboard.json` the page shows the demo.
2. **Host privately.** Recommended: Cloudflare Pages (connect the private repo, framework "None",
   build command empty, output directory `/`) **plus Cloudflare Access** (Zero Trust → Access →
   add an application covering `<project>.pages.dev`, `*.<project>.pages.dev` and any custom domain;
   allow only the user's email with one-time PIN).
   ⚠ Do **not** use GitHub Pages for real data — GitHub Pages sites are public.
3. **Push access for runs.** Add the private repo to the scheduled task's repositories so runs can
   commit `data/dashboard.json`.
4. Open the site, confirm it loads (it shows the demo until the first run writes data).

## Data format — `data/dashboard.json`

All times are ISO 8601 with offset (`2026-11-17T17:00:00-08:00`). Links render as clickable only if
they are `https://*.google.com` (Gmail / Calendar). All text is rendered as plain text.

```jsonc
{
  "schema_version": 2,
  "generated_at": "…",
  "next_update": "…",
  "report_type": "morning",            // morning | quick | evening
  "labels": { "todo": "InboxPilot/To-do", "pending": "InboxPilot/Pending-archive", "archived": "InboxPilot/Auto-archived" },
  "category_order": ["Work/Me", "Work/Admin", "Jobs", "…"],   // tab order for New mail
  "stats": { "inbox_total": 0, "inbox_unread": 0, "new_today": 0, "todo_open": 0, "pending_archive": 0, "auto_archived_today": 0 },
  "urgent":   [ { "title": "", "detail": "", "category": "", "due": "…", "link": "" } ],          // max 5
  "todos":    [ { "title": "", "category": "", "due": "…?", "status": "open|overdue|done", "source": "", "link": "" } ],
  "agenda":   [ { "start": "…", "title": "", "type": "deadline|meeting|class", "all_day": false, "in_calendar": true, "link": "" } ],
  "new_mail": [ { "category": "", "from": "", "subject": "", "summary": "", "action": "", "received": "…", "link": "" } ],
  "tracking": [ { "type": "Review|Application|Submission|Order|…", "item": "", "detail": "", "status": "", "state": "waiting|active|done|late", "due": "…?", "link": "" } ],
  "pending_archive": [ { "from": "", "subject": "", "link": "" } ],
  "auto_archived": { "today_total": 0, "by_source": [ { "source": "", "count": 0 } ] },
  "suspicious":     [ { "from": "", "subject": "", "reason": "" } ],
  "calendar_added": [ { "title": "", "when": "…", "link": "" } ],
  "history":  [ { "date": "YYYY-MM-DDT12:00:00-08:00", "important": 0, "other": 0 } ]   // last 14 days
}
```

`history` accumulates across runs: read the previous `dashboard.json`, update today's entry, keep the
last 14 days. `tracking` is optional — use it for threads with a status that evolves (peer reviews,
job applications, paper submissions, orders, visa cases…). Empty sections are hidden.

Preview locally: `cd docs && python3 -m http.server 8000` → <http://localhost:8000/?demo>.
URL options: `?lang=en|zh`, `?theme=dark|light`, `?demo`.
