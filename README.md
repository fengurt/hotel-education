# 酒店教育课件生成系统 v1.0

## 架构总览

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Manus AI + TABLE AI 方法论                        │
│  研究分析 → 知识体系构建 → 叙事规划 → HTML 幻灯片生成               │
├─────────────────────────────────────────────────────────────────────┤
│                    设计系统 (3 套主题)                               │
│  Stripe 极简顶奢  ·  Linear 深色精准  ·  酒店教育专用               │
├─────────────────────────────────────────────────────────────────────┤
│                    核心生成器                                        │
│  slide_generator.py — 课程生成器 (支持 24/7 持续运行)                │
│  输出: ~/hotel-education/output/{theme}/{course}.html                │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 目录结构

```
~/hotel-education/
├── generator/
│   └── slide_generator.py     # 核心生成器
├── knowledge/
│   └── KNOWLEDGE_SYSTEM.md    # 酒店教育知识体系
├── output/
│   ├── hotel/                 # 酒店教育专用风格 (5门课)
│   ├── stripe/                # Stripe 极简顶奢风格 (5门课)
│   ├── linear/                 # Linear 深色精准风格 (5门课)
│   └── demo/                   # 演示课程
├── config.yaml                # 生成配置
└── README.md
```

---

## 已生成的课程

| 课程 | 主题 | 状态 |
|------|------|------|
| HE.01.01 前厅部运营管理 | hotel/stripe/linear | ✅ |
| HE.01.02 客房部运营管理 | hotel/stripe/linear | ✅ |
| HE.01.03 餐饮部运营管理 | hotel/stripe/linear | ✅ |
| HE.02.01 收益管理基础 | hotel/stripe/linear | ✅ |
| HE.04 酒店领导力与团队管理 | hotel/stripe/linear | ✅ |

共 **15 个 HTML 课件文件** + 1 个演示

---

## 使用方法

### 生成命令

```bash
# 生成演示课程
python3 generator/slide_generator.py demo

# 生成所有课程 (单次)
python3 generator/slide_generator.py once hotel     # 酒店风格
python3 generator/slide_generator.py once stripe   # Stripe 风格
python3 generator/slide_generator.py once linear   # Linear 风格

# 24/7 持续生成 (每小时)
python3 generator/slide_generator.py continuous 1

# 查看生成状态
python3 generator/slide_generator.py list
```

### 预览课件

直接用浏览器打开 HTML 文件即可:
```bash
open ~/hotel-education/output/hotel/front-office.html
open ~/hotel-education/output/stripe/revenue.html
open ~/hotel-education/output/linear/leadership.html
```

---

## 设计系统

### 酒店教育专用 (hotel)
- 主色: 深森林绿 `#1B4D3E`
- 强调色: 香槟金 `#C9A962`
- 背景: 米白 `#F5F1E8`
- 字体: Playfair Display (标题) + Noto Sans SC (正文)
- 风格: 温暖、专业、学院感

### Stripe 极简顶奢 (stripe)
- 主色: 深海军蓝 `#061b31`
- 强调色: 紫 `#533afd`
- 背景: 纯白 `#ffffff`
- 字体: Source Sans 3
- 风格: 克制、精致、金融级

### Linear 深色精准 (linear)
- 主色: 近黑 `#08090a`
- 强调色: 靛蓝紫 `#7170ff`
- 背景: 多层次深色
- 字体: Inter
- 风格: 精准、工程感、现代

---

## 核心方法论

### Manus AI 的端到端流程
1. **研究** — 分析酒店教育领域知识结构
2. **结构化** — 构建课程模块化学体系
3. **生成** — AI 生成幻灯片内容
4. **组装** — 输出完整可演示的 HTML

### TABLE AI BP 的高品质标准
- 深度分析: 知识体系理论背书
- 叙事规划: 课程逻辑闭环
- HTML 规范: min-height:720px、克制排版、金色点缀

### Stripe 设计系统的关键规则
- 字重 300 为标题标准 (轻盈=自信)
- 蓝色调阴影 `rgba(50,50,93,0.25)` — 品牌化深度
- 4px-8px 保守圆角 — 克制优雅

### Linear 设计系统的关键规则
- 510 字重作为签名重量
- 半透明边框 `rgba(255,255,255,0.08)` — 夜色中的结构
- 深色画布原生感

---

## 扩展课程体系

编辑 `generator/slide_generator.py` 中的 `COURSE_TEMPLATES` 字典，添加新课程:

```python
"new-course": {
    "title": "新课程名称",
    "level": "intermediate",
    "course_id": "HE.XX.XX",
    "modules": [
        {
            "module_id": "MOD-001",
            "title": "模块标题",
            "duration_minutes": 45,
            "lesson_type": "theory",
            "objectives": ["目标1", "目标2"],
            "slides": [
                {
                    "title": "幻灯片标题",
                    "body": "描述文字",
                    "content_type": "list",  # title, section, list, process, highlight, comparison
                    "items": ["要点1", "要点2", "要点3"]
                }
            ]
        }
    ]
}
```

然后运行:
```bash
python3 generator/slide_generator.py once hotel
```

---

## 持续生成模式

要实现 24/7 不间断生成课件:

```bash
# 后台运行
nohup python3 generator/slide_generator.py continuous 4 > generator.log 2>&1 &

# 查看日志
tail -f ~/hotel-education/generator.log

# 停止
pkill -f "slide_generator.py continuous"
```

---

## 与 bb-browser 监控系统的结合

本课件生成系统可与 `~/social-monitor/` 中的社交媒体监控结合:

```python
# monitor.py 中添加
def on_new_content(platform, account, content):
    # 当监控到行业新闻时，自动生成相关课件
    if is_hospitality_news(content):
        course_key = generate_course_from_news(content)
        regenerate_course(course_key)
        send_telegram(f"📚 新课件已生成: {course_key}")
```

---

## 知识体系 (HE 标准)

```
HE.01 酒店运营管理
├── HE.01.01 前厅部 ✅ 已生成
├── HE.01.02 客房部 ✅ 已生成
├── HE.01.03 餐饮部 ✅ 已生成
├── HE.01.04 宴会与会议
├── HE.01.05 健身与休闲

HE.02 酒店市场营销
├── HE.02.01 收益管理 ✅ 已生成
├── HE.02.02 数字营销
├── HE.02.03 品牌管理
├── HE.02.04 客户关系管理

HE.03 酒店财务管理
├── HE.03.01 成本控制
├── HE.03.02 预算管理
├── HE.03.03 财务分析

HE.04 人力资源 ✅ 已生成
HE.05 工程与安全
HE.06 战略管理
```

---

## 下一步

1. 添加更多课程模板到 `COURSE_TEMPLATES`
2. 实现 AI 生成内容增强 (接入 LLM API)
3. 添加字幕/音频同步导出
4. 实现交互式测验功能
5. 搭建 Web 预览界面
