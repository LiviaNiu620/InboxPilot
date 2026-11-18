# Usage: python3 scripts/make_demo.py docs/data
"""Generate fictional demo data for the InboxPilot dashboard.

Persona: a 3rd-year PhD student in neuroscience (TA, revising a paper).
Two languages -> docs/data/demo.en.json, docs/data/demo.zh.json

Every person, school, company, journal and address here is made up.
"""
import json
import sys
from datetime import datetime, timedelta, timezone

TZ = timezone(timedelta(hours=-8))
BASE = datetime(2026, 11, 17, 7, 55, tzinfo=TZ)
G = "https://mail.google.com/mail/u/0/#inbox"
CAL = "https://calendar.google.com/calendar/r"


def at(days=0, h=0, m=0):
    return (BASE + timedelta(days=days)).replace(hour=h, minute=m, second=0).isoformat()


def ago(hours):
    return (BASE - timedelta(hours=hours)).isoformat()


def history(pairs):
    return [{"date": at(i - 13, 12), "important": a, "other": b} for i, (a, b) in enumerate(pairs)]


def T(e, z):
    return {"en": e, "zh": z}


def loc(obj, lang):
    """Resolve every {"en":..,"zh":..} leaf to one language."""
    if isinstance(obj, dict):
        if set(obj) == {"en", "zh"}:
            return obj[lang]
        return {k: loc(v, lang) for k, v in obj.items()}
    if isinstance(obj, list):
        return [loc(x, lang) for x in obj]
    return obj


LABELS = {"todo": T("InboxPilot/To-do", "InboxPilot/待办"),
          "pending": T("InboxPilot/Pending-archive", "InboxPilot/待归档"),
          "archived": T("InboxPilot/Auto-archived", "InboxPilot/已自动归档")}


