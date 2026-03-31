# Midjourney 提示词构造完整指南

Last_Updated: 2026-03-06

---

## Overview

本指南提供 Midjourney 提示词构造的系统性规范与实战技巧，涵盖从基础语法到高级控制的完整工作流。

### 适用范围

适用于使用 Midjourney 进行静态图像生成的所有场景，包括文生图、图生图、风格迁移、角色与物体一致性保持。
---

## Core Concepts

### Token

提示词被模型解析后的最小语义单元。Midjourney 高度依赖自然语言的句法结构与明确的语义指向，而非离散的关键词堆砌。

### Prompt Adherence（提示词依从性）

模型准确理解并呈现提示词中所有细节与指令的能力。现代版本在此方面具有显著提升。

### Compositional Subject（构图主体）

画面中占据核心视觉焦点的人、动物或主要物体。背景元素与附属道具不计入构图主体。

### Environmental Archetypes（环境原型）

模型潜空间中预训练的场景概念集合（如"垃圾场"、"维多利亚时代小巷"），调用原型可自动补全符合该场景的默认细节，无需冗余描述。

### Semantic Understanding（语义理解）

模型对参考图像的认知方式。模型不仅复制像素，更能识别图像的本质概念，并倾向于将其还原为最常见的原型状态。

### The Cowbell Method（牛铃法则/冗余强调法）

通过在提示词中多次使用同义词或重组短语来增加特定细节的注意力权重，强制模型渲染易丢失元素的技巧。

### Slope of Influence（影响斜率）

提示词中词汇位置对生成结果的影响梯度。位于提示词前端的词汇拥有更高的注意力权重，决定画面的核心焦点。

### Semantic Anchoring（语义锚定）

通过叠加具体名词、介词短语与关联动作，强制模型将注意力集中在特定视觉元素上的技术手段。

### Archetype（视觉原型）

模型预训练数据中对某一概念的最普遍形态认知。触发原型可节省算力，但打破原型需投入大量描述权重。

---

## Consolidated Principles

### 原则 1: 构图主体数量限制（Subject Count Limit = 4）

Midjourney 在单次生成中最多能稳定处理 4 个独立的构图主体。

- 构图主体指画面中的核心人物、动物或主要视觉对象
- 背景元素（如树木、建筑）与附属道具（如手中的剑、桌上的杯子）不计入此限制
- 当需求超过 4 个主体时，必须使用"多主体压缩"技术，否则会导致特征融合、肢体崩坏或主体丢失

### 原则 2: 禁用否定句式（No Negation）

严禁在文本提示词中使用否定词汇，如"no"、"not"、"without"、"never"、"nothing"。

- 模型在处理否定词时，往往会因为注意力机制的特性，反而将该元素引入画面
- 替代方案：将否定需求重构为正向的视觉线索
  - 将"没有胡子（no beard）"替换为"光洁的下巴（clean-shaven）"
  - 将"没有标志（no logo）"替换为"纯色（plain）"或"无标记（unmarked）"
- 若必须排除特定元素，可使用 `--no` 参数（如 `--no logo`），而非在正文中使用否定句

### 原则 3: 禁用祈使句与指令（No Imperatives）

严禁使用命令式动词，如"画（draw）"、"添加（add）"、"制作（make）"、"生成（generate）"。

- Midjourney 的标准提示词模式并非对话式大语言模型（LLM），它无法理解执行动作的指令，只能解析视觉描述
- 替代方案：直接描述最终画面的客观状态
  - 将"画一个站在山上的男人"替换为"一个男人站在山上"

### 原则 4: 禁用用途说明（No Purpose Explanations）

严禁在提示词中解释图像的最终用途，如"用于标志设计（for a logo）"、"用于我的应用（for my app）"、"作为壁纸（as a wallpaper）"。

- 这些词汇会引入与视觉无关的噪声，稀释有效 Token 的权重
- 替代方案：将用途转化为具体的风格描述词
  - 将"用于标志设计"替换为"矢量图标（vector icon）"、"极简图形（minimalist graphic）"

### 原则 5: 禁用尺寸与排版描述（No Dimensions or Layout）

严禁使用自然语言描述画面的物理尺寸或排版方向，如"方形布局（square layout）"、"垂直图像（vertical image）"、"宽屏（widescreen）"。

- 替代方案：使用宽高比参数控制画布尺寸

### 原则 6: 禁用抽象与概念性语言（No Abstract or Conceptual Language）

严禁使用无法直接转化为视觉像素的抽象形容词，如"神秘的（mysterious）"、"标志性的（iconic）"、"美丽的（beautiful）"、"令人惊叹的（stunning）"。

