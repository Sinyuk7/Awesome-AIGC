# Midjourney 提示词构造禁忌指南
Last_Updated: 2026-03-06

## Overview

- **Purpose**: 本文档汇总 Midjourney 提示词构造中所有已知的禁忌、错误模式与无效写法，供提示词编写者用于校验与规避

## Core Concepts

- **注意力预算（Attention Budget）**: 模型处理提示词时的算力资源是有限的；提示词中描述的内容越多，每个元素分配到的注意力就越少，超出阈值后细节开始丢失
- **语义原型（Archetype）**: 模型预训练中对某一概念最普遍形态的认知；调用环境原型（如"垃圾场"）会自动填充该场景的默认细节，重复描述这些隐含细节属于无效浪费
- **影响斜率（Slope of Influence）**: 提示词中词汇越靠前，对画面焦点与渲染优先级的影响越大；顺序错误会导致焦点偏移
- **逻辑冻结帧（Frozen Moment）**: Midjourney 捕捉的是单一静态瞬间，而非叙事、情节或时间线；超出单帧范畴的语言对模型无效
- **关键词汤（Keyword Soup）**: 逗号分隔的标签列表式写法；在当前版本中会导致画布失控，属于已过时的提示词策略

## Consolidated Principles

- P1 [Critical]: 禁止使用否定词（no、not、without、never、nothing）——模型注意力机制会因否定词反而强化该元素的渲染概率
- P2 [Critical]: 禁止使用关键词汤（逗号分隔的标签列表）——此为旧版本写法，当前版本中会导致构图失控，必须重构为包含主谓宾的完整简单句
- P3 [Critical]: 禁止使用祈使句与系统指令（draw、add、make、generate）——Midjourney 不是指令执行型 LLM，标准提示词模式不解析命令，只解析视觉描述
- P4 [High]: 禁止使用抽象与概念性语言（mysterious、iconic、beautiful、stunning）——抽象词汇触发不可控的随机视觉填充，降低提示词依从性
- P5 [High]: 禁止使用文学隐喻与叙事性语言——Midjourney 捕捉冻结瞬间，不处理故事情节、时间轴或文学比喻
- P6 [High]: 禁止使用技术性相机元数据（ISO、mm 镜头、f/2.8、HDR、4K/8K/16K）——这些术语在训练数据中与视觉效果关联性极低，作为噪声消耗算力
- P7 [High]: 禁止使用保真度与真实感修饰词（realistic、hyperrealistic、ultra-detailed、high-quality）——在当前版本中无效且干扰注意力分配
- P8 [Normal]: 禁止使用"或"逻辑分支（red dress or blue dress）——模型无法执行单次生成内的逻辑选择，结果为特征混合或随机忽略
- P9 [Normal]: 禁止使用用途说明（for a logo、for my app、as a wallpaper）——与视觉无关的词汇稀释有效 Token 权重
- P10 [Normal]: 禁止使用自然语言描述画布尺寸或排版方向（square layout、vertical image、widescreen）——尺寸控制只能通过参数实现

## Constraints

**C1: 词法禁忌——否定词**

- 禁止：`no`、`not`、`without`、`never`、`nothing` 及所有否定前缀表达
- 禁止写法示例：`no logo`、`without glasses`、`not wearing a hat`
- 机制：否定词触发模型对该元素的注意力，反而提升其出现概率
- 唯一例外：需排除元素时，只能通过参数处理，不属于提示词文本范畴

**C2: 词法禁忌——抽象形容词**

- 禁止：抽象的、无法直接映射为视觉像素的形容词
- 禁止词汇清单（典型示例）：
  - `mysterious`（神秘的）
  - `iconic`（标志性的）
  - `beautiful`（美丽的）
  - `stunning`（令人惊叹的）
  - `amazing`（惊人的）
  - `epic`（史诗般的）
  - `perfect`（完美的）
  - `wonderful`（精彩的）
  - `magical`（神奇的）——除非"magic"是场景中的物理可见元素
- 机制：抽象词汇无法被模型解析为具体像素，会触发不受控的随机视觉填充

**C3: 词法禁忌——保真度与画质修饰词**

- 禁止：所有强调画质或写实程度的冗余修饰词
- 禁止词汇清单：
  - `realistic`、`hyperrealistic`、`ultra-realistic`、`photorealistic`
  - `ultra-detailed`、`highly detailed`、`super detailed`
  - `high-quality`、`high resolution`、`best quality`
  - `masterpiece`
  - `4K`、`8K`、`16K`（作为质量标签时）
  - `trending on artstation`、`award-winning`
