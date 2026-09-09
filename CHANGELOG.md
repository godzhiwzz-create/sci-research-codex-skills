# Changelog

本文件记录 `sci-research-codex-skills` 的公开版本变化。格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，版本号遵循[语义化版本](https://semver.org/lang/zh-CN/)。

## [Unreleased]

### Added

- 新增标准库安全安装器：默认预览、选择性安装、内容相同跳过、显式升级及目录备份，并以临时目录测试覆盖冲突、软链接、状态变化与失败回滚。
- 新增通用最近先例与研究投入决策检查，明确检索扩展、证据范围、可检验差别和停止条件。
- 新增科研协作、证据诚信、隐私和行为报告准则。
- 新增统一维护手册，覆盖日常更新、Release、回滚、定期巡检和交接。
- 新增可执行维护一致性检查及 release candidate/tag 核验。
- 新增每月只读维护工作流和 GitHub Actions Dependabot 配置。
- 新增项目 Source-ID/LiteratureClaim 接口、实验库生命周期、跨库交接和最终提交六门审核规范。
- 新增稿件七阶段工作流，覆盖初稿、成稿打磨、提交前审核、大修、小修、最终提交审核和校样纠正。
- 新增可配置的 `audit_research_libraries.py` 与覆盖文本、OOXML/ODF、PDF、图片和压缩包的 `scan_external_disclosures.py`。
- 新增非标准库布局、扩展 vocabulary、审计退出码、披露扫描、全 Skill 引用和隐私标记的回归测试。

### Changed

- 对齐项目管理/精读教程与模块交接：负责人表示职责，不强制额外代理；窄任务直接完成，局部改稿不触发全阶段产物，清单检查不触发完整投稿审计。
- 实验 ID、综合记录和资产审查按实际接受/授权与事件触发，保留原始子卡片；可选模块缺失不自动安装或扩展流程。
- CI 保留 Python 3.10/3.11/3.13 全矩阵，任务分支只经 PR 触发，主分支/版本标签继续验证；同一 PR 的更新可取消旧检查。
- 重整 README、Pages 与教程导航首页，前置任务/安装入口、稳定版与 main 区别，并同步仓库 About；改进键盘焦点、页内导航和 Markdown 阅读入口。
- 区分讨论、定向查新、最小探索、正式实验和投稿审计；上下文按变化读取、记录按事件更新，既有授权在原范围内继续有效。
- 已知论文采用查重、身份验证和增量登记；小问题按决定性原文回答，不自动创建完整阅读包或全领域检索。
- 机械工作优先确定性脚本，委派需覆盖范围和收益合理；主负责人继续核验决定性证据。尚未量化实际 token 或额度节省。
- PR 测试现在先验证版本、文档、社区配置和公开 Skill 的维护不变量。
- GitHub Actions 升级到官方当前主要版本的运行时。
- 稳定标签核验兼容 GitHub Actions 的 detached HEAD，同时仍要求标签可达 `origin/main`。
- 在保持 8 个公开 Skill ID 的前提下，将 `sci-research-manager` 明确为研究状态与证据 owner，将 `academic-manuscript-writing` 明确为稿件阶段与主线 owner；其余 Skill 通过 typed handback 协作。
- 新项目的默认实验状态统一为五个正交轴；已有 `EXPERIMENT_INDEX.*`、自定义 vocabulary、模板和公开 CLI 继续兼容，不强制批量迁移。
- 旧写作 reference 路径保留为阶段化规范的兼容入口，避免形成第二套稿件工作流。

### Safety

- 远端工作统一描述为通过 SSH 连接用户配置的服务器；单负责人监控，连接退出不等于远端结束，状态不明时有界核验而非盲目重启。
- 保留统计、协议、公平对照、原始证据与有效负结果；相关先例或单次失败不自动否定整个方向。公开隐私检查新增基础设施专有名称和非示例 IP 防回归。
- 对外材料披露候选扫描在不支持或未分类的格式、缺少 PDF/OCR 能力、未扫描的嵌入对象、资源/超时上限或软链接边界上返回 `incomplete_scan`，不把部分覆盖报告成通过。
- 新增公开仓库文本检查，拒绝个人绝对路径和高置信凭据模式；维护提交使用 GitHub noreply 身份。
- 审计、package 准备和 portal staging 不自动授权修复、上传、发布或最终提交。

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
