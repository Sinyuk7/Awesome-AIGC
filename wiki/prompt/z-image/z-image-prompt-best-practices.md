# Z-Image Prompt Construction: Best Practices Guide

Last_Updated: 2025-03-05

---

## Overview [Required]

- **Purpose**: 提供 Z-Image / Z-Image-Turbo 模型提示词构造的系统性最佳实践与优化策略
- **Scope**: 涵盖提示词结构设计、内容描述技巧、风格控制方法、参数优化建议 / 不包含 LoRA 训练、工作流参数配置、安全审核机制
- **Target Audience**: 希望充分发挥 Z-Image 模型生成能力的创作者、设计师和开发者

---

## Core Concepts [Required]

### S3-DiT Architecture

Z-Image 采用 **6B 参数的单流扩散 Transformer (S3-DiT)** 架构，文本 token 与图像 token 在同一序列中联合处理。这意味着模型对自然语言描述的理解能力远超传统标签式提示词模型。

**关键特性**：
- 文本与视觉信息深度融合
- 对详细描述式提示词响应更佳
- 支持中英文双语输入

### Few-Step Distillation

Z-Image-Turbo 是经过蒸馏优化的快速生成模型，约 **8 步实际扩散步骤**即可完成生成。这种设计使其在保持高质量的同时实现极速生成。

**对提示词的影响**：
- 提示词需更加明确具体，模型依赖描述而非多次迭代修正
- 详细的正向描述比模糊的精炼更有效

### Instruction Following

Z-Image 模型具有出色的指令遵循能力，能够理解和执行复杂的视觉描述指令。

**最佳利用方式**：
- 使用清晰的指令性语言
- 按优先级组织描述元素
- 明确指定需要呈现和避免的内容

---

## Consolidated Principles [Required]

### P1 [Critical]: 采用长而详细的自然语言描述

**核心原则**：Z-Image 对长而详细的提示词响应最佳，应避免极简或标签式提示词。

**推荐做法**：
- 使用 **80-250 词**的结构化描述
- 采用完整的句子而非碎片化标签
- 按逻辑顺序组织描述：构图 → 主体 → 服装 → 环境 → 光照 → 风格

**示例对比**：

| 不推荐 | 推荐 |
|--------|------|
| `1girl, long blue hair, red eyes, school uniform` | `A medium-shot portrait of a young woman with long flowing blue hair and striking red eyes, wearing a neatly pressed school uniform with a navy blazer and pleated skirt, standing in a sunlit classroom with large windows, soft morning light streaming in, modern anime style with clean linework and vibrant colors` |
| `cute anime girl` | `A cheerful anime-style character portrait of a young woman with shoulder-length pink hair styled in soft waves, large expressive amber eyes with a gentle smile, wearing a cozy oversized cream-colored sweater, sitting by a window with raindrops on the glass, warm indoor lighting creating a cozy atmosphere, detailed character design with soft shading` |

**提示词结构模板**：
```
[构图与镜头] + [主体描述] + [外貌特征] + [服装细节] + [环境背景] + [光照条件] + [情绪氛围] + [艺术风格] + [技术规格] + [约束条件]
```

（请同时参考 z-image-prompt-donot-guide.md 以规避相关禁止项）

### P2 [Critical]: 使用 Prompt Enhancer 优化提示词

**核心原则**：利用 LLM 增强提示词质量，将简短概念扩展为详细描述。

**工作流程**：
1. 先用自然语言简要描述想要的效果
2. 使用 Prompt Enhancer (PE) 模板扩展为详细提示词
3. 人工审查并调整结果，去除不必要的修饰
4. 添加具体的约束和限定条件

**PE 模板关键要素**：
- 将抽象概念转化为具体视觉元素
- 添加空间关系和构图信息
- 明确材质、纹理和光影描述
- 补充风格和艺术媒介信息

**示例转换**：

**原始概念**：`赛博朋克风格的城市夜景`

