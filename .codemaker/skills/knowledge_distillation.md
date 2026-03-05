# SKILL: distill

## 触发方式

- `distill {目标目录}`
- `@skill distill {目标目录}`

## 输入参数

- **target_directory** (必需): 需要分析的目标目录路径
- **output_category** (可选): 输出分类目录名，不指定则由 AI 推荐

## 执行规范

**严格遵循**: [docs/protocols/Knowledge_Distillation_Protocol.md](docs/protocols/Knowledge_Distillation_Protocol.md)

执行时必须先读取上述协议文件，按照其中定义的所有规则执行蒸馏。

## 执行流程

### Phase 1: 准备阶段

1. 读取 `docs/protocols/Knowledge_Distillation_Protocol.md` 协议
2. 递归扫描 `{target_directory}` 下所有文件
3. 读取并分析所有文件内容
4. 根据内容推荐输出分类 → 询问用户确认或修改
5. 确定输出路径: `output/{确认的分类}/{文档名}.md`
6. 若分类目录不存在，创建该目录

### Phase 2: 渐进式生成（防止超时）

**关键策略**: 每完成一个模块立即写入文件，不等待全部完成

按照协议中 Output Format 定义的模块顺序，逐模块处理并立即追加写入：

1. 创建文件（标题 + Last_Updated）→ 立即写入
2. Overview [Required] → 立即追加写入
3. Core Concepts [Required] → 立即追加写入
4. Consolidated Principles [Required] → 立即追加写入
5. 后续 Conditional/Optional 模块 → 有内容则追加写入，无内容则跳过
6. Appendix 模块 → 有内容则追加写入

### Phase 3: 完成报告

- 源文件列表及处理状态
- 输出文件路径
- 蒸馏统计（原始字数 vs 蒸馏后字数）

## 写入策略约束

- 每个模块完成后**必须立即写入**，不缓存到最后
- 空的 Conditional/Optional 模块直接跳过，不写入
- 写入失败时保留已写入内容，报告错误位置

## 错误处理

- **读取失败**: 跳过该文件，在完成报告中标记
- **写入失败**: 停止并报告，已写入内容保留
- **超时**: 渐进式写入已规避，若仍超时可从断点继续

## 示例

```
distill raw_data/ai_video
```

```
AI: 已分析目录，包含 4 个文件。
    推荐: output/wiki/prompt/ai_video_prompt_engineering.md
    确认？

用户: 确认

AI: ✓ 标题和元数据
    ✓ Overview
    ✓ Core Concepts
    ✓ Consolidated Principles
    ✓ Constraints
    ⊘ Mechanisms & Logic (跳过)
    ✓ Appendix
    
    ✅ 完成! output/wiki/prompt/ai_video_prompt_engineering.md
部分内容已忽略。```