- 机制：这些词汇在当前版本中不产生有效的视觉指令，仅占用 Token 配额并干扰注意力分配

**C4: 词法禁忌——相机与技术元数据**

- 禁止：具体的相机技术参数和文件格式标签
- 禁止词汇清单：
  - `ISO 100`、`ISO 1600`（及所有 ISO 值）
  - `50mm lens`、`35mm`、`85mm`（及所有焦距）
  - `f/2.8`、`f/1.8`（及所有光圈值）
  - `EV 15`（及所有曝光值）
  - `HDR`
  - `8-bit per channel RGBA`
  - `WebP`、`AVIF`（文件格式标签）
  - `RAW`（相机格式）
- 例外：风格化的摄影术语允许保留（`Polaroid`、`cinematic still-shot`、`shallow depth of field`）

**C5: 词法禁忌——选择逻辑连词**

- 禁止：在单一提示词中使用逻辑选择连词 `or`（或）
- 禁止写法示例：
  - `red dress or blue dress`
  - `standing or sitting`
  - `a cat or a dog`
- 机制：模型无法在单次生成中执行分支选择，结果为特征随机混合或其中一项被忽略

**C6: 词法禁忌——用途与指向说明**

- 禁止：说明图像的最终用途或使用场景
- 禁止写法示例：
  - `for a logo`
  - `for my app`
  - `as a wallpaper`
  - `suitable for social media`
  - `for commercial use`
- 这些描述对模型的视觉生成无任何指导作用

**C7: 词法禁忌——叙事性与文学性语言**

- 禁止：文学比喻、故事情节描述、时间跨度语言
- 禁止写法示例：
  - `a relic of a forgotten time`（被遗忘时代的遗物）
  - `bathed in the regret of his past`（沐浴在过去的遗憾中）
  - `a symbol of hope in a world of despair`
  - `once a warrior, now broken`
  - `the last guardian of an ancient order`
- 机制：Midjourney 只渲染单帧冻结瞬间，无法解析情节或时间序列

**C8: 句法禁忌——关键词汤与标签列表**

- 禁止：用逗号分隔的离散关键词/标签列表作为提示词主体结构
- 禁止写法示例：
  - `cyberpunk city, neon lights, rain, dark alley, a man, glowing sword, mysterious, ultra-detailed`
  - `fantasy, dragon, fire, mountains, epic, dramatic lighting, 8k`
- 机制：此为旧版本遗留写法；在当前版本中，逗号列表导致模型失去对构图的控制，画布各区域随机争抢注意力
- 替代方向：所有描述必须重构为包含主谓宾关系的完整简单句

**C9: 句法禁忌——祈使句与系统指令**

- 禁止：以命令动词开头的指令性句式
- 禁止写法示例：
  - `Draw a man standing on a mountain`
  - `Add a red hat to the character`
  - `Make this look more cinematic`
  - `Generate an image of a forest`
  - `Create a portrait of a woman`
  - `Show me a dragon`
  - `Give the character blue eyes`
- 机制：标准提示词模式不是对话式语言模型，不解析执行指令，只解析客观视觉描述

**C10: 句法禁忌——长篇复合从句**

- 禁止：将多个视觉动作或特征堆砌在同一个长句中
- 禁止写法示例：
  - `A woman who is wearing a red dress and holding a basket of flowers while standing next to a tree that has a bird on it and a stream running by it in a forest that is full of golden light`
- 机制：长句结构导致模型在解析主从关系时发生注意力分散，核心元素渲染不稳定
- 原则：每个独立的视觉动作或特征对应一个独立的简短句子

**C11: 句法禁忌——自然语言描述画布尺寸**

- 禁止：在提示词正文中用文字描述画布的物理尺寸、方向或排版
- 禁止写法示例：
  - `square layout`
  - `vertical image`
  - `widescreen format`
  - `horizontal composition`
  - `portrait orientation`
- 机制：这些描述被模型解析为视觉内容描述，而非画布配置指令，会产生无法预期的渲染行为

**C12: 语法禁忌——模糊惯用语与拟人化短语**

