---
name: dst-distiller
description: 知识蒸馏器 - 将多源材料蒸馏为结构化知识文档。当用户说distill或整理知识或合并文档时使用。
argument-hint: 目录路径或 dst-planner 生成的 JSON 规格
license: MIT
metadata:
  version: "1.0"
  author: Sinyuk
  email: 80998062@qq.com
  input: 支持自然语言或 JSON 快速启动
---

# Knowledge Distiller

将多源材料蒸馏为单一结构化认知型知识文档的交互式 Skill。

## 核心协议

**必须遵循**: 在执行蒸馏前，先读取项目中的 `docs/protocols/Knowledge_Distillation_Protocol.md` 协议文件。该协议定义了：
- 文档结构模板（Required/Conditional/Optional 模块）
- Markdown 语法约束（禁止表格、引用块等）
- 信息保留规则（MUST PRESERVE vs MAY COMPRESS）
- 优先级标记规则

## 启动模式

### 模式 A: 标准对话模式（默认）
当用户以自然语言启动蒸馏任务时，进入完整的 Phase 1-6 交互流程。

### 模式 B: JSON 快速启动模式
当检测到用户输入中包含 `distill-planner` 生成的 JSON 规格时：

```
检测条件: 输入包含有效的 JSON 且包含 "source" + "output" + "topic" 字段
```

**快速启动流程**:
1. 解析 JSON 规格
2. 显示规格摘要，请求用户最终确认
3. 确认后直接跳转到 **Phase 3: 模块选择**（基于 JSON 中的 include/exclude 自动推断）
4. 继续 Phase 4-6

**JSON 字段映射**:
| JSON 字段 | 对应 Phase | 处理方式 |
|-----------|------------|----------|
| `source` | Phase 1 | 直接使用，无需询问 |
| `output` | Phase 1 | 直接使用，无需询问 |
| `topic` | Phase 2 | 直接使用，无需询问 |
| `focus` | Phase 2 | 决定知识提取方向 |
| `terminology.unify` | Phase 2 | 术语统一规则，自动应用 |
| `exclude.categories` | Phase 2 | 内容排除规则，自动应用 |
| `include.focus` | Phase 2/3 | 决定模块选择 |
| `output_constraints` | Phase 4/5 | 应用到输出生成 |

**规格确认示例**:
```
检测到 distill-planner JSON 规格，解析结果：

📂 源: raw_data/ai_image/z-image
📄 输出: wiki/prompt/z-image/z-image-prompt-donot-guide.md
🎯 主题: z-image 提示词构造禁忌指南
📝 焦点: negative（禁止事项）
🔄 术语统一: z-image-turbo → z-image
❌ 排除: 11 类技术参数
📏 长度: ≥300 行

确认启动？[Y/继续] 或 [N/返回标准模式]
```

---

## 对话流程

这是一个**驱动型对话流程**，每个阶段都需要与用户交互确认后再进入下一阶段。

### Phase 1: 范围确认

**目标**: 明确蒸馏的输入范围和知识边界

执行步骤:
- 扫描用户指定的目标目录
- 向用户展示文件列表概览（文件名、类型、大小）
- 与用户确认以下问题:
  - 哪些文件需要纳入蒸馏范围？（可以是全部，也可以排除某些）
  - 知识的主题边界是什么？（帮助聚焦核心内容）
  - 有什么明确的排除条件？（如"忽略历史版本"、"只看 .md 文件"）

等待用户确认后，进入 Phase 2。

### Phase 2: 蒸馏焦点

**目标**: 理解用户的蒸馏意图，确定知识提取的方向

执行步骤:
- 快速分析纳入范围的材料内容
- 识别材料中的知识类型（概念定义、操作规则、约束条件、因果关系等）
- 基于用户的原始输入和材料分析，向用户确认以下内容:

**2.1 核心主题**
- 核心知识内容是什么？（主题、领域）
- 用户是否在输入中暗示了术语等价关系？（如用户混用 A 和 B，需确认是否视为同一实体）

