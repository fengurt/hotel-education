# 酒店课程开发者技能
# Hotel Course Developer Skill — For Subagent Use
# Version 1.0 — 2026-04-18

---

## 触发条件

当主 agent 将课程开发任务分配给你 (subagent) 时，自动加载本技能。

---

## 你的任务

```
开发课程: {course_id} — {course_title}
目标: 生成符合酒店教育标准的三主题 HTML 课件
工作目录: ~/hotel-education/
```

---

## 执行步骤

### Step 1: 读取知识体系

```bash
cat ~/hotel-education/knowledge/KNOWLEDGE_SYSTEM.md
```

确认你要开发的课程编号存在于 HE 体系中，且了解其前置课程。

---

### Step 2: 检查课程目录是否存在

```bash
ls ~/hotel-education/courses/{course_id}/
```

**如果目录存在**: 说明课程已在开发中，检查现有文件，决定是继续还是重新开发。

**如果目录不存在**: 创建以下结构:

```
courses/{course_id}/
├── course.yaml              # 课程元数据
├── modules/
│   ├── MOD-001/
│   │   ├── module.yaml
│   │   └── slides/
│   │       ├── 01.md
│   │       ├── 02.md
│   │       └── ...
│   ├── MOD-002/
│   └── ...
├── cases/
├── templates/
└── resources/
```

---

### Step 3: 编写 course.yaml

创建 `courses/{course_id}/course.yaml`:

```yaml
course_id: {course_id}
title: {course_title}
title_en: {English Title}
level: intermediate
version: 1.0.0
language: zh-CN
estimated_hours: {X}
prerequisites:
  - {prerequisite_course_id}
target_audience:
  - {audience description}
learning_outcomes:
  - "{outcome 1}"
  - "{outcome 2}"
modules:
  - module_id: MOD-001
    title: {module_title}
    duration_minutes: {N}
design_theme: hotel
status: in_development
```

---

### Step 4: 编写模块内容

每个模块需要:
1. `module.yaml` — 模块定义
2. `slides/*.md` — 各幻灯片内容 (至少 3-5 页/模块)

**幻灯片 Markdown 格式**:

```markdown
---
slide_id: 01
type: title
title: 模块封面标题
subtitle: "模块 1 · 45 分钟 · theory"
---

---
slide_id: 02
type: section
title: 内容章节
---

---
slide_id: 03
type: list
title: 学习目标
body: "完成本模块学习后，您应掌握:"
items:
  - 目标点 1
  - 目标点 2
  - 目标点 3
---

---
slide_id: 04
type: process
title: 流程步骤
body: "标准操作流程如下:"
items:
  - 步骤 1
  - 步骤 2
  - 步骤 3
---

---
slide_id: 05
type: highlight
title: 核心要点
body: "这是需要特别记住的关键内容"
items:
  - "强调说明 1"
---

---
slide_id: 06
type: comparison
title: 对比分析
items:
  - title: 场景 A
    content: A 的描述内容
  - title: 场景 B
    content: B 的描述内容
```

---

### Step 5: 生成 HTML

调用 slide_generator.py 生成三套主题的 HTML:

```bash
cd ~/hotel-education

# 生成 hotel 主题
python3 generator/slide_generator.py once hotel

# 生成 stripe 主题
python3 generator/slide_generator.py once stripe

# 生成 linear 主题
python3 generator/slide_generator.py once linear
```

如果 COURSE_TEMPLATES 中还没有这门课程，需要先更新 slide_generator.py:

编辑 `generator/slide_generator.py`，在 `COURSE_TEMPLATES` 字典中添加:

```python
"{course_key}": {
    "title": "{course_title}",
    "level": "intermediate",
    "course_id": "{course_id}",
    "modules": [
        {
            "module_id": "MOD-001",
            "title": "{module_title}",
            "duration_minutes": 45,
            "lesson_type": "theory",
            "objectives": [
                "目标1",
                "目标2",
            ],
            "slides": [
                {
                    "title": "幻灯片标题",
                    "body": "描述文字",
                    "content_type": "list",
                    "items": ["要点1", "要点2", "要点3"]
                },
                # 更多幻灯片...
            ]
        },
        # 更多模块...
    ]
},
```

