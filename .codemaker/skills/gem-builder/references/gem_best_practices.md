# GEM 最佳实践指南
Last_Updated: 2025-03-05

## Overview [Required]
- Purpose: 提供构建高效、可复用 GEM 的系统性方法论，帮助用户通过定制化指令优化 Gemini 的响应质量
- Scope: 
  - Covers: GEM 的核心概念、指令编写框架、文件管理策略、高级工作流、常见问题与解决方案
  - Does not cover: Gemini 底层模型技术细节、API 开发、第三方集成开发

## Core Concepts [Required]
- **GEM**: Gemini 的定制化版本，通过预设指令让 Gemini 针对特定任务或领域提供个性化响应
- **指令 (Instructions)**: 定义 GEM 行为、角色、输出格式的文本配置，相当于 GEM 的"系统提示词"
- **知识库 (Knowledge Base)**: 上传到 GEM 的参考文件，包括 PDF、Google Docs、Google Sheets 等，用于提供上下文
- **预设 GEM (Premade Gems)**: Google 提供的现成 GEM 模板，如 Brainstormer、Coding Partner、Writing Editor
- **对话上下文 (Conversation Context)**: GEM 在单次对话中保持的记忆，跨对话不保留
- **实时文档 (Live Documents)**: 连接到 Google Drive 的文档，修改后 GEM 自动获取最新内容
- **Deep Research**: Gemini 的深度研究功能，可用于生成 GEM 的知识基础

## Consolidated Principles [Required]
- P1 [Critical]: 指令完整性
  - GEM 的效果完全取决于指令的质量
  - 指令应覆盖 Persona、Task、Context、Format 四个维度
  - 缺失关键维度会导致响应不一致或偏离预期

- P2 [Critical]: 知识库与指令分离
  - 将静态知识放入文件上传，而非全部写入指令
  - 指令定义"如何做事"，知识库定义"做什么事"
  - 避免指令过长导致核心行为被稀释

- P3 [High]: 可复用性优先
  - 设计 GEM 时考虑重复使用的场景
  - 将通用配置提取到指令，特定输入留给对话
  - 为每个独立项目创建新的 GEM 对话实例

- P4 [High]: 渐进式迭代
  - 先用简单指令创建 GEM，测试后再逐步完善
  - 使用预览功能验证 GEM 行为
  - 保存前必须点击 Save，预览不会自动保存

- P5 [High]: 负面约束优先
  - 明确告知 GEM 不应该做什么
  - 定义边界比定义能力更重要
  - 示例: "Never discuss anything except for coding"

- P6 [Normal]: 实时文档优势利用
  - 优先使用 Google Docs/Sheets 而非上传静态文件
  - 实时文档更新后 GEM 自动同步
  - 适用于需要频繁更新的参考资料

- P7 [Normal]: 对话隔离
  - 每个 GEM 可创建多个独立对话
  - 不同项目使用不同对话避免上下文混淆
  - 对话历史不会跨 GEM 保留

## Mechanisms & Logic [Conditional]
- GEM 创建流程
  1. 访问 gemini.google.com
  2. 左侧点击 Explore Gems → New Gem
  3. 命名 GEM 并编写指令
  4. 右侧预览窗口测试
  5. 点击 Save 保存

- 指令优化流程
  1. 在指令框输入目标描述（1-2 句话）
  2. 点击 Use Gemini to re-write instructions
  3. 审核并编辑生成的指令
  4. 预览测试 → 保存

- 知识库构建工作流
  1. 使用 Deep Research 研究生成知识文档
  2. 导出研究结果为 Google Doc
  3. 将文档添加到 GEM 文件区域
  4. 在指令中引用知识库的使用方式

- GEM 调用工作流
  1. 打开已保存的 GEM
  2. 输入具体任务（无需重复背景信息）
  3. GEM 基于预设指令和知识库响应
  4. 如需切换任务，开启新对话

## Constraints [Conditional]
- 平台限制
  - 创建 GEM 需要 Google 账号且年满 13 岁
  - 部分功能在 Gemini 移动应用暂不可用
  - 免费用户 Deep Research 每月限 5 次

- 文件限制
  - 最多可上传 10 个文件到单个 GEM
  - 支持 PDF、Word、Google Doc、Drive 文件
  - Google Drive 文件需要开启 Keep Activity 并连接 Google Workspace

- 功能限制
  - GEM 暂不支持 Deep Research 模式
  - 上传的文件 GEM 可能无法直接引用（需正确提示）
  - 引用 Gmail 邮件需要使用 @doc 语法

- 指令约束
  - 指令长度无硬性限制，但过长会稀释重点
  - 避免在指令中嵌入敏感信息（人工审核可能查看）
  - 指令变更后需重新保存才能生效

## Derived Insights [Optional]
- GEM 本质上是用户的"系统提示词"代理
  - 相当于给 Gemini 一个固定的人格和知识背景
  - 减少重复输入，提高响应一致性
  - 特别适合需要特定格式输出的重复任务

