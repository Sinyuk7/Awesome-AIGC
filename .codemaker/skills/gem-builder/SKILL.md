---
name: gem-builder
<<<<<<< HEAD
description: |
  GEM 构造器 - 帮助用户设计和生成 Gemini GEM 的完整配置（Name、Description、Instructions、Knowledge）。
  当用户想要创建一个 GEM、定制 Gemini 助手、构建专属 AI 角色、或提到"GEM"、"Gem"、"gem"时，应该使用这个 skill。
  也适用于用户描述一个重复性任务希望让 AI 自动化处理的场景，即使他们没有明确说"GEM"。
=======
description: GEM 构造器 - 帮助用户设计和生成 Gemini GEM 的完整配置（Name、Description、Instructions、Knowledge）。当用户想要创建一个 GEM、定制 Gemini 助手、构建专属 AI 角色、或提到"GEM"、"Gem"、"gem"时，应该使用这个 skill。也适用于用户描述一个重复性任务希望让 AI 自动化处理的场景，即使他们没有明确说"GEM"。
argument-hint: 描述你想创建的 GEM 的功能和用途
license: MIT
metadata:
  version: "1.0"
  author: Sinyuk
  email: 80998062@qq.com
  output: GEM config (Name, Description, Instructions, Knowledge)
>>>>>>> e66b05a560ece06ac738113d23305c30f0cd2211
---

# GEM 构造器

## 触发方式

- `/gem` - 启动 GEM 构造器
- `/gem {需求描述}` - 直接带上需求描述启动
- `@skill gem-builder` - 显式调用

## 输入参数

- **需求描述** (可选): 用户对 GEM 的需求描述，如不提供则进入交互式引导

帮助用户从模糊的想法出发，通过智能对话收集必要信息，最终生成可直接使用的 GEM 配置。

## 核心工作流

### Phase 1: 理解用户意图

首先分析用户的输入，识别已提供的信息和缺失的关键维度。

**四个核心维度（基于 PTCF 框架）：**

1. **Persona（角色）**：GEM 应该扮演什么角色？专家、助手、导师？
2. **Task（任务）**：GEM 的核心工作是什么？要完成什么具体任务？
3. **Context（上下文）**：有什么约束、边界、特殊要求？什么不应该做？
4. **Format（格式）**：期望的输出格式是什么？列表、表格、特定结构？

**信息收集策略：**

- 不要逐项询问，而是根据用户已提供的信息，只追问真正缺失的关键信息
- 如果用户描述已经足够清晰，可以直接进入设计阶段
- 优先关注 Task（任务）和 Context（边界），这两个维度最影响 GEM 质量

### Phase 2: 设计思路确认

在生成完整配置之前，先输出 Instructions 的**设计大纲**，让用户确认：

```
## 设计思路

**GEM 名称**: [拟定名称]

**Instructions 大纲**:
- Persona: [角色定位概述]
- Task: [核心任务列表]
- Context: [约束和边界]
- Format: [输出格式要求]

**知识库建议**: [如果需要，列出建议上传的文件类型]

请确认这个方向是否正确，或告诉我需要调整的地方。
```

### Phase 3: 生成完整配置

用户确认后，按以下格式输出最终配置：

---

## Name
[GEM 名称 - 简洁有力，2-4 个词]

## Description
[简短描述 GEM 的功能和用途，1-2 句话]

## Instructions

[纯文本格式的完整指令，可直接复制到 Gemini]

按照 PTCF 框架组织，包含：
- Persona 部分
- Task 部分
- Context 部分
- Format 部分

## Knowledge
[需要上传的文件列表，如果用户提到了具体文件名，原样列出]

---

## 指令编写规范

### 语言
Instructions 内容**必须使用英文**，即使用户用中文沟通。

### 结构模板

<<<<<<< HEAD
**标准模板（适用于大多数 GEM）：**

