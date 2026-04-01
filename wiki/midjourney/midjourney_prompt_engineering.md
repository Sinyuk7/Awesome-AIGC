# Midjourney 提示词工程完全指南

Last_Updated: 2025-03-05

## Overview [Required]

**Purpose**

- 提供 Midjourney V6/V6.1/V7 版本的系统化提示词构造规范与实战控制技巧
- 建立从自然语言意图到高保真视觉呈现的精准转化协议
- 消除语义稀释、构图偏移、特征丢失等常见渲染问题

**Scope**

- **Covers**: 提示词语法结构、空间构图控制、姿态引导、细节强调与弱化、全身肖像约束、Omni-Reference 语义迁移、参数调优策略
- **Does not cover**: Midjourney V5 及更早版本的关键词堆砌流派；视频动态生成任务；模型底层训练机制

## Core Concepts [Required]

**Token**

- 提示词被模型解析后的最小语义单元
- V6+ 模型按句法结构而非关键词密度处理 Token

**Semantic Anchoring (语义锚定)**

- 通过叠加具体名词、介词短语与关联动作，强制模型将注意力集中在特定视觉元素上的技术手段

**Cowbell Method (冗余注入法/牛铃法则)**

- 针对模型忽略特定细节的问题，在提示词中通过同义词、近义词或重复描述多次重申同一概念的强制强调策略

**The Footwear/Foot-where Rule (鞋履/立足点法则)**

- 通过明确描述角色的脚部穿搭（Footwear）与脚下接触的地面环境（Foot-where），强制模型拉远镜头以包含全身的渲染技术

**Slope of Influence (影响斜率)**

- 提示词中词汇位置对生成结果的影响梯度
- 位于提示词前端的词汇拥有更高的注意力权重，决定画面的核心焦点

**Prompt Adherence (提示词依从性)**

- 模型准确理解并呈现提示词中所有细节与指令的能力
- V7 版本在此方面具有显著提升

**Compositional Subject (构图主体)**

- 画面中占据核心视觉焦点的人、动物或主要物体
- 背景元素与附属道具不计入构图主体

**Archetype (视觉原型/语义原型)**

- 模型预训练数据中对某一概念的最普遍形态认知
- 触发原型可节省算力，但打破原型需投入大量描述权重
- 模型倾向于将参考物还原为最常见的原型状态

**Environmental Archetypes (环境原型)**

- 模型潜空间中预训练的场景概念集合（如"垃圾场"、"维多利亚时代小巷"）
- 调用原型可自动补全符合该场景的默认细节，无需冗余描述

**Multi-Subject Compression (多主体压缩)**

- 当画面需要超过 4 个主体时，通过定义"群体原型"（Group Archetype）并结合"词汇锚定"（Lexical Anchoring）来规避模型渲染混乱的技术

**Portrait Bias (肖像偏差)**

- 模型因训练数据分布导致的默认生成半身像或特写的倾向

**Style Bleeding (风格出血)**

- 媒介描述词意外影响整个画面风格的现象

**Semantic Dilution (语义稀释)**

- 过多细节描述导致镜头被迫拉近、宏观构图指令失效的现象

**Omni-Reference / --oref (全能参考)**

- V7 引入的基于语义理解的参考系统
- 模型通过识别参考图的深层概念（Archetype）而非纯像素进行特征迁移

**Omni-Weight / --ow (全能权重)**

- 控制 --oref 语义迁移强度的参数
- 取值范围 1-1000，默认 100
- 高值强化原型语义，低值允许跨原型重构

**Promptlet (提示词切片)**

- 在 V6.1 等版本中，使用多重提示语法（::）分割出的独立文本单元，可单独赋予正向或负向权重

**Stylize / --s (风格化参数)**

- 控制模型艺术美化干预程度的参数
- 取值范围 0-1000，默认 100
- 降低此值可提高 Prompt Adherence（提示词依从度）

## Consolidated Principles [Required]

**P1 [Critical]: 主体数量上限 = 4**

- V7 模型在单次生成中最多能稳定处理 4 个独立的构图主体
- 构图主体指画面中的核心人物、动物或主要视觉对象
- 背景元素与附属道具不计入此限制
- 超过 4 个主体时必须使用"多主体压缩"技术

**P2 [Critical]: 禁用否定句式**

