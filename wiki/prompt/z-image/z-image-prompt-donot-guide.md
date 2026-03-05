# Z-Image Prompt Construction: DO NOT / MUST NOT Guide

Last_Updated: 2025-03-05

## Overview [Required]

- Purpose: 定义 Z-Image / Z-Image-Turbo 模型提示词构造的严格禁止事项与不建议做法
- Scope: Covers 提示词结构、内容约束、参数误区、风格控制禁忌 / Does not cover LoRA 训练、工作流参数、安全审核机制

## Core Concepts [Required]

- **S3-DiT (Single-Stream Diffusion Transformer)**: 6B 参数的单流扩散 Transformer 架构，文本与图像 token 在同一序列中联合处理
- **Few-Step Distilled Model**: 约 8 步实际扩散步骤的蒸馏模型，优化用于快速生成
- **Classifier-Free Guidance (CFG)**: Z-Image-Turbo 在推理时不使用 CFG，guidance_scale 通常设为 0
- **Prompt Enhancer (PE)**: 官方提供的提示词增强模板，用于将简短描述扩展为详细提示词
- **Negative Prompt**: 传统扩散模型使用的负面提示词机制，在 Z-Image-Turbo 中完全无效

## Consolidated Principles [Required]

### P1 [Critical]: 禁止依赖负面提示词

- **MUST NOT** 使用 `negative_prompt` 参数期望控制生成内容
- **MUST NOT** 在 UI 的负面提示词框中填写内容并认为其会生效
- **MUST NOT** 使用传统负面提示词如 `bad anatomy, poorly drawn hands, extra fingers, deformed face, blurry, low quality, watermark`
- 上下文: Z-Image-Turbo 是 few-step 蒸馏模型，推理时不依赖 classifier-free guidance，官方 pipeline 完全忽略 negative_prompt
- 后果: 负面提示词框在官方 pipeline 中仅为"装饰性"存在，不会实际影响生成结果

### P2 [Critical]: 禁止过短或模糊的提示词

- **MUST NOT** 使用极简提示词如 `cute anime girl` 或 `a beautiful woman`
- **MUST NOT** 期望模型从模糊描述中自行推断细节
- **MUST NOT** 使用纯标签式提示词如 `1girl, long blue hair, red eyes, school uniform`
- 上下文: Z-Image-Turbo 对长而详细的自然语言描述响应最佳，模糊提示词会产生通用化、缺乏特色的结果
- 后果: 生成结果与预期严重偏离，缺乏可控性

### P3 [Critical]: 禁止超出 Token 限制的长提示词

- **MUST NOT** 在不调整参数的情况下使用超过 512 tokens 的提示词
- **MUST NOT** 使用 600-1000 词的提示词而不设置 `max_sequence_length=1024`
- **MUST NOT** 忽略 tokenizer 计算（约 0.75 词/token）导致提示词被截断
- 上下文: 官方代码默认最大文本长度为 512 tokens，超长提示词会被截断，导致后半部分描述丢失
- 后果: 提示词后半部分被忽略，生成结果与完整描述不符，多次生成几乎无变化

### P4 [High]: 禁止混合使用不兼容的风格控制方式

- **MUST NOT** 同时使用 Pony Diffusion 风格的 score tags 与 Z-Image 的自然语言描述风格
- **MUST NOT** 期望 SDXL 风格的权重修饰符 `(keyword:1.2)` 产生显著效果
- **MUST NOT** 混合使用标签式提示词与详细描述式提示词而不重新组织结构
- 上下文: Z-Image-Turbo 对自然语言描述响应最佳，传统标签模型（Pony、Animagine）的提示词习惯不完全适用
- 后果: 提示词结构混乱，模型理解困难，生成质量下降

### P5 [High]: 禁止在提示词中使用未经验证的推理模式