- 抽象词汇会导致模型调用不可控的随机视觉元素来填补语义空白，降低提示词依从性
- 替代方案：将抽象概念拆解为具体的视觉特征
  - 将"神秘的森林"替换为"被浓雾笼罩的森林，光线昏暗，树木扭曲"

### 原则 7: 禁用隐喻与叙事性语言（No Metaphors or Narrative Language）

严禁使用文学性的比喻或长篇故事叙述，如"被遗忘时代的遗物（a relic of a forgotten time）"、"沐浴在过去的遗憾中（bathed in the regret of his past）"。

- Midjourney 捕捉的是一个"冻结的瞬间（frozen moment）"，而非一段剧情或时间线
- 替代方案：使用密集的视觉描述语言
  - 将"沐浴在过去的遗憾中"替换为"低着头，双手捂住脸，处于阴影中"

### 原则 8: 简短、简单、直接与禁用词组列表（Short, Simple, Direct & No Phrase Lists）

提示词必须由结构完整的简单句组成。每个句子只描述一个图像动作或特征。

- 严禁使用冗长的连词句（run-on sentences）
- 严禁使用逗号分隔的视觉标签链（Phrase Lists），如"发光的光线，破损的墙壁，赛博朋克（glowing light, broken wall, cyberpunk）"。这种"关键词汤"会导致画布失控
- 替代方案：将标签链重构为包含主谓宾的完整句子
  - 将"赛博朋克风格的破损墙壁上散发着发光的光线"

### 原则 9: 环境原型隐含细节（Environmental Archetypes Imply Details）

避免重复描述环境原型中已经隐含的默认细节。

- Midjourney 模型拥有强大的"原型"认知能力。例如，当提示词包含"在垃圾场（in a junkyard）"时，模型会自动渲染垃圾、生锈的金属、破败的背景等元素
- 冗余描述会浪费 GPU 处理时间，并可能导致画面过度拥挤
- 仅当需要打破原型默认设定时，才需进行额外描述（如"在垃圾场，有一架崭新的白色钢琴"）

### 原则 10: 移除相机与元数据术语（Remove Camera & Metadata Terms）

严禁使用技术性的相机参数或文件元数据，如"ISO 100"、"50mm 镜头（50mm lens）"、"f/2.8"、"HDR"、"16K"、"8-bit per channel RGBA"、"WebP/AVIF"。

- 这些术语在训练数据中与实际视觉效果的关联性极低，作为噪声存在，会消耗算力并导致生成失败或不可控
- 替代方案：使用风格化的摄影术语
  - 使用"宝丽来风格（Polaroid）"、"电影级静态镜头（cinematic still-shot）"、"浅景深（shallow depth of field）"来替代具体的数字参数

### 原则 11: 重构标志性视觉品牌（Recast Iconic Visual Brands）

允许使用具有明确、统一视觉特征的品牌或艺术家名称作为风格修饰（如"吉卜力风格（Ghibli style）"）。

- 严禁将品牌名称作为抽象的质量或风格代名词（如使用"苹果公司风格"来表达极简主义）
- 替代方案：必须将抽象的品牌名称重构为具体的视觉特征描述
  - 将"苹果风格"替换为"极简主义，白色背景，光滑的金属表面，干净的线条"

### 原则 12: 禁用保真度与真实感语言（No Fidelity or Realism Language）

严禁使用强调画质的冗余词汇，如"逼真的（realistic）"、"超写实的（hyperrealistic）"、"超详细的（ultra-detailed）"、"高品质（high-quality）"、"4K/8K"。

- 这些词汇不仅无效，还会干扰模型对核心主体的注意力分配
- 替代方案：使用明确的媒介描述词
  - 使用"照片风格（photo style）"、"摄影作品（photograph）"或具体的视觉特征（如"皮肤纹理可见"）来替代"逼真"

### 原则 13: 消除"或"短语（Eliminate 'Or' Phrases）

严禁在提示词中使用选择性连词"或（or）"，如"红裙子或蓝裙子（red dress or blue dress）"。

- 模型无法在单次生成中执行逻辑选择，这会导致特征混合（生成紫裙子）或随机忽略其中一项
- 替代方案：做出明确决定，只选择其中一项；或者将需求拆分为两个独立的提示词分别运行

### 原则 14: 多主体压缩技术（Multi-Subject Compression）

当画面必须包含超过 4 个构图主体时，强制使用"多主体压缩"工作流，分为三个步骤：

1. **定义群体原型（Group Archetype）**：使用集合名词将多个主体打包为一个单一的逻辑主体。例如："三个角色走过城市（Three characters walk through a city）"
2. **词汇锚定（Lexical Anchoring）**：通过空间位置介词为群体中的个体分配特征。例如："左边的人穿红衣……中间的人戴帽子……右边的人拿伞……"
3. **逻辑降维**：经过压缩后，该群体在模型解析中仅占用 1 个主体名额。附属道具（如伞、帽子）不计入主体数量