**增强后**：`A wide-angle night scene of a futuristic cyberpunk cityscape, towering neon-lit skyscrapers with holographic advertisements in Japanese and English characters, wet streets reflecting the vibrant pink and cyan lights, flying vehicles leaving light trails in the misty air, dense urban architecture with intricate details, cinematic atmosphere with dramatic lighting, highly detailed digital art style, 8K quality, sharp focus throughout`

（请同时参考 z-image-prompt-donot-guide.md 以规避相关禁止项）

### P3 [Critical]: 精确控制 Token 长度

**核心原则**：理解并管理提示词的 token 数量，确保完整描述被模型接收。

**Token 计算指南**：
- 约 **0.75 词/token** 的换算比例
- 默认最大长度：**512 tokens**
- 扩展长度：**1024 tokens**（需手动设置 `max_sequence_length=1024`）

**最佳实践**：
- 600-1000 词的提示词需要设置 1024 token 限制
- 使用 Qwen3-4B 的 tokenizer 精确计算 token 数量
- 将最重要的描述放在提示词前半部分

**代码示例**：
```python
image = pipe(
    prompt=prompt,
    height=1024,
    width=1024,
    num_inference_steps=9,
    guidance_scale=0.0,
    max_sequence_length=1024  # 扩展 token 限制
).images[0]
```

（请同时参考 z-image-prompt-donot-guide.md 以规避相关禁止项）

### P4 [High]: 优化采样步数与质量平衡

**核心原则**：在生成速度和图像质量之间找到最佳平衡点。

**推荐设置**：
- **8-12 步**：快速预览和概念探索
- **20-30 步**：质量与速度的最佳平衡
- **30+ 步**：追求最高质量时的选择

**步数选择策略**：

| 使用场景 | 推荐步数 | 预期效果 |
|----------|----------|----------|
| 快速概念验证 | 8-12 | 足够评估构图和基本元素 |
| 角色设计迭代 | 20-25 | 清晰的特征和细节 |
| 最终输出 | 25-30 | 精致的细节和纹理 |
| 艺术渲染 | 30+ | 最大细节和质感 |

**注意事项**：
- Turbo 模型设计为在较少步数下工作良好
- 超过 30 步后质量提升边际递减
- 根据具体需求调整，不必一味追求高步数

（请同时参考 z-image-prompt-donot-guide.md 以规避相关禁止项）

### P5 [High]: 掌握正向约束描述技巧

**核心原则**：由于 negative prompt 无效，所有约束和限定必须通过正向描述实现。

**约束描述模式**：

**1. 排除性描述**：
- 使用 "no"、"without"、"free of" 等短语
- 示例：`no text, no watermark, no logos, plain background`

**2. 规范性描述**：
- 明确指定应有的特征
- 示例：`correct human anatomy, natural hand proportions, sharp focus on subject`

**3. 场景限定**：
- 通过上下文暗示约束
- 示例：`professional office setting, business attire, formal pose`

**常用约束短语库**：

| 目标 | 推荐短语 |
|------|----------|
| 清晰无水印 | `no text, no watermark, no logos, no branding` |
| 正确解剖 | `correct human anatomy, natural proportions, proper limb structure` |
| 清晰焦点 | `sharp focus on subject, clear details, no motion blur` |
| 简洁背景 | `plain background, simple uncluttered setting, minimal distractions` |
| 正确透视 | `proper perspective, natural proportions, realistic spatial relationships` |

（请同时参考 z-image-prompt-donot-guide.md 以规避相关禁止项）

### P6 [High]: 精细化构图与镜头控制

**核心原则**：明确的构图指令能显著提升生成结果的可控性。

**镜头类型关键词**：
- **特写**：`close-up`, `extreme close-up`, `macro shot`
- **中景**：`medium shot`, `waist-up shot`, `chest-up portrait`
- **全景**：`full-body shot`, `wide shot`, `establishing shot`
- **环境**：`wide angle`, `aerial view`, `bird's eye view`