然后运行生成命令。

---

### Step 6: 验证输出

```bash
# 检查文件存在
ls -la ~/hotel-education/output/hotel/{course_key}.html
ls -la ~/hotel-education/output/stripe/{course_key}.html
ls -la ~/hotel-education/output/linear/{course_key}.html

# 检查文件大小 (> 5KB 才算有效)
wc -c ~/hotel-education/output/hotel/{course_key}.html

# 检查 HTML 基本结构
head -20 ~/hotel-education/output/hotel/{course_key}.html
```

**验证标准**:
- ✅ 文件存在且 > 5KB
- ✅ 包含 `<!DOCTYPE html>` 和 `<div class="slide"`
- ✅ 包含至少 3 个 `.slide` 元素
- ✅ 三套主题全部生成成功

---

### Step 7: 完成报告

输出以下格式的报告:

```
✅ 课程 {course_id} 开发完成

📁 输出文件:
   - ~/hotel-education/output/hotel/{course_key}.html
   - ~/hotel-education/output/stripe/{course_key}.html
   - ~/hotel-education/output/linear/{course_key}.html

📊 课程统计:
   - 模块数: {N}
   - 幻灯片数: {M}
   - 总时长: 约 {X} 小时

🔍 质量检查:
   - HTML 语法: ✅ 通过
   - 设计系统合规: ✅ 三主题全部符合规范
   - 内容深度: ✅ 要点均有 2+ 句展开
```

---

## 常见问题处理

### Q1: slide_generator.py 中 COURSE_TEMPLATES 没有这门课

**解决**: 先更新 slide_generator.py 中的 COURSE_TEMPLATES，再运行生成命令。

### Q2: 三主题只生成了部分

**解决**:
```bash
# 清理状态文件，重新生成
rm ~/hotel-education/generation_state.json
python3 generator/slide_generator.py once {theme}
```

### Q3: 生成的 HTML 是空的或只有标题页

**原因**: COURSE_TEMPLATES 中的 slides 数组为空或模块没有正确配置。

**解决**: 检查 module 下的 slides 配置是否正确填充。

### Q4: 需要修改已生成的课程

**解决**:
1. 修改 COURSE_TEMPLATES 中对应课程的内容
2. 删除对应课程的所有已生成文件
3. 重新运行生成命令

---

## 关键路径参考

| 资源 | 路径 |
|------|------|
| 酒店教育根目录 | `~/hotel-education/` |
| 核心生成器 | `~/hotel-education/generator/slide_generator.py` |
| 知识体系 | `~/hotel-education/knowledge/KNOWLEDGE_SYSTEM.md` |
| 系统政策 | `~/hotel-education/guidelines/POLICY.md` |
| 设计系统规范 | `~/hotel-education/guidelines/DESIGN_SYSTEM.md` |
| 输出目录 | `~/hotel-education/output/{theme}/` |
| 课程元数据 | `~/hotel-education/courses/{course_id}/course.yaml` |

---

## 参考: 已有课程示例

已有课程的结构可供参考:

```bash
# 查看 front-office 课程是如何配置的
cat ~/hotel-education/generator/slide_generator.py | grep -A 50 "front-office"
```

---

## 注意事项

1. **不要硬编码** — 所有课程内容必须通过 COURSE_TEMPLATES 配置，不允许在 slide_generator.py 之外单独生成单课程 HTML
2. **三主题必须齐全** — 每门课程必须同时生成 hotel/stripe/linear 三套主题，缺一不可
3. **内容深度** — 避免空洞的"这个很重要"式废话，每个要点至少 2-3 句实质内容
4. **模块时长** — 每个模块建议 30-90 分钟，超出需特别说明原因
5. **学习目标** — 每个模块必须有 objectives，且与课程整体 learning_outcomes 对齐
