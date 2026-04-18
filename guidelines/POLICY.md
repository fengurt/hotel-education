# 酒店教育课件开发系统政策与指南
# Hotel Education Course Development — System Policy & Guidelines
# Version 1.0 — 2026-04-18

---

## 一、系统愿景

**目标**: 建立一个可持续、可扩展的酒店教育课件工业化生产体系。

**核心原则**:
1. **独立性** — 每门课程可独立开发、测试、发布，互不阻塞
2. **一致性** — 所有课程遵循统一的设计系统与方法论
3. **可量化** — 课件数量、学习目标、知识点可追踪审计
4. **工业化** — 支持 24/7 自动化持续生成，而非人工手动制作

---

## 二、组织架构

```
social-monitor/                        # 社交媒体/官网监控系统
├── monitors/                          #   各平台监控器 (monitor_*.py)
├── scripts/                           #   数据采集脚本
└── output/                            #   原始内容输出

hotel-education/                      # 酒店教育课件生成系统
├── generator/                         #   核心生成器 (slide_generator.py)
├── knowledge/                         #   知识体系定义 (KNOWLEDGE_SYSTEM.md)
├── guidelines/                        #   系统政策与开发指南
│   ├── POLICY.md                      #   ⭐ 本文件 — 系统政策
│   ├── ARCHITECTURE.md                #   系统架构蓝图
│   └── DESIGN_SYSTEM.md               #   设计系统规范 (3套主题)
├── skills/                             #   技能定义 (可被 subagent 加载)
│   └── hotel-course-developer/        #   ⭐ 课程开发者技能
├── output/                            #   生成的 HTML 课件
│   ├── hotel/
│   ├── stripe/
│   └── linear/
└── README.md
```

---

## 二、知识体系 (GHE Global Hospitality Education 标准)

**版本**: v2.0 — 融合康奈尔 + 洛桑 EHL + 香港理工 HK PolyU 三大标杆

### GHE.0 预备知识 (Foundations) — P0 核心基础

| ID | 课程名称 | 对应标杆 | 优先级 |
|----|---------|---------|--------|
| GHE.01 | 酒店业历史与演变 | Cornell | P0 |
| GHE.02 | 酒店业利益相关方与生态系统 | EHL | P0 |
| GHE.03 | 酒店运营核心概念 | Cornell + EHL | P0 |
| GHE.04 | 酒店职业发展路径与行业准入 | HK PolyU | P0 |
| GHE.05 | 酒店专业英语 | 所有院校 | P0 |

### GHE.1 运营管理 (Operations Management) — 最优先开发

#### GHE.1.1 前厅与入住 (Front Office & Check-in)

| ID | 课程名称 | 优先级 |
|----|---------|--------|
| GHE.1.1.01 | 前厅部组织架构与岗位职责 | P0 |
| GHE.1.1.02 | 标准入住流程 (Check-in SOP) | P0 |
| GHE.1.1.03 | 退房流程 (Check-out) 与结账管理 | P0 |
| GHE.1.1.04 | VIP & 会员客人接待标准 | P0 |
| GHE.1.1.05 | 投诉处理与危机管理 | P0 |
| GHE.1.1.06 | 酒店管理系统 (PMS) 操作 | P0 |
| GHE.1.1.07 | 礼宾服务与金钥匙标准 | P0 |
| GHE.1.1.08 | 团队入住 (Group Check-in) 处理 | P1 |
| GHE.1.1.09 | 超额预订 (Overbooking) 管理 | P1 |
| GHE.1.1.10 | 外币兑换与金融服务 | P1 |
| GHE.1.1.11 | 酒店安全管理与治安管理 | P0 |
| GHE.1.1.12 | 无障碍服务与特殊需求客人 | P1 |

#### GHE.1.2 客房管理 (Housekeeping)