- **MUST NOT** 在 ComfyUI 中直接使用 Qwen3-4B-Thinking 作为 text encoder 期望复现官方推理效果
- **MUST NOT** 期望在 ComfyUI 中存在与官方相同的 reasoning 节点功能
- **DO NOT** 认为 CLIP 本身具备推理能力
- 上下文: 官方 reasoning 功能尚未在 ComfyUI 中实现，CLIP 仅作为翻译器而非推理引擎
- 后果: 无法复现官方演示效果，生成结果与预期存在差距

### P6 [Normal]: 禁止在角色一致性要求高的场景使用

- **DO NOT** 期望 Z-Image-Turbo 在多图生成中保持严格的角色一致性
- **DO NOT** 使用 Z-Image-Turbo 进行视觉小说或漫画的连续角色生成而不配合其他技术
- **DO NOT** 将 Z-Image-Turbo 用于需要 50+ 张图像保持同一角色的项目
- 上下文: Z-Image-Turbo 的通用架构和速度优化使其在角色一致性方面不如专用模型
- 后果: 同一角色在不同生成中外观差异显著，无法用于一致性要求高的项目

### P9 [Normal]: 不建议用于复杂多角色场景

- **DO NOT** 使用 Z-Image-Turbo 生成多个角色互动的复杂场景
- **DO NOT** 期望模型正确处理超过 2-3 个角色的构图
- 上下文: 6B 参数容量在处理复杂多角色交互时存在局限
- 后果: 角色间关系混乱、肢体交错错误、构图失衡

### P10 [Normal]: 禁止依赖固定种子获得一致风格

- **DO NOT** 完全依赖固定种子来控制风格一致性
- **DO NOT** 期望相同种子在不同提示词下产生风格一致的输出
- 上下文: Z-Image-Turbo 的设计优先考虑生成速度而非严格的可复现性
- 后果: 即使使用相同种子，提示词的微小变化也可能导致风格显著不同

## Constraints [Conditional]

### C1: 提示词结构约束

- **禁止**: 超过 2 层的列表嵌套
- **禁止**: 使用表格呈现信息
- **禁止**: 使用 HTML 标签
- **禁止**: 使用代码块展示提示词示例

### C2: 内容约束

- **禁止**: 包含安全审核相关内容的讨论
- **禁止**: 涉及 LoRA 训练技术细节
- **禁止**: 涉及工作流参数配置（如 BF16 模式、scheduler 选择等）

### C3: 语言约束

- **不建议**: 混合使用中英双语描述同一概念
- **不建议**: 在单句中频繁切换语言
- 上下文: 虽然模型支持双语，但单一语言块描述效果更佳

## Mechanisms & Logic [Conditional]

### 提示词失效机制

1. **Negative Prompt 失效**: 模型架构不支持 CFG → 负面提示词被完全忽略
2. **Token 截断**: 超过 max_sequence_length 的提示词被截断 → 后半部分描述丢失
3. **模糊推断**: 提示词过于简略 → 模型使用训练数据中的高频模式填充 → 结果偏离预期

### 质量下降触发条件

- 步数 < 8 → 伪影增加
- 提示词 < 30 词 → 细节缺失
- 混合风格修饰符 → 模型困惑
- 超出参数容量的复杂场景 → 解剖结构错误

## Derived Insights [Optional]

### 关于模型行为的洞察

- Z-Image-Turbo 的"服从性"特征意味着: 如果提示词没有明确禁止某事，模型可能自行添加
- 蒸馏过程导致模型在某些概念上表现出"abliteration"特征: 知道概念存在但生成结果不完善
- 速度优化带来的副作用: 同一提示词多次生成结果变化较小，需要显著修改提示词才能获得多样性

### 关于提示词策略的洞察

- 正向约束优于负向排除: 由于 negative prompt 无效，必须通过详细的正向描述来限定生成范围
- 具体性优于泛化性: 模型对明确的物理描述响应优于抽象形容词
- 结构化描述优于自由文本: 按"构图→主体→服装→环境→光照→风格"的顺序组织提示词效果更佳


