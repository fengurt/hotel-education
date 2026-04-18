# 酒店教育知识体系 (Hotel Education Knowledge System)
# Hotel Education Architecture - Hierarchical Framework

## 一级体系：酒店管理学科总览

### HE.01 酒店运营管理 (Hotel Operations Management)
- HE.01.01 前厅部管理 (Front Office Operations)
- HE.01.02 客房部管理 (Housekeeping Management)
- HE.01.03 餐饮部管理 (Food & Beverage Management)
- HE.01.04 宴会与会议管理 (Banquet & Conference Management)
- HE.01.05 健身与休闲管理 (Spa & Recreation Management)

### HE.02 酒店市场营销 (Hotel Marketing & Sales)
- HE.02.01 收益管理 (Revenue Management)
- HE.02.02 数字营销 (Digital Marketing)
- HE.02.03 品牌管理 (Brand Management)
- HE.02.04 客户关系管理 (CRM & Guest Relations)

### HE.03 酒店财务管理 (Hotel Financial Management)
- HE.03.01 成本控制 (Cost Control)
- HE.03.02 预算管理 (Budgeting)
- HE.03.03 财务分析 (Financial Analysis)

### HE.04 酒店人力资源 (Hotel Human Resources)
- HE.04.01 招聘与培训 (Recruitment & Training)
- HE.04.02 绩效管理 (Performance Management)
- HE.04.03 员工关系 (Labor Relations)

### HE.05 酒店工程与安全管理 (Hotel Engineering & Security)
- HE.05.01 设施维护 (Facility Maintenance)
- HE.05.02 能源管理 (Energy Management)
- HE.05.03 安全管理 (Safety & Security)

### HE.06 酒店战略管理 (Hotel Strategic Management)
- HE.06.01 酒店估值与投资 (Hotel Valuation & Investment)
- HE.06.02 品牌加盟与合作 (Franchising & Partnerships)
- HE.06.03 可持续发展 (Sustainability in Hospitality)

---

## 二级知识点结构 (每门课程)

```
Course {
  id: HE.XX.XX
  name: 课程名称
  level: 入门/进阶/高级
  
  modules: [
    Module {
      id: MOD-001
      title: 模块标题
      duration: 课时(分钟)
      type: 理论/实操/案例
      
      lessons: [
        Lesson {
          id: LESSON-001
          title: 课时标题
          objectives: ["学习目标1", "学习目标2"]
          content_slides: 幻灯片数量
          assessment: 评估方式
        }
      ]
    }
  ]
  
  resources: {
    case_studies: 案例列表
    templates: 模板列表
    readings: 阅读材料
  }
}
```

---

## 知识图谱关系

```
酒店管理
├── 运营
│   ├── 前厅 ──→ 入住流程 / 投诉处理 / VIP管理
│   ├── 客房 ──→ 清洁标准 / 布草管理 / 库存控制
│   └── 餐饮 ──→ 厨房管理 / 服务标准 / 食品安全
├── 营销
│   ├── 收益 ──→ 动态定价 / 渠道管理 / 预测模型
│   └── 品牌 ──→ VI规范 / 市场定位 / 声誉管理
└── 战略
    ├── 投资 ──→ 可行性分析 / 现金流 / 退出策略
    └── 人才 ──→ 胜任力模型 / 领导力 / 文化传承
```

---

## 课件生成优先级

### Phase 1: 核心必修课 (优先级最高)
1. 前厅操作标准 (HE.01.01)
2. 客房清洁标准 (HE.01.02)
3. 餐饮服务流程 (HE.01.03)
4. 收益管理基础 (HE.02.01)

### Phase 2: 管理进阶课
5. 客户关系管理 (HE.02.04)
6. 成本控制 (HE.03.01)
7. 酒店安全 (HE.05.03)
8. 领导力基础 (HE.04)

### Phase 3: 战略与专项
9. 酒店投资分析 (HE.06.01)
10. 品牌管理 (HE.02.03)
11. 可持续发展 (HE.06.03)
12. 数字化运营 (HE.01 + IT)

---

## 瑞士洛桑酒店管理学院 (EHL) 课程体系对标

| EHL 模块 | 对应 HE 编号 | 核心内容 |
|---------|-------------|---------|
| Hospitality Essentials | HE.01 | 酒店运营基础 |
| Food & Beverage Management | HE.01.03 | 餐饮管理 |
| Rooms Division Management | HE.01.01+02 | 前厅与客房 |
| Hospitality Marketing | HE.02 | 酒店营销 |
| Hospitality Finance | HE.03 | 酒店财务 |
| Human Capital | HE.04 | 人力资源 |
| Real Estate & Leadership | HE.06 | 战略与领导力 |
