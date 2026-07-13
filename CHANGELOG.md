# Changelog

本文件记录 `sci-research-codex-skills` 的公开版本变化。格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，版本号遵循[语义化版本](https://semver.org/lang/zh-CN/)。

## [Unreleased]

### Added

- 新增科研协作、证据诚信、隐私和行为报告准则。

## [2.0.0] - 2026-07-13

### Added

- 为全部 8 个 Skill 补齐 `agents/openai.yaml`。
- 新增研究状态模型、artifact contract、审计清单和 specialist routing。
- 新增只读工作区审计与 provenance/mtime/hash 保护工具。
- 新增零第三方依赖测试与 Python 3.10、3.11、3.13 GitHub Actions。
- 新增仓库维护规则、架构说明和 GitHub 社区维护入口。

### Changed

- 将 `sci-research-manager` 收敛为科研生命周期与证据中枢。
- 将其他 7 个 Skill 收敛为职责明确的专门能力，同时保留全部公开名称。
- 实验卡、索引、结果收集、claim map、handoff 和一致性审计改为通用、可配置形式。
- 移除 portable Skill 中写死的项目目录、特定数据集和 teacher/student 假设。

### Safety

- 生成器拒绝静默覆盖 canonical 文件。
- 维护和审计默认只读，不自动改写原始文件时间。
- 远程检查、执行和昂贵计算需要用户明确授权。

## [1.0.0] - 2026-05-22

### Added

- 建立最初的 8 个 SCI research Codex Skills。
- 提供项目管理、文献、实验、结果审计、论文、资产和写作模板。
- 提供论文精读教程、可视化规范和 Attention Is All You Need 演示。
- 建立 MIT License 和 GitHub Pages 教程站点。

### Archived

- 此版本固定在提交 `67a99716ddbcdbd1c87f5b0cc6adc2120c3fb25e`，用于旧项目复现与兼容维护。
- 此版本不再接收功能更新；新安装应使用 v2。

[Unreleased]: https://github.com/godzhiwzz-create/sci-research-codex-skills/compare/v2.0.0...HEAD
[2.0.0]: https://github.com/godzhiwzz-create/sci-research-codex-skills/compare/v1.0.0...v2.0.0
[1.0.0]: https://github.com/godzhiwzz-create/sci-research-codex-skills/releases/tag/v1.0.0
