# CLAUDE.md

## 项目简介

这是一个 AIGC (AI 生成内容) 知识库，包含 AI 图像生成、视频生成、提示词工程等方面的资料和最佳实践。

## 知识库 MCP 工具

本仓库配置了一个本地 MCP 知识库服务器 (`aigc-knowledge`)，提供以下工具：

### 何时使用知识库工具

**优先使用知识库工具** 当用户询问以下内容时：
- AI 图像生成提示词（Midjourney、Stable Diffusion、z-image 等）
- AI 视频生成相关内容（可灵、即梦 Seedance 等）
- 提示词最佳实践和技巧
- 本仓库中记录的任何知识、笔记或方案
- 历史总结、方法论、参考资料

**不要使用知识库工具** 当：
- 用户询问通用编程问题（与本仓库无关）
- 用户明确要求查看代码文件（使用普通文件读取）
- 问题与 AIGC 内容无关

### 使用优先级

1. **search_knowledge** - 首选。当需要查找知识时，先搜索
2. **read_knowledge_file** - 根据搜索结果，读取具体文件详情
3. **list_knowledge_sources** - 浏览可用内容，当不确定搜索什么时使用
4. **get_knowledge_status** - 检查索引状态，用于调试

### 示例用法

用户问："Midjourney v7 有什么新特性？"
→ 调用 `search_knowledge(query="Midjourney v7")`

用户问："帮我看看这个仓库有哪些关于提示词的内容"
→ 调用 `list_knowledge_sources(path="wiki/prompt")`

用户问："读取 Midjourney 提示词指南"
→ 先 `search_knowledge(query="Midjourney prompt guide")`，然后根据结果 `read_knowledge_file(path="...")`

## 仓库结构

```
wiki/           # 结构化知识文档
  ├── prompt/   # 提示词相关
  ├── gem/      # GEM (Gemini) 相关
  └── ...
docs/           # 协议和规范文档
raw_data/       # 原始资料
  ├── ai_image/ # AI 图像生成资料
  ├── ai_video/ # AI 视频生成资料
  └── ai_tools/ # AI 工具使用资料
```

## 开发说明

- MCP 服务器代码在 `tools/mcp/`
- 初始化命令：`./scripts/setup_mcp.sh`
- 重建索引：`./scripts/rebuild_knowledge_index.sh`