- 严禁在文本提示词中使用否定词汇：no、not、without、never、nothing
- V7 模型在处理否定词时，往往会因为注意力机制的特性，反而将该元素引入画面
- 替代方案：将否定需求重构为正向的视觉线索
- 例如："no beard" → "clean-shaven"；"no logo" → "plain" 或 "unmarked"
- 若必须排除特定元素，使用独立的负面参数 `--no`（如 `--no logo`）

**P3 [Critical]: 禁用祈使句与指令**

- 严禁使用命令式动词：draw、add、make、generate
- Midjourney V7 的标准提示词模式并非对话式大语言模型（LLM）
- 它无法理解执行动作的指令，只能解析视觉描述
- 替代方案：直接描述最终画面的客观状态
- 例如："画一个站在山上的男人" → "一个男人站在山上"

**P4 [Critical]: 禁用抽象与概念性语言**

- 严禁使用无法直接转化为视觉像素的抽象形容词
- 禁用词：mysterious、iconic、beautiful、stunning、masterpiece、ultra-detailed
- 抽象词汇会导致模型调用不可控的随机视觉元素来填补语义空白
- 替代方案：将抽象概念拆解为具体的视觉特征
- 例如："神秘的森林" → "被浓雾笼罩的森林，光线昏暗，树木扭曲"

**P5 [Critical]: 禁用隐喻与叙事性语言**

- 严禁使用文学性的比喻或长篇故事叙述
- 禁用表达："a relic of a forgotten time"、"bathed in the regret of his past"
- Midjourney V7 捕捉的是一个"冻结的瞬间（frozen moment）"，而非一段剧情或时间线
- 替代方案：使用密集的视觉描述语言
- 例如："沐浴在过去的遗憾中" → "低着头，双手捂住脸，处于阴影中"

**P6 [High]: 自然语言优先，禁用关键词汤**

- V6/V7 架构已从"关键词汤"模式转向自然语言理解模式
- 禁止使用逗号分隔的关键词列表
- 禁用垃圾词：4k、8k、photorealistic、ultra-detailed、award-winning、HDR、ISO 100、50mm lens
- 这些词在 V6+ 模型中作为噪声稀释有效 Token 的权重
- 替代方案：将抽象质量要求转化为具体物理属性
- 例如："Cinematic lighting, realistic" → "Shot on 35mm film, f/1.8 aperture, depth of field"

**P7 [High]: 简短、简单、直接的句子结构**

- 提示词必须由结构完整的简单句组成
- 每个句子只描述一个图像动作或特征
- 严禁使用冗长的连词句（run-on sentences）
- 严禁使用逗号分隔的视觉标签链（Phrase Lists）
- 例如：禁用 "glowing light, broken wall, cyberpunk"
- 替代方案：将标签链重构为包含主谓宾的完整句子
- 例如："赛博朋克风格的破损墙壁上散发着发光的光线"

**P8 [High]: 三段式架构标准**

- 提示词必须遵循以下结构，顺序不可颠倒：
  - `[参考图像 URLs] + [文本描述核心] + [后缀参数]`
- 参考图像必须位于提示词最前端，作为像素级视觉锚点
- 参数必须位于提示词最后，用于调节生成器的数学约束

**P9 [High]: 文本描述的七层序列**

- 在文本描述模块内部，按以下顺序组织内容：
  1. **主体 (Subject)**：核心名词短语，使用具体实体名词
  2. **媒介 (Medium)**：艺术形式（Oil painting、Polaroid photo、3D render）
  3. **环境 (Environment)**：使用动态介词定义空间关系
  4. **光影 (Lighting)**：物理照明条件
  5. **色彩 (Color)**：调色板与色调映射
  6. **情绪/氛围 (Mood)**：情感基调
  7. **构图 (Composition)**：镜头角度与取景范围

**P10 [High]: 环境原型隐含细节，避免冗余**

- 避免重复描述环境原型中已经隐含的默认细节
- 例如："in a junkyard" 已自动包含垃圾、生锈金属等元素
- 冗余描述会浪费 GPU 处理时间，可能导致画面过度拥挤
- 仅当需要打破原型默认设定时，才需进行额外描述
- 例如："在垃圾场，有一架崭新的白色钢琴"

**P11 [High]: 序列决定焦点**

- 提示词文本序列中越靠前的实体名词，占据画面核心焦点（Focal Point）的概率越高
- 通过调整语序改变视觉中心
- 若需将某主体推至画面边缘，在提示词前端先描述其他中心物体或环境

**P12 [High]: 空间介词锚定**