**角度与视角**：
- `front view`, `side profile`, `three-quarter view`
- `looking slightly up`, `looking slightly down`, `eye-level shot`
- `low angle`, `high angle`, `Dutch angle`

**构图法则关键词**：
- `rule of thirds composition`
- `centered composition`
- `symmetrical framing`
- `dynamic diagonal composition`
- `leading lines`

**示例应用**：
```
A medium shot portrait with rule of thirds composition, subject positioned slightly off-center, soft blurred background creating depth, shallow depth of field, 85mm lens perspective, natural eye-level angle, professional photography style
```

（请同时参考 z-image-prompt-donot-guide.md 以规避相关禁止项）

### P7 [High]: 精确描述光照与氛围

**核心原则**：Z-Image 对光照描述响应极佳，精细的光照控制能显著提升图像质感。

**光照类型词汇**：

| 光照风格 | 描述关键词 |
|----------|------------|
| 自然日光 | `soft diffused daylight`, `golden hour sunlight`, `overcast natural light` |
| 室内照明 | `warm indoor lighting`, `soft studio lighting`, `candlelight ambiance` |
| 戏剧照明 | `dramatic side lighting`, `high contrast noir lighting`, `rim lighting` |
| 环境光 | `ambient city lights`, `neon glow`, `moonlight illumination` |
| 特殊效果 | `god rays`, `lens flare`, `volumetric lighting`, `bokeh background` |

**氛围描述词汇**：
- `calm and serene`, `tense and dramatic`, `cozy and warm`
- `mysterious and moody`, `uplifting and hopeful`, `melancholic and nostalgic`

**组合示例**：
```
Soft diffused daylight streaming through sheer curtains, creating gentle shadows and warm highlights on the subject's face, calm and contemplative atmosphere, shallow depth of field with creamy bokeh background, professional portrait photography lighting
```

（请同时参考 z-image-prompt-donot-guide.md 以规避相关禁止项）

### P8 [Normal]: 角色特征精确描述

**核心原则**：具体的角色特征描述能产生更具辨识度和一致性的角色形象。

**描述维度**：

**1. 基础信息**：
- 年龄：`young adult`, `middle-aged`, `elderly`
- 性别与体型：`adult woman with athletic build`, `slender young man`

**2. 面部特征**：
- 脸型：`oval face`, `heart-shaped face`, `angular jawline`
- 眼睛：`large almond-shaped eyes`, `deep-set blue eyes`, `expressive green eyes`
- 发型：`waist-length wavy hair`, `short cropped hair`, `intricate braided hairstyle`
- 特殊标记：`small beauty mark below left eye`, `faint freckles across nose`

**3. 表情与姿态**：
- `gentle smile with crinkled eyes`, `confident determined expression`
- `relaxed posture with hands in pockets`, `elegant poised stance`

**4. 服装细节**：
- 风格：`casual streetwear`, `elegant evening gown`, `professional business attire`
- 颜色与材质：`crimson silk blouse`, `worn leather jacket`, `crisp white linen shirt`
- 配饰：`delicate silver necklace`, `vintage wristwatch`, `minimalist earrings`

**完整角色描述示例**：
```
A young woman in her mid-20s with an oval face and soft features, large expressive amber eyes with subtle winged eyeliner, waist-length wavy auburn hair with natural highlights, small beauty mark below her left eye, wearing a cream-colored oversized knit sweater over a collared shirt, dark high-waisted jeans, and simple gold hoop earrings, standing with a relaxed confident posture, gentle warm smile, soft natural lighting highlighting her features
```

（请同时参考 z-image-prompt-donot-guide.md 以规避相关禁止项）

### P9 [Normal]: 风格与艺术媒介控制

**核心原则**：明确的风格描述能确保生成结果符合预期的艺术方向。

**风格分类词汇**：