### 原则 15: 仅使用有效参数（Valid Parameters Only）

提示词后缀必须且只能使用官方支持的有效参数。

- 严禁编造或使用已废弃的参数。如果参数不在官方列表中，模型将报错或产生不可预知的行为

---

## Mechanisms & Logic

### 构图与空间关系控制（Composition Control）

#### 空间介词定位法

在 Midjourney 中，必须使用明确的空间介词来定义物体间的相对位置。

有效介词包括：
- 基础方位：Left（左侧）、Right（右侧）、Center（中心）、Middle（中间）
- 深度层次：Foreground（前景）、Background（背景）
- 垂直关系：Above（上方）、Below（下方）、Beneath（下方）、Underneath（底下）
- 相邻关系：Adjacent（相邻）、Parallel（平行）、Perpendicular（垂直）、Beside（旁边）、Between（之间）、Behind（背后）、In front of（前方）
- 空间范围：Within（之内）、Containing（包含）、Around（周围）、Over（上方）、Through（穿过）、Along（沿着）、Near（附近）、Against（靠着）、Outside（外部）、Inside（内部）、Beyond（远处）、Across（横跨）

示例："一只鸭子在前景，背景是一片花田（A duck in the foreground, a field of flowers in the background）"

#### 影响斜率（Slope of Influence）与焦点控制

提示词中越靠前的词汇，越容易成为画面的视觉焦点。

- 若提示词为"田野里的鸭子带着一篮花"，鸭子将占据焦点
- 若提示词为"一篮花在田野里，旁边有一只鸭子"，花篮将占据焦点

策略：若需将某主体推至画面边缘，应在提示词开头先描述其他中心物体或环境（如"一个巨大的水晶球在王座室中央发光，红国王在旁边踱步"）

#### 语法影响构图

通过调整主语和环境的语序，可以控制画面焦点：

- "喷泉上的美人鱼雕像" → 焦点在喷泉
- "美人鱼雕像立于喷泉之上" → 焦点在美人鱼

通过使用原型动词（如"growing"）可以改变模型对物体关系的理解：

- "盘子上有森林状的西兰花" → 平面食物摆盘
- "盘子上生长着微型西兰花森林" → 三维立体景观

### 姿态与表情控制（Pose Control）

#### 专业肖像术语

使用摄影学标准术语来定义基础姿态：

- 侧面照（profile shot）
- 四分之三侧面照（three-quarter shot）
- 歪头姿势（head-tilt pose）
- 双手叉腰（hands-on-hips pose）
- 倾斜姿势（leaning pose）
- S型曲线姿势（S-curve pose）
- 双臂交叉（crossed-arms pose）
- 双手插兜（hands-in-pockets pose）
- 坐姿（sitting pose）
- 斜躺姿势（reclining pose）

#### 情绪与动作关联法

当标准术语失效时，必须同时结合以下两种描述：

1. 赋予模特与目标姿态高度相关的情绪、态度或活动（如：害羞的、困倦的、放松的、分心的、激烈的、愤怒的）
2. 添加面部细节的具象描述（如：明亮的眼睛、强烈的凝视、笔直的鼻子、皱眉、脸红、大笑、对称的脸）

示例："一个害羞的女孩，低着头，脸颊泛红，避开镜头（A bashful girl, looking down, blushing cheeks, avoiding the camera）"

### 全身肖像生成规范（Full-Body Character Portraits）

为确保角色从头到脚完整出现在画面中，必须严格执行以下检查清单：

1. **首词定义媒介**：提示词必须以艺术媒介或风格开头（如"插画（Illustration of...）"、"照片（Photograph of...）"）
2. **使用"全长"术语**：必须使用"全长（full-length）"来引入主体
   - 严禁使用"全身（Full Body）"（可能触发敏感词过滤）
   - 严禁使用"镜头（Shot）"（语义多重）
   - 严禁使用"肖像（Portrait）"（默认截断于腰部或肩部）
3. **两端锚定法（Top & Bottom Anchoring）**：必须同时描述角色的顶部（头部、头发、帽子）与底部（脚、爪子、鞋子）。只要描述了鞋子（如"跑鞋"、"光脚"），模型为了遵循提示词，就必须将脚部纳入画幅
4. **环境与地面互动**：必须描述角色脚下的地面（如"站在木地板上"、"走在泥地里"）或头顶的空间（如"头顶的蓝天"），以强制模型构建完整的垂直空间
5. **垂直宽高比**：必须使用足够高的宽高比（如 2:3 或 3:4）

示例：
```
Illustration of a full-length female elf with blue hair wandering in a sunny forest. Her bare feet walk on lush green moss. Above her head is a magical bluebird.
```

### 细节强调与弱化策略（Emphasis & De-Emphasis）

