# z-image Prompt Engineering Knowledge

Last_Updated: 2025-03-05

---

## Overview [Required]

z-image (含 z-image-turbo) 是面向快速推理优化的文本到图像生成模型。其提示词工程的核心特征在于**无传统负面提示词支持**，所有控制必须通过正向提示词完成。

关键认知：z-image 的指令跟随能力较强，提示词中的约束性描述（如 "no text"、"fully clothed"）能够被模型理解并执行。这要求提示词工程师转变思维——从"正向描述+负面排除"的双轨模式，转向"全正向精细化描述"的单轨模式。

提示词长度建议控制在 **320-512 token** 范围内。作为参考，英文单词平均占用 1.3-1.5 token，中文汉字平均占用 1.8-2.2 token。换算为字数：英文约 210-400 词，中文约 150-280 字。此范围在细节丰富度与模型处理效率之间取得平衡。

## Core Concepts [Required]

### 正向约束语法

z-image 通过正向提示词中的约束性短语实现控制。有效模式包括：

- **排除性约束**：`no text`、`no watermark`、`no logos`、`no extra limbs`
- **否定性状态**：`without motion blur`、`not busy or cluttered`
- **明确边界**：`plain background`、`simple uncluttered background`

这些短语置于提示词后段效果较佳，模型对位置敏感。

### 提示词顺序效应

提示词中元素的排列顺序影响生成结果的权重分配。建议遵循从宏观到微观的自然视觉逻辑：

主体定义 → 外观细节 → 环境背景 → 光影氛围 → 风格媒介 → 质量约束

此顺序非强制结构，而是反映人类描述场景的直觉流程。关键原则：**先确立核心对象，再叠加修饰层**。

### 角色描述模式

z-image 对"角色+2-3个特征"的描述模式响应良好。示例：

`a software developer, adult woman, short dark hair, glasses, wearing a hoodie and jeans, focused expression`

相比单一标签（如"programmer"），此模式提供更强的可控性，减少模型对标签隐含属性的自动填充。

### 约束嵌入策略

将安全与质量约束嵌入提示词末段：

`safe for work, fully clothed, no revealing clothing, no suggestive poses, no logos or text`

多重重叠描述（clothed + modest + non-sexual）比单一约束更可靠。

## Consolidated Principles [Required]

### 原则一：具体优于抽象

模糊描述导致模型自由发挥。将"a beautiful woman"扩展为：

`an adult woman in her 30s, medium-length brown hair, friendly confident expression, natural makeup`

每个新增细节都压缩模型的不确定性空间。

### 原则二：服装显性化

为避免意外的身体暴露，服装描述应占据显著位置：

- 基础版：`wearing a dark business suit and shirt`
- 强化版：`fully clothed, modest professional outfit, arms and legs covered`
- 场景锚定：`office setting`、`street scene`、`classroom`

非性感场景上下文与服装描述形成双重约束。

### 原则三：光照词的画质杠杆

z-image 对光照关键词响应敏感，适当的光照描述可显著提升画面质感：

- `soft diffused daylight` — 自然柔和
- `cinematic warm key light` — 电影感
- `studio portrait lighting` — 专业人像
- `rim lighting` — 轮廓分离
- `noir high-contrast lighting` — 戏剧张力

光照描述兼具风格定义与质量提升的双重功能。

### 原则四：标签解构与重建

高负载标签（CEO、witch、rock star、fashion model）携带不可控的默认属性。解构策略：

1. **显式覆盖**：`four adult colleagues of diverse ethnicities and genders` 替代 "diverse team"
2. **中性替换**：`office worker`、`professional` 替代 "businessman"
3. **特征拆解**：用 2-3 个具体特征替代单一标签

### 原则五：约束的冗余设计

关键约束通过多短语重叠实现：

`no text, no watermark, no logos, no branding` — 而非仅 `no text`

`fully clothed, modest outfit, no revealing clothing` — 而非仅 `clothed`

冗余不是低效，而是对抗模型不确定性的缓冲机制。

### 原则六：末段约束集中

将排除性约束置于提示词末尾 20% 区域：

`...realistic photography, shallow depth of field. plain background, no logos, no text, no watermark, safe for work`

此位置约束的识别率较高。

## Mechanisms & Logic [Conditional]

### 文本编码器的约束理解

z-image 的文本编码器（基于多语言 T5 架构）对自然语言指令具有较强理解能力。关键机制：

**否定语义的编码**：短语 "no watermark" 在嵌入空间形成对 watermark 概念的抑制向量。这种抑制虽非传统负面提示词的显式减法，但在注意力机制中产生类似的衰减效应。

**位置权重衰减**：提示词前段 token 获得更高交叉注意力权重。因此核心主体应前置，约束性指令后置但仍需保持在有效感知窗口内（后 30% 区域仍有较好响应）。

### 指令跟随的边界

z-image 的指令跟随存在以下特征边界：

- **显式优于隐式**：直接声明 "wearing a red dress" 比 "in a striking outfit" 更可靠
- **肯定优于否定**："sharp focus" 比 "no blur" 更直接有效（尽管两者均可工作）
- **具体优于概括**："three people" 比 "a group" 更精确

### 上下文锚定效应

场景描述对人物渲染具有锚定作用：

`conference stage` 上下文提升正式着装概率
`beach at sunset` 上下文提升休闲/泳装概率（需额外约束对冲）

利用此效应：选择与非期望结果冲突的场景词，可减少约束短语的数量需求。

## Output Format / Style Hints [Conditional]

### 提示词的自然流动

提示词应呈现为一段连贯的视觉描述，而非机械的结构清单。避免将提示词写成公式化的字段填充。

**建议方式**：

`A medium-shot portrait of an adult woman in her 30s, natural look with medium-length brown hair, wearing a dark business suit and shirt, standing in a modern office with soft blurred background, soft diffused daylight illuminating her calm confident expression, realistic photography with shallow depth of field, plain background with no logos or text.`

**避免方式**：

`Subject: woman. Age: 30s. Hair: brown. Clothing: business suit. Background: office. Lighting: soft daylight.`

### 元素顺序的自然逻辑

虽然不强求固定结构，但以下顺序通常符合视觉描述的直觉：

1. **镜头与主体** — 建立画面框架和核心对象
2. **外观细节** — 填充主体的视觉特征
3. **环境与背景** — 建立空间上下文
4. **光照与氛围** — 定义情绪和时间感
5. **风格与媒介** — 指定渲染方式
6. **质量约束** — 收尾的排除性指令

此顺序可灵活调整，但建议保持"先确立主体，后叠加修饰"的基本原则。

### 语言选择

z-image 对英文提示词的优化程度较高。建议输出使用英文，即使原始构思为中文。

### Token 预算意识

撰写时保持对长度的感知：

- 简洁场景：约 250 token（英文 ~180 词）
- 标准描述：约 400 token（英文 ~300 词）
- 复杂场景：约 512 token（英文 ~380 词）

超过 512 token 时，考虑删减次要修饰词而非核心约束。