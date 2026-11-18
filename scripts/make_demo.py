# Usage: python3 scripts/make_demo.py docs/data
"""Generate fictional demo data (EN + ZH) for the InboxPilot dashboard.
Every person, school, company, journal and address here is made up."""
import json, sys
from datetime import datetime, timedelta, timezone

TZ = timezone(timedelta(hours=-8))
BASE = datetime(2026, 11, 17, 7, 55, tzinfo=TZ)
G = "https://mail.google.com/mail/u/0/#inbox"
CAL = "https://calendar.google.com/calendar/r"


def at(days=0, h=0, m=0):
    d = (BASE + timedelta(days=days)).replace(hour=h, minute=m, second=0)
    return d.isoformat()


def ago(hours):
    return (BASE - timedelta(hours=hours)).isoformat()


history_counts = [(9, 31), (12, 28), (7, 19), (5, 14), (11, 35), (14, 30), (10, 27),
                  (8, 33), (13, 29), (6, 17), (4, 12), (12, 38), (15, 31), (9, 14)]
history = [{"date": at(i - 13, 12), "important": a, "other": b} for i, (a, b) in enumerate(history_counts)]

C = {
    "en": dict(adv="Advisor & collaborators", me="School · for me", adm="School · admin", rev="Reviews",
               sub="Submissions & conferences", job="Jobs", crs="Courses", ppl="Personal", ntc="School notices"),
    "zh": dict(adv="导师/合作者", me="学校·与我相关", adm="学校·事务", rev="审稿",
               sub="投稿/会议", job="求职", crs="课程", ppl="真人来信", ntc="学校通知"),
}