**2.2 提取范围**
- 用户想要提取什么类型的知识？
- 如果用户的输入中有明确的范围限制（如"只要 X"、"不要 Y"），需要确认理解是否正确
- 如果用户没有明确限制，按完整蒸馏处理

**2.3 内容排除**
- 用户是否在输入中提到了排除条件？
- 如果有，确认排除规则
- 如果没有，询问是否有需要忽略的内容

**2.4 语调和风格**
- 如果用户的输入暗示了特定语调（如"禁令"、"建议"），确认理解
- 如果没有，使用中性的知识陈述风格

等待用户确认后，进入 Phase 3。

### Phase 3: 模块选择

**目标**: 确定输出文档的模块结构

根据协议，模块分为三类:
- `[Required]`: Overview, Core Concepts, Consolidated Principles
- `[Conditional]`: Mechanisms & Logic, Constraints, Conflict Register, Assumptions
- `[Optional]`: Derived Insights, Output Format / Style Hints, Cross-Document References

执行步骤:
- 基于 Phase 2 确认的蒸馏焦点，推荐适配的模块组合
- 根据用户的提取范围和材料内容，判断哪些模块有意义

向用户展示建议:
- **必选模块**: 列出并简述每个模块预计包含的内容
- **建议包含**: 根据材料内容推荐的 Conditional 模块
- **建议跳过**: 材料中缺乏相关内容的模块
- **可选添加**: Optional 模块是否需要

用户可以修改这个配置。

等待用户确认后，进入 Phase 4。

### Phase 4: 输出格式分析

**目标**: 识别是否需要定义特定的输出格式或风格指南

执行步骤:
- 分析材料中是否暗示特定的输出格式需求，例如:
  - Prompt 模板结构
  - 代码风格约定
  - 命名规范
  - 特定的表达模式
- 如果识别到这类需求:
  - 主动向用户说明发现的格式特征
  - 询问是否需要添加 `Output Format / Style Hints` 模块
  - 用户确认后，将这些格式要求纳入该模块
- 如果没有识别到:
  - 简单告知用户，直接进入执行阶段

等待用户确认后，进入 Phase 5。

### Phase 5: 执行蒸馏

**目标**: 生成最终的蒸馏文档

**关键策略**: 渐进式写入，防止超时

执行步骤:
1. 确定输出文件名（基于主题，如 `{topic}_knowledge.md`），放在目标目录下
2. 创建文件，写入标题和 `Last_Updated: YYYY-MM-DD`
3. 按模块顺序逐个生成并**立即追加写入**:
   - Overview [Required] → 写入
   - Core Concepts [Required] → 写入
   - Consolidated Principles [Required] → 写入
   - 用户选定的 Conditional 模块 → 逐个写入
   - 用户选定的 Optional 模块 → 逐个写入
   - Appendix（如有 Conflict Register 或 Assumptions）→ 写入
4. 每个模块写入后，简短报告进度

**写入约束**:
- 每个模块完成后必须立即写入，不缓存到最后
- 空模块直接跳过，不写占位符
- 严格遵循协议中的 Markdown 语法约束

### Phase 6: 完成报告

**目标**: 汇总蒸馏结果

输出内容:
- 源文件列表及处理状态
- 输出文件路径
- 蒸馏统计（原始材料概况 vs 输出文档结构）
- 如有冲突信息，提醒用户查看 Appendix 中的 Conflict Register

## 错误处理

- **文件读取失败**: 跳过该文件，在最终报告中标记
- **写入失败**: 停止执行，报告错误位置，已写入内容保留
- **用户中断**: 已写入的内容保留在文件中，可从断点继续

## 交互原则

- 每个 Phase 结束时，明确等待用户确认再继续
- 提供合理的默认建议，但给用户修改空间
- 对于复杂决策，解释你的推理过程
- 保持对话简洁，避免冗长解释
