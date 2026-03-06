# Midjourney 提示词构造指南

Last_Updated: 2026-03-06

---

## Overview

Midjourney 提示词构造的核心原则：**想看到什么，就明确说出来**。

提示词不是给人类看的标题或描述，而是向模型传递视觉意图的指令。模型通过训练数据学习词汇与视觉特征的关联，因此提示词的清晰度直接决定生成结果的准确度。

有效的提示词构造需要理解：
- 词序影响视觉焦点（斜率效应）
- 自然语言语法优于关键词堆砌
- 具体视觉描述优于抽象概念
- 环境原型可节省描述成本

---

## Core Concepts

### 语义锚定 (Semantic Anchoring)

通过叠加具体名词、介词短语与关联动作，强制模型将注意力集中在特定视觉元素上的技术手段。

- 将 "a man with a hat" 锚定为 "a man wearing a wide-brimmed straw hat casting shadow over his eyes"
- 使用空间介词（Left, Right, Foreground, Background, Above, Below）固定元素位置

### 视觉原型 (Archetype)

模型预训练数据中对某一概念的最普遍形态认知。触发原型可节省算力，但打破原型需投入大量描述权重。

- "in a junkyard" 自动触发垃圾、生锈金属、废弃车辆的视觉联想
- 无需重复描述原型已包含的细节
- 打破原型（如让苹果发光）需要额外描述权重和参数调整

### 注意力预算 (Attention Budget)

模型处理提示词时的计算资源有限。提示词越长、细节越多，每个细节分配到的注意力越少。

- 当关键细节丢失时，删除无关紧要的环境描述为目标细节腾出预算
- 优先保证核心主体的描述精度

### 斜率效应 (Slope of Influence)

提示词中越靠前的词汇获得越高的注意力权重，对构图焦点的影响越大。

- 前置主体成为画面核心
- 后置元素退化为背景或上下文
- 利用此效应可控制视觉层次而不依赖复杂描述

---

## Consolidated Principles

### 提示词构造三要素

每个完整的提示词应包含：

1. **主体 (Subject)** - 画面中是什么
2. **环境/背景 (Setting/Background)** - 在哪里、什么情境
3. **风格 (Style)** - 什么美学效果

缺失任一要素，模型将用原型自动填充，可能导致不可控结果。

### 词汇选择策略

**使用密集视觉语言：**
- 描述事物的外观而非概念
- 将 "mysterious forest" 转化为 "dense canopy blocking sunlight, twisted roots emerging from fog"

**禁用抽象与隐喻：**
- 避免 "beautiful", "iconic", "a relic of forgotten time"
- 转化为具体的光影、材质、形态描述

**禁用技术元数据：**
- 剔除 "HDR", "8K", "ISO 100", "50mm lens"
- 保留风格术语如 "Polaroid", "Cinematic still-shot"

### 句子结构规范

**使用自然语言短句：**
- 采用标准语法结构的完整句子
- 避免逗号分隔的关键词列表

**单一动作单一句子：**
- 每个视觉动作或特征对应一个独立句子
- 杜绝复杂从句和长篇嵌套

**消除选择逻辑：**
- 禁用 "or" 及其同义表达
- 模型无法处理选择逻辑，必须提供单一确定描述

### 否定重构原则

禁用否定词汇（no, not, without, never），将缺失状态重构为正向视觉线索：

- "no logo" → "plain unmarked surface"
- "without hat" → "bare head with visible hair"

### 环境原型依赖

利用环境原型减少冗余描述：

- "in a Victorian library" 自动暗示书架、木质装潢、暖色灯光
- 无需重复列举原型已包含的元素
- 仅描述偏离原型的特殊细节

### 全身肖像强制渲染

生成全身像时的特殊约束：

- 首句声明 "Photograph of a full-length..."
- 描述顶部锚点（发型、头饰）
- 描述底部锚点（鞋履、足部细节）
- 描述触地介质（站在什么地面上）
- 使用垂直比例（--ar 2:3 或 9:16）

### 姿态与表情控制

**摄影术语调用：**
- profile shot, three-quarter shot, head-tilt pose
- hands-on-hips pose, leaning pose, S-curve pose

