# Knowledge Distillation Markdown Protocol

Last_Updated: YYYY-MM-DD

## Overview

**Purpose**

* 定义多源材料向单文件认知型知识规范文档的蒸馏标准
* 确保 LLM 可稳定读取、信息完整、冲突显式

**Scope**

* Covers: 知识蒸馏文档的结构、格式、信息优先级规则
* Does not cover: 具体领域知识内容、执行 SOP

## Core Concepts

**知识蒸馏**

* 从多个输入材料中提取、合并、结构化核心知识
* 输出单一 Markdown 文件

**模块强制性**

* `[Required]` - 必须存在，缺失则文档不完整
* `[Conditional]` - 有相关内容时才需要，无内容时省略整个模块
* `[Optional]` - 增值内容，可选添加

**优先级标记**（仅用于 Consolidated Principles）

* `[Critical]` - 核心规则，必须严格遵守
* `[High]` - 重要规则，优先遵守
* `[Normal]` - 常规规则，正常遵守

## Consolidated Principles

**P1 [Critical]: 信息完整性**

* 核心信息绝不丢失

**P2 [Critical]: 冲突显式化**

* 不能隐式解决冲突，正文知识断层处需放置指针（如 `[Conflict: Ref Appendix]`），并在 Appendix 中记录

**P3 [High]: 冗余合并**

* 语义等价的表述合并为单一表达

**P4 [High]: 主次结构清晰**

* 认知层次分明，正文与附录分离

**P5 [High]: DO NOT > DO**

* 负面约束优先于正面指导
* 先说禁止什么，再说允许什么

**P6 [Normal]: 列表为主要表达**

* 优先使用列表，避免长段落

## Constraints

**Markdown 语法与排版约束**

禁止的语法

* `| table |` - 禁止表格 → 转为列表或键值对格式
* `> blockquote` - 禁止引用块 → 直接陈述内容
* `---` - 禁止水平分割线 → 用标题层级分隔
* `*italic*` - 禁止斜体 → 用加粗替代
* ````` - 禁止代码块 → 用行内代码或列表
* `<html>` - 禁止任何 HTML 标签
* `![image]()` - 禁止图片嵌入 → 用文字描述或链接
* 自定义引用格式、XML、伪标签 - 全部禁止

允许的语法与 Token 优化策略

* `# Heading` - 最多两级（`#` 和 `##`）
* `- list` - 无序列表（主要表达方式）
* `1. list` - 有序列表（用于有顺序的步骤）
* `**bold**` - 加粗（仅用于关键词突出）
* ``code`` - 行内代码（用于术语、命令、变量）
* `[text](url)` - 链接（用于跨文档引用）
* **层级控制** - 列表嵌套最多 2 级，禁止深层无意义缩进
* **绝对去噪** - 禁止修辞与填充词（如“需要注意的是”、“总而言之”）

**信息保留约束**

MUST PRESERVE（绝对不能丢）

* **核心概念定义** - 术语的精确含义（多源分歧需在此归一化，正文统一词汇）
* **隐式前提显式化** - 结论成立的前置条件、环境依赖或系统假设
* **认知与动作分离** - 过滤动作指令（SOP），转化为系统状态描述或原理映射
* **负面约束** - 不能做什么、如果这样做会导致什么坏处
* **因果关系** - 条件 → 结果的映射
* **硬性边界** - 数值限制、不变量
* **冲突信息** - 不同来源的矛盾（必须显式保留）
* **例外情况** - 除非...、除了...

MAY COMPRESS（可以压缩）

* **背景信息** - 压缩为最小必要上下文
* **修饰性语言** - 删除非常、极其等无信息量词汇
* **重复表述** - 合并为单一精确表达
* **冗长解释** - 提炼为简洁结论
* **历史演变** - 除非影响当前理解，否则可省略

判断标准

* 如果丢失会**改变语义** → 必须保留
* 如果丢失只会**减少细节** → 可以压缩
* 如果丢失会**引入歧义** → 必须保留

**模块使用约束**

* 空模块省略 - Conditional/Optional 模块无内容时，直接省略整个模块，不留空占位
* 优先级只用于 Principles - 其他模块不使用 `[Critical/High/Normal]` 标记
* Appendix 是元信息 - 不是最终知识本身，可 review 后删除或保留
* 极简元数据 - 仅保留 `Last_Updated: YYYY-MM-DD`，不需要来源追溯、版本信息、置信度标注

## Output Format

**模板结构**

```markdown
# {Document Title}
Last_Updated: YYYY-MM-DD

## Overview [Required]
- Purpose: ...
- Scope: Covers ... / Does not cover ...

## Core Concepts [Required]
- **Term A**: definition
- **Term B**: definition
- Conceptual Model: ...

## Consolidated Principles [Required]
- P1 [Critical]: ...
- P2 [High]: ...
- P3 [Normal]: ...

## Mechanisms & Logic [Conditional]
- Flow: 1. Step → 2. Step → 3. Step
- Decision Rules: Condition → Outcome

## Constraints [Conditional]
- C1: ...
- C2: ...

## Derived Insights [Optional]
- Insight 1: ...
- Insight 2: ...

## Output Format / Style Hints [Optional]
- Format: ...
- Style: ...

## Cross-Document References [Optional]
- See: [Related Topic](related_doc.md)

# Appendix

## Conflict Register [Conditional]
- Conflict 1: Position A vs Position B
  - Type: Semantic | Version | Scope
  - Affects: ...
  - Resolution Hint: ...

## Assumptions [Conditional]
- A1: ...
- A2: ...

```

**表格替代方案**

原表格格式

```markdown
| Key | Value |
| A   | 1, 2, 3 |
| B   | 4       |

```

替代格式（键值对平铺）

* **A**: 1; 2; 3
* **B**: 4