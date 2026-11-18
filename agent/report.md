# Digest format

Short, scannable, phone-first. Most important first. Plain text or simple HTML (headings, bullets,
bold). Each item links to the Gmail thread. Write in the user's language.

## Structure

1. **Needs you today** — at most 5 items, each: what · why · deadline
2. **To-dos** — open items, overdue first, then by deadline
3. **New mail** — tier C, grouped by category, one line each: sender — summary → action
4. **Next 7 days** — deadlines and meetings (mark ones not yet on the calendar)
5. **Waiting for your approval** — tier B list; "remove the label to keep"
6. **Archived for you** — counts by source (tier A + approved B)
7. **One-liners** — tier D
8. **⚠ Suspicious** — if any
9. Footer: next run time · how to change rules ("reply in Claude: always archive X")

Quick updates: only sections with something new. If nothing important arrived: a single line
("Nothing new that needs you. 6 archived.").

## English example

```
[InboxPilot] Morning report · Tue Nov 17 · 3 need action

NEEDS YOU TODAY
• Submit review JUM-2026-0418 — due tonight 23:59
• Reply to Prof. Rivera with convergence plots — by 17:00
• Pick a phone-screen slot with Northwind Labs (Thu 10:00 / Fri 14:00)

TO-DOS (7 open · 1 overdue)
! Book lab-safety training — 2 days overdue
• Renew tax-treaty form — tomorrow 17:00
• Fellowship statement — Fri 17:00
…

NEW MAIL
Advisor & collaborators
• Dr. Sam Okafor — 12 comments on section 4, two need new runs → before Fri 1:1
Jobs
• Bluepeak Analytics — application received (no action)
…

NEXT 7 DAYS
Wed 13:30 Group meeting · Thu 10:00 Northwind phone screen (not in calendar) · Sun Conference abstract due

WAITING FOR YOUR APPROVAL (6) — remove “InboxPilot/Pending-archive” to keep
Campus Store · Athletics · MileHigh Rewards · Society eNews · CloudNote · Foodly

ARCHIVED FOR YOU (17)
Social 5 · Job alerts 4 · Receipts 3 · Calendar digests 2 · Login codes 2 · Research sites 1

⚠ SUSPICIOUS
it-helpdesk@northfield-help.example — "Your mailbox will be closed" — look-alike sender, asks for password. Not archived; don't click.

Next update 09:53 · To change a rule, just tell Claude.
```

## 中文示例

```
[InboxPilot] 晨报 · 11月17日 周二 · 3 件要处理

今天必须处理
• 提交审稿意见 JUM-2026-0418 — 今晚 23:59 截止
• 给 Rivera 教授发收敛曲线 — 17:00 前
• 选 Northwind Labs 电话面试时间（周四 10 点 / 周五 14 点）

待办（7 项 · 1 项逾期）
! 预约实验室安全培训 — 逾期 2 天
• 更新税务协定表 — 明天 17:00
…

新邮件
导师/合作者
• Sam Okafor — 第 4 节 12 条意见，两条要重跑 → 周五 1:1 前
…

等你批准归档（6）— 想保留就去掉“InboxPilot/待归档”标签
Campus Store · Athletics · MileHigh Rewards · …

已帮你归档（17）
社交通知 5 · 职位推送 4 · 订单收据 3 · …

⚠ 可疑邮件
it-helpdesk@northfield-help.example —“你的邮箱将被关闭”— 仿冒发件人要密码，未归档，别点链接。

下次更新 09:53 · 想改规则，直接跟 Claude 说。
```
