# 设计系统规范
# Hotel Education Design System — Specification
# Version 1.0 — 2026-04-18

---

## 一、设计理念

酒店教育课件的设计系统融合三大来源:

| 来源 | 核心特征 | 适用场景 |
|------|---------|---------|
| **Stripe Design** | 极简顶奢、300字重、金融级克制 | 商务风格课件、收益管理类 |
| **Linear Design** | 深色精准、510字重、半透明边框 | 技术类课程、数据分析类 |
| **酒店教育专用** | 温暖学院感、金色点缀、Playfair 衬线 | 通用课件、运营管理类 |

---

## 二、字体系统

### 2.1 字体家族

| 用途 | 推荐字体 | 字重范围 |
|------|---------|---------|
| 标题字体 | Playfair Display | 400, 500, 600 |
| 中文中性 | Noto Sans SC | 300, 400, 500 |
| 英文中性 | Inter | 300, 400, 500, 590, 510 |
| 数据/代码 | JetBrains Mono | 400, 500 |
| Stripe 专用 | Source Sans 3 | 300, 400, 500, 600 |
| Stripe 代码 | Source Code Pro | 400, 500 |

### 2.2 Google Fonts CDN 引入方式

```
酒店主题:
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600&family=Inter:wght@300;400;500&family=Noto+Sans+SC:wght@300;400;500&display=swap" rel="stylesheet">

Stripe 主题:
<link href="https://fonts.googleapis.com/css2?family=Source+Sans+3:wght@300;400;500;600&family=Source+Code+Pro:wght@400;500&display=swap" rel="stylesheet">

Linear 主题:
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
```

---

## 三、色彩系统

### 3.1 酒店教育专用主题 (hotel)

```css
:root {
    --bg:        #F5F1E8;   /* 米白 — 温暖的学院感背景 */
    --heading:   #0A1628;   /* 深蓝黑 — 庄重的标题 */
    --body:      #4a5568;   /* 中性灰 — 柔和的正文 */
    --accent:    #1B4D3E;   /* 森林绿 — 酒店品牌主色 */
    --gold:      #C9A962;   /* 香槟金 — 点缀强调 */
    --border:    rgba(27,77,62,0.15);   /* 绿色透明边框 */
    --surface:   rgba(27,77,62,0.05);   /* 淡绿色表面 */
    --warm:      #8B4513;   /* 暖棕色 — 可选辅助色 */
    --alert:     #C41E3A;   /* 警示红 — 错误/警告状态 */
}
```

### 3.2 Stripe 极简顶奢主题 (stripe)

```css
:root {
    --bg:        #ffffff;   /* 纯白 — 极致干净 */
    --heading:   #061b31;   /* 深海军蓝 — 品牌化标题 */
    --body:      #64748b;   /* 冷灰 — 正文 */
    --label:     #273951;   /* 深蓝灰 — 标签/次要标题 */
    --accent:    #533afd;   /* 品牌紫 — CTA/高亮 */
    --accent-hover: #4434d4; /* 深紫 — 悬停态 */
    --border:    #e5edf5;   /* 极浅蓝灰 — 边框 */
    --shadow:    rgba(50,50,93,0.25); /* 品牌化深度阴影 */
    --radius:    4px;       /* 保守圆角 — 克制优雅 */
    --gold:      #A88B52;   /* 淡金 — 可选强调 */
    --gold-light: #C9A962;  /* 亮金 — 高亮 */
    --muted:     #999;      /* 次要信息 */
}
```

### 3.3 Linear 深色精准主题 (linear)

```css
:root {
    --bg:        #08090a;   /* 近黑 — 深色原生感 */
    --surface:   #0f1011;   /* 深灰 — 卡片/面板 */
    --surface-el: #191a1b;  /* 稍浅 — 提升元素 */
    --heading:   #f7f8f8;   /* 近白 — 高对比标题 */
    --body:      #d0d6e0;   /* 浅灰 — 正文 */
    --muted:     #8a8f98;   /* 次要灰 — 注释/元信息 */
    --accent:    #7170ff;   /* 靛蓝紫 — 品牌色 */
    --accent-bg: #5e6ad2;   /* 紫蓝 — 次要背景 */
    --border:    rgba(255,255,255,0.08);   /* 半透明白 — 结构线 */
    --border-subtle: rgba(255,255,255,0.05); /* 更淡 — 细分边框 */
    --green:     #10b981;   /* 成功绿 */
    --red:       #ef4444;   /* 错误红 */
    --radius:    8px;       /* 现代圆角 */
}
```