- 使用明确的方位介词界定实体间的空间关系
- 有效介词：Left、Right、Center、Middle、Foreground、Background、Above、Below、Beneath、Adjacent、Parallel、Perpendicular、Behind、In front of、Beside、Between、Beyond、Underneath、Across、Within、Containing、Around、Over、Through、Along、Near、Against、Outside、Inside

**P13 [Normal]: 消除"或"短语**

- 严禁在提示词中使用选择性连词"或（or）"
- 模型无法在单次生成中执行逻辑选择
- 这会导致特征混合（生成紫裙子）或随机忽略其中一项
- 替代方案：做出明确决定，只选择其中一项；或者将需求拆分为两个独立的提示词分别运行

**P14 [Normal]: 仅使用有效参数**

- 提示词后缀必须且只能使用官方支持的有效参数
- 严禁编造或使用已废弃的参数
- V7 核心有效参数：--ar、--stylize/--s、--draft、--seed、--v 7、--oref、--ow、--no

## Mechanisms & Logic [Conditional]

**多主体压缩工作流**

- 当画面必须包含超过 4 个构图主体时，强制使用以下三个步骤：
  1. **定义群体原型（Group Archetype）**：使用集合名词将多个主体打包为一个单一的逻辑主体
     - 例如："Three characters walk through a city"
  2. **词汇锚定（Lexical Anchoring）**：通过空间位置介词为群体中的个体分配特征
     - 例如："The one on the left wears red... The center figure wears a hat..."
  3. **逻辑降维**：经过压缩后，该群体在模型解析中仅占用 1 个主体名额
     - 附属道具（如伞、帽子）不计入主体数量

**全身肖像强制渲染工作流**

- 为确保角色从头到脚完整出现在画面中，执行以下检查清单：
  1. **首词定义媒介**：提示词必须以艺术媒介或风格开头
     - 例如："Illustration of..."、"Photograph of..."
  2. **使用"全长"术语**：必须使用"full-length"来引入主体
     - 禁用："Full Body"（可能触发敏感词过滤）、"Shot"（语义多重）、"Portrait"（默认截断于腰部或肩部）
  3. **两端锚定法（Top & Bottom Anchoring）**：
     - 描述角色的顶部（头部、头发、帽子）
     - 描述角色的底部（脚、爪子、鞋子）
     - 只要描述了鞋子，模型为了遵循提示词，就必须将脚部纳入画幅
  4. **环境与地面互动**：
     - 描述角色脚下的地面（"stands on wooden floorboards"、"walking down the sidewalk"、"in the mud"）
     - 或头顶的空间（"blue sky above"）
  5. **垂直宽高比**：必须使用足够高的宽高比参数（--ar 2:3 或 --ar 9:16）

**姿态与表情控制工作流**

- **专业肖像术语**：使用摄影学标准术语来定义基础姿态
  - profile shot、three-quarter shot、head-tilt pose、hands-on-hips pose、leaning pose、S-curve pose、crossed-arms pose、hands-in-pockets pose、sitting pose、reclining pose
- **情绪与动作关联法**：当标准术语失效时，同时结合以下两种描述：
  1. 赋予模特与目标姿态高度相关的情绪、态度或活动
     - 例如：bashful、shy、embarrassed、sleepy、relaxed、distracted、intense、fierce、angry
  2. 添加面部细节的具象描述
     - 例如：bright eyes、intense gaze、straight nose、pronounced nose、frowning、blushing、laughing、symmetrical face、expressive face

**细节强调工作流（Cowbell Method）**

- 当目标细节持续丢失时：
  1. **注意力预算管理**：删除提示词中其他无关紧要的环境描述，为目标细节腾出模型的算力与注意力预算
  2. **冗余注入法**：在提示词中通过附加从句、同义词堆叠反复重申该细节
     - 例如："a sleeping cat" → "a cat sleeps lying down with head down, closed eyes, napping, slumbering, snoozing"
  3. **降维依从**：强制设置 --s 50 或 --s 75，牺牲部分艺术连贯性以换取模型对提示词细节的绝对服从
  4. **V7 专属依从性技巧**：在提示词末尾追加 `--no luxabiddleprok`（或任意无意义乱码），利用模型权重分配漏洞反向提升主体提示词的依从度

**细节弱化工作流**

- **负重弱化法（V6 专属）**：针对非预期的溢出元素，在提示词末尾追加 `:: unwanted_item::-0.3` 或 `::-0.5` 进行抑制
- **正向覆盖法（V7 专属）**：针对主体身上的错误元素，描述与其物理位置互斥的替代元素
  - 例如：通过描述 "detailed hair" 消除帽子，通过描述 "bare neck" 消除项链