| ID | 课程名称 | 优先级 |
|----|---------|--------|
| GHE.1.2.01 | 客房清洁标准操作流程 (SOP) | P0 |
| GHE.1.2.02 | 退房清洁 vs 在住清洁区分 | P0 |
| GHE.1.2.03 | 布草生命周期管理 | P0 |
| GHE.1.2.04 | 客房耗用品与库存管理 | P0 |
| GHE.1.2.05 | 楼层管理与质量检查体系 | P0 |
| GHE.1.2.06 | 特殊房型清洁 | P1 |
| GHE.1.2.07 | 预防性维护与客房工程协同 | P1 |
| GHE.1.2.08 | 绿色酒店与可持续发展清洁标准 | P1 |

#### GHE.1.3 餐饮管理 (F&B Management)

| ID | 课程名称 | 优先级 |
|----|---------|--------|
| GHE.1.3.01 | 餐饮部组织架构与厨房布局 | P0 |
| GHE.1.3.02 | 餐桌服务标准流程 (西餐零点) | P0 |
| GHE.1.3.03 | 中餐服务标准与宴会服务 | P0 |
| GHE.1.3.04 | 客房送餐服务 (Room Service) | P0 |
| GHE.1.3.05 | 酒吧与酒水管理 | P0 |
| GHE.1.3.06 | 食品安全与卫生标准 (HACCP) | P0 |
| GHE.1.3.07 | 菜单工程与定价策略 | P0 |
| GHE.1.3.08 | 餐饮成本控制与毛利率管理 | P0 |
| GHE.1.3.09 | 厨房团队管理 (Kitchen Brigade) | P1 |
| GHE.1.3.10 | 特殊餐饮概念 (自助餐/主题晚宴) | P1 |
| GHE.1.3.11 | 葡萄酒与烈酒知识 | P1 |
| GHE.1.3.12 | 餐饮科技与预订系统 | P1 |

#### GHE.1.4 宴会与会议管理 (Banquet & Conference)

| ID | 课程名称 | 优先级 |
|----|---------|--------|
| GHE.1.4.01 | MICE 市场概述 | P0 |
| GHE.1.4.02 | 宴会预订流程与合同管理 | P0 |
| GHE.1.4.03 | 宴会摆台与空间布置标准 | P0 |
| GHE.1.4.04 | 宴会服务流程与上菜时机 | P0 |
| GHE.1.4.05 | 会议技术设备管理 | P0 |
| GHE.1.4.06 | 茶歇与鸡尾酒会管理 | P1 |
| GHE.1.4.07 | 大型宴会风险评估与应急预案 | P1 |
| GHE.1.4.09 | 婚礼统筹与管理 | P1 |

#### GHE.1.5 健康与休闲 (Spa, Fitness & Recreation)

| ID | 课程名称 | 优先级 |
|----|---------|--------|
| GHE.1.5.01 | 水疗中心运营标准 | P1 |
| GHE.1.5.02 | 健身中心管理 | P2 |
| GHE.1.5.03 | 儿童俱乐部与家庭服务 | P2 |
| GHE.1.5.04 | 高尔夫/网球/水上运动管理 | P2 |

### GHE.2 市场营销与收益管理 (Marketing & Revenue Management)

| ID | 课程名称 | 优先级 |
|----|---------|--------|
| GHE.2.1.01 | 收益管理理论框架 | P0 |
| GHE.2.1.02 | 动态定价策略与价格优化 | P0 |
| GHE.2.1.03 | 需求预测与数据分析 | P0 |
| GHE.2.1.04 | 分销渠道管理 | P0 |
| GHE.2.1.05 | 酒店品牌建设与定位 | P0 |
| GHE.2.1.06 | 数字营销与社交媒体战略 | P0 |
| GHE.2.1.07 | 客户关系管理 (CRM) 与会员计划 | P0 |
| GHE.2.1.08 | 酒店官网设计与直销优化 | P1 |
| GHE.2.1.09 | 公关与媒体关系 | P1 |
| GHE.2.1.10 | 活动营销与节日策划 | P1 |
| GHE.2.1.12 | 口碑营销与点评管理 | P1 |
| GHE.2.1.13 | 搜索引擎优化与内容营销 | P1 |

