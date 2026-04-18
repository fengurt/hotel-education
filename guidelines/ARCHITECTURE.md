# 系统架构蓝图
# Hotel Education System — Architecture Blueprint
# Version 1.0 — 2026-04-18

---

## 一、整体架构

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          主 Agent (Hermes CLI)                          │
│                    负责任务调度、知识管理、质量审计                       │
└──────────────────────────────────────┬──────────────────────────────────┘
                                       │ delegate_task
                    ┌──────────────────┼──────────────────┐
                    ▼                  ▼                  ▼
          ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
          │ Subagent A   │   │ Subagent B   │   │ Subagent C   │
          │ HE.01.04     │   │ HE.02.02     │   │ HE.03.01     │
          │ 宴会会议     │   │ 数字营销     │   │ 成本控制     │
          └──────┬───────┘   └──────┬───────┘   └──────┬───────┘
                 │                  │                  │
                 └──────────────────┼──────────────────┘
                                      │
                              ┌───────▼───────┐
                              │  slide_gen   │
                              │  (共享生成器) │
                              └───────┬───────┘
                                      │
                    ┌─────────────────┼─────────────────┐
                    ▼                 ▼                 ▼
           ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
           │ output/hotel │  │output/stripe │  │output/linear │
           └──────────────┘  └──────────────┘  └──────────────┘
```

---

## 二、模块职责

### 2.1 主 Agent

- 维护 `KNOWLEDGE_SYSTEM.md` — HE 编号注册表
- 维护 `generation_state.json` — 生成状态追踪
- 调度 subagent 并行开发课程
- 最终质量审计
- 监控系统集成决策

### 2.2 Subagent (课程开发者)

- 独立运行，无状态共享
- 每个 subagent 独占一个 `course_id` 的开发任务
- 读取 `skills/hotel-course-developer/SKILL.md` 获取开发规范
- 完成后报告给主 agent

### 2.3 共享生成器 (slide_generator.py)

- 所有 subagent 共用同一个生成器实例
- 通过 `generation_state.json` 防止重复生成
- 支持三种主题并行生成
- 维护 COURSE_TEMPLATES 作为内容模板库

---

## 三、数据流

### 3.1 课程开发数据流

```
主 Agent 调度
    ↓ (course_id, course_title, modules[])
    ↓
Subagent 接收任务
    ↓
Subagent 检查 ~/hotel-education/courses/{course_id}/
    ↓ (不存在则创建)
Subagent 编写 course.yaml + modules + slides
    ↓
Subagent 更新 COURSE_TEMPLATES (generator/slide_generator.py)
    ↓
Subagent 运行: python3 generator/slide_generator.py once hotel/stripe/linear
    ↓
生成器输出 HTML → output/{theme}/{course_key}.html
    ↓
Subagent 验证输出文件
    ↓
Subagent 返回完成报告
    ↓
主 Agent 审计并更新 generation_state.json
```

### 3.2 监控触发数据流

```
social-monitor/ 监控系统
    ↓ 检测到行业相关内容
    ↓
主 Agent 判断内容相关性
    ↓ (相关)
    ↓
触发 delegate_task 开发新课程 OR 更新现有课程
    ↓