---

## 四、排版规范

### 4.1 全局排版

| 属性 | 规范 |
|------|------|
| 幻灯片最小高度 | 720px |
| 幻灯片内边距 | 80px 垂直 (padding-top/bottom), 100px 水平 (padding-left/right) |
| 幻灯片间分隔 | 1px solid border-bottom |
| 最大内容宽度 | 1200px (居中) |

### 4.2 字号层级

**酒店主题:**

| 元素 | 字号 | 字重 | 字体 | 行高 |
|------|------|------|------|------|
| 封面大标题 | 52px | 500 | Playfair Display | 1.2 |
| 章节标题 (h2) | 42px | 500 | Playfair Display | 1.2 |
| 内容标题 (h3) | 30px | 500 | Playfair Display | 1.3 |
| 正文 | 17px | 300 | Noto Sans SC | 1.9 |
| 列表项 | 16px | 400 | Noto Sans SC | 1.8 |
| 元信息/页码 | 11px | 400 | Noto Sans SC | 1.5 |

**Stripe 主题:**

| 元素 | 字号 | 字重 | 字体 | 行高 |
|------|------|------|------|------|
| 封面大标题 | 56px | 300 | Source Sans 3 | 1.03 |
| 章节标题 (h2) | 48px | 300 | Source Sans 3 | 1.1 |
| 内容标题 (h3) | 32px | 300 | Source Sans 3 | 1.2 |
| 正文 | 18px | 300 | Source Sans 3 | 1.7 |
| 列表项 | 18px | 300 | Source Sans 3 | 1.8 |
| 标签/页码 | 12px | 400 | Source Sans 3 | 1.5 |

**Linear 主题:**

| 元素 | 字号 | 字重 | 字体 | 行高 |
|------|------|------|------|------|
| 封面大标题 | 56px | 510 | Inter | 1.05 |
| 章节标题 (h2) | 40px | 510 | Inter | 1.1 |
| 内容标题 (h3) | 28px | 590 | Inter | 1.15 |
| 正文 | 17px | 400 | Inter | 1.7 |
| 列表项 | 16px | 400 | Inter | 1.7 |
| 标签/页码 | 12px | 400 | Inter | 1.5 |

### 4.3 字重哲学

> **字重越轻 = 越自信** — Stripe Design Principle
> 
> 顶级品牌使用 300 Light 作为标题，传达克制与高级感。
> 数字 510 是 Linear 的"签名重量"，用于需要强视觉焦点的场景。

---

## 五、组件规范

### 5.1 幻灯片类型样式

#### 封面幻灯片 (type="title")

酒店主题:
```css
.slide--title {
    justify-content: center;
    align-items: center;
    text-align: center;
    background: linear-gradient(135deg, #0A1628 0%, #1B4D3E 100%);
    color: white;
}
.slide--title h1 {
    font-family: 'Playfair Display', serif;
    font-size: 52px;
    font-weight: 500;
    letter-spacing: -0.5px;
    line-height: 1.2;
    margin-bottom: 24px;
}
.slide--title .subtitle {
    font-size: 18px;
    font-weight: 300;
    opacity: 0.85;
    letter-spacing: 2px;
    text-transform: uppercase;
}
```

Stripe 主题:
```css
.slide--title {
    justify-content: center;
    align-items: center;
    text-align: center;
    background: linear-gradient(135deg, #061b31 0%, #1a2a4a 100%);
    color: white;
}
.slide--title h1 {
    font-family: 'Source Sans 3', sans-serif;
    font-size: 56px;
    font-weight: 300;
    letter-spacing: -1.4px;
    line-height: 1.03;
    margin-bottom: 24px;
}
```

Linear 主题:
```css
.slide--title {
    justify-content: center;
    align-items: center;
    text-align: center;
    background: #08090a;
    color: white;
}
.slide--title h1 {
    font-family: 'Inter', sans-serif;
    font-size: 56px;
    font-weight: 510;
    letter-spacing: -1.4px;
    line-height: 1.05;
}
```

#### 章节分隔页 (type="section")