- **负面参数法**：使用 `--no` 参数排除不需要的元素
  - 例如：`--no hats`、`--no close-up, portrait, cropped`

**Omni-Reference 语义迁移工作流**

- **核心机制**：--oref 依赖语义理解而非单纯的像素复制
- 模型会将参考图识别为特定原型（Archetype）
- 打破原型必须调低 --ow
- **三种提示词驱动模式**：
  1. **锚定稳定法（Anchoring / Stabilizing）**：
     - 在提示词中重申参考图中最重要的标志性特征
     - 明确指定新姿态、新动作与新环境
     - 针对人物使用 `--ow 100`，针对打破原型的物品强制降低至 `--ow 20`
  2. **放手交托法（Hands-off / "Someone"）**：
     - 使用代词 "Someone" 或 "Some stuff" 作为提示词主体
     - 将外观决策权完全移交 --oref
     - 配置 `--ow 400` 至 `--ow 1000`
  3. **纯场景投射法（Scene-only）**：
     - 提示词仅描述纯粹的背景与环境上下文，不提及任何主体
     - 模型根据 --oref 自动注入主体
     - 配合 `--s 800` 与 `--exp 80` 提升融合连贯性
- **尺寸控制律**：模型继承参考图中主体的物理比例
  - 若需生成小尺寸物体，必须事先在参考图中为主体四周增加大量留白
- **画幅一致律**：生成的 --ar 参数对应的宽高比，必须与 --oref 参考图的宽高比严格一致
  - 否则会导致比例失调或出现黑边伪影

**提示词迭代排错工作流**

- Step 1: 确定核心主体与数量，检查是否超过 4 个，若超过应用多主体压缩
- Step 2: 构建环境与背景，选择强有力的环境原型，依赖原型的默认细节
- Step 3: 定义风格与媒介，删除所有抽象的质量词汇
- Step 4: 应用高级控制（全身像、姿态、--oref 等）
- Step 5: 附加有效参数，确保所有参数均在 V7 官方支持列表中
- Step 6: 迭代与排错，针对丢失的细节应用牛铃法则，或删除其他竞争元素

## Constraints [Conditional]

**C1: 语法与词汇结构基准约束**

- 禁用逗号分隔的关键词列表，必须使用具有标准语法结构的自然语言长句描述视觉元素
- 禁用抽象概念与文学隐喻，将 "mysterious" 或 "a relic of a forgotten time" 等非视觉词汇转化为具体的物理形态、光影与材质描述
- 禁用技术术语与元数据，剔除 "HDR", "16K", "8-bit per channel RGBA", "ISO 100", "50mm lens"
- 风格术语如 "Polaroid" 或 "Cinematic still-shot" 予以保留
- 禁用模糊连词，剔除 "or" 及其同义表达
- 禁用否定前缀表达，剔除 "no", "not", "without", "never", "nothing"

**C2: 空间构图与焦点控制规则**

- 序列决定焦点：提示词文本序列中越靠前的实体名词，占据画面核心焦点的概率越高
- 空间介词锚定：使用明确的方位介词界定实体间的空间关系
- 焦点反制转移：当需要某主体偏离中心时，在提示词前端先描述一个环境道具

**C3: 角色姿态与表情强制约束规则**

- 摄影术语调用：直接使用人像摄影特定术语界定基础姿态
- 行为/情绪关联引导：赋予角色与期望姿态强相关的情绪或行为动作
- 面部微特征固化：通过极度具体的面部细节锁定头部形态，防止渲染崩坏

**C4: 注意力分配与细节强调/弱化规则**

- 注意力预算控制：当目标细节持续丢失时，必须删减提示词中其他无关紧要的环境描述
- 冗余注入法（强调）：在提示词中通过附加从句、同义词堆叠反复重申该细节
- 降维依从（强调）：强制设置 --s 50 或 --s 75
- 乱码降权法（强调/V7 专属）：在提示词末尾追加 `--no luxabiddleprok`
- 负重弱化法（弱化/V6 专属）：针对非预期的溢出元素，在提示词末尾追加 `:: hats::-0.3`
- 正向覆盖法（弱化）：针对主体身上的错误元素，描述与其物理位置互斥的替代元素

**C5: 全身肖像强制渲染规则（Full-Length Checklist）**