(后续同上)
```

---

## 四、目录结构

```
~/hotel-education/
│
├── generator/                         # ⭐ 核心生成器 (所有 subagent 共用)
│   ├── slide_generator.py            #   主生成器脚本
│   └── generation_state.json         #   生成状态追踪 (共享文件)
│
├── knowledge/                         # ⭐ 知识体系定义
│   └── KNOWLEDGE_SYSTEM.md           #   HE 编号注册表
│
├── guidelines/                        # ⭐ 系统政策与设计
│   ├── POLICY.md                     #   系统政策 (本文件)
│   ├── ARCHITECTURE.md               #   架构蓝图
│   └── DESIGN_SYSTEM.md             #   设计系统规范
│
├── skills/                           # ⭐ Subagent 技能定义
│   └── hotel-course-developer/       #   课程开发者技能
│       └── SKILL.md                  #   开发规范与步骤
│
├── courses/                          # ⭐ 课程内容 (各 subagent 独立编写)
│   ├── HE.01.01/                    #   前厅部运营管理
│   │   ├── course.yaml
│   │   └── modules/
│   │       └── MOD-001/
│   ├── HE.01.02/                    #   客房部运营管理
│   └── ...                          #   更多课程
│
├── output/                           # ⭐ 生成输出 (共享目录)
│   ├── hotel/                       #   酒店教育风格
│   │   ├── front-office.html
│   │   ├── housekeeping.html
│   │   └── ...
│   ├── stripe/                      #   Stripe 极简顶奢
│   └── linear/                       #   Linear 深色精准
│
└── README.md
```

---

## 五、并发控制

### 5.1 Subagent 并发限制

**最大并发 subagent 数量**: 3 个 (由 delegate_task 的 `tasks` 数组限制)

原因:
- 超过 3 个 subagent 并发会导致资源竞争
- 共享的 `generation_state.json` 可能产生写冲突
- 符合 API rate limit 和系统稳定性

### 5.2 写冲突解决

`generation_state.json` 采用 **乐观锁** 策略:

```
Subagent A 读取 state
Subagent B 读取 state  (同一时刻)
Subagent A 更新 state → 写入
Subagent B 更新 state → 写入 (覆盖 A 的更新!)

→ 解决方案:
   使用文件锁 (fcntl.flock) 或在每次写入前 re-read 并合并
   目前简化处理: 主 agent 在调度时指定课程分配，确保不重复
```

**当前策略**: 主 agent 在调度前检查 `generation_state.json`，确保每个 course_id 只分配给一个 subagent。

### 5.3 生成器并发

slide_generator.py 内部是顺序执行的，每个 theme 按序生成。

---

## 六、部署拓扑

### 6.1 本地开发 (当前)

```
MacBook Pro M1 Pro (本地)
├── social-monitor/                  # 监控脚本
├── hotel-education/                # 课程生成系统
│   ├── generator/                   #   运行在此
│   └── output/                     #   HTML 课件
└── Hermes CLI (主 agent)            #   运行在此
```

### 6.2 云端扩展 (未来)

```
Cloud Server (如 Vultr / 阿里云)
├── cron: 定期运行 social-monitor
├── social-monitor/                  # 监控服务
├── hotel-education/                # 课程生成服务
│   └── generator/                   #   按需唤醒
└── Hermes Gateway (Telegram Bot)   #   通知推送
```

---

## 七、扩展路线图

### Phase 1: 当前完成 (v1.0)
- ✅ 单一机器、本地文件
- ✅ 手动触发生成
- ✅ 三主题 HTML 输出

### Phase 2: 下一个版本 (v1.1)
- [ ] 自动触发: 监控到相关内容自动生成课程
- [ ] Web 界面: 课程浏览 + 预览
- [ ] 增量更新: 只更新变化的模块，不全量重新生成

### Phase 3: 工业化 (v2.0)
- [ ] 多机器并行 subagent
- [ ] AI 内容增强: 接入 LLM API 丰富课程内容
- [ ] 视频导出: HTML → MP4 演示视频
- [ ] 多语言: zh-CN / en-US / 多语言版本

### Phase 4: 平台化 (v3.0)
- [ ] SaaS 化: 多人协作
- [ ] 酒店客户定制: 白标课程生成
- [ ] API 开放: 第三方接入

---

## 八、关键技术选型

| 组件 | 技术选型 | 原因 |
|------|---------|------|
| 课件格式 | HTML + CSS | 跨平台、可预览、不依赖专有软件 |
| 生成器语言 | Python 3 | 生态系统成熟，与 Agent 工具链一致 |
| 状态存储 | JSON 文件 | 简单、无依赖、人类可读 |
| 内容模板 | Python dict (COURSE_TEMPLATES) | 类型安全、易版本控制 |
| 三主题渲染 | 策略模式 (Renderer 抽象类) | 开闭原则，新增主题不修改核心代码 |
| Subagent 通信 | 主 agent → subagent 单向报告 | 简化，不需双向状态同步 |
| 监控系统 | 独立 cron + Python 脚本 | 解耦，可独立运行 |