#### 注意力预算管理

模型的注意力是稀缺资源。如果某个细节反复丢失，必须删除提示词中其他不重要的竞争元素，为该细节腾出"注意力预算"。

#### 牛铃法则（冗余强调）

通过同义词堆叠或短语重组来强制模型关注。例如，若"一只睡觉的猫"生成了睁眼的猫，应修改为：

```
a cat sleeps lying down with his head down, closed eyes, napping, slumbering
```

#### 扩展画幅空间

细节丢失可能是因为画布空间不足。扩大宽高比（如从 1:1 改为 16:9）可为缺失细节提供渲染空间。

#### 弱化与消除（De-Emphasis）

若画面中出现了不需要的元素（如所有人都在戴帽子）：

- 对于主体身上的错误元素：描述与其物理位置互斥的替代元素。例如通过描述"detailed hair"消除帽子，通过描述"bare neck"消除项链
- 对于背景中的泛滥元素：使用 `--no` 参数（如 `--no hats`）

---

## Constraints

### 语法结构约束

- 必须使用具有标准语法结构的自然语言长句
- 禁用逗号分隔的关键词列表
- 每个句子只描述一个图像动作或特征
- 禁用冗长的连词句

### 词汇选择约束

- 禁用否定词汇（no, not, without, never, nothing）
- 禁用祈使动词（draw, add, make, generate）
- 禁用抽象形容词（mysterious, iconic, beautiful, stunning）
- 禁用隐喻与叙事性语言
- 禁用技术术语与元数据（HDR, 16K, ISO 100, 50mm lens）
- 禁用保真度修饰词（realistic, hyperrealistic, ultra-detailed, 4K/8K）
- 禁用"或"逻辑分支

### 风格与媒介约束

- 必须以艺术媒介或风格开头（Illustration, Photograph, Painting 等）
- 将抽象品牌名重构为具象风格特征描述
- 使用风格化摄影术语替代具体数字参数

---

## Output Format / Style Hints

### 提示词结构模板

```
[媒介/风格] + [主体描述] + [环境/背景] + [细节补充]
```

#### 标准句式结构

1. **以媒介开头**：Illustration of... / Photograph of... / Painting of...
2. **定义主体**：a full-length [角色] with [特征]
3. **描述动作/状态**：walking in... / standing on... / sitting at...
4. **添加环境**：in a [环境原型] / surrounded by...
5. **补充细节**：wearing... / holding... / with...

### 词汇选择模式

#### 具体替代抽象

| 抽象概念 | 具体视觉特征 |
|---------|-------------|
| mysterious forest | fog-covered forest with twisted trees and dim lighting |
| beautiful sunset | golden-orange sky with scattered clouds reflecting on calm water |
| iconic building | tall structure with distinctive spires and ornate architectural details |
| stunning portrait | sharp facial features with dramatic side lighting and visible skin texture |

#### 情绪-姿态关联词

| 目标姿态 | 关联情绪词 | 面部细节 |
|---------|-----------|---------|
| 低头/避开视线 | bashful, shy, embarrassed, awkward | looking down, averted gaze, blushing cheeks |
| 放松/慵懒 | sleepy, relaxed, distracted | soft eyes, gentle expression, loose posture |
| 直视/强烈 | intense, fierce, angry | bright eyes, intense gaze, furrowed brows |

### 空间描述模式

#### 焦点控制句式

- **主体为焦点**：A [主体] in [环境] with [附属物]
- **环境为焦点**：A [环境] with [主体] in the distance
- **推至边缘**：A massive [环境物体] dominates the center while [主体] stands at the side

#### 多主体定位句式

```
A group of [数量] [群体原型] [动作] in [环境].
The one on the left [特征A].
The figure in the center [特征B].
The one on the right [特征C].
```

### 全身肖像句式模板

```
[媒介] of a full-length [角色] with [顶部特征], [动作] in [环境].
[角色] wears [鞋履] on [地面类型].
Above [角色] is [顶部空间元素].
```

### 细节强调句式

#### 同义词堆叠

```
a sleeping cat lies down with head down, closed eyes, napping, slumbering, snoozing
```

#### 短语重组

```
a green hat on his head, a hat worn on his head, head topped with a green hat
```

### 风格描述替代方案

| 禁用术语 | 替代描述 |
|---------|---------|
| realistic / hyperrealistic | photo style, photograph, photorealistic style |
| 4K / 8K / 16K | high detail, crisp details, sharp focus |
| cinematic lighting | dramatic lighting, chiaroscuro, golden hour lighting |
| HDR | high contrast, vivid colors, dynamic range |
| masterpiece | museum quality, gallery style, professionally composed |

---

*本指南基于 Midjourney 官方文档与社区最佳实践整理，持续更新中。*
