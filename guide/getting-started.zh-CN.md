# InboxPilot 使用指南

[English](getting-started.md) · [返回 README](../README.zh-CN.md)

## 1. 开始之前

| 需要 | 用途 | 在哪里开 |
|---|---|---|
| Claude 账号 | 运行 agent | claude.ai 或 Claude App |
| **Gmail 连接器**（必需） | 读邮件、打标签、归档、把汇总发给你自己 | Claude → 设置 → Connectors → Gmail |
| **Google 日历连接器**（推荐） | 把截止日期写进日历并提醒 | Claude → 设置 → Connectors → Google Calendar |
| **定时任务**（推荐） | 每天自动发几次汇总 | 支持定时任务的账号可用 |

没有定时任务也能用：随时在 Claude 里说一句“运行 InboxPilot”。

## 2. 配置：一次对话搞定

新开一个对话，粘贴：

```text
帮我配置 InboxPilot：https://github.com/LiviaNiu620/InboxPilot
```

Claude 会读这个仓库里的说明，然后一次性问你大约 8 个问题。每个问题都有默认值，直接回“都用默认”也可以。
值得花心思的几个：

- **保护名单**：谁的邮件永远不能归档（导师、老板、家人、重要客户），写名字或邮箱都行。
- **汇总时间**：默认你所在时区的 8:00 / 13:00 / 17:00 / 20:00。
- **哪些直接归档**：社交通知、职位推送、旧收据、验证码……

接着 Claude 会**只读**扫描你最近 30 天的邮件，给你一张表：

| 发件人 | 建议分类 | 处理方式 |
|---|---|---|
| hr@yourcompany.example | 工作/事务 | C 保留 + 报告 |
| notifications@social.example | 通知 | A 直接归档 |
| deals@store.example | 广告 | B 等批准再归档 |

不对的直接说（“store.example 其实是房东的账单，要保留”）。然后 Claude 会：

1. 按[模板](../agent/rules.template.md)写好你的规则文件，给你过目。
2. 在 Gmail 里建好 `InboxPilot/` 开头的标签。
3. **可选**：一次性清理旧邮件——先给你看每类有多少封，你同意了才动。
4. 马上运行一次，你立刻收到第一封晨报。
5. 创建定时任务。

## 3. 日常怎么用

**看汇总。** 汇总发到你自己的邮箱，标题像 `[InboxPilot] 晨报 · … · N 件要处理`。
顺序是：今天必须处理 → 待办 → 分类新邮件 → 未来 7 天 → 等你批准 → 已归档 → 一行带过 → ⚠ 可疑邮件。
收件箱里只保留最新一封汇总。

**批准归档。** 营销邮件白天会打上 `InboxPilot/待归档` 标签留在收件箱。想留哪封，就在 Gmail 里去掉它的标签；
不动的，晚报时统一归档。

**划掉待办。** 去掉 `InboxPilot/待办` 标签，或者直接回复那封邮件，下次运行会标为完成。

**找回归档。** 在 Gmail 搜 `label:InboxPilot/已自动归档`，移回收件箱即可。

## 4. 改规则：直接说

在 Claude 里（连着 Gmail 的对话，最好就是当初配置的那个）：

- “以后 newsletter@site.example 的邮件都直接归档。”
- “招聘邮件单独一类，都算重要。”
- “取消下午 1 点那次，改成 3 点。”
- “把合伙人 dana@startup.example 加进保护名单。”
- “以后汇总用英文写。”

Claude 会同时更新规则文件和定时任务。

## 5. 可选：你自己的看板网页

[在线演示](https://livianiu620.github.io/InboxPilot/?lang=zh)用的是虚构数据。想要自己的，跟 Claude 说
“帮我配置 InboxPilot 看板”，它会带你：

1. 建一个**私有** GitHub 仓库，放 `docs/` 里的文件。
2. 用 Cloudflare Pages（免费）托管，再加 **Cloudflare Access**，只有你的邮箱能打开。
3. 给定时任务这个仓库的推送权限，每次运行自动更新 `data/dashboard.json`。

⚠ 不要把真实数据放到 GitHub Pages，那是公开网站。

## 6. 常见问题排查

| 现象 | 解决 |
|---|---|
| Claude 说“没有 Gmail 工具” | 去 设置 → Connectors 连接 Gmail，再新开对话 |
| 没收到汇总 | 看定时任务是否存在、运行是否卡在等待批准；账号允许的话，给这个任务开启自动批准 |
| 重要邮件被归档了 | 在 `label:InboxPilot/已自动归档` 找回，然后告诉 Claude“这类邮件永远不要归档” |
| 汇总太多 | “只要晨报和晚报。” |
| 看板一直是演示数据 | 还没有运行写入 `data/dashboard.json`，或者定时任务没有推送权限 |

## 7. 不想用了

在 Claude 里删掉定时任务即可。`InboxPilot/*` 标签可以在 Gmail 里删掉——邮件本身不会受影响
（归档的邮件一直在“所有邮件”里）。