- 最佳 GEM 往往由 GEM 生成
  - 使用"GEM 制造 GEM"的工作流可获得更专业的指令
  - 先用 Deep Research 生成知识库，再让 GEM 基于知识库构建专业 GEM
  - 迭代优化比一次性完美设计更有效

- 知识库 > 长指令
  - 将详细内容放入文件，指令只定义框架
  - 实时文档让 GEM 具备"活知识"能力
  - 适用于策略文档、风格指南、参考资料等

- GEM 与 NotebookLM 的差异化定位
  - GEM: 交互式、可重复、定制化响应
  - NotebookLM: 深度分析、研究、内容生成
  - 两者可配合使用：NotebookLM 生成知识库，GEM 提供交互界面

## Output Format / Style Hints [Optional]
- 指令编写格式建议
  - 使用清晰的标题分隔不同模块（Persona/Task/Context/Format）
  - 使用项目符号列出具体要求
  - 使用加粗标记关键术语
  - 示例:
    ```
    Persona: You are a professional code reviewer
    Task: Review code diffs and provide structured feedback
    Context: Focus on major concerns, note nitpicks separately
    Format: Categorized feedback with severity levels
    ```

- 响应格式控制技巧
  - 在 Format 部分明确指定输出结构
  - 要求编号列表便于引用
  - 要求分类输出便于阅读
  - 指定语气、详细程度、专业水平

- 文件引用语法
  - Google Doc: 使用 @doc 标题 引用
  - 上传文件: 在对话中明确提及文件名
  - 实时文档: 无需特殊语法，GEM 自动访问

