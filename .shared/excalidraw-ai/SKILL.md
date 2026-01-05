---
name: excalidraw-ai
description: >
  AI-powered Excalidraw diagram generator that converts natural language descriptions 
  into professional diagrams. Use when: (1) Creating flowcharts from text descriptions,
  (2) Generating architecture diagrams, (3) Building mind maps, (4) Designing system workflows,
  (5) Creating technical documentation visuals, or (6) Converting complex ideas into visual diagrams.
---

# excalidraw-ai

AI驱动的Excalidraw图表生成器，将自然语言描述转换为专业图表。

## 使用方法

```bash
# 生成基本流程图
python3 .shared/excalidraw-ai/scripts/excalidraw_generator.py "用户登录 -> 验证 -> 访问数据" --type flowchart

# 生成架构图
python3 .shared/excalidraw-ai/scripts/excalidraw_generator.py "API Gateway -> 微服务 -> 数据库" --type architecture

# 生成思维导图
python3 .shared/excalidraw-ai/scripts/excalidraw_generator.py "Python开发：FastAPI，SQLAlchemy，Redis" --type mindmap

# ✅ Python 项目（上下文感知）自动生成后端架构图
# 在项目根目录执行（会扫描 *.py 并基于结构生成图）
python3 .shared/excalidraw-ai/scripts/excalidraw_generator.py --project . --type architecture --output backend_arch.json

# （可选）如果安装了 Astral ty，则附带类型检查元信息（不会影响图生成）
# uv tool install ty@latest
python3 .shared/excalidraw-ai/scripts/excalidraw_generator.py --project . --type architecture --use-ty

# 使用自定义样式
python3 .shared/excalidraw-ai/scripts/excalidraw_generator.py "系统架构" --theme modern --output diagram.json

# 交互式生成
python3 .shared/excalidraw-ai/scripts/excalidraw_generator.py --interactive
```

## 支持的图表类型

- `flowchart` - 流程图
- `architecture` - 架构图  
- `mindmap` - 思维导图

> 注：`sequence` / `network` 目前尚未实现（后续可扩展模板）。

## 可用主题

- `modern` - 现代简洁风格
- `sketchy` - 手绘风格
- `technical` - 技术文档风格
- `colorful` - 多彩风格

## 输出格式

生成的图表可以：
- 直接导入到 Excalidraw.com
- 通过API集成到Web应用
- 转换为PNG/SVG图片
- 嵌入到Markdown文档

## 核心功能

1. **文本生成图表** - 从自然语言描述生成流程图/架构图/思维导图
2. **Python 项目分析（AST）** - 扫描代码结构并生成后端架构草图（`--project`）
3. **可选 ty 元信息** - 结合 Astral `ty` 输出类型检查摘要（`--use-ty`）
4. **样式主题** - 多种视觉风格
5. **交互编辑** - 支持迭代优化