- 启动声明：提示词首句必须声明艺术媒介与 "full-length" 概念
- 顶部锚点：明确描述角色头部最顶端的可视特征（帽子、发型、耳朵）
- 底部锚点：明确描述角色的鞋履与足部细节
- 触地介质：明确描述足部接触的物理地面类型
- 比例支撑：强制使用适合容纳全身的宽高比参数，设置 --ar 2:3 或 --ar 9:16

**C6: Midjourney V7 核心约束十五法则**

- Rule 1: 构图主体数量上限设为 4 个
- Rule 2: 禁止使用否定词汇
- Rule 3: 禁止使用祈使句与系统指令（"draw", "add", "make"）
- Rule 4: 禁止描述用途解释（"for a logo"），转换为纯风格描述
- Rule 5: 禁止使用文本描述尺寸与布局，必须使用 --ar 参数
- Rule 6: 剔除抽象与概念性语言（"iconic", "beautiful"）
- Rule 7: 剔除故事叙述性语言，只描述被冻结的单帧视觉瞬间
- Rule 8: 保持单句简短直接，单一视觉动作或特征对应一个独立句子
- Rule 8b: 禁止并列短语列表（"glowing light, broken wall"）
- Rule 9: 依赖环境原型，剔除冗余隐含细节
- Rule 10: 移除所有相机元数据参数
- Rule 11: 将抽象品牌名重构为具象风格特征描述
- Rule 12: 移除保真度修饰词（"hyperrealistic", "ultra-detailed"），统一使用 "photo style"
- Rule 13: 消除 "or" 逻辑分支
- Rule 14: 多主体压缩协议，使用原型概括群组，再通过空间锚点分离个体特征
- Rule 15: 仅使用官方支持的尾缀参数

**C7: Omni-Reference (--oref) 语义迁移协议**

- 机制认知：--oref 并非像素级拷贝，而是语义级识别
- 方法一（参数锚定控制）：在提示词中重申参考图中最重要的标志性特征
- 方法二（语义托管）：使用代词 "Someone" 或 "Some stuff" 作为提示词主体
- 方法三（纯场景投射）：提示词仅描述纯粹的背景与环境上下文，不提及任何主体
- 尺寸控制律：模型继承参考图中主体的物理比例
- 画幅一致律：生成的 --ar 参数对应的宽高比，必须与 --oref 参考图的宽高比严格一致

## Derived Insights [Optional]

**Insight 1: 提示词不是标题，而是视觉指令集**

- 提示词的核心目标是向模型传达清晰的视觉信息，而非向人类读者解释画面
- 文学性的优美描述在 Midjourney 中往往适得其反
- 有效的提示词是"密集的视觉描述语言"，而非"诗意的叙事"

**Insight 2: 注意力是稀缺资源，需要预算管理**

- 模型的注意力机制类似于人类的认知资源，是有限的
- 每个提示词元素都在争夺模型的注意力预算
- 当细节丢失时，问题往往不是描述不够，而是竞争元素太多
- 解决方案：删减而非添加，聚焦而非扩散

**Insight 3: 原型是一把双刃剑**

- 原型（Archetype）是模型预训练中的概念归纳，可以节省描述成本
- 但原型也具有强大的"还原力"，会将非典型表现拉回常见形态
- 打破原型需要大幅降低 --ow 权重，并配合极其冗余的文本锚定
- 艺术创作往往发生在"打破原型"的过程中

**Insight 4: 版本演进意味着范式的根本转变**

- V5 时代的关键词堆砌（Keyword Soup）在 V6/V7 中已成为反模式
- 自然语言理解能力的提升，要求提示词从"标签集合"进化为"语义句子"
- 这一转变类似于从"搜索引擎关键词"到"对话式查询"的演进
- 适应新范式的用户将获得更高的生成质量和控制力

**Insight 5: 负面约束优先于正面指导**

- 在提示词工程中，明确"不要什么"比"要什么"更容易控制
- 模型的生成空间极其广阔，负面约束可以有效缩小搜索范围
- 例如：使用 `--no close-up, portrait, cropped` 比单纯描述 "full-length" 更有效防止截断

## Output Format / Style Hints [Optional]

**提示词构造模板**

```
[参考图像 URLs] [媒介] [主体描述] [环境/背景] [光影] [色彩] [情绪] [构图] [参数]
```

**标准示例**

```
A man stands in a dark cyberpunk alleyway holding a glowing sword. Neon lights reflect on the rainy street. Cinematic lighting. --ar 16:9 --v 7
```

**全身像示例**

```
Photograph of a full-length female elf with blue hair wandering in a sunny forest. Her bare feet walk on lush green moss. Above her head is a magical bluebird. --ar 2:3 --v 7
```

