# InboxPilot rules — <USER NAME>

<!-- Agent: fill every <…>. Write in the user's language. Delete rows that don't apply. -->

Last updated: <YYYY-MM-DD>

## Basics

- Mailbox: `<user@example.com>`
- Time zone: `<America/Los_Angeles>`
- Language for digests and labels: `<English | 中文>`
- Digest delivered to: `<user@example.com>` (own address only) + `<push / chat only>`
- Runs: `<08:00 morning · 13:00 quick · 17:00 quick · 20:00 evening>`, weekends `<yes/no>`
- Scope per run: mail from the last 3 days not yet labelled `InboxPilot/Processed`
- Keep only the latest digest in the inbox; archive older digests. Digests are never counted in stats.

## Protected senders (never archived)

| Who | Address / domain |
|---|---|
| <Manager / advisor> | <name@company.example> |
| <Family> | <…> |
| <Key clients> | <@client.example> |

## Categories

| Label | What goes here | Tier |
|---|---|---|
| `<Work/Me>` | Written to the user personally, needs attention | C |
| `<Work/Admin>` | HR, payroll, IT tickets, benefits, forms | C |
| `<Work/Notices>` | All-hands notices, newsletters from own org | D |
| `<Jobs>` | Recruiters, interview scheduling, application updates | C |
| `<Receipts>` | Orders, invoices, shipping | A |
| `<Notifications>` | Social networks, apps, calendar digests | A |
| `<Promo>` | Marketing, sales, bulk newsletters | B |

**Presets by role** (agent: start from one, then adjust):

- *Student / researcher*: Advisor · School/Me · School/Admin · School/Notices · Courses · Reviews · Submissions · Fellowships · Jobs · Receipts · Notifications · Promo
- *Job seeker*: Recruiters · Interviews · Applications · Offers · Job alerts (A) · Receipts · Promo
- *Professional*: Work/Me · Work/Admin · Work/Notices · Clients · Finance · Receipts · Notifications · Promo
- *Freelancer*: Clients · Leads · Invoices · Contracts · Tools/Billing · Receipts · Promo

## Four tiers

| Tier | Handling | Typical mail |
|---|---|---|
| **A** Auto-archive + tell | category label + `Auto-archived`, remove from inbox, count in digest | <social notifications, job alerts, receipts > 7 days, login codes > 1 day, calendar digests> |
| **B** Archive after approval | `Promo` + `Pending-archive`, stays in inbox; archived by the evening run unless the user removes the label | <marketing, sales, bulk newsletters> |
| **C** Keep + report | category label; `To-do` if action needed; full line in digest | <protected senders, personal mail, admin, deadlines, recruiters, invitations, ⚠ suspicious> |
| **D** Keep, one line | category label; one line in digest | <org notices, digests that need no action> |

## Sender-specific rules

<!-- Grows over time as the user says "always do X with Y". -->

| Sender / pattern | Rule |
|---|---|
| <newsletter@site.example> | <A — archive directly> |
| <@society.org eNews> | <B> |

## Calendar

- Clear deadlines → create event "<[Due] …>" with reminders <1 day> and <2 hours> before. Check for duplicates first.
- Meetings and invitations → mention in digest only, never create or answer.

## Change log

- <YYYY-MM-DD>: Initial setup.
