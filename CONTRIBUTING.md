# 贡献指南

感谢你考虑为 md2pdf 贡献代码！请花几分钟阅读以下规范。

---

## 📋 提交 Issue（Bug 报告 / 功能请求）

### Bug 报告模板

```markdown
**描述 Bug**
清晰简洁地描述问题是什么。

**重现步骤**
1. 执行命令 `md2pdf ...`
2. 看到错误：...

**期望行为**
你期望应该发生什么。

**环境信息**
- OS: macOS / Linux
- 安装方式: pip install / 源码安装
- `md2pdf --version` 输出:
- `python3 --version` 输出:

**日志 / 截图**
如有，附上相关输出或截图。
```

### 功能请求模板

```markdown
**需求描述**
你想让 md2pdf 支持什么新功能？

**使用场景**
在什么情况下你会用到它？示例命令：

```bash
md2pdf ... --your-new-flag
```

**备选方案**
你考虑过其他实现方式吗？
```

---

## 🔀 Pull Request 规范

### 分支命名

| 类型 | 格式 | 示例 |
|------|------|------|
| 功能 | `feat/<简短描述>` | `feat/latex-math-support` |
| Bug 修复 | `fix/<简短描述>` | `fix/weasyprint-path-priority` |
| 文档 | `docs/<简短描述>` | `docs/cherry-studio-config` |
| 重构 | `refactor/<简短描述>` | `refactor/i18n-module` |
| 测试 | `test/<简短描述>` | `test/html-output-mode` |

### 提交信息规范

使用 [Conventional Commits](https://www.conventionalcommits.org/)：

```
<type>: <简短描述>

<详细说明（可选）>
```

| 类型 | 用途 |
|------|------|
| `feat` | 新功能 |
| `fix` | Bug 修复 |
| `docs` | 文档变更 |
| `refactor` | 重构 |
| `test` | 测试 |
| `chore` | 构建/工具链 |
| `style` | 格式调整（无逻辑变更） |

**示例：**

```
feat: add --html flag for intermediate HTML output

Expose the Markdown→HTML intermediate step as a first-class
output format, bypassing WeasyPrint for users who only need HTML.
```

### PR 检查清单

提交 PR 前请逐项确认：

- [ ] 代码遵循现有风格（命名、缩进、空行）
- [ ] 新增功能有对应的 CLI 参数和帮助文本
- [ ] 新增文本已添加 i18n 翻译（`i18n.py` 中 `zh-CN` 和 `en`）
- [ ] 没有硬编码的本地路径、密钥或个人信息
- [ ] `python3 -m md2pdf --help` 输出正确
- [ ] `python3 -m md2pdf samples/sample.md --html` 正常生成
- [ ] 已在本地测试通过

---

## 🛠️ 本地开发

### 环境要求

- Python >= 3.10
- WeasyPrint（推荐 conda 安装: `conda install -c conda-forge weasyprint`）
- MCP SDK（可选，仅开发 MCP 功能时需要）

### 安装开发环境

```bash
# 1. 克隆项目
git clone https://github.com/fudonglee/md2pdf.git
cd md2pdf

# 2. 可编辑模式安装（修改源码后 CLI 自动同步）
pip install -e ".[full]"

# 3. 验证
md2pdf --version
md2pdf --help
```

### 项目结构

```
md2pdf/
├── md2pdf/              # 核心 Python 包
│   ├── cli.py           # 命令行入口
│   ├── renderer.py      # Markdown → HTML → PDF 渲染
│   ├── parser.py        # Markdown 解析（markdown-it-py）
│   ├── css.py           # CSS 样式模板（多语言字体）
│   ├── i18n.py          # 国际化翻译
│   └── utils.py         # 工具函数
├── mcp/
│   └── mcp-server.py    # MCP 服务器
├── samples/             # 示例文件
└── scripts/             # 安装脚本
```

### 添加一门新语言

1. 在 `md2pdf/i18n.py` 的 `LANGUAGES` 字典中添加条目
2. 在 `SUPPORTED_LANGS` 中添加语言代码映射
3. 在 `README.md` 的语言支持表中添加一行

---

## 🔐 安全准则

- **禁止**提交 API 密钥、Token、密码到仓库
- **禁止**硬编码本地文件路径（如 `/Users/xxx/`）
- `.env` 文件已加入 `.gitignore`，勿强行提交
- 发现安全漏洞请参考 `SECURITY.md` 中的报告方式
