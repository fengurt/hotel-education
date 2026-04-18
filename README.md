# 酒店教育课件生成系统 v2.0
## GHE Aligned — Global Hospitality Education

## 架构总览

```
┌─────────────────────────────────────────────────────────────────────┐
│                 GHE 知识体系 (Cornell + EHL + HK PolyU)             │
│  Cornell 运营卓越  ·  EHL 奢华服务  ·  HK PolyU 亚洲市场           │
├─────────────────────────────────────────────────────────────────────┤
│                    设计系统 (3 套主题)                               │
│  Stripe 极简顶奢  ·  Linear 深色精准  ·  酒店教育专用               │
├─────────────────────────────────────────────────────────────────────┤
│                    核心生成器                                        │
│  slide_generator.py — 课程生成器 (支持 24/7 持续运行)                │
│  输出: ~/hotel-education/output/{theme}/{course}.html                │
│  自动 Push: 生成完成即推送到 GitHub                                   │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 目录结构

```
~/hotel-education/
├── generator/
│   └── slide_generator.py     # 核心生成器 + GitHub Auto-Push
├── knowledge/
│   ├── GHE_SYSTEM.md          # GHE 全球酒店教育知识体系 (134门课)
│   └── KNOWLEDGE_SYSTEM.md    # 知识体系总览
├── guidelines/
│   ├── POLICY.md              # 系统政策 (GHE v2.0)
│   ├── ARCHITECTURE.md        # 架构蓝图
│   └── DESIGN_SYSTEM.md       # 三主题设计系统
├── skills/
│   └── hotel-course-developer/
│       └── SKILL.md           # Subagent 开发指南
├── output/
│   ├── hotel/                 # 酒店教育专用风格
│   ├── stripe/                # Stripe 极简顶奢风格
│   ├── linear/                # Linear 深色精准风格
│   └── demo/                  # 演示课程
└── README.md
```

---

## 已生成的课程

| 课程 ID | 课程名称 | 主题 | 状态 |
|---------|---------|------|------|
| GHE.1.1.01 | 前厅部组织架构 | hotel/stripe/linear | ✅ |
| GHE.1.1.02 | 标准入住流程 | hotel/stripe/linear | ✅ |
| GHE.1.1.04 | VIP接待标准 | hotel/stripe/linear | ✅ |
| GHE.1.2.01 | 客房清洁SOP | hotel/stripe/linear | ✅ |
| GHE.1.3.01 | 餐饮部架构 | hotel/stripe/linear | ✅ |
| GHE.1.3.06 | 食品安全HACCP | hotel | ✅ |
| GHE.1.4 | 宴会与会议管理 | hotel | ✅ |
| GHE.2.1.01 | 收益管理理论 | stripe | ✅ |
| GHE.2.1.05 | 品牌建设定位 | stripe | ✅ |
| GHE.2.1.06 | 数字营销策略 | stripe | ✅ |
| GHE.2.1.07 | 收益管理基础 | stripe | ✅ |
| GHE.3.1.01 | 财务报表分析 | linear | ✅ |
| GHE.3.1.01 | 成本控制 | linear | ✅ |
| GHE.4 | 领导力与团队管理 | hotel/stripe/linear | ✅ |

共 **23 个 HTML 课件文件** (3套主题)

---

## GitHub 仓库

| 仓库 | 内容 |
|------|------|
| [hotel-education](https://github.com/fengurt/hotel-education) | 代码系统、政策、知识体系、Subagent 技能 |
| [hotel-education-courses](https://github.com/fengurt/hotel-education-courses) | 所有生成的 HTML 课件 |

---

## 使用方法

### 生成命令

```bash
# 生成所有课程 (单次) + 自动推送到 GitHub
python3 generator/slide_generator.py once hotel     # 酒店风格
python3 generator/slide_generator.py once stripe   # Stripe 风格
python3 generator/slide_generator.py once linear    # Linear 风格

# 24/7 持续生成 (每小时)
python3 generator/slide_generator.py continuous 1

# 查看生成状态
python3 generator/slide_generator.py list

# 手动 Push 到 GitHub
python3 generator/slide_generator.py push
```

### 预览课件

直接用浏览器打开 HTML 文件即可:
```bash
open ~/hotel-education/output/hotel/vip-reception.html
open ~/hotel-education/output/stripe/brand-building.html
open ~/hotel-education/output/linear/financial-statements.html
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

## GHE 知识体系

GHE (Global Hospitality Education) 对标全球三大酒店管理教育标杆:

- **Cornell (美国康奈尔)** — 运营卓越、数据驱动、市场化思维
- **EHL (瑞士洛桑)** — 奢华服务、欧洲标准、酒店业西点军校
- **HK PolyU (香港理工)** — 亚洲市场、中国特色、产教融合

```
GHE.1 酒店运营管理
├── GHE.1.1 前厅与入住 ✅
├── GHE.1.2 客房管理 ✅
├── GHE.1.3 餐饮管理 ✅
├── GHE.1.4 宴会与会议 ✅
├── GHE.1.5 健身与休闲
└── GHE.1.6 礼宾与管家

GHE.2 市场营销与收益管理
├── GHE.2.1 收益管理 ✅
├── GHE.2.2 数字营销 ✅
├── GHE.2.3 品牌管理 ✅
└── GHE.2.4 客户关系管理

GHE.3 财务与投资管理
├── GHE.3.1 成本控制 ✅
├── GHE.3.2 预算管理
└── GHE.3.3 财务报表分析 ✅

GHE.4 人力资源管理 ✅
GHE.5 工程与安全管理
GHE.6 战略管理与创新
```

---

## 扩展课程体系

编辑 `generator/slide_generator.py` 中的 `COURSE_TEMPLATES` 字典，添加新课程:

```python
"new-course": {
    "title": "新课程名称",
    "level": "intermediate",
    "course_id": "GHE.X.X.XX",
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

## 下一步

1. 添加更多课程模板到 `COURSE_TEMPLATES`
2. 实现 AI 生成内容增强 (接入 LLM API)
3. 添加字幕/音频同步导出
4. 实现交互式测验功能
5. 搭建 Web 预览界面
