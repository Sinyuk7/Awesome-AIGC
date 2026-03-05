# Knowledge Base

个人知识管理仓库，用于：

1. **存档各类文档** - 收集和整理有价值的资料
2. **输出想法和总结** - 记录个人见解和总结性概念
3. **记录有用信息** - 保存值得参考的内容

## 目录结构

```
├── raw_data/          # 原始数据（未标准化的信息）
│   ├── ai_image/      # AI 图像生成相关（Midjourney、Nano Banana 等）
│   ├── ai_video/      # AI 视频生成相关
│   ├── ai_tools/      # 其他 AI 工具资料
│   └── moderation/    # 内容审核相关
│
├── docs/              # 项目依赖的标准化文档和规则
│   └── protocols/     # 协议和规范文档
│
├── output/            # 最终输出产物
│   ├── wiki/          # Wiki 文档
│   └── gem/           # GEM 指令
│
└── openspec/          # 规范和变更管理
    ├── specs/         # 规范定义
    └── changes/       # 变更记录
```

## 工作流程

`raw_data/` → 整理加工 → `output/`

- **raw_data**: 存放从网页复制、搜索结果等原始未处理的信息
- **docs**: 存放项目本身依赖的文档和规则
- **output**: 存放经过整理后的最终产物