=======
>>>>>>> e66b05a560ece06ac738113d23305c30f0cd2211
```
Persona:
- [Role definition]
- [Expertise and capabilities]

Task:
- [Primary task]
- [Secondary tasks]
- [Specific deliverables]

Context:
- [Constraints and boundaries]
- [What NOT to do - use "Never" or "Do not"]
- [Tone and style requirements]
- [Assumptions about user]

Format:
- [Output structure]
- [Specific formatting requirements]
<<<<<<< HEAD
- [从用户需求/知识库中提取的格式约束，如长度、结构等]
- [Examples if helpful]
```

**工作流模板（适用于多步骤任务型 GEM）：**

当 GEM 需要执行明确的多步骤流程时，Task 部分采用 Step 结构：

```
Persona:
- [Role definition]

Task:
Follow this workflow:

Step 1 - [Name]:
- [Action]

Step 2 - [Name]:
- Reference [document_name] if applicable
- [Action]

Step 3 - [Name]:
- [Action]

Step N - Output:
- [Final deliverable only]

Context:
- [Core constraints - keep minimal, avoid repeating Task content]

Never:
- [Critical prohibitions]

Format:
- [Output structure and constraints]
```

工作流模板原则：
- 每步职责单一，不重叠
- 文档加载在对应步骤中明确声明（"Reference [filename]"）
- 最后一步专门定义输出
- Context 和 Never 保持精简，避免与 Task 步骤内容重复

=======
- [Examples if helpful]
```

>>>>>>> e66b05a560ece06ac738113d23305c30f0cd2211
### 关键原则

1. **负面约束优先**：明确写出 GEM 不应该做什么，使用 "Never" 或 "Do not"
2. **具体胜过模糊**：与其说"be helpful"，不如说具体如何帮助
3. **文件引用正确**：如果用户提到具体文件名，在 Instructions 中使用相同的文件名引用
4. **长度适中**：避免过长的指令稀释重点，详细内容应放入知识库
<<<<<<< HEAD
5. **无重复冗余**：同一概念不应在 Persona、Task、Context、Format 中重复出现

### 知识库文件处理策略

当用户提供知识库文件用于 GEM 参考时：

1. **概括而非引用**：Instructions 中应概括文档的核心原则，而非逐条复制内容
2. **明确加载指令**：如果 GEM 需要在运行时参考文档，在 Task 中明确写出 "Reference [filename]" 或 "Load [filename]"
3. **分离关注点**：
   - Instructions = 工作流程 + 核心约束（精简）
   - Knowledge = 详细规则 + 参考数据（完整）
4. **文件名一致性**：使用用户提供的原始文件名
=======
>>>>>>> e66b05a560ece06ac738113d23305c30f0cd2211

### 文件引用处理

如果用户提到了需要引用的文件（如"参考 XXX 文档"），必须：

1. 在 Knowledge 部分提醒用户上传该文件
2. 在 Instructions 中使用用户提供的**原始文件名**进行引用
3. 使用正确的引用语法建议：
   - Google Doc: 使用 @doc 文件名
   - 上传文件: 在指令中明确提及文件名

## 质量检查清单

生成 Instructions 前，确保覆盖：

- [ ] 角色定位清晰
- [ ] 核心任务明确
- [ ] 边界和约束已定义（有 "Never" 或 "Do not" 语句）
<<<<<<< HEAD
- [ ] 输出格式有具体要求（包含从用户需求/知识库中提取的格式约束）
- [ ] 文件引用使用正确的文件名
- [ ] **无重复内容**：同一概念不在 Persona/Task/Context/Format 中重复出现
- [ ] **无冗余步骤**：每个 Step 都有独立价值，不与其他步骤重叠
- [ ] **精简度**：Instructions 总长度适中（建议 200-400 词），知识库承载详细内容
=======
- [ ] 输出格式有具体要求
- [ ] 文件引用使用正确的文件名
- [ ] 指令长度适中，没有冗余内容
>>>>>>> e66b05a560ece06ac738113d23305c30f0cd2211

## 参考资源

当需要更深入了解 GEM 最佳实践时，阅读知识库文件：

- `references/gem_best_practices.md` - GEM 最佳实践完整指南，包含示例模板和高级工作流