### GHE.3 财务与投资管理 (Finance & Investment)

| ID | 课程名称 | 优先级 |
|----|---------|--------|
| GHE.3.1.01 | 酒店财务报表分析 | P0 |
| GHE.3.1.02 | 酒店成本结构分析 | P0 |
| GHE.3.1.03 | 食品成本控制 | P0 |
| GHE.3.1.04 | 人工成本管理 | P0 |
| GHE.3.1.05 | 预算编制与预测 | P0 |
| GHE.3.1.06 | 酒店资产估值方法 | P0 |
| GHE.3.1.07 | 酒店投资可行性分析 | P1 |
| GHE.3.1.08 | 酒店并购与交易管理 | P1 |
| GHE.3.1.11 | 采购与供应链管理 | P1 |

### GHE.4 人力资源管理 (Human Resources)

| ID | 课程名称 | 优先级 |
|----|---------|--------|
| GHE.4.1.01 | 酒店组织行为学 | P0 |
| GHE.4.1.02 | 招聘、选拔与入职管理 | P0 |
| GHE.4.1.03 | 培训体系构建与能力模型 | P0 |
| GHE.4.1.04 | 绩效管理与评估系统 | P0 |
| GHE.4.1.05 | 薪酬福利设计与激励体系 | P0 |
| GHE.4.1.06 | 员工关系与劳动法合规 | P0 |
| GHE.4.1.07 | 教练式领导力 | P0 |
| GHE.4.1.08 | 服务文化打造 | P0 |
| GHE.4.1.09 | 跨文化管理与国际团队 | P0 |
| GHE.4.1.12 | 员工敬业度与留任策略 | P1 |

### GHE.5 战略管理与领导力 (Strategy & Leadership)

