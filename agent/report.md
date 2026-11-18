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

## English example (fictional master's student)

```
[InboxPilot] Morning report · Tue Nov 17 · 3 need action

NEEDS YOU TODAY
• Finish Kestrel AI online assessment — link expires tonight 23:59
• Pick a phone-screen slot with Brightline (Wed 10:00 / Thu 14:00) — reply by 18:00
• Send cleaned capstone dataset to Dr. Singh — by Wed noon

TO-DOS (7 open · 1 overdue)
! Internship CPT form — 1 day overdue
• ML homework 6 — Fri 23:59
• Update resume for career fair — Sat 09:00
…

NEW MAIL
Interviews
• Orbitly — final round Monday 1 pm, three 45-min interviews incl. a case
Applications
• Vantage Retail — not moving forward (no action)
Personal
• Ken Liu — offers a referral at Brightline → send him your resume
…

NEXT 7 DAYS
Wed 10:00 Brightline phone screen (not in calendar) · Thu 15:00 Capstone check-in · Sat 10:00 Tech career fair

WAITING FOR YOUR APPROVAL (6) — remove “InboxPilot/Pending-archive” to keep
CodePrep Pro · JobBoard Weekly · Campus Store · DataCon 2027 · Foodly · CloudNote

ARCHIVED FOR YOU (31)
Job alerts 12 · Social 8 · Application auto-replies 5 · Receipts 3 · Login codes 3

⚠ SUSPICIOUS
hr-team@brightline-careers.example — "Offer letter — pay $85 for equipment" — fake recruiter domain asking for money. Not archived; don't click.

Next update 09:53 · To change a rule, just tell Claude.
```

## 中文示例（虚构的本科生）

```
[InboxPilot] 晨报 · 11月17日 周二 · 3 件要处理

今天必须处理
• 心理学导论实验报告 — 今晚 23:59 截止
• 提交助学金核验表 — 17:00 前，不交春季助学金会暂停
• 回复周四图书馆换班 — 今晚前

待办（6 项 · 1 项逾期）
! 还逾期的图书 — 逾期 1 天
• 春季选课 — 周四 9:00 开放
• 交换项目申请文书 — 周日 17:00
…

新邮件
老师/助教
• Hannah Kim 教授 — 图表可以放附录，正文还是 5 页上限
朋友/家人
• 妈妈 — 问你哪天回家 → 有空回复
…

等你批准归档（8）— 想保留就去掉“InboxPilot/待归档”标签
Campus Store · Athletics · Foodly · StreamBox · …

已帮你归档（23）
社交通知 9 · 课程平台推送 6 · 订单收据 4 · 验证码 3 · 群聊摘要 1

⚠ 可疑邮件
payroll@campus-jobs-portal.example —“立即更新工资账户”— 不是学校真正的发薪邮箱，要银行登录信息，没归档，别点。

下次更新 09:53 · 想改规则，直接跟 Claude 说。
```