**Omni-Reference 示例**

```
A portrait in the style of Teen Magazine photography. Jo is a young woman with blue curly hair, pink sunglasses, and a colorful scarf around her neck. She stands on a sidewalk on a busy city street. --oref [URL] --ow 100 --v 7
```

**多主体压缩示例**

```
A group of five small animals sits on a sofa. On the left is a dog and a cat. In the center is a bird. On the right is a mouse and a rabbit. --ar 16:9 --v 7
```

## Cross-Document References [Optional]

- 无外部文档引用

# Appendix

## Conflict Register [Conditional]

**Conflict 1: V6 与 V7 的多重提示语法差异**

- **Position A (V6/V6.1)**：支持使用 `::` 进行语义切割与权重分配，支持负权重（`::-0.5`）
- **Position B (V7)**：不支持 `::` 权重语法，必须使用 `--no` 进行负面约束
- **Type**: Version
- **Affects**: 细节弱化策略的选择
- **Resolution Hint**: 根据使用的模型版本选择对应策略，V7 优先使用 `--no` 参数

**Conflict 2: 全身像描述中的语义稀释悖论**

- **Position A**：描述更多面部细节可以获得更好的表情表现
- **Position B**：过多的面部细节会导致镜头被迫拉近，全身像指令失效
- **Type**: Semantic
- **Affects**: 全身肖像生成
- **Resolution Hint**: 想要宏大构图时，克制对微小细节的描写，转而描写姿态、轮廓和环境

**Conflict 3: Omni-Reference 的原型还原 vs 创意重塑**

- **Position A**：高 --ow 权重（400-1000）可以最大程度保持参考图特征
- **Position B**：高 --ow 权重会强化原型束缚，使创意重塑（如将靴子变成帽子）变得困难
- **Type**: Semantic
- **Affects**: --oref 参数的使用
- **Resolution Hint**: 需要高度还原时使用高 --ow，需要创意变形时使用低 --ow（20-50）并配合冗余文本锚定

## Assumptions [Conditional]

**A1: 模型版本假设**

- 本指南主要针对 Midjourney V6.0、V6.1 和 V7.0 版本
- 部分策略（如 `--no luxabiddleprok` 技巧）仅适用于 V7
- 使用早期版本（V5.x 及以前）时，部分规则可能不适用或需要调整

**A2: 硬件与性能假设**

- 所有生成任务假设在标准 GPU 计算资源下运行
- 提示词长度和复杂度受限于单次任务的固定处理时间分配
- 过度复杂的提示词可能导致"运行 out of time"，造成细节丢失或渲染不完整

**A3: 用户能力假设**

- 用户具备基本的英语语言能力，能够理解并构造简单句
- 用户具备基础的视觉艺术概念（如构图、光影、色彩）
- 用户能够访问 Midjourney 的 Discord 或 Web 界面进行实际操作

**A4: 输出质量期望假设**

- 用户期望的生成结果具有较高的提示词依从性（Prompt Adherence）
- 用户愿意在"艺术美感"和"指令精确度"之间进行权衡
- 用户接受迭代优化作为标准工作流程的一部分

## Source Files Summary

**已处理的源文件列表**

1. Control Composition .txt - 构图控制方法（介词定位、序列焦点）
2. Control Poses.txt - 姿态控制技巧（摄影术语、情绪关联）
3. Create Emphasis & De-Emphasis.txt - 细节强调与弱化策略
4. Create Full-Body Character Portraits.txt - 全身肖像生成规范
5. Image Prompting Guide.txt - V6/V7 提示词编写指南
6. midjourney_advanced_prompting_guide.txt - 进阶提示词构造规范（中文）
7. midjourney_prompt_engineering.txt - 提示词工程完整规范（中文）
8. midjourney_v7_best_practices.txt - V7 最佳实践（中文）
9. Omni-Reference.txt - --oref 参数深度解析

**蒸馏统计**

- 原始文件数：9 个
- 原始总字数：约 35,000 字
- 蒸馏后字数：约 5,200 字
- 压缩率：约 85%

**内容覆盖范围**

- Midjourney V6/V6.1/V7 版本差异
- 提示词语法结构与词汇选择
- 空间构图与焦点控制
- 角色姿态与表情引导
- 细节强调与弱化技术
- 全身肖像生成工作流
- Omni-Reference 语义迁移
- 核心参数调优策略
- 常见问题排查与迭代优化