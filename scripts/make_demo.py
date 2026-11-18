# Usage: python3 scripts/make_demo.py docs/data
"""Generate fictional demo data for the InboxPilot dashboard.

Three personas x two languages -> docs/data/demo.<persona>.<lang>.json
  undergrad : 2nd-year undergraduate (psychology), part-time library job
  master    : 1st-year master's in data science, internship hunting
  phd       : 3rd-year PhD in neuroscience, TA, preparing a paper

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


# --------------------------------------------------------------- undergrad
def undergrad():
    c = dict(prof=T("Professors & TAs", "老师/助教"), crs=T("Courses", "课程"), adm=T("Registrar & aid", "教务/助学金"),
             job=T("Campus job", "校内工作"), club=T("Clubs", "社团"), ppl=T("Friends & family", "朋友/家人"),
             ntc=T("Campus notices", "校园通知"))
    return {
        "category_order": [c["prof"], c["crs"], c["adm"], c["job"], c["club"], c["ppl"], c["ntc"]],
        "stats": {"inbox_total": 214, "inbox_unread": 41, "new_today": 19, "todo_open": 6, "pending_archive": 8, "auto_archived_today": 23},
        "urgent": [
            {"title": T("Psych 101 lab report due", "心理学导论实验报告截止"), "detail": T("Upload to the course site before midnight", "今晚 12 点前传到课程网站"),
             "category": c["crs"], "due": at(0, 23, 59), "link": G},
            {"title": T("Submit financial-aid verification form", "提交助学金核验表"), "detail": T("Aid for spring is on hold until it's in", "不交的话春季助学金会暂停"),
             "category": c["adm"], "due": at(0, 17, 0), "link": G},
            {"title": T("Swap Thursday library shift?", "周四图书馆班要换吗？"), "detail": T("Supervisor needs an answer by tonight", "主管今晚前要答复"),
             "category": c["job"], "due": at(0, 20, 0), "link": G},
        ],
        "todos": [
            {"title": T("Finish Psych 101 lab report", "写完心理学实验报告"), "category": c["crs"], "due": at(0, 23, 59), "status": "open", "source": "Psych 101", "link": G},
            {"title": T("Upload aid verification form", "上传助学金核验表"), "category": c["adm"], "due": at(0, 17, 0), "status": "open", "source": T("Financial Aid Office", "助学金办公室"), "link": G},
            {"title": T("Answer shift-swap request", "回复换班请求"), "category": c["job"], "due": at(0, 20, 0), "status": "open", "source": T("Library desk", "图书馆前台"), "link": G},
            {"title": T("Register for spring classes", "选春季课"), "category": c["adm"], "due": at(2, 9, 0), "status": "open", "source": T("Registrar", "教务处"), "link": G},
            {"title": T("Study-abroad application essay", "交换项目申请文书"), "category": c["adm"], "due": at(5, 17, 0), "status": "open", "source": T("Global Programs", "海外项目办公室"), "link": G},
            {"title": T("Pay robotics club dues", "交机器人社团会费"), "category": c["club"], "status": "open", "source": "Robotics Club", "link": G},
            {"title": T("Return overdue library book", "还逾期的图书"), "category": c["ntc"], "due": at(-1, 17, 0), "status": "overdue", "source": T("Library", "图书馆"), "link": G},
            {"title": T("Sign up for stats office hours", "预约统计课答疑"), "category": c["crs"], "status": "done", "source": "Stats 120", "link": G},
        ],
        "agenda": [
            {"start": at(0, 9, 0), "title": T("Stats 120 lecture", "统计课"), "type": "class", "link": CAL},
            {"start": at(0, 17, 0), "title": T("Aid form", "助学金表"), "type": "deadline", "link": CAL},
            {"start": at(0, 23, 59), "title": T("Psych lab report", "心理学实验报告"), "type": "deadline", "link": CAL},
            {"start": at(1, 11, 0), "title": T("Psych 101 lecture", "心理学导论"), "type": "class", "link": CAL},
            {"start": at(1, 18, 30), "title": T("Robotics club build night", "机器人社团活动"), "type": "meeting", "link": CAL},
            {"start": at(2, 9, 0), "title": T("Spring registration opens", "春季选课开放"), "type": "deadline", "link": CAL},
            {"start": at(2, 15, 0), "title": T("Study group — stats", "统计学习小组"), "type": "meeting", "in_calendar": False, "link": G},
            {"start": at(3, 10, 0), "title": T("Stats midterm", "统计期中考"), "type": "class", "link": CAL},
            {"start": at(5, 17, 0), "title": T("Study-abroad essay", "交换项目文书"), "type": "deadline", "link": CAL},
            {"start": at(6, 0, 0), "title": T("Thanksgiving break begins", "感恩节假期开始"), "type": "meeting", "all_day": True, "link": CAL},
        ],
        "new_mail": [
            {"category": c["prof"], "from": "Prof. Hannah Kim", "subject": T("Lab report: one clarification", "实验报告补充说明"),
             "summary": T("Figures can go in an appendix; page limit stays at 5.", "图表可以放附录，正文还是 5 页上限。"), "received": ago(3), "link": G},
            {"category": c["prof"], "from": T("Leo Martins (TA)", "助教 Leo Martins"), "subject": T("Midterm review session moved", "期中复习课改时间"),
             "summary": T("Now Wednesday 6 pm, Room 114.", "改到周三 18 点，114 教室。"), "received": ago(8), "link": G},
            {"category": c["crs"], "from": "Stats 120", "subject": T("Practice midterm posted", "期中模拟题已发布"),
             "summary": T("Solutions released Thursday.", "答案周四公布。"), "received": ago(10), "link": G},
            {"category": c["adm"], "from": T("Financial Aid Office", "助学金办公室"), "subject": T("Action required: verification", "需要处理：材料核验"),
             "summary": T("One form missing for spring aid.", "春季助学金还缺一张表。"), "action": T("Upload by 5 pm", "17 点前上传"), "received": ago(5), "link": G},
            {"category": c["adm"], "from": T("Registrar", "教务处"), "subject": T("Your spring registration time", "你的春季选课时间"),
             "summary": T("Window opens Thursday 9:00.", "周四 9 点开放。"), "action": T("Check holds before then", "提前检查有没有选课限制"), "received": ago(14), "link": G},
            {"category": c["job"], "from": T("Library desk", "图书馆前台"), "subject": T("Can anyone swap Thu 4–8?", "周四 4–8 点有人换班吗？"),
             "summary": T("Maya asked you directly.", "Maya 点名问你。"), "action": T("Reply tonight", "今晚回复"), "received": ago(2), "link": G},
            {"category": c["club"], "from": "Robotics Club", "subject": T("Build night + dues reminder", "社团活动 + 会费提醒"),
             "summary": T("Wednesday 6:30; dues $20.", "周三 18:30；会费 20 美元。"), "received": ago(20), "link": G},
            {"category": c["ppl"], "from": "Mom", "subject": T("Flight for break?", "放假机票订了吗？"),
             "summary": T("Asking which day you fly home.", "问你哪天回家。"), "action": T("Reply when you can", "有空回复"), "received": ago(6), "link": G},
            {"category": c["ntc"], "from": T("Campus Safety", "校园安全"), "subject": T("Elm Street closed Friday night", "周五晚 Elm 街封路"),
             "summary": T("No action.", "无需操作。"), "received": ago(11), "link": G},
            {"category": c["ntc"], "from": T("Dining Services", "餐饮中心"), "subject": T("Holiday dining hours", "假期食堂时间"),
             "summary": T("Only North Hall open next week.", "下周只开北区食堂。"), "received": ago(16), "link": G},
        ],
        "tracking": [
            {"type": T("Application", "申请"), "item": T("Study abroad · spring", "春季交换项目"), "detail": T("Essay + 1 recommendation", "文书 + 1 封推荐信"), "status": T("Essay missing", "缺文书"), "state": "waiting", "due": at(5, 17, 0), "link": G},
            {"type": T("Aid", "助学金"), "item": T("Spring financial aid", "春季助学金"), "detail": "", "status": T("On hold — form missing", "暂停：缺表"), "state": "late", "due": at(0, 17, 0), "link": G},
            {"type": T("Order", "订单"), "item": T("Used textbook", "二手教材"), "detail": "Stats 120", "status": T("Shipped", "已发货"), "state": "active", "link": G},
            {"type": T("Job", "工作"), "item": T("Summer RA position", "暑期研究助理"), "detail": T("Psych dept.", "心理系"), "status": T("Applied", "已投递"), "state": "active", "link": G},
        ],
        "pending_archive": [
            {"from": "Campus Store", "subject": T("Hoodies 30% off this week", "卫衣本周七折"), "link": G},
            {"from": "Athletics", "subject": T("Student tickets for Saturday", "周六比赛学生票"), "link": G},
            {"from": "Foodly", "subject": T("Free delivery this weekend", "本周末免配送费"), "link": G},
            {"from": "StreamBox", "subject": T("Student plan: 3 months free", "学生套餐免费 3 个月"), "link": G},
            {"from": "Greek Life", "subject": T("Winter formal tickets", "冬季舞会门票"), "link": G},
            {"from": "CloudNote", "subject": T("Upgrade to Pro", "升级 Pro"), "link": G},
            {"from": "SkyTrip", "subject": T("Holiday flight deals", "假期机票特价"), "link": G},
            {"from": "Campus Rec", "subject": T("New spin classes", "新开动感单车课"), "link": G},
        ],
        "auto_archived": {"today_total": 23, "by_source": [
            {"source": T("Social notifications", "社交通知"), "count": 9},
            {"source": T("Course-site digests", "课程平台推送"), "count": 6},
            {"source": T("Receipts", "订单收据"), "count": 4},
            {"source": T("Old login codes", "过期验证码"), "count": 3},
            {"source": T("Group-chat digests", "群聊摘要"), "count": 1},
        ]},
        "suspicious": [
            {"from": "payroll@campus-jobs-portal.example", "subject": T("Update your direct deposit now", "立即更新工资账户"),
             "reason": T("Not the real payroll sender; asks for bank login", "不是学校真正的发薪邮箱，要银行登录信息")},
        ],
        "calendar_added": [
            {"title": T("[Due] Spring registration", "[截止] 春季选课"), "when": at(2, 9, 0), "link": CAL},
            {"title": T("[Due] Study-abroad essay", "[截止] 交换项目文书"), "when": at(5, 17, 0), "link": CAL},
        ],
        "history": history([(5, 30), (7, 26), (4, 22), (3, 15), (6, 34), (8, 29), (5, 27), (6, 31), (9, 33), (4, 18), (2, 13), (7, 36), (8, 30), (6, 13)]),
    }


# --------------------------------------------------------------- master
def master():
    c = dict(rec=T("Recruiters", "招聘方"), iv=T("Interviews", "面试"), app=T("Applications", "投递进度"),
             cap=T("Capstone", "毕业项目"), crs=T("Courses", "课程"), prog=T("Program office", "项目办公室"),
             ppl=T("Personal", "真人来信"), ntc=T("Notices", "通知"))
    return {
        "category_order": [c["iv"], c["rec"], c["app"], c["cap"], c["crs"], c["prog"], c["ppl"], c["ntc"]],
        "stats": {"inbox_total": 352, "inbox_unread": 27, "new_today": 26, "todo_open": 7, "pending_archive": 6, "auto_archived_today": 31},
        "urgent": [
            {"title": T("Finish Kestrel AI coding assessment", "完成 Kestrel AI 在线笔试"), "detail": T("90 minutes, link expires tonight", "限时 90 分钟，链接今晚失效"),
             "category": c["iv"], "due": at(0, 23, 59), "link": G},
            {"title": T("Pick a slot: Brightline phone screen", "选 Brightline 电话面试时间"), "detail": T("Recruiter offered Wed 10:00 or Thu 14:00", "招聘方给了周三 10 点或周四 14 点"),
             "category": c["rec"], "due": at(0, 18, 0), "link": G},
            {"title": T("Send capstone dataset to Dr. Singh", "把毕业项目数据集发给 Singh 老师"), "detail": T("She wants it before Thursday's check-in", "周四例会前要"),
             "category": c["cap"], "due": at(1, 12, 0), "link": G},
        ],
        "todos": [
            {"title": T("Kestrel AI online assessment", "Kestrel AI 在线笔试"), "category": c["iv"], "due": at(0, 23, 59), "status": "open", "source": "Kestrel AI", "link": G},
            {"title": T("Reply to Brightline recruiter", "回复 Brightline 招聘方"), "category": c["rec"], "due": at(0, 18, 0), "status": "open", "source": "Priya Shah", "link": G},
            {"title": T("Share cleaned dataset", "发清洗好的数据集"), "category": c["cap"], "due": at(1, 12, 0), "status": "open", "source": "Dr. Amara Singh", "link": G},
            {"title": T("ML homework 6", "机器学习作业 6"), "category": c["crs"], "due": at(3, 23, 59), "status": "open", "source": "DS 541", "link": G},
            {"title": T("Update resume for career fair", "为招聘会更新简历"), "category": c["prog"], "due": at(4, 9, 0), "status": "open", "source": T("Career center", "就业中心"), "link": G},
            {"title": T("Thank-you note to Orbitly interviewer", "给 Orbitly 面试官写感谢信"), "category": c["iv"], "status": "open", "source": "Orbitly", "link": G},
            {"title": T("Internship CPT form", "实习 CPT 表"), "category": c["prog"], "due": at(-1, 17, 0), "status": "overdue", "source": T("Program office", "项目办公室"), "link": G},
            {"title": T("Book mock interview", "预约模拟面试"), "category": c["prog"], "status": "done", "source": T("Career center", "就业中心"), "link": G},
        ],
        "agenda": [
            {"start": at(0, 14, 0), "title": T("DS 541 Machine Learning", "机器学习课"), "type": "class", "link": CAL},
            {"start": at(0, 18, 0), "title": T("Reply to Brightline", "回复 Brightline"), "type": "deadline", "link": CAL},
            {"start": at(0, 23, 59), "title": T("Kestrel assessment", "Kestrel 笔试"), "type": "deadline", "link": CAL},
            {"start": at(1, 10, 0), "title": T("Brightline phone screen", "Brightline 电话面试"), "type": "meeting", "in_calendar": False, "link": G},
            {"start": at(1, 12, 0), "title": T("Dataset to Dr. Singh", "数据集给 Singh 老师"), "type": "deadline", "link": CAL},
            {"start": at(2, 15, 0), "title": T("Capstone check-in", "毕业项目例会"), "type": "meeting", "link": CAL},
            {"start": at(3, 23, 59), "title": T("ML homework 6", "机器学习作业 6"), "type": "deadline", "link": CAL},
            {"start": at(4, 10, 0), "title": T("Tech career fair", "科技招聘会"), "type": "meeting", "link": CAL},
            {"start": at(5, 13, 0), "title": T("Orbitly final round", "Orbitly 终面"), "type": "meeting", "link": CAL},
        ],
        "new_mail": [
            {"category": c["iv"], "from": "Kestrel AI", "subject": T("Your online assessment", "你的在线笔试"),
             "summary": T("2 coding + 1 SQL question, 90 min.", "2 道编程 + 1 道 SQL，90 分钟。"), "action": T("Finish by tonight", "今晚前完成"), "received": ago(15), "link": G},
            {"category": c["iv"], "from": "Orbitly", "subject": T("Final round — Monday 1 pm", "终面：周一下午 1 点"),
             "summary": T("Three 45-min interviews incl. a case.", "三轮 45 分钟，含一轮 case。"), "received": ago(4), "link": G},
            {"category": c["rec"], "from": "Priya Shah · Brightline", "subject": T("Data Science Intern — next step", "数据科学实习：下一步"),
             "summary": T("30-min phone screen, two slots offered.", "30 分钟电话面试，给了两个时间。"), "action": T("Pick a slot", "选时间"), "received": ago(3), "link": G},
            {"category": c["app"], "from": "Lumen Health", "subject": T("Application received", "已收到申请"),
             "summary": T("No action.", "无需操作。"), "received": ago(18), "link": G},
            {"category": c["app"], "from": "Vantage Retail", "subject": T("Update on your application", "申请结果更新"),
             "summary": T("Not moving forward this cycle.", "本轮未进入下一步。"), "received": ago(21), "link": G},
            {"category": c["cap"], "from": "Dr. Amara Singh", "subject": T("Dataset before Thursday?", "周四前能发数据集吗？"),
             "summary": T("Wants the cleaned version + a short data dictionary.", "要清洗后的版本和一份简短字段说明。"), "action": T("Send by Wed noon", "周三中午前发"), "received": ago(6), "link": G},
            {"category": c["crs"], "from": "DS 541", "subject": T("HW 6 released", "作业 6 已发布"),
             "summary": T("Due Friday; Kaggle-style leaderboard.", "周五截止，有排行榜。"), "received": ago(9), "link": G},
            {"category": c["prog"], "from": T("Career Center", "就业中心"), "subject": T("Tech fair: employer list", "科技招聘会企业名单"),
             "summary": T("62 employers; resume review drop-ins Thu.", "62 家企业；周四可现场改简历。"), "received": ago(12), "link": G},
            {"category": c["prog"], "from": T("Program office", "项目办公室"), "subject": T("CPT form overdue", "CPT 表已逾期"),
             "summary": T("Needed before any summer offer can start.", "暑期实习入职前必须交。"), "action": T("Submit this week", "本周提交"), "received": ago(7), "link": G},
            {"category": c["ppl"], "from": "Ken Liu", "subject": T("Referral at Brightline?", "Brightline 内推？"),
             "summary": T("Classmate offers to refer you.", "同学说可以帮你内推。"), "action": T("Send him your resume", "把简历发给他"), "received": ago(5), "link": G},
            {"category": c["ntc"], "from": T("IT Services", "IT 服务"), "subject": T("Wi-Fi maintenance Saturday", "周六 Wi-Fi 维护"),
             "summary": T("No action.", "无需操作。"), "received": ago(13), "link": G},
        ],
        "tracking": [
            {"type": T("Application", "求职"), "item": "Kestrel AI", "detail": T("ML Engineer Intern", "机器学习实习"), "status": T("Online assessment", "在线笔试"), "state": "late", "due": at(0, 23, 59), "link": G},
            {"type": T("Application", "求职"), "item": "Brightline", "detail": T("Data Science Intern", "数据科学实习"), "status": T("Phone screen", "电话面试"), "state": "waiting", "due": at(1, 10, 0), "link": G},
            {"type": T("Application", "求职"), "item": "Orbitly", "detail": T("Product Analyst Intern", "产品分析实习"), "status": T("Final round", "终面"), "state": "active", "due": at(5, 13, 0), "link": G},
            {"type": T("Application", "求职"), "item": "Lumen Health", "detail": T("Data Analyst Intern", "数据分析实习"), "status": T("Applied", "已投递"), "state": "active", "link": G},
            {"type": T("Application", "求职"), "item": "Vantage Retail", "detail": T("BI Intern", "BI 实习"), "status": T("Rejected", "未通过"), "state": "done", "link": G},
        ],
        "pending_archive": [
            {"from": "CodePrep Pro", "subject": T("50% off interview prep", "面试题库五折"), "link": G},
            {"from": "JobBoard Weekly", "subject": T("23 new roles for you", "为你推荐 23 个岗位"), "link": G},
            {"from": "Campus Store", "subject": T("Graduation gear pre-order", "毕业服预订"), "link": G},
            {"from": "DataCon 2027", "subject": T("Early-bird tickets", "早鸟票"), "link": G},
            {"from": "Foodly", "subject": T("Weekend promo", "周末优惠"), "link": G},
            {"from": "CloudNote", "subject": T("Student discount", "学生折扣"), "link": G},
        ],
        "auto_archived": {"today_total": 31, "by_source": [
            {"source": T("Job alerts", "职位推送"), "count": 12},
            {"source": T("Social notifications", "社交通知"), "count": 8},
            {"source": T("Application auto-replies", "投递自动回复"), "count": 5},
            {"source": T("Receipts", "订单收据"), "count": 3},
            {"source": T("Old login codes", "过期验证码"), "count": 3},
        ]},
        "suspicious": [
            {"from": "hr-team@brightline-careers.example", "subject": T("Offer letter — pay $85 for equipment", "录用通知：先付 85 美元设备费"),
             "reason": T("Fake recruiter domain asking for payment", "仿冒招聘域名，要求先付钱")},
        ],
        "calendar_added": [
            {"title": T("[Due] Kestrel assessment", "[截止] Kestrel 笔试"), "when": at(0, 23, 59), "link": CAL},
            {"title": T("[Due] ML homework 6", "[截止] 机器学习作业 6"), "when": at(3, 23, 59), "link": CAL},
        ],
        "history": history([(10, 34), (12, 31), (6, 20), (5, 17), (13, 38), (11, 33), (9, 30), (12, 36), (14, 32), (7, 19), (4, 15), (12, 40), (15, 34), (10, 16)]),
    }


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


PERSONAS = {"undergrad": undergrad, "master": master, "phd": phd}

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "docs/data"
    for name, fn in PERSONAS.items():
        body = fn()
        for lang in ("en", "zh"):
            data = {"schema_version": 2, "generated_at": BASE.isoformat(), "next_update": at(0, 9, 53),
                    "report_type": "morning", "persona": name, "labels": LABELS, **body}
            with open(f"{out}/demo.{name}.{lang}.json", "w", encoding="utf-8") as f:
                json.dump(loc(data, lang), f, ensure_ascii=False, indent=2)
    print("ok")