| 主题 | 背景色 | 标题色 | 特殊处理 |
|------|--------|--------|---------|
| hotel | #1B4D3E (酒店绿) | white | Playfair Display |
| stripe | #061b31 (深蓝) | white | Source Sans 3 300 |
| linear | #0f1011 (深灰) | white | 左侧 3px accent 边框 |

#### 内容页 (type="list", "highlight", "process")

统一规则:
- 左上标题 (h3)
- 标题下可选正文 (body-text)
- 内容区域
- 右下页码 (page-num)

### 5.2 列表样式

**酒店主题:**
```css
.items-list { list-style: none; }
.items-list li {
    display: flex;
    align-items: flex-start;
    gap: 16px;
    padding: 14px 0;
    border-bottom: 1px solid var(--border);
}
.items-list li::before {
    content: "✦";  /* 金色星号 */
    color: var(--gold);
    font-size: 12px;
    flex-shrink: 0;
    margin-top: 4px;
}
```

**Stripe 主题:**
```css
.items-list li::before {
    content: "—";  /* 破折号 */
    color: var(--gold);
}
```

**Linear 主题:**
```css
.items-list li::before {
    content: "";   /* 6px 圆点 */
    width: 6px;
    height: 6px;
    background: var(--accent);
    border-radius: 50%;
}
```

### 5.3 流程步骤 (type="process")

```css
.process-step {
    display: flex;
    align-items: center;
    gap: 20px;
    margin: 16px 0;
}
.step-num {
    width: 36px;
    height: 36px;
    background: var(--accent);
    color: white;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 14px;
    font-weight: 500;
    flex-shrink: 0;
}
.step-text { font-size: 16px; }
```

### 5.4 高亮框 (type="highlight")

酒店主题:
```css
.highlight-box {
    background: var(--surface);
    border-left: 4px solid var(--gold);
    padding: 24px 30px;
    border-radius: 0 4px 4px 0;
}
```

Stripe 主题:
```css
.highlight-box {
    background: rgba(168,139,82,0.08);
    border: 1px solid rgba(168,139,82,0.2);
    border-radius: 4px;
    padding: 30px;
}
```

### 5.5 对比组件 (type="comparison")

```css
.two-col {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 50px;
    margin-top: 30px;
}
.col {
    background: white;  /* 酒店主题 */
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 28px;
}
.col h4 {
    font-family: 'Playfair Display', serif;  /* 酒店主题 */
    font-size: 18px;
    margin-bottom: 14px;
}
```

---

## 六、交互动画

### 6.1 过渡效果

默认过渡: `transition: fade` (CSS fade)

所有幻灯片切换建议使用淡入:
```css
.slide {
    animation: fadeIn 0.3s ease-out;
}
@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}
```

### 6.2 悬停效果

按钮/可交互元素悬停态:
```css
/* Stripe */
.button:hover {
    background: var(--accent-hover);
    transform: translateY(-1px);
}

/* Linear */
.button:hover {
    background: var(--accent-bg);
    border-color: var(--accent);
}
```

---

## 七、响应式策略

当前版本聚焦 **16:9 横屏** 单页展示，不做响应式。

未来版本可扩展:
```css
@media (max-width: 768px) {
    .slide { padding: 40px 30px; min-height: auto; }
    .slide h1 { font-size: 36px; }
    .two-col { grid-template-columns: 1fr; }
}
```

---

## 八、质量检查清单

生成课件后，用此清单验证设计系统合规性:

```
[ ] 字体引入: Google Fonts CDN 链接正确
[ ] CSS 变量: 三套主题的 :root 变量全部定义
[ ] 色彩: --bg, --heading, --body, --accent, --gold 均已设置
[ ] 字号: 标题/正文/页码层级正确
[ ] 字重: 酒店主题标题用 500, Stripe 用 300, Linear 用 510/590
[ ] 幻灯片高度: min-height: 720px
[ ] 内边距: 80px 垂直, 100px 水平
[ ] 列表样式: ::before 符号/圆点正确
[ ] 流程步骤: step-num 圆形数字正确
[ ] 高亮框: 左边框 4px gold
[ ] 封面背景: 渐变色或深色背景
[ ] 页码位置: 右下角
```

---

## 九、主题切换规范

当需要同时支持三种主题时，确保:

1. **每个主题独立的 Renderer 类** — 不共享状态
2. **独立的 CSS 变量注入** — 不互相渗透
3. **独立的字体配置** — Google Fonts 分别引入
4. **相同的幻灯片内容** — 三套主题输出内容一致