## Cross-Document References [Optional]
- See: [Gemini Apps Privacy Hub](https://support.google.com/gemini/answer/13594961)
- See: [Gemini Advanced Features](https://gemini.google.com/advanced)

# Appendix

## Assumptions [Conditional]
- A1: 用户具备基本的 Gemini 使用经验
- A2: 用户拥有 Google 账号并可以访问 Gemini
- A3: 用户理解提示工程的基本概念
- A4: 用户有明确的重复任务场景需要使用 GEM

## GEM 类型示例库

### Brainstormer GEM 模板
- Persona
  - Your purpose is to inspire and spark creativity
  - Help brainstorm ideas for gifts, party themes, story ideas, weekend activities
- Task
  - Act like a personal idea generation tool
  - Come up with relevant, original, out-of-the-box ideas
  - Collaborate and look for input to make ideas more relevant
- Context
  - Ask questions to find new inspiration
  - Use energetic, enthusiastic tone and easy vocabulary
  - Keep context across entire conversation
  - If greeted, briefly explain purpose with short examples
- Format
  - Clarify request first: Ask pointed questions about interests, needs, themes, location
  - Offer at least 3 numbered ideas tailored to request
  - Share in easy-to-read format with short introduction
  - For location ideas: Ask geographic area if unclear
  - For traveling: Ask preferred transportation, default to fastest for long distances
  - Check if more details needed
  - If idea picked: Dive deeper with concise details

### Coding Partner GEM 模板
- Persona
  - Purpose: Help with writing, fixing, and understanding code
  - Assist in crafting code needed to succeed
- Task
  - Code creation: Write complete code when possible
  - Education: Teach steps involved in development
  - Clear instructions: Explain implementation in easy way
  - Thorough documentation: Document each step/part
- Context
  - Maintain positive, patient, supportive tone
  - Use clear, simple language, assume basic code understanding
  - Never discuss non-coding topics
  - Keep context across conversation
  - If greeted, briefly explain purpose with examples
- Format
  - Gather info: Ask clarifying questions about purpose, usage, details
  - Show overview: Clear summary of what code does, development steps, assumptions
  - Show code: Easy to copy-paste, explain reasoning and adjustable variables
  - Implementation: Clear instructions on how to implement

### Writing Editor GEM 模板
- Persona
  - Assist in editing writing
  - Provide thorough line-by-line edits and feedback
  - Cover grammar, spelling, tense, dialect, style, structure
- Task
  - Accept text via copy-paste or upload (PDF, Word, Google Doc, Drive)
  - Edit various writing types (essays, fiction, letters)
  - Give specific line-by-line edits with reasoning
  - Provide comprehensive feedback and general guidance
  - Offer structural suggestions and formatting advice
- Context
  - Assume moderate (high-school) writing ability
  - Maintain positive tone with constructive criticism
  - Use clear bullet points for spelling/grammar edits
  - Explain reasoning behind each suggestion
  - Keep context across conversation
  - If greeted, briefly explain purpose with examples
- Format
  - Ask about goals and feedback type needed
  - Provide overview of editorial guidance based on goals
  - Categorized feedback structure:
    - Overall Feedback: Main themes, general guidance
    - Spelling Edits: Itemized errors with explanations
    - Grammar Edits: Itemized errors with explanations
    - Structural Suggestions: Changes with reasoning
    - Opportunities for Improvement: Additional enhancement areas
    - Formatting Guidance: Correct formatting for writing type
  - Check if further assistance needed
  - Offer to rewrite with all suggested changes

## 高级工作流详解

### 工作流 1: Deep Research → GEM 制造 GEM
- 适用场景
  - 需要专业领域 GEM
  - 希望 GEM 具备深度知识
  - 追求高质量、专业化输出
- 步骤
  1. 向 Gemini 请求 Deep Research，研究生成 GEM 指令的最佳实践
  2. 收集至少 60+ 个 GEM 指令理念/术语/理论
  3. 导出研究结果为文档
  4. 重复步骤 1-2，研究生成提示工程的最佳实践
  5. 创建"GEM 制造 GEM"，导入两份研究文档作为知识库
  6. 使用该 GEM 创建特定领域的专业 GEM
- 优势
  - 基于系统性研究而非直觉
  - 可复用的 GEM 工厂
  - 持续迭代优化

### 工作流 2: 实时文档驱动 GEM
- 适用场景
  - 参考资料频繁更新
  - 多人协作场景
  - 需要保持信息同步
- 步骤
  1. 在 Google Drive 创建核心文档（策略、指南、模板）
  2. 创建 GEM 并添加实时文档到文件区域
  3. 在指令中定义如何使用这些文档
  4. 文档更新后 GEM 自动获取最新内容
- 示例场景
  - 简历优化 GEM: 连接简历文档 + 职位要求表格
  - 营销助手 GEM: 连接品牌指南 + 活动日历
  - 学习辅导 GEM: 连接课程大纲 + 参考资料

### 工作流 3: 提示优化 GEM
- 适用场景
  - 频繁需要优化提示词
  - 追求最佳 AI 输出效果
  - 需要标准化提示格式
- 配置
  - Persona: 提示工程专家
  - Task: 分析输入提示，应用最佳实践优化
  - Context: 掌握各类提示技术（CoT、Few-shot、Role-playing 等）
  - Format: 输出优化后的提示 + 优化说明
- 使用方式
  1. 向提示优化 GEM 输入原始提示
  2. 获取优化版本
  3. 在新对话中使用优化后的提示

## 常见问题与解决方案

### 问题 1: GEM 无法引用上传的文件
- 症状: GEM 回复说无法访问知识库文件
- 原因: 文件引用需要正确的提示语法
- 解决方案:
  - 使用 @doc 标题 语法引用 Google Doc
  - 在对话中明确提及文件名
  - 优先使用实时文档而非静态上传

### 问题 2: GEM 响应偏离预期
- 症状: 输出格式或内容与指令不符
- 原因: 指令不够具体或存在歧义
- 解决方案:
  - 使用 DO NOT 明确禁止的行为
  - 提供具体示例说明期望输出
  - 在 Format 部分详细定义结构

### 问题 3: 指令过长导致重点稀释
- 症状: GEM 忽略部分指令要求
- 原因: 指令信息过载
- 解决方案:
  - 将详细内容移入知识库文件
  - 指令只保留核心框架和行为定义
  - 使用分层结构组织指令

### 问题 4: 对话上下文丢失
- 症状: GEM 不记得之前的对话内容
- 原因: 开启了新对话或超出上下文窗口
- 解决方案:
  - 重要信息放入知识库而非依赖对话记忆
  - 使用 Google Doc 记录对话历史并附加到 GEM
  - 定期总结关键信息到指令中

### 问题 5: GEM 无法访问 Gmail
- 症状: 引用邮件时 GEM 无法找到内容
- 原因: 需要正确的引用语法和权限
- 解决方案:
  - 使用 @doc 邮件标题 语法
  - 确保 Gemini 有 Gmail 访问权限
  - 考虑将重要邮件导出为文档附加到 GEM

## 最佳实践检查清单

### 创建前
- [ ] 明确 GEM 的核心用途和目标用户
- [ ] 确定需要重复执行的具体任务
- [ ] 评估是否需要知识库支持
- [ ] 选择合适的创建方式（从零开始/复制预设）

### 指令编写
- [ ] 覆盖 Persona、Task、Context、Format 四个维度
- [ ] 使用 DO NOT 定义边界
- [ ] 提供具体示例
- [ ] 使用清晰的层级结构
- [ ] 长度适中，避免信息过载

### 知识库管理
- [ ] 优先使用 Google Drive 实时文档
- [ ] 文件命名清晰便于引用
- [ ] 定期更新保持信息时效性
- [ ] 控制文件数量（最多 10 个）

### 测试与迭代
- [ ] 使用预览功能测试多种场景
- [ ] 验证边界情况处理
- [ ] 收集实际使用反馈
- [ ] 定期优化指令

### 维护
- [ ] 监控知识库文档的更新
- [ ] 记录常见问题和解决方案
- [ ] 备份重要 GEM 的指令配置
- [ ] 评估是否需要拆分为多个专用 GEM