| 风格类型 | 关键词示例 |
|----------|------------|
| 写实风格 | `photorealistic`, `hyperrealistic`, `cinematic photography`, `documentary style` |
| 动漫风格 | `modern anime style`, `90s anime aesthetic`, `chibi style`, `anime key visual` |
| 绘画风格 | `oil painting`, `watercolor`, `acrylic painting`, `impasto technique` |
| 数字艺术 | `digital painting`, `concept art`, `matte painting`, `3D render` |
| 插画风格 | `flat vector illustration`, `line art`, `crosshatching`, `children's book illustration` |
| 复古风格 | `vintage film photography`, `polaroid style`, `retro 80s aesthetic`, `art deco` |

**风格强化技巧**：
- 指定艺术家参考：`in the style of Studio Ghibli`, `reminiscent of Greg Rutkowski's work`
- 指定艺术运动：`impressionist style`, `art nouveau elements`, `cyberpunk aesthetic`
- 指定技术特征：`clean linework`, `soft pastel colors`, `high contrast black and white`

**示例**：
```
Digital painting in the style of modern concept art, vibrant saturated colors with strong value contrast, dynamic brushwork, cinematic composition, dramatic lighting with strong rim light, highly detailed textures, professional game art quality, 4K resolution
```

（请同时参考 z-image-prompt-donot-guide.md 以规避相关禁止项）

### P10 [Normal]: 种子管理与迭代策略

**核心原则**：合理使用种子控制生成的一致性和变异性。

**种子使用策略**：

**1. 固定种子迭代**：
- 使用相同种子测试提示词修改效果
- 隔离变量，准确评估提示词变化的影响
- 适合精细化调整特定元素

**2. 随机种子探索**：
- 使用随机种子探索设计空间
- 发现意外的优质结果
- 适合概念探索阶段

**3. 混合策略**：
- 初期使用随机种子广泛探索
- 锁定优质方向后固定种子微调
- 最终阶段微调提示词细节

**迭代工作流**：
1. 生成 5-10 个随机种子变体
2. 评估并选择最接近目标的结果
3. 记录该结果的种子值
4. 基于该种子进行提示词微调
5. 重复直到满意

（请同时参考 z-image-prompt-donot-guide.md 以规避相关禁止项）

---

## Constraints [Conditional]

### C1: 提示词结构规范

- 使用清晰的段落分隔不同描述维度
- 避免过度复杂的嵌套结构
- 保持描述的逻辑流：从整体到局部，从主体到环境

### C2: 内容描述规范

- 优先使用具体可观察的描述而非抽象形容词
- 使用精确的数值和度量（如 `waist-length hair` 而非 `long hair`）
- 避免模糊的程度副词，使用明确的限定词

### C3: 语言使用规范

- 单一语言块描述效果更佳
- 英文提示词通常表现更稳定
- 中文提示词适用于特定文化元素描述

---

## Mechanisms & Logic [Conditional]

### 提示词解析机制

Z-Image 的 S3-DiT 架构将文本和图像 token 统一处理：

1. **文本编码**：使用 Qwen3-4B 作为文本编码器，理解复杂的自然语言描述
2. **跨模态融合**：文本特征与图像生成过程深度交互
3. **指令遵循**：模型对明确的指令性描述响应强烈

### 质量优化机制

- **详细描述** → 更精确的图像特征控制
- **结构化组织** → 更好的元素优先级处理
- **明确约束** → 减少不期望的生成内容

### 多样性控制机制

- 提示词的微小变化会产生显著不同的结果
- 需要实质性修改提示词才能获得真正的多样性
- 种子控制与提示词修改结合使用效果更佳

---

## Appendix [Optional]

### A1: 实用提示词模板库

#### 模板 1：专业人像摄影
```
A professional headshot portrait of [SUBJECT], [AGE] years old with [FEATURES], wearing [CLOTHING], [EXPRESSION] expression, studio setting with [BACKGROUND], [LIGHTING] lighting creating [EFFECT], shot with [LENS] lens, [DEPTH] depth of field, [STYLE] photography style, high resolution, sharp focus on eyes, professional quality
```