def build(lang):
    c = C[lang]
    zh = lang == "zh"
    L = (lambda e, z: z if zh else e)
    data = {
        "schema_version": 2,
        "generated_at": BASE.isoformat(),
        "next_update": at(0, 9, 53),
        "report_type": "morning",
        "labels": {
            "todo": L("InboxPilot/To-do", "InboxPilot/待办"),
            "pending": L("InboxPilot/Pending-archive", "InboxPilot/待归档"),
            "archived": L("InboxPilot/Auto-archived", "InboxPilot/已自动归档"),
        },
        "category_order": [c["adv"], c["me"], c["adm"], c["rev"], c["sub"], c["job"], c["crs"], c["ppl"], c["ntc"]],
        "stats": {"inbox_total": 386, "inbox_unread": 29, "new_today": 24, "todo_open": 7,
                  "pending_archive": 6, "auto_archived_today": 17},
        "urgent": [
            {"title": L("Submit review for Journal of Urban Mobility", "提交《城市出行学报》审稿意见"),
             "detail": L("Manuscript JUM-2026-0418, due tonight", "稿件 JUM-2026-0418，今晚截止"),
             "category": c["rev"], "due": at(0, 23, 59), "link": G},
            {"title": L("Send weekly progress to Prof. Rivera", "给 Rivera 教授发周进度"),
             "detail": L("She asked for the convergence plots before group meeting", "她想在组会前看到收敛曲线"),
             "category": c["adv"], "due": at(0, 17, 0), "link": G},
            {"title": L("Confirm phone-screen slot with Northwind Labs", "确认 Northwind Labs 电话面试时间"),
             "detail": L("Recruiter offered Thu 10:00 or Fri 14:00", "招聘方给了周四 10 点或周五 14 点"),
             "category": c["job"], "due": at(0, 20, 0), "link": G},
        ],
        "todos": [
            {"title": L("Submit JUM-2026-0418 review", "提交 JUM-2026-0418 审稿意见"), "category": c["rev"], "due": at(0, 23, 59), "status": "open", "source": L("Review system", "审稿系统"), "link": G},
            {"title": L("Reply to Prof. Rivera with progress", "回复 Rivera 教授进度"), "category": c["adv"], "due": at(0, 17, 0), "status": "open", "source": "Prof. Rivera", "link": G},
            {"title": L("Pick a phone-screen slot", "选电话面试时间"), "category": c["job"], "due": at(0, 20, 0), "status": "open", "source": "Northwind Labs", "link": G},
            {"title": L("Renew tax-treaty form", "更新税务协定表"), "category": c["adm"], "due": at(1, 17, 0), "status": "open", "source": L("International office", "国际学生办公室"), "link": G},
            {"title": L("Fellowship application: upload statement", "Fellowship 申请：上传个人陈述"), "category": c["me"], "due": at(3, 17, 0), "status": "open", "source": L("Graduate school", "研究生院"), "link": G},
            {"title": L("RSVP for department holiday party", "院系年终聚会 RSVP"), "category": c["adm"], "due": at(6, 12, 0), "status": "open", "source": L("Dept. coordinator", "院系秘书"), "link": G},
            {"title": L("Answer Mia's question about the reading group", "回复 Mia 关于读书会的问题"), "category": c["ppl"], "status": "open", "source": "Mia Park", "link": G},
            {"title": L("Book lab-safety training", "预约实验室安全培训"), "category": c["adm"], "due": at(-2, 17, 0), "status": "overdue", "source": "EHS", "link": G},
            {"title": L("Submit travel reimbursement", "提交差旅报销"), "category": c["sub"], "status": "done", "source": L("Dept. finance", "院系财务"), "link": G},
        ],
        "agenda": [
            {"start": at(0, 10, 0), "title": L("Optimization lecture", "优化课"), "type": "class", "link": CAL},
            {"start": at(0, 17, 0), "title": L("Progress to advisor", "给导师发进度"), "type": "deadline", "link": CAL},
            {"start": at(0, 23, 59), "title": L("JUM review", "JUM 审稿"), "type": "deadline", "link": CAL},
            {"start": at(1, 13, 30), "title": L("Group meeting", "组会"), "type": "meeting", "link": CAL},
            {"start": at(1, 17, 0), "title": L("Tax-treaty form", "税务协定表"), "type": "deadline", "link": CAL},
            {"start": at(2, 10, 0), "title": L("Northwind phone screen", "Northwind 电话面试"), "type": "meeting", "in_calendar": False, "link": G},
            {"start": at(2, 15, 0), "title": L("Optimization lecture", "优化课"), "type": "class", "link": CAL},
            {"start": at(3, 17, 0), "title": L("Fellowship statement", "Fellowship 陈述"), "type": "deadline", "link": CAL},
            {"start": at(4, 11, 0), "title": L("1:1 with co-author", "和合作者 1:1"), "type": "meeting", "link": CAL},
            {"start": at(5, 0, 0), "title": L("Conference abstract due", "会议摘要截止"), "type": "deadline", "all_day": True, "link": CAL},
            {"start": at(6, 12, 0), "title": L("Holiday party RSVP", "年终聚会 RSVP"), "type": "deadline", "link": CAL},
        ],
        "new_mail": [
            {"category": c["adv"], "from": "Prof. Elena Rivera", "subject": L("Plots before Thursday?", "周四前能看到图吗？"),
             "summary": L("Wants convergence plots for the equilibrium model and a one-paragraph summary.", "想看均衡模型的收敛曲线，再附一段总结。"),
             "action": L("Reply by 5 pm today", "今天 17 点前回复"), "received": ago(2), "link": G},
            {"category": c["adv"], "from": "Dr. Sam Okafor", "subject": L("Shared draft — section 4 comments", "共享稿：第 4 节意见"),
             "summary": L("Left 12 comments on the experiments section; two need new runs.", "在实验部分留了 12 条意见，其中两条需要重跑。"),
             "action": L("Review comments before Friday 1:1", "周五 1:1 前看完"), "received": ago(9), "link": G},
            {"category": c["me"], "from": L("Graduate School", "研究生院"), "subject": L("Your fellowship application is incomplete", "你的 Fellowship 申请还缺材料"),
             "summary": L("Personal statement missing; portal closes in 3 days.", "缺个人陈述，系统 3 天后关闭。"),
             "action": L("Upload statement", "上传个人陈述"), "received": ago(5), "link": G},
            {"category": c["adm"], "from": L("International Office", "国际学生办公室"), "subject": L("Action needed: tax-treaty renewal", "需要处理：税务协定续期"),
             "summary": L("Annual renewal for the 2027 tax year.", "2027 税务年度的年度续期。"),
             "action": L("Complete form by tomorrow", "明天前填完"), "received": ago(11), "link": G},
            {"category": c["rev"], "from": L("Journal of Urban Mobility", "城市出行学报"), "subject": L("Reminder: review due today", "提醒：审稿今天到期"),
             "summary": "JUM-2026-0418", "action": L("Submit tonight", "今晚提交"), "received": ago(3), "link": G},
            {"category": c["rev"], "from": L("Transport Systems Letters", "交通系统快报"), "subject": L("Invitation to review TSL-26-0932", "审稿邀请 TSL-26-0932"),
             "summary": L("Mixed-traffic signal control; 21-day review window.", "混合交通信号控制，审稿期 21 天。"),
             "action": L("Accept or decline by Friday", "周五前接受或拒绝"), "received": ago(14), "link": G},
            {"category": c["sub"], "from": L("Mobility Systems Conference 2027", "2027 出行系统会议"), "subject": L("Abstract deadline in 5 days", "摘要 5 天后截止"),
             "summary": L("Extended abstracts (2 pages) accepted until Sunday.", "两页扩展摘要，周日截止。"), "received": ago(18), "link": G},
            {"category": c["job"], "from": "Jordan Lee · Northwind Labs", "subject": L("Next step: 30-min phone screen", "下一步：30 分钟电话面试"),
             "summary": L("Offers Thu 10:00 or Fri 14:00 PT for the Data Scientist intern role.", "数据科学实习岗，周四 10 点或周五 14 点。"),
             "action": L("Pick a slot", "选一个时间"), "received": ago(4), "link": G},
            {"category": c["job"], "from": "Bluepeak Analytics", "subject": L("Thanks for applying", "感谢投递"),
             "summary": L("Application received; no action.", "已收到申请，无需操作。"), "received": ago(20), "link": G},
            {"category": c["crs"], "from": L("Optimization (Fall)", "优化课（秋季）"), "subject": L("HW 7 posted", "第 7 次作业已发布"),
             "summary": L("Due next Wednesday; office hours moved to Room 210.", "下周三交；答疑改到 210 教室。"), "received": ago(7), "link": G},
            {"category": c["ppl"], "from": "Mia Park", "subject": L("Reading group this week?", "这周读书会吗？"),
             "summary": L("Asks if you can lead the discussion on Thursday.", "问你周四能不能带讨论。"),
             "action": L("Reply when you can", "有空回复"), "received": ago(6), "link": G},
            {"category": c["ntc"], "from": L("Campus Safety", "校园安全"), "subject": L("Road closure on Elm Street", "Elm 街临时封路"),
             "summary": L("Friday 6–10 pm. No action.", "周五 18–22 点，无需操作。"), "received": ago(10), "link": G},
            {"category": c["ntc"], "from": L("Dept. Newsletter", "院系通讯"), "subject": L("Seminar: equilibrium in congested networks", "讲座：拥堵网络中的均衡"),
             "summary": L("Wednesday 4 pm, Hall B.", "周三 16 点，B 厅。"), "received": ago(16), "link": G},
        ],
        "tracking": [
            {"type": L("Review", "审稿"), "item": "JUM-2026-0418", "detail": L("Equilibrium pricing with ride-hailing", "网约车的均衡定价"), "status": L("Due today", "今天到期"), "state": "late", "due": at(0, 23, 59), "link": G},
            {"type": L("Review", "审稿"), "item": "TSL-26-0932", "detail": L("Signal control in mixed traffic", "混合交通信号控制"), "status": L("Invitation — reply needed", "邀请待回复"), "state": "waiting", "due": at(3, 17, 0), "link": G},
            {"type": L("Submission", "投稿"), "item": L("Paper: coalition routing", "论文：联盟路径选择"), "detail": L("Network Economics Review", "《网络经济评论》"), "status": L("Under review · day 41", "在审 · 第 41 天"), "state": "active", "link": G},
            {"type": L("Application", "求职"), "item": "Northwind Labs", "detail": L("Data Scientist Intern", "数据科学实习"), "status": L("Phone screen", "电话面试"), "state": "waiting", "due": at(2, 10, 0), "link": G},
            {"type": L("Application", "求职"), "item": "Bluepeak Analytics", "detail": L("Research Intern", "研究实习"), "status": L("Applied", "已投递"), "state": "active", "link": G},
            {"type": L("Fellowship", "Fellowship"), "item": L("Graduate Fellowship", "研究生奖学金"), "detail": "", "status": L("Missing statement", "缺个人陈述"), "state": "waiting", "due": at(3, 17, 0), "link": G},
        ],
        "pending_archive": [
            {"from": "Campus Store", "subject": L("Black Friday: 30% off hoodies", "黑五：卫衣七折"), "link": G},
            {"from": "Athletics", "subject": L("Get tickets for Saturday's game", "周六比赛门票开抢"), "link": G},
            {"from": "MileHigh Rewards", "subject": L("Your points are about to expire", "你的积分即将过期"), "link": G},
            {"from": "Society eNews", "subject": L("November member digest", "11 月会员通讯"), "link": G},
            {"from": "CloudNote", "subject": L("Upgrade to Pro and save 40%", "升级 Pro 省 40%"), "link": G},
            {"from": "Foodly", "subject": L("Free delivery this weekend", "本周末免配送费"), "link": G},
        ],
        "auto_archived": {"today_total": 17, "by_source": [
            {"source": L("Social notifications", "社交通知"), "count": 5},
            {"source": L("Job alerts", "职位推送"), "count": 4},
            {"source": L("Receipts", "订单收据"), "count": 3},
            {"source": L("Calendar digests", "日程摘要"), "count": 2},
            {"source": L("Old login codes", "过期验证码"), "count": 2},
            {"source": L("Research-site digests", "学术网站推送"), "count": 1},
        ]},
        "suspicious": [
            {"from": "it-helpdesk@northfield-help.example", "subject": L("Your mailbox will be closed", "你的邮箱将被关闭"),
             "reason": L("Look-alike sender asking you to re-enter your password", "仿冒发件人，要求重新输入密码")},
        ],
        "calendar_added": [
            {"title": L("[Due] Tax-treaty form", "[截止] 税务协定表"), "when": at(1, 17, 0), "link": CAL},
            {"title": L("[Due] Fellowship statement", "[截止] Fellowship 个人陈述"), "when": at(3, 17, 0), "link": CAL},
        ],
        "history": history,
    }
    return data


out = sys.argv[1]
for lang in ("en", "zh"):
    with open(f"{out}/demo.{lang}.json", "w", encoding="utf-8") as f:
        json.dump(build(lang), f, ensure_ascii=False, indent=2)
print("ok")