| ID | 课程名称 | 优先级 |
|----|---------|--------|
| GHE.5.1.01 | 酒店战略规划框架 | P0 |
| GHE.5.1.02 | 酒店商业模式画布 | P0 |
| GHE.5.1.03 | 竞争战略 (Porter's Five Forces) | P0 |
| GHE.5.1.10 | 可持续发展与 ESG 战略 | P0 |
| GHE.5.1.11 | 数字化转型与酒店科技 | P0 |
| GHE.5.1.04 | 品牌组合战略 | P1 |
| GHE.5.1.05 | 特许经营与管理合同 | P1 |
| GHE.5.1.06 | 酒店开发与新项目筹建 | P1 |
| GHE.5.1.07 | 酒店资产管理 | P1 |
| GHE.5.1.09 | 创业与商业计划书撰写 | P1 |

### GHE.6 奢华业态管理 (Luxury & Segment-Specific)

| ID | 课程名称 | 优先级 |
|----|---------|--------|
| GHE.6.1.01 | 奢华酒店运营标准 | P0 |
| GHE.6.1.02 | 精品酒店管理 | P1 |
| GHE.6.1.03 | 全包式度假村 | P1 |
| GHE.6.1.04 | 博彩酒店与娱乐场管理 | P2 |
| GHE.6.1.05 | 经济型酒店与有限服务酒店 | P1 |
| GHE.6.1.06 | 民宿与短租管理 | P1 |

### GHE.7 旅游与目的地管理 (Tourism & Destination)

| ID | 课程名称 | 优先级 |
|----|---------|--------|
| GHE.7.1.01 | 旅游经济学基础 | P0 |
| GHE.7.1.05 | 会展旅游管理 | P1 |
| GHE.7.1.07 | 可持续旅游 | P1 |

**状态图**: ✅ 已生成 → 🔄 开发中 → 🔲 待开发

**优先级**: P0 = 核心必修 / P1 = 管理进阶 / P2 = 战略专项

**总课程规模**: ~134 门课程，~5650 页幻灯片内容

---

## 四、课程开发标准

### 4.1 单门课程结构规范

每门课程必须包含以下组件：

```
courses/
└── {course_id}/                       # 例如: courses/HE.01.04/
    ├── course.yaml                    # ⭐ 课程元数据 (必须)
    ├── modules/                       #   模块目录
    │   ├── MOD-001/                  #   模块1
    │   │   ├── module.yaml           #   模块定义
    │   │   └── slides/               #   幻灯片内容 (Markdown)
    │   └── MOD-002/
    │       └── ...
    ├── cases/                         #   案例研究
    ├── templates/                     #   可复用模板
    └── resources/                     #   阅读材料/参考资料
```

### 4.2 course.yaml 元数据规范

```yaml
course_id: HE.01.04
title: 宴会与会议管理
title_en: Banquet & Conference Management
level: intermediate                    # beginner | intermediate | advanced
version: 1.0.0
language: zh-CN
estimated_hours: 4
prerequisites:
  - HE.01.01                          # 前厅部基础 (建议)
target_audience:
  - 酒店运营管理人员
  - 宴会销售专员
  - 会议统筹协调员
learning_outcomes:
  - "掌握宴会预订到执行的全流程管理"
  - "能够独立策划并执行中小型会议活动"
  - "理解宴会收益管理与成本控制要点"
modules:
  - module_id: MOD-001
    title: 宴会运营概述
    duration_minutes: 60
  - module_id: MOD-001
    title: 宴会预订与合同管理
    duration_minutes: 75

design_theme: hotel                    # hotel | stripe | linear
generated_html:
  hotel: output/hotel/banquet.html
  stripe: output/stripe/banquet.html
  linear: output/linear/banquet.html
status: generated
generated_at: "2026-04-18"
```

### 4.3 幻灯片内容类型

| 类型 | 用途 | 关键字段 |
|------|------|---------|
| `title` | 封面/章节封面 | `title`, `subtitle` |
| `section` | 章节分隔页 | `title` |
| `list` | 要点列表 | `title`, `body`, `items[]` |
| `process` | 流程步骤 | `title`, `body`, `items[]` |
| `highlight` | 重点强调 | `title`, `body`, `items[]` |
| `comparison` | 对比分析 | `title`, `items[{title, content}]` |
| `quote` | 名言/引用 | `title`, `body` |
| `stats` | 数据统计 | `title`, `data.stats[]` |

---

## 五、设计系统政策

### 5.1 三套主题规范

所有课程必须生成 **全部三套主题** 的 HTML:
- `hotel` (酒店教育专用)
- `stripe` (Stripe 极简顶奢)
- `linear` (Linear 深色精准)

每套主题有独立的 CSS 设计系统，不得混用。

### 5.2 排版规范

| 元素 | 规范 |
|------|------|
| 幻灯片高度 | min-height: 720px |
| 内边距 | 80px 垂直, 100px 水平 |
| 标题字号 | 42-56px |
| 正文字号 | 16-18px |
| 行高 | 1.7-1.9 |
| 边框 | 1px solid，使用半透明或极浅色 |

### 5.3 酒店主题色彩

```
--bg:        #F5F1E8   (米白背景)
--heading:   #0A1628   (深蓝黑标题)
--body:      #4a5568    (中性灰正文)
--accent:    #1B4D3E   (酒店绿)
--gold:      #C9A962   (香槟金强调)
--border:    rgba(27,77,62,0.15)
```

### 5.4 字体政策

```
标题字体 (Title):  Playfair Display (衬线, 学院感)
正文字体 (Body):   Noto Sans SC / Inter
等宽字体 (Code):   JetBrains Mono / Source Code Pro
字重规范:
  - 轻 (Light 300): 标题主色, 表达轻盈自信
  - 中 (Normal 400): 正文标准
  - 准粗 (Medium 500): 模块标题
  - 签名 (Signature 510/600): Linear 签名重量
```

---

## 六、独立开发政策 (Subagent 模式)

### 6.1 为什么需要独立 Subagent 开发

- **避免上下文膨胀**: 15+ 门课程的完整内容塞入一个对话窗口会导致性能下降
- **真正并行**: 每门课程在独立的 agent process 中运行，CPU/GPU 资源不受限
- **隔离性**: 一门课程开发失败不影响其他课程
- **可追溯**: 每个 subagent 的工作独立记录，不污染主会话

### 6.2 Subagent 开发协议

当主 agent 调用 `delegate_task` 开发独立课程时，**subagent 必须遵循**:

```
1. 加载技能: skill_view("hotel-course-developer")
2. 读取知识体系: courses/{course_id}/course.yaml
3. 如课程目录不存在:
   a. 创建 courses/{course_id}/ 目录结构
   b. 编写 course.yaml 元数据
   c. 编写各模块 module.yaml
   d. 编写各幻灯片 Markdown 内容
4. 调用 slide_generator.py 生成 HTML:
   subprocess.run(["python3", "generator/slide_generator.py", "once", theme])
5. 验证输出文件存在且非空
6. 返回完成报告
```

### 6.3 Subagent 输入格式

```python
delegate_task(
    goal="开发课程 HE.01.04 宴会与会议管理",
    context="""
    知识体系: HE.01 酒店运营管理
    课程编号: HE.01.04
    目标学员: 宴会运营管理人员
    核心模块:
      1. 宴会运营概述 (60分钟)
      2. 宴会预订与合同管理 (75分钟)
      3. 宴会执行与服务标准 (90分钟)
      4. 会议管理专题 (60分钟)
    设计主题: hotel
    输出目录: ~/hotel-education/output/hotel/banquet.html
    参考已有课程: ~/hotel-education/output/hotel/front-office.html
    """,
    toolsets=["terminal", "file"],
)
```

### 6.4 Subagent 输出格式

每个 subagent 完成时必须报告:
```
✅ 课程 HE.01.04 开发完成
📁 输出文件:
   - ~/hotel-education/output/hotel/banquet.html (hotel主题)
   - ~/hotel-education/output/stripe/banquet.html (stripe主题)
   - ~/hotel-education/output/linear/banquet.html (linear主题)
📊 课程统计:
   - 模块数: 4
   - 幻灯片数: 24
   - 总时长: 约 4.75 小时
🔍 质量检查:
   - HTML 语法: ✅ 通过
   - 资源加载: ✅ Google Fonts 可访问
   - 排版合规: ✅ 三主题全部符合规范
```

---

## 七、持续生成运营政策

### 7.1 状态追踪

所有课程的状态存储在 `generation_state.json`:
```json
{
  "generated": ["front-office", "housekeeping", "fnb", "revenue", "leadership"],
  "pending": ["banquet", "revenue-digital", "crm", "cost-control"],
  "failed": [],
  "last_run": "2026-04-18T23:37:00Z"
}
```

### 7.2 生成频率

| 场景 | 频率 | 说明 |
|------|------|------|
| 持续监控模式 | 每 1-4 小时 | 自动检测新课程并生成 |
| 批量生成 | 每日一次 | 合并多个课程的生成任务 |
| 单课程增量 | 按需 | 新增/修订课程时触发 |

### 7.3 失败处理策略

```
失败检测 → 等待 5 分钟 → 重试 1 次 → 若仍失败:
  → 记录到 failed 列表
  → 发送通知 (Telegram)
  → 跳过，继续处理其他课程
  → 主 agent 下次会话时分析失败原因
```

---

## 八、监控系统集成政策

### 8.1 数据流向

```
社交媒体/官网监控 (social-monitor/)
    ↓ 检测到新内容 (行业趋势/案例/法规变化)
    ↓
触发条件判断:
    IF 内容类型 == 酒店教育相关:
        → 生成课程更新任务
        → delegate_task(独立开发新课程/更新现有课程)
    ELSE:
        → 仅记录存档
```

### 8.2 内容相关性判断

触发课程生成的内容类型:
- 新酒店管理理念/方法论
- 行业法规/标准更新 (如新版酒店星级评定标准)
- 头部酒店集团战略动向
- 数字化转型案例 ( Marriott / Hilton / Accor )
- 收益管理实战案例
- 餐饮创新模式
- 酒店可持续发展实践

不触发课程生成的内容类型:
- 娱乐新闻/明星八卦
- 与酒店业无关的宏观经济
- 纯营销推广内容

---

## 九、质量保证政策

### 9.1 最低质量标准

每门课程必须通过以下检查:

```
✅ HTML 有效性: 无语法错误，可被浏览器解析
✅ 设计系统合规: 三套主题色彩/字体/间距符合规范
✅ 学习目标对齐: 每个模块有明确 objectives，与 course.yaml 一致
✅ 内容深度: 每个要点至少 2-3 句展开，而非单行列出
✅ 模块时长合理: 单模块 30-90 分钟，偏离此区间需说明
✅ 知识体系映射: 课程编号正确归属 HE.0X.XX 分类
```

### 9.2 禁止行为

```
❌ 不得生成无实质内容的"填充课程"
❌ 不得将同义反复的废话作为正文 (如"酒店管理很重要")
❌ 不得跳过 course.yaml 元数据直接生成 HTML
❌ 不得将幻灯片内容硬编码在 slide_generator.py 中 (须从 COURSE_TEMPLATES 模板读取)
❌ 不得在 hotel 主题中使用 linear 的深色配色
```

---

## 十、扩展与维护政策

### 10.1 添加新课程

1. 在 `KNOWLEDGE_SYSTEM.md` 中注册 HE 编号
2. 在 `COURSE_TEMPLATES` (slide_generator.py) 中添加课程模板
3. 运行 `python3 generator/slide_generator.py once hotel`
4. 更新 `generation_state.json`

### 10.2 修订现有课程

1. 修改对应课程的 module.yaml / slides Markdown
2. 重新运行生成器
3. 对比新旧 HTML diff，确保变更正确

### 10.3 设计系统迭代

若需要修改设计系统 (新增主题/调整色彩):
1. 修改 `slide_generator.py` 中对应 Renderer 类的 CSS
2. 运行 `python3 generator/slide_generator.py once {theme}` 验证
3. 更新 `DESIGN_SYSTEM.md`

---

## 十一、角色与职责

| 角色 | 职责 | 执行者 |
|------|------|--------|
| **系统管理员** | 维护生成器、监控系统、状态文件 | 主 Agent |
| **课程开发者 (Subagent)** | 独立开发指定课程，负责内容与生成 | Subagent |
| **质量审计员** | 审查生成课程是否符合政策标准 | 主 Agent (最终审查) |
| **知识管理员** | 维护 KNOWLEDGE_SYSTEM.md，更新 HE 编号 | 主 Agent |

---

## 十二、关键文件索引

| 文件 | 用途 | 维护者 |
|------|------|--------|
| `generator/slide_generator.py` | 核心生成器 | 系统管理员 |
| `knowledge/KNOWLEDGE_SYSTEM.md` | 知识体系定义 | 知识管理员 |
| `generator/COURSE_TEMPLATES` | 课程内容模板 | 课程开发者 |
| `generation_state.json` | 状态追踪 | 系统管理员 |
| `skills/hotel-course-developer/SKILL.md` | Subagent 开发指南 | 系统管理员 |
| `guidelines/POLICY.md` | ⭐ 本文件 | 系统管理员 |
| `guidelines/DESIGN_SYSTEM.md` | 设计系统规范 | 设计管理员 |