#### 模板 2：角色概念设计
```
Full-body character concept art of [CHARACTER_TYPE], [DISTINCTIVE_FEATURES], wearing [OUTFIT_DETAILS], [POSE] pose, [EXPRESSION] expression, [SETTING] background, [LIGHTING] lighting, [STYLE] art style, clean design, detailed costume elements, turnaround-ready illustration
```

#### 模板 3：场景环境设计
```
[SHOT_TYPE] of [ENVIRONMENT_TYPE], [TIME_OF_DAY], [WEATHER_CONDITIONS], [KEY_ELEMENTS], [ATMOSPHERE] atmosphere, [LIGHTING] lighting, [STYLE] style, highly detailed, [MOOD] mood, cinematic composition, 8K quality
```

#### 模板 4：产品展示
```
Professional product photography of [PRODUCT], [MATERIAL] material, [COLOR] color, placed on [SURFACE], [LIGHTING] lighting, [ANGLE] angle, [BACKGROUND] background, sharp details, commercial photography style, clean and minimal
```

#### 模板 5：动漫角色
```
[STYLE] anime style illustration of [CHARACTER], [HAIR_DESCRIPTION], [EYE_DESCRIPTION], wearing [OUTFIT], [POSE] pose, [EXPRESSION] expression, [BACKGROUND] background, [LIGHTING] lighting, clean linework, vibrant colors, detailed character design
```

### A2: 描述词汇速查表

#### 外貌描述
- **脸型**：oval, round, square, heart-shaped, diamond, oblong
- **眼睛**：almond-shaped, round, hooded, deep-set, monolid
- **鼻子**：straight, button, aquiline, Roman, snub
- **嘴唇**：full, thin, heart-shaped, bow-shaped
- **肤色**：fair, olive, tan, deep, porcelain, ebony

#### 服装材质
- **天然材质**：cotton, linen, silk, wool, cashmere, leather
- **合成材质**：polyester, nylon, spandex, velvet, satin
- **纹理描述**：smooth, textured, ribbed, quilted, embroidered

#### 环境元素
- **自然**：forest, mountain, ocean, desert, meadow, canyon
- **城市**：skyscraper, street, alley, plaza, rooftop, subway
- **室内**：living room, bedroom, kitchen, office, studio, warehouse

#### 情绪氛围
- **积极**：joyful, serene, hopeful, triumphant, peaceful
- **消极**：melancholic, tense, ominous, despairing, chaotic
- **中性**：mysterious, contemplative, nostalgic, dreamlike

### A3: 常见问题解决方案

| 问题 | 解决方案 |
|------|----------|
| 生成结果过于相似 | 大幅修改提示词描述，而非仅调整参数 |
| 细节不够清晰 | 增加具体描述词，明确指定材质和纹理 |
| 背景过于杂乱 | 添加 `simple background`, `minimal setting` 等约束 |
| 解剖结构问题 | 添加 `correct anatomy`, `natural proportions` 等描述 |
| 风格不统一 | 在提示词开头明确指定整体风格方向 |

### A4: 进阶技巧

#### 分层描述法
将复杂场景分解为多个层次分别描述：
1. **前景层**：主要主体和互动元素
2. **中景层**：支撑性元素和环境细节
3. **背景层**：远景和环境氛围
4. **大气层**：光照、天气、空气效果

#### 对比强化法
通过对比描述强化视觉效果：
- `warm subject against cool background`
- `sharp focus foreground with blurred background`
- `bright highlights contrasting with deep shadows`

#### 叙事描述法
为静态图像添加叙事元素增强感染力：
- `capturing a moment of...`
- `as if caught mid-action...`
- `suggesting a story of...`

---

**文档结束**

*本指南专注于 Z-Image 提示词构造的正向最佳实践。如需了解禁止事项和注意事项，请参阅 [z-image-prompt-donot-guide.md](./z-image-prompt-donot-guide.md)*