- 禁止：使用英语惯用语、俚语或拟人化的抽象短语
- 禁止写法示例：
  - `inspired by a salamander`（若字面结果是不想要的 ——模型会取字面意义并过度渲染该元素）
  - `cradles a mug`（"cradle"是惯用语，模型可能字面解析为摇篮）
  - `a heart of gold`（隐喻，模型可能渲染出字面上的金色心脏）
- 机制：当惯用语的字面含义与意图含义不同时，模型倾向于字面解析，产生偏差

**C13: 语法禁忌——过度依赖自然语言否定来排除元素**

- 禁止：用正文描述来尝试排除不想要的元素（使用否定词）
- 禁止写法示例：
  - `The door should not be open`
  - `The man has no hat`
  - `A person without any accessories`
- 机制：否定句不可靠；`not` 及其同义词在扩散模型的注意力机制中往往被忽略，反而将注意力引至被否定的元素

**C14: 主体数量禁忌——超过 4 个独立构图主体**

- 禁止：在单一提示词中列举超过 4 个独立的构图主体（人物、动物、核心物体）而不进行压缩处理
- 构图主体的定义边界：
  - 计入主体数量：独立的人物、动物、占据画面焦点的主要物体
  - 不计入主体数量：背景元素（树木、建筑）、附属道具（角色手中的物品、桌上的杯子）
- 禁止写法示例：
  - `A dog, a cat, a bird, a mouse, and a rabbit are sitting on a sofa`（5 个主体，超出限制）
- 机制：模型在单次生成中稳定处理的构图主体上限为 4 个；超出后出现特征融合（"弗兰肯斯坦"现象）、肢体崩坏或主体丢失

**C15: 主体数量禁忌——多主体混合属性描述**

- 禁止：在描述多个主体时，将不同主体的属性混写在同一个长句中
- 禁止写法示例：
  - `A man in a red jacket and a dog with green fur standing next to each other`（属性边界模糊，易导致红色的狗或绿色的夹克）
- 机制：属性绑定错误（Cross-Subject Style Bleeding）会导致属性错误地附着到相邻主体上

**C16: 逻辑禁忌——在提示词正文中描述画布方向**

- 禁止：在正文文字中用于控制构图方向的描述性语言
- 禁止写法示例：
  - `The subject should be on the left side`（"should"是指令语气）
  - `Place the tree in the background`（"place"是祈使动词）
- 正确做法：使用空间介词直接描述位置关系（`A tree stands in the background`）

**C17: 结构禁忌——环境原型中重复隐含细节**

- 禁止：描述环境原型时，重复列举该原型已默认包含的细节
- 禁止写法示例：
  - `In a junkyard with rusty metal, broken car parts, and piles of garbage`（"in a junkyard"已隐含这些元素）
  - `A Victorian-era alley with cobblestone streets and gas lamps`（原型已包含这些细节）
- 机制：冗余描述浪费算力（注意力预算），可能导致画面过度拥挤或主体被次要细节稀释
- 例外：只有当需要**打破**原型默认设定时，才需额外描述（如"垃圾场里有一架崭新的白色钢琴"）

**C18: 结构禁忌——全身像中的错误术语**

- 禁止：在请求全身像时使用以下特定词汇
- 禁止词汇：
  - `Full Body`（全身）——可能触发内容审核过滤
  - `Shot`（镜头）——词义多重，语义不清
  - `Portrait`（肖像）——模型默认将肖像裁切至腰部或肩部

**C19: 结构禁忌——将指令写入视觉描述流**

- 禁止：将任何属于操作指令、对话或解释性语言的内容混入提示词的视觉描述中
- 禁止写法示例：
  - `Make this photograph into a painting`
  - `Include luxury details`
  - `The door should be open`
  - `I want this to look dramatic`
  - `Can you add some fog?`
- 机制：Midjourney 标准提示词模式不是对话式大语言模型，这类输入会作为视觉 Token 被解析，引入随机噪声

**C20: 结构禁忌——使用模糊品牌名替代具体风格描述**

- 禁止：将品牌名或公司名作为抽象风格代称（当其不具有明确统一的视觉特征时）
- 禁止写法示例：
  - `Apple-style design`（指极简主义时）
  - `Google aesthetic`
  - `Netflix vibe`
- 例外：具有明确且统一视觉特征的艺术 IP 允许保留（如 `Ghibli style`、`Pixar style`）
- 机制：模糊的品牌引用会触发随机联想，而非可控的视觉特征提取
