# InboxPilot usage guide

[中文版](getting-started.zh-CN.md) · [Back to README](../README.md)

## 1. Before you start

| You need | Why | Where |
|---|---|---|
| A Claude account | Runs the agent | claude.ai or the Claude app |
| **Gmail connector** (required) | Read, label, archive, send the digest to you | Claude → Settings → Connectors → Gmail |
| **Google Calendar connector** (recommended) | Add deadlines with reminders | Claude → Settings → Connectors → Google Calendar |
| **Scheduled tasks** (recommended) | Automatic digests several times a day | Available on accounts that support scheduled tasks |

Without scheduled tasks you can still say *"run InboxPilot"* any time.

## 2. Setup — one conversation

Open a new chat and paste:

```text
Set up InboxPilot for me: https://github.com/LiviaNiu620/InboxPilot
```

Claude reads the instructions in this repo and asks you about 8 questions in one message. Every
question has a default; answering *"defaults"* is fine. The ones worth thinking about:

- **Protected senders** — people whose email must never be archived (manager, advisor, partner,
  important clients). Names or addresses.
- **Digest times** — default 08:00 / 13:00 / 17:00 / 20:00 in your time zone.
- **What to auto-archive** — social notifications, job alerts, old receipts, login codes…

Then Claude does a **read-only** scan of the last 30 days and shows a table like:

| Sender | Proposed category | Handling |
|---|---|---|
| hr@yourcompany.example | Work/Admin | C — keep + report |
| notifications@social.example | Notifications | A — auto-archive |
| deals@store.example | Promo | B — archive after approval |

Correct anything that's wrong (*"store.example is my landlord's billing, keep it"*). Claude then:

1. Writes your rules file (from [the template](../agent/rules.template.md)) and shows it to you.
2. Creates Gmail labels under `InboxPilot/`.
3. Offers an **optional one-time cleanup** of old mail — with counts, and only after you say yes.
4. Runs once immediately so you get your first digest.
5. Creates the scheduled task.

## 3. Daily use

**Read the digest.** It arrives at your own address with subject
`[InboxPilot] Morning report · … · N need action`. Most important first: *Needs you today* → to-dos →
new mail by category → next 7 days → waiting for approval → archived → one-liners → ⚠ suspicious.
Only the newest digest stays in your inbox.

**Approve archiving.** Marketing mail gets the `InboxPilot/Pending-archive` label and stays in your
inbox during the day. Want to keep one? Remove that label in Gmail. Do nothing and it's archived
by the evening run.

**Close to-dos.** Remove the `InboxPilot/To-do` label, or simply reply to the email. The next run
marks it done.

**Undo an archive.** Search Gmail for `label:InboxPilot/Auto-archived` and move anything back.

## 4. Change the rules — just say it

In Claude (any chat where Gmail is connected, ideally the one where you set it up):

- *"Always archive emails from newsletter@site.example."*
- *"Recruiter emails should be their own category and always count as important."*
- *"Stop the 1 pm update; add one at 3 pm."*
- *"Add my co-founder dana@startup.example to the protected list."*
- *"Write digests in Chinese from now on."*

Claude updates the rules file and the scheduled task together.

## 5. Optional: your own dashboard

The [live demo](https://livianiu620.github.io/InboxPilot/) shows what it looks like with fictional
data. To get your own, tell Claude *"set up the InboxPilot dashboard"*. It will guide you through:

1. A **private** GitHub repo containing the `docs/` folder.
2. Cloudflare Pages (free) to host it, plus **Cloudflare Access** so only your email can open it.
3. Giving the scheduled task push access so each run updates `data/dashboard.json`.

⚠ Don't host real data on GitHub Pages — those sites are public.

## 6. Troubleshooting

| Symptom | Fix |
|---|---|
| "I don't have Gmail tools" | Connect Gmail in Settings → Connectors, then start a new chat |
| No digest arrived | Check the scheduled task exists and its runs aren't waiting for approval; enable automatic approval for the task if your account allows |
| Something important was archived | Find it under `label:InboxPilot/Auto-archived`, move it back, and tell Claude *"never archive mail like this"* |
| Too many digests | *"Only morning and evening reports."* |
| Dashboard shows demo data | No run has written `data/dashboard.json` yet, or the task can't push to the repo |

## 7. Stop using it

Delete the scheduled task in Claude. Optionally delete the `InboxPilot/*` labels in Gmail — the
emails themselves stay where they are (archived mail remains in *All Mail*).