**情绪关联引导：**
- "bashful, shy, embarrassed" 引导低头、躲避视线
- "intense, fierce, angry" 引导直视镜头

**面部微特征固化：**
- 追加 "bright eyes, intense gaze"
- "frowning, blushing, laughing"
- 锁定头部形态防止渲染崩坏

---

## Mechanisms & Logic

### 语法影响构图机制

词序直接决定视觉焦点和元素关系：

**焦点控制：**
- "A fountain with a mermaid statue" - 喷泉是主体，美人鱼是装饰
- "A mermaid statue topping a fountain" - 美人鱼是主体，喷泉是底座

**空间关系控制：**
- "A miniature city contained by a glass tank" - 城市是焦点
- "A glass tank with a miniature city inside it" - 玻璃罐是焦点

**原型动词强化：**
- 使用 "growing", "driving", "emerging" 等动词激活场景原型
- "A forest of broccoli on a plate" → "A tiny forest of broccoli trees growing on a plate"

### Omni-Reference 语义迁移机制

--oref 参数通过语义理解而非像素匹配进行特征迁移：

**方法一：参数锚定控制**
- 在提示词中重申参考图的标志性特征
- 明确指定新姿态、新环境
- 适用于保持原型特征的场景

**方法二：语义托管**
- 使用 "Someone" 或 "Some stuff" 作为主体
- 将外观决策权完全移交 --oref
- 适用于完全复制参考图特征的场景

**方法三：纯场景投射**
- 提示词仅描述背景环境
- 不提及任何主体，由 --oref 自动注入
- 适用于将参考主体融入新场景

**尺寸控制律：**
- 模型继承参考图中主体的物理比例
- 生成小尺寸物体需在参考图中预留大量留白

**画幅一致律：**
- 生成比例 --ar 必须与参考图比例一致
- 防止出现黑边伪影

---

## Constraints

### V7 十五法则

1. **禁用否定词汇** - 重构为正向视觉线索
2. **禁用祈使句** - 不使用 "draw", "add", "make"
3. **禁用用途解释** - "for a logo" 转为 "vector icon style"
4. **禁用文本描述尺寸** - 使用 --ar 参数而非 "square layout"
5. **禁用抽象语言** - "beautiful" 转为具体视觉特征
6. **禁用叙述性语言** - 只描述冻结的单帧瞬间
7. **保持简短直接** - 单一动作对应单一短句
8. **禁用短语列表** - 不使用 "glowing light, broken wall" 式并列
9. **依赖环境原型** - 剔除冗余隐含细节
10. **移除相机元数据** - 剔除 ISO、焦距等技术参数
11. **重构品牌引用** - 抽象品牌转为风格特征，保留视觉 IP 原型
12. **移除保真度修饰词** - "hyperrealistic" 转为 "photo style"
13. **消除选择逻辑** - 禁用 "or" 分支
14. **多主体压缩** - 使用群组原型 + 空间锚点分离个体
15. **仅使用官方参数** - 剔除自造参数

---

## Output Format / Style Hints

### 标准提示词结构

```
[主体描述]. [环境/背景描述]. [风格描述].
```

**结构原则：**
- 主体前置确保视觉焦点
- 环境承接提供情境上下文
- 风格后置统一美学基调

### 语法风格规范

**自然语言优先：**
- 使用完整句子而非关键词列表
- 保持标准语法和标点

**短句原则：**
- 每个句子承载一个视觉信息单元
- 避免复杂从句嵌套

**具体化原则：**
- 所有描述必须对应可视觉化的物理特征
- 将抽象概念逐层拆解为形态、光影、材质

**顺序敏感性：**
- 关键主体置于提示词前部
- 次要细节置于提示词后部
- 利用斜率效应控制视觉层次

### 提示词优化检查清单

- [ ] 是否包含主体、环境、风格三要素
- [ ] 是否使用自然语言短句
- [ ] 是否剔除所有抽象词汇
- [ ] 是否剔除所有技术元数据
- [ ] 是否剔除所有否定表达
- [ ] 是否利用环境原型减少冗余
- [ ] 关键细节是否前置获得足够注意力
- [ ] 整体长度是否控制在合理范围（避免过度稀释）

---

*本指南基于 Midjourney 官方文档及社区最佳实践整合而成*