# --------------------------------------------------------------- phd
def phd():
    c = dict(adv=T("Advisor & lab", "导师/实验室"), col=T("Collaborators", "合作者"), pub=T("Papers & journals", "论文/期刊"),
             conf=T("Conferences", "会议"), ta=T("Teaching", "助教"), dept=T("Department", "院系事务"),
             fund=T("Funding", "经费/奖学金"), ntc=T("Seminars & notices", "讲座/通知"))
    return {
        "category_order": [c["adv"], c["col"], c["pub"], c["conf"], c["ta"], c["dept"], c["fund"], c["ntc"]],
        "stats": {"inbox_total": 468, "inbox_unread": 33, "new_today": 22, "todo_open": 7, "pending_archive": 5, "auto_archived_today": 15},
        "urgent": [
            {"title": T("Return revised manuscript to Journal of Neural Circuits", "向《神经环路》返回修改稿"), "detail": T("Revision window closes tonight", "修改期限今晚截止"),
             "category": c["pub"], "due": at(0, 23, 59), "link": G},
            {"title": T("Post Bio 210 midterm grades", "上传 Bio 210 期中成绩"), "detail": T("Professor wants them before section tomorrow", "教授要求明天讨论课前上传"),
             "category": c["ta"], "due": at(0, 18, 0), "link": G},
            {"title": T("Confirm qualifying-exam date", "确认资格考日期"), "detail": T("Committee poll closes today", "委员会投票今天截止"),
             "category": c["dept"], "due": at(0, 17, 0), "link": G},
        ],
        "todos": [
            {"title": T("Submit revision + response letter", "提交修改稿和回复信"), "category": c["pub"], "due": at(0, 23, 59), "status": "open", "source": T("Journal of Neural Circuits", "《神经环路》"), "link": G},
            {"title": T("Upload Bio 210 grades", "上传 Bio 210 成绩"), "category": c["ta"], "due": at(0, 18, 0), "status": "open", "source": "Prof. Grace Osei", "link": G},
            {"title": T("Vote in quals date poll", "资格考日期投票"), "category": c["dept"], "due": at(0, 17, 0), "status": "open", "source": T("Grad coordinator", "研究生秘书"), "link": G},
            {"title": T("Book confocal microscope time", "预约共聚焦显微镜机时"), "category": c["adv"], "due": at(1, 12, 0), "status": "open", "source": T("Lab manager", "实验室管理员"), "link": G},
            {"title": T("Poster abstract for neuroscience meeting", "神经科学年会海报摘要"), "category": c["conf"], "due": at(4, 17, 0), "status": "open", "source": "NeuroMeet 2027", "link": G},
            {"title": T("Send co-author the new figure 3", "给合作者发新版图 3"), "category": c["col"], "status": "open", "source": "Dr. Tomas Berg", "link": G},
            {"title": T("Animal-protocol training renewal", "动物实验培训续期"), "category": c["dept"], "due": at(-2, 17, 0), "status": "overdue", "source": T("Research compliance", "科研合规办公室"), "link": G},
            {"title": T("Order antibodies", "订抗体"), "category": c["adv"], "status": "done", "source": T("Lab manager", "实验室管理员"), "link": G},
        ],
        "agenda": [
            {"start": at(0, 11, 0), "title": T("Bio 210 section (TA)", "Bio 210 讨论课（助教）"), "type": "class", "link": CAL},
            {"start": at(0, 17, 0), "title": T("Quals poll", "资格考投票"), "type": "deadline", "link": CAL},
            {"start": at(0, 23, 59), "title": T("Manuscript revision", "论文修改稿"), "type": "deadline", "link": CAL},
            {"start": at(1, 9, 30), "title": T("Lab meeting", "组会"), "type": "meeting", "link": CAL},
            {"start": at(1, 14, 0), "title": T("Microscope session", "显微镜机时"), "type": "meeting", "in_calendar": False, "link": G},
            {"start": at(2, 16, 0), "title": T("Neuro seminar", "神经科学讲座"), "type": "meeting", "link": CAL},
            {"start": at(3, 11, 0), "title": T("Bio 210 section (TA)", "Bio 210 讨论课（助教）"), "type": "class", "link": CAL},
            {"start": at(4, 17, 0), "title": T("Poster abstract", "海报摘要"), "type": "deadline", "link": CAL},
            {"start": at(5, 10, 0), "title": T("1:1 with Prof. Morales", "和 Morales 教授 1:1"), "type": "meeting", "link": CAL},
        ],
        "new_mail": [
            {"category": c["adv"], "from": "Prof. David Morales", "subject": T("Response letter looks good", "回复信没问题"),
             "summary": T("Two small edits to reviewer 2; then submit.", "回复审稿人 2 的地方改两处就可以提交。"), "action": T("Submit tonight", "今晚提交"), "received": ago(2), "link": G},
            {"category": c["adv"], "from": T("Lab manager", "实验室管理员"), "subject": T("Confocal booking for Wednesday", "周三共聚焦显微镜预约"),
             "summary": T("Two slots left; first come first served.", "只剩两个时段，先到先得。"), "action": T("Book by tomorrow noon", "明天中午前预约"), "received": ago(9), "link": G},
            {"category": c["col"], "from": "Dr. Tomas Berg", "subject": T("Figure 3 colours", "图 3 配色"),
             "summary": T("Asks for a colour-blind-safe palette.", "希望换成色盲友好的配色。"), "action": T("Send updated figure", "发新版图"), "received": ago(12), "link": G},
            {"category": c["pub"], "from": T("Journal of Neural Circuits", "《神经环路》"), "subject": T("Reminder: revision due", "提醒：修改稿到期"),
             "summary": "JNC-2026-0771", "action": T("Submit tonight", "今晚提交"), "received": ago(4), "link": G},
            {"category": c["pub"], "from": T("Cell Methods Letters", "《细胞方法快报》"), "subject": T("Invitation to review", "审稿邀请"),
             "summary": T("Calcium-imaging pipeline; 14-day window.", "钙成像分析流程，审稿期 14 天。"), "action": T("Accept or decline", "接受或拒绝"), "received": ago(15), "link": G},
            {"category": c["conf"], "from": "NeuroMeet 2027", "subject": T("Abstract submission closes Saturday", "摘要周六截止"),
             "summary": T("Poster or short talk; 250 words.", "海报或短报告，250 词。"), "received": ago(19), "link": G},
            {"category": c["ta"], "from": "Prof. Grace Osei", "subject": T("Midterm grades by 6 pm", "期中成绩 18 点前"),
             "summary": T("Use the curve we discussed.", "按之前说的方式调分。"), "action": T("Upload grades", "上传成绩"), "received": ago(5), "link": G},
            {"category": c["ta"], "from": T("Student (Bio 210)", "Bio 210 学生"), "subject": T("Regrade request Q4", "第 4 题申请复核"),
             "summary": T("Asks to look at partial credit.", "希望重新看部分得分。"), "received": ago(7), "link": G},
            {"category": c["dept"], "from": T("Grad coordinator", "研究生秘书"), "subject": T("Quals date poll", "资格考日期投票"),
             "summary": T("Three dates in January.", "一月的三个日期。"), "action": T("Vote today", "今天投票"), "received": ago(22), "link": G},
            {"category": c["fund"], "from": T("Graduate School", "研究生院"), "subject": T("Travel grant applications open", "差旅资助开放申请"),
             "summary": T("Up to $800 for presenting students.", "有报告的学生最多 800 美元。"), "received": ago(17), "link": G},
            {"category": c["ntc"], "from": T("Neuro program", "神经科学项目"), "subject": T("Seminar: sleep and memory", "讲座：睡眠与记忆"),
             "summary": T("Thursday 4 pm, Auditorium A.", "周四 16 点，A 报告厅。"), "received": ago(10), "link": G},
        ],
        "tracking": [
            {"type": T("Revision", "修改"), "item": "JNC-2026-0771", "detail": T("Our paper · major revision", "我们的论文 · 大修"), "status": T("Due today", "今天到期"), "state": "late", "due": at(0, 23, 59), "link": G},
            {"type": T("Review", "审稿"), "item": "CML-26-1180", "detail": T("Calcium-imaging pipeline", "钙成像分析流程"), "status": T("Invitation — reply needed", "邀请待回复"), "state": "waiting", "due": at(3, 17, 0), "link": G},
            {"type": T("Abstract", "摘要"), "item": "NeuroMeet 2027", "detail": T("Poster", "海报"), "status": T("Drafting", "撰写中"), "state": "active", "due": at(4, 17, 0), "link": G},
            {"type": T("Grant", "资助"), "item": T("Travel grant", "差旅资助"), "detail": "", "status": T("Not started", "未开始"), "state": "waiting", "link": G},
            {"type": T("Order", "订单"), "item": T("Antibodies", "抗体"), "detail": "", "status": T("Delivered", "已送达"), "state": "done", "link": G},
        ],
        "pending_archive": [
            {"from": "LabSupply Co.", "subject": T("Year-end pipette sale", "年底移液器促销"), "link": G},
            {"from": "Society eNews", "subject": T("November member digest", "11 月会员通讯"), "link": G},
            {"from": "SciPublish", "subject": T("Call for papers (special issue)", "特刊征稿"), "link": G},
            {"from": "Webinar Hub", "subject": T("Free webinar: imaging tips", "免费网课：成像技巧"), "link": G},
            {"from": "CloudNote", "subject": T("Upgrade to Pro", "升级 Pro"), "link": G},
        ],
        "auto_archived": {"today_total": 15, "by_source": [
            {"source": T("Research-site digests", "学术网站推送"), "count": 5},
            {"source": T("Calendar digests", "日程摘要"), "count": 3},
            {"source": T("Social notifications", "社交通知"), "count": 3},
            {"source": T("Receipts", "订单收据"), "count": 2},
            {"source": T("Old login codes", "过期验证码"), "count": 2},
        ]},
        "suspicious": [
            {"from": "editor@journal-neural-circuits.example", "subject": T("Pay APC to avoid rejection", "付版面费否则拒稿"),
             "reason": T("Look-alike journal domain asking for payment", "仿冒期刊域名索要费用")},
        ],
        "calendar_added": [
            {"title": T("[Due] Poster abstract", "[截止] 海报摘要"), "when": at(4, 17, 0), "link": CAL},
        ],
        "history": history([(8, 26), (10, 24), (6, 15), (4, 11), (9, 29), (11, 25), (8, 22), (7, 27), (10, 26), (5, 14), (3, 9), (9, 31), (12, 27), (8, 12)]),
    }


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "docs/data"
    body = phd()
    for lang in ("en", "zh"):
        data = {"schema_version": 2, "generated_at": BASE.isoformat(), "next_update": at(0, 9, 53),
                "report_type": "morning", "labels": LABELS, **body}
        with open(f"{out}/demo.{lang}.json", "w", encoding="utf-8") as f:
            json.dump(loc(data, lang), f, ensure_ascii=False, indent=2)
    print("ok")
