# Contributing

感谢参与 `sci-research-codex-skills`。本仓库优先接受能够提高科研证据纪律、可复现性、兼容性或维护安全性的改进。

## 开始之前

1. 搜索现有 [Issues](https://github.com/godzhiwzz-create/sci-research-codex-skills/issues) 和 Pull Requests，避免重复工作。
2. Bug 使用 Bug report；新能力或行为变化使用 Feature request。
3. 安全问题不要公开提交，按 [SECURITY.md](SECURITY.md) 私密报告。
4. 阅读根目录 [AGENTS.md](AGENTS.md)，它定义 Skill、证据、文件和发布边界。

## 兼容性边界

- 不改变仓库名和 8 个公开 Skill 文件夹名，除非变更被明确批准为破坏性大版本。
- 不在 portable Skill 中写入个人路径、凭据、数据集、项目指标或具体论文结论。
- 不把文献发现、聊天记忆或模拟数据提升为项目实验事实。
- 维护工具默认只读，写入时使用明确的 generated 路径并拒绝危险覆盖。
- 已发布标签不可移动或复用。

## 本地工作流

从最新 `main` 创建分支：

```bash
git switch main
git pull --ff-only
git switch -c agent/short-description
```

提交前运行：

```bash
python -m unittest discover -s tests -v
```

如果修改了 Skill，还应对每个受影响目录运行系统 `skill-creator` 提供的 `quick_validate.py`。修改 Python 脚本时，同时执行类型检查或等价的静态检查。

## Pull Request 要求

Pull Request 应说明：

- 改了什么以及为什么；
- 对用户、证据边界和兼容性的影响；
- 是否改变文件、路径、时间或远程执行行为；
- 运行过哪些测试；
- 是否需要版本号、Changelog、README 或 Pages 同步更新。

提交贡献即表示你同意代码按本仓库 [MIT License](LICENSE) 发布。
