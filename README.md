# 🧠 SmartNote-CLI

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square&logo=python" alt="Python 3.8+">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="MIT License">
  <img src="https://img.shields.io/badge/Platform-Linux%20%7C%20macOS%20%7C%20Windows-lightgrey?style=flat-square" alt="Platform">
</p>

<p align="center">
  <b>AI-Powered Smart Markdown Note Manager</b><br>
  <i>Terminal-based intelligent note-taking with AI-enhanced features</i>
</p>

---

## 🌍 Language | 语言 | 語言

- [English](#english)
- [简体中文](#简体中文)
- [繁體中文](#繁體中文)

---

<a name="english"></a>
## 🎉 Project Introduction

SmartNote-CLI is an **AI-powered terminal note manager** designed for developers, writers, and knowledge workers who live in the terminal. It combines the simplicity of Markdown with intelligent AI features to transform how you capture, organize, and retrieve your thoughts.

### 💡 Why SmartNote-CLI?

- **🚀 Terminal-First**: No heavy Electron apps — lightning fast, keyboard-driven workflow
- **🤖 AI-Powered**: Auto-tagging, smart summarization, sentiment analysis, and keyword extraction
- **🔍 Full-Text Search**: Instantly find any note with powerful search capabilities
- **📊 Knowledge Insights**: Track your writing habits and note statistics
- **🎨 Beautiful TUI**: Rich terminal interface with syntax highlighting and markdown rendering

### ✨ Core Features

| Feature | Description | Status |
|---------|-------------|--------|
| 📝 **Markdown Support** | Full CommonMark & GFM compatibility | ✅ |
| 🤖 **AI Auto-Tagging** | Intelligent tag generation via local LLM | ✅ |
| 🧠 **Smart Summary** | Automatic content summarization | ✅ |
| 🔍 **Full-Text Search** | Lightning-fast note retrieval | ✅ |
| 🏷️ **Tag Management** | Hierarchical tag organization | ✅ |
| ⭐ **Favorites** | Pin important notes | ✅ |
| 📦 **Archive** | Clean up without losing data | ✅ |
| 📤 **Export** | JSON & Markdown export formats | ✅ |
| 🖥️ **Rich TUI** | Interactive terminal interface | ✅ |
| 🔌 **Ollama Integration** | Local AI, no data leaves your machine | ✅ |

---

## 🚀 Quick Start

### Requirements

- Python 3.8+
- (Optional) [Ollama](https://ollama.com/) for AI features

### Installation

```bash
# Install from source
pip install git+https://github.com/gitstq/SmartNote-CLI.git

# Or clone and install
git clone https://github.com/gitstq/SmartNote-CLI.git
cd SmartNote-CLI
pip install -e .
```

### Basic Usage

```bash
# Launch interactive TUI
smartnote tui

# Add a new note
smartnote add "My First Note" -c "This is my first SmartNote!"

# Add with AI assistance
smartnote add "Python Tips" -c "List comprehensions are powerful..." --ai

# List all notes
smartnote list

# Search notes
smartnote search "python"

# Show note details
smartnote show 1

# AI analyze a note
smartnote analyze 1

# Export notes
smartnote export --format markdown -o notes.md
```

---

## 📖 Detailed Usage Guide

### CLI Commands

```bash
# Note Management
smartnote add <title> [options]       # Create new note
smartnote list [options]              # List notes
smartnote show <id>                   # View note details
smartnote edit <id> [options]         # Edit note
smartnote delete <id>                 # Delete note
smartnote search <query>              # Search notes

# Organization
smartnote favorite <id>               # Toggle favorite
smartnote archive <id>                # Archive/unarchive
smartnote tags                        # List all tags

# AI Features
smartnote analyze <id>                # AI analyze note
smartnote config --model llama3.2     # Configure AI

# Utilities
smartnote stats                       # Show statistics
smartnote export [options]            # Export notes
smartnote tui                         # Launch TUI
```

### TUI Interface

The Textual-based TUI provides:
- **Sidebar**: Category and tag filtering
- **Main Panel**: Sortable note table
- **Search Bar**: Real-time full-text search
- **Status Bar**: Live statistics

**Keyboard Shortcuts:**

| Key | Action |
|-----|--------|
| `n` | New note |
| `e` | Edit note |
| `d` | Delete note |
| `f` | Toggle favorite |
| `a` | Archive note |
| `s` | Focus search |
| `r` | Refresh |
| `q` | Quit |

---

## 💡 Design Philosophy

### Tech Stack Choices

- **Python 3.8+**: Universal availability, rich ecosystem
- **Click**: Intuitive CLI framework
- **Textual**: Modern Python TUI framework
- **SQLite**: Zero-config, serverless database
- **Ollama**: Privacy-first local AI

### Architecture

```
smartnote/
├── __init__.py      # Package metadata
├── database.py      # SQLite data layer
├── ai_engine.py     # AI feature engine
├── cli.py           # Click CLI interface
└── tui_app.py       # Textual TUI application
```

---

## 📦 Deployment Guide

### Development Setup

```bash
git clone https://github.com/gitstq/SmartNote-CLI.git
cd SmartNote-CLI
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest tests/ -v --cov=smartnote
```

### Building Distribution

```bash
python setup.py sdist bdist_wheel
```

---

## 🤝 Contributing

We welcome contributions! Please follow these guidelines:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing`)
3. **Commit** with conventional messages (`feat:`, `fix:`, `docs:`)
4. **Push** to your fork
5. **Open** a Pull Request

### Commit Convention

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation update
- `refactor:` Code refactoring
- `test:` Test updates

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

<a name="简体中文"></a>
## 简体中文

## 🎉 项目介绍

SmartNote-CLI 是一款**AI驱动的终端笔记管理器**，专为生活在终端中的开发者、写作者和知识工作者设计。它将 Markdown 的简洁性与智能 AI 功能相结合，改变您捕捉、组织和检索想法的方式。

### 💡 为什么选择 SmartNote-CLI？

- **🚀 终端优先**：没有沉重的 Electron 应用 —— 极速、键盘驱动的工作流
- **🤖 AI 驱动**：自动标签、智能摘要、情感分析和关键词提取
- **🔍 全文搜索**：强大的搜索能力，瞬间找到任何笔记
- **📊 知识洞察**：追踪您的写作习惯和笔记统计
- **🎨 精美 TUI**：语法高亮和 Markdown 渲染的富终端界面

### ✨ 核心特性

| 特性 | 描述 | 状态 |
|------|------|------|
| 📝 **Markdown 支持** | 完整 CommonMark 和 GFM 兼容性 | ✅ |
| 🤖 **AI 自动标签** | 通过本地 LLM 智能生成标签 | ✅ |
| 🧠 **智能摘要** | 自动内容摘要 | ✅ |
| 🔍 **全文搜索** | 闪电般快速的笔记检索 | ✅ |
| 🏷️ **标签管理** | 分层标签组织 | ✅ |
| ⭐ **收藏夹** | 固定重要笔记 | ✅ |
| 📦 **归档** | 清理而不丢失数据 | ✅ |
| 📤 **导出** | JSON 和 Markdown 导出格式 | ✅ |
| 🖥️ **丰富 TUI** | 交互式终端界面 | ✅ |
| 🔌 **Ollama 集成** | 本地 AI，数据不离开您的机器 | ✅ |

---

## 🚀 快速开始

### 环境要求

- Python 3.8+
- (可选) [Ollama](https://ollama.com/) 用于 AI 功能

### 安装

```bash
# 从源码安装
pip install git+https://github.com/gitstq/SmartNote-CLI.git

# 或克隆后安装
git clone https://github.com/gitstq/SmartNote-CLI.git
cd SmartNote-CLI
pip install -e .
```

### 基本用法

```bash
# 启动交互式 TUI
smartnote tui

# 添加新笔记
smartnote add "我的第一条笔记" -c "这是我的第一条 SmartNote！"

# 使用 AI 辅助添加
smartnote add "Python 技巧" -c "列表推导式很强大..." --ai

# 列出所有笔记
smartnote list

# 搜索笔记
smartnote search "python"

# 显示笔记详情
smartnote show 1

# AI 分析笔记
smartnote analyze 1

# 导出笔记
smartnote export --format markdown -o notes.md
```

---

## 📖 详细使用指南

### CLI 命令

```bash
# 笔记管理
smartnote add <标题> [选项]       # 创建新笔记
smartnote list [选项]              # 列出笔记
smartnote show <id>                   # 查看笔记详情
smartnote edit <id> [选项]         # 编辑笔记
smartnote delete <id>                 # 删除笔记
smartnote search <查询>              # 搜索笔记

# 组织
smartnote favorite <id>               # 切换收藏
smartnote archive <id>                # 归档/取消归档
smartnote tags                        # 列出所有标签

# AI 功能
smartnote analyze <id>                # AI 分析笔记
smartnote config --model llama3.2     # 配置 AI

# 工具
smartnote stats                       # 显示统计
smartnote export [选项]            # 导出笔记
smartnote tui                         # 启动 TUI
```

### TUI 界面

基于 Textual 的 TUI 提供：
- **侧边栏**：分类和标签筛选
- **主面板**：可排序的笔记表格
- **搜索栏**：实时全文搜索
- **状态栏**：实时统计

**键盘快捷键：**

| 按键 | 操作 |
|------|------|
| `n` | 新建笔记 |
| `e` | 编辑笔记 |
| `d` | 删除笔记 |
| `f` | 切换收藏 |
| `a` | 归档笔记 |
| `s` | 聚焦搜索 |
| `r` | 刷新 |
| `q` | 退出 |

---

## 💡 设计理念

### 技术栈选择

- **Python 3.8+**：通用可用，丰富生态
- **Click**：直观的 CLI 框架
- **Textual**：现代 Python TUI 框架
- **SQLite**：零配置、无服务器数据库
- **Ollama**：隐私优先的本地 AI

---

## 📦 打包与部署指南

### 开发环境搭建

```bash
git clone https://github.com/gitstq/SmartNote-CLI.git
cd SmartNote-CLI
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -e ".[dev]"
```

### 运行测试

```bash
pytest tests/ -v --cov=smartnote
```

### 构建分发

```bash
python setup.py sdist bdist_wheel
```

---

## 🤝 贡献指南

欢迎贡献！请遵循以下准则：

1. **Fork** 仓库
2. **创建** 功能分支 (`git checkout -b feature/amazing`)
3. **提交** 使用约定式提交 (`feat:`, `fix:`, `docs:`)
4. **推送** 到您的 fork
5. **打开** Pull Request

### 提交规范

- `feat:` 新功能
- `fix:` Bug 修复
- `docs:` 文档更新
- `refactor:` 代码重构
- `test:` 测试更新

---

## 📄 开源协议

MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。

---

<a name="繁體中文"></a>
## 繁體中文

## 🎉 專案介紹

SmartNote-CLI 是一款**AI 驅動的終端筆記管理器**，專為生活在終端中的開發者、寫作者和知識工作者設計。它將 Markdown 的簡潔性與智慧 AI 功能相結合，改變您捕捉、組織和檢索想法的方式。

### 💡 為什麼選擇 SmartNote-CLI？

- **🚀 終端優先**：沒有沉重的 Electron 應用 —— 極速、鍵盤驅動的工作流
- **🤖 AI 驅動**：自動標籤、智慧摘要、情感分析和關鍵詞提取
- **🔍 全文搜尋**：強大的搜尋能力，瞬間找到任何筆記
- **📊 知識洞察**：追蹤您的寫作習慣和筆記統計
- **🎨 精美 TUI**：語法高亮和 Markdown 渲染的豐富終端介面

### ✨ 核心特性

| 特性 | 描述 | 狀態 |
|------|------|------|
| 📝 **Markdown 支援** | 完整 CommonMark 和 GFM 相容性 | ✅ |
| 🤖 **AI 自動標籤** | 透過本地 LLM 智慧生成標籤 | ✅ |
| 🧠 **智慧摘要** | 自動內容摘要 | ✅ |
| 🔍 **全文搜尋** | 閃電般快速的筆記檢索 | ✅ |
| 🏷️ **標籤管理** | 分層標籤組織 | ✅ |
| ⭐ **收藏夾** | 固定重要筆記 | ✅ |
| 📦 **歸檔** | 清理而不遺失資料 | ✅ |
| 📤 **匯出** | JSON 和 Markdown 匯出格式 | ✅ |
| 🖥️ **豐富 TUI** | 互動式終端介面 | ✅ |
| 🔌 **Ollama 整合** | 本地 AI，資料不離開您的機器 | ✅ |

---

## 🚀 快速開始

### 環境要求

- Python 3.8+
- (可選) [Ollama](https://ollama.com/) 用於 AI 功能

### 安裝

```bash
# 從原始碼安裝
pip install git+https://github.com/gitstq/SmartNote-CLI.git

# 或複製後安裝
git clone https://github.com/gitstq/SmartNote-CLI.git
cd SmartNote-CLI
pip install -e .
```

### 基本用法

```bash
# 啟動互動式 TUI
smartnote tui

# 新增筆記
smartnote add "我的第一條筆記" -c "這是我的第一條 SmartNote！"

# 使用 AI 輔助新增
smartnote add "Python 技巧" -c "列表推導式很強大..." --ai

# 列出所有筆記
smartnote list

# 搜尋筆記
smartnote search "python"

# 顯示筆記詳情
smartnote show 1

# AI 分析筆記
smartnote analyze 1

# 匯出筆記
smartnote export --format markdown -o notes.md
```

---

## 📖 詳細使用指南

### CLI 命令

```bash
# 筆記管理
smartnote add <標題> [選項]       # 建立新筆記
smartnote list [選項]              # 列出筆記
smartnote show <id>                   # 檢視筆記詳情
smartnote edit <id> [選項]         # 編輯筆記
smartnote delete <id>                 # 刪除筆記
smartnote search <查詢>              # 搜尋筆記

# 組織
smartnote favorite <id>               # 切換收藏
smartnote archive <id>                # 歸檔/取消歸檔
smartnote tags                        # 列出所有標籤

# AI 功能
smartnote analyze <id>                # AI 分析筆記
smartnote config --model llama3.2     # 設定 AI

# 工具
smartnote stats                       # 顯示統計
smartnote export [選項]            # 匯出筆記
smartnote tui                         # 啟動 TUI
```

### TUI 介面

基於 Textual 的 TUI 提供：
- **側邊欄**：分類和標籤篩選
- **主面板**：可排序的筆記表格
- **搜尋欄**：即時全文搜尋
- **狀態欄**：即時統計

**鍵盤快捷鍵：**

| 按鍵 | 操作 |
|------|------|
| `n` | 新增筆記 |
| `e` | 編輯筆記 |
| `d` | 刪除筆記 |
| `f` | 切換收藏 |
| `a` | 歸檔筆記 |
| `s` | 聚焦搜尋 |
| `r` | 重新整理 |
| `q` | 退出 |

---

## 💡 設計理念

### 技術棧選擇

- **Python 3.8+**：通用可用，豐富生態
- **Click**：直觀的 CLI 框架
- **Textual**：現代 Python TUI 框架
- **SQLite**：零配置、無伺服器資料庫
- **Ollama**：隱私優先的本地 AI

---

## 📦 打包與部署指南

### 開發環境搭建

```bash
git clone https://github.com/gitstq/SmartNote-CLI.git
cd SmartNote-CLI
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -e ".[dev]"
```

### 執行測試

```bash
pytest tests/ -v --cov=smartnote
```

### 構建分發

```bash
python setup.py sdist bdist_wheel
```

---

## 🤝 貢獻指南

歡迎貢獻！請遵循以下準則：

1. **Fork** 倉庫
2. **建立** 功能分支 (`git checkout -b feature/amazing`)
3. **提交** 使用約定式提交 (`feat:`, `fix:`, `docs:`)
4. **推送** 到您的 fork
5. **開啟** Pull Request

### 提交規範

- `feat:` 新功能
- `fix:` Bug 修復
- `docs:` 文件更新
- `refactor:` 程式碼重構
- `test:` 測試更新

---

## 📄 開源協議

MIT 授權條款 - 詳見 [LICENSE](LICENSE) 檔案。

---

<p align="center">
  Made with ❤️ by SmartNote Team
</p>
