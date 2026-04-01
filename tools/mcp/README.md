# AIGC Knowledge MCP Server

本地运行的 MCP (Model Context Protocol) 知识库服务器，专为 Claude Code 设计。

## 为什么选择这个方案

**问题**：需要一个可跨设备同步的 AI 知识库，让 Claude 能够检索项目中的文档和笔记。

**方案**：
- **知识内容通过 Git 同步** - 利用现有的版本控制基础设施
- **MCP Server 本地运行** - 无需云服务、无延迟、无成本
- **Claude Code 原生支持** - 通过 project-scoped `.mcp.json` 自动加载

**优势**：
- ✅ 离线可用 - 不依赖网络
- ✅ 数据安全 - 敏感内容不上传
- ✅ 零成本 - 无需付费 API
- ✅ 版本控制 - 知识变更可追溯
- ✅ 跨设备同步 - git pull 即可更新

## 快速开始

### 1. 初始化环境

```bash
./scripts/setup_mcp.sh
```

这会：
- 检查 Python 版本 (需要 3.10+)
- 创建虚拟环境 (`tools/mcp/.venv/`)
- 安装依赖
- 构建初始知识索引

### 2. 重启 Claude Code

重启 Claude Code 以加载 MCP 服务器。首次使用时会提示授权 MCP 连接。

### 3. 测试

在 Claude Code 中尝试：
- "搜索知识库中关于 Midjourney 提示词的内容"
- "列出所有知识来源"
- "查看知识库状态"

## 知识来源

当前索引的目录：

| 目录 | 内容 |
|------|------|
| `wiki/` | 结构化知识文档 |
| `docs/` | 协议和规范文档 |
| `raw_data/` | 原始资料（AI图像、视频、工具等） |

支持的文件格式：`.md`, `.txt`, `.mdx`

## 日常使用

### 更新知识库

1. 添加/修改知识文件到 `wiki/`, `docs/`, 或 `raw_data/`
2. 重建索引：
   ```bash
   ./scripts/rebuild_knowledge_index.sh
   ```
3. 新内容立即可搜索

### 换一台电脑

```bash
# 1. Clone 仓库
git clone <repo-url>

# 2. 初始化 MCP
./scripts/setup_mcp.sh

# 3. 重启 Claude Code
```

### 同步更新

```bash
git pull
./scripts/rebuild_knowledge_index.sh
```

## 提供的工具

### search_knowledge
搜索知识库，返回最相关的文档片段。

**参数**：
- `query` (必需): 搜索关键词
- `top_k` (可选): 返回结果数量，默认 10
- `path_filter` (可选): 路径过滤，如 `wiki/prompt`

**返回**：按相关度排序的结果，包含 path、title、score、snippet、updated_at

### read_knowledge_file
读取指定知识文件的完整内容。

**参数**：
- `path` (必需): 文件相对路径，如 `wiki/prompt/midjourney/midjourney-prompt-guide.md`

**返回**：文件内容（超大文件截断为 50KB）

### list_knowledge_sources
列出知识库中的目录和文件。

**参数**：
- `path` (可选): 子目录路径。为空则列出所有知识源概览。

**返回**：目录结构和文件列表

### get_knowledge_status
获取知识索引状态信息。

**返回**：文档数量、最后更新时间、按来源/格式的统计

## 技术细节

### 目录结构

```
tools/mcp/
├── server.py          # MCP 服务器主程序
├── pyproject.toml     # Python 依赖配置
├── README.md          # 本文档
├── .venv/             # 虚拟环境 (gitignore)
└── .knowledge_index/  # 本地索引 (gitignore)
```

### 搜索算法

第一阶段使用简单的关键词匹配：
- 标题完全匹配：+10 分
- 标题单词匹配：+3 分/词
- 路径匹配：+2 分/词
- 内容匹配：+0.5 分/次（上限 5 分）

### 索引格式

索引存储为 JSON，包含文件元数据（路径、标题、大小、更新时间）。不存储完整内容。

## 第二阶段扩展建议

### 本地 RAG (向量检索)
- 接入本地 embedding 模型（如 sentence-transformers）
- 使用 chromadb 或 lancedb 做向量存储
- 实现语义搜索

### MCP Prompts
- 添加预定义的知识检索 prompt 模板
- 让 Claude 更自然地发起知识查询

### MCP Resources
- 暴露知识文件为 MCP resources
- 支持 Claude 直接引用

### Claude Code Skill
- 封装为 Claude Code skill
- 提供更自然的触发方式

## 故障排除

### MCP 服务器未启动

```bash
# 检查虚拟环境是否存在
ls tools/mcp/.venv/

# 如果不存在，重新初始化
./scripts/setup_mcp.sh
```

### 搜索无结果

```bash
# 检查索引状态
cat tools/mcp/.knowledge_index/index.json | head -20

# 重建索引
./scripts/rebuild_knowledge_index.sh
```

### Python 版本问题

需要 Python 3.10 或更高版本：

```bash
python3 --version
```

## 许可证

与主项目相同。
