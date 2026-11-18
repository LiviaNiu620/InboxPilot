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

## English example (fictional PhD student)

```
[InboxPilot] Morning report · Tue Nov 17 · 3 need action

NEEDS YOU TODAY
• Return revised manuscript JNC-2026-0771 — revision window closes tonight 23:59
• Post Bio 210 midterm grades — by 18:00
• Vote in the qualifying-exam date poll — closes 17:00

TO-DOS (7 open · 1 overdue)
! Animal-protocol training renewal — 2 days overdue
• Book confocal microscope time — tomorrow 12:00
• Poster abstract for NeuroMeet 2027 — Sat 17:00
…

NEW MAIL
Advisor & lab
• Prof. David Morales — response letter looks good, two small edits for reviewer 2 → submit tonight
Collaborators
• Dr. Tomas Berg — asks for a colour-blind-safe palette in figure 3 → send updated figure
Papers & journals
• Cell Methods Letters — invitation to review CML-26-1180, 14-day window → accept or decline
…

NEXT 7 DAYS
Wed 09:30 Lab meeting · Wed 14:00 Microscope session (not in calendar) · Thu 16:00 Neuro seminar · Sat Poster abstract due

WAITING FOR YOUR APPROVAL (5) — remove “InboxPilot/Pending-archive” to keep
LabSupply Co. · Society eNews · SciPublish · Webinar Hub · CloudNote

ARCHIVED FOR YOU (15)
Research-site digests 5 · Calendar digests 3 · Social 3 · Receipts 2 · Login codes 2

⚠ SUSPICIOUS
editor@journal-neural-circuits.example — "Pay APC to avoid rejection" — look-alike journal domain asking for money. Not archived; don't click.

Next update 09:53 · To change a rule, just tell Claude.
```

## 中文示例（虚构的博士生）

```
[InboxPilot] 晨报 · 11月17日 周二 · 3 件要处理

今天必须处理
• 向《神经环路》返回修改稿 JNC-2026-0771 — 今晚 23:59 截止
• 上传 Bio 210 期中成绩 — 18:00 前
• 资格考日期投票 — 17:00 截止

待办（7 项 · 1 项逾期）
! 动物实验培训续期 — 逾期 2 天
• 预约共聚焦显微镜机时 — 明天 12:00
• NeuroMeet 2027 海报摘要 — 周六 17:00
…

新邮件
导师/实验室
• Morales 教授 — 回复信没问题，审稿人 2 那里改两处 → 今晚提交
合作者
• Tomas Berg — 图 3 换成色盲友好配色 → 发新版图
…

等你批准归档（5）— 想保留就去掉“InboxPilot/待归档”标签
LabSupply Co. · Society eNews · SciPublish · Webinar Hub · CloudNote

已帮你归档（15）
学术网站推送 5 · 日程摘要 3 · 社交通知 3 · 订单收据 2 · 验证码 2

⚠ 可疑邮件
editor@journal-neural-circuits.example —“付版面费否则拒稿”— 仿冒期刊域名索要费用，没归档，别点。

下次更新 09:53 · 想改规则，直接跟 Claude 说。
```
