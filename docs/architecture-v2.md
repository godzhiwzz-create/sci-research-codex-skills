# v2 架构与兼容说明

> `v2.0.0` 是当前稳定 Release；本页同时描述 `main` 分支已进入 Changelog `Unreleased` 的升级。正式版本号将在独立发布 PR 中按最终兼容性审计确定。

## 两个 owner，六个专门入口

仓库继续保留全部 8 个公开 Skill 名称，不新增会竞争触发的第 9、10 个入口：

- `sci-research-manager` 是研究状态、项目文献接口、实验语义、证据晋升、方向决策、跨库交接和最终提交门的 owner。
- `academic-manuscript-writing` 是稿件阶段、主线、正文、修订、回复、clean/marked-up 和 proof 内容的 owner。
- `sci-literature-manager`、`sci-paper-reader`、`sci-experiment-manager`、`sci-result-auditor`、`sci-paper-manager`、`sci-asset-manager` 接收有界输入并返回 typed handback，不成为第二个工作流 owner。

项目自己的 `AGENTS.md`、schema、模板和事实来源始终优先。公共 Skill 提供默认语义和兼容映射，不为统一外观重写历史。

## 一个事实一个 owner

| 事实 | 默认 owner | 其他文件/Skill 的职责 |
|---|---|---|
| 来源身份、题录、版本、别名和去重 | 全局文献库及 `sci-literature-manager` | 项目通过稳定 Source ID 引用 |
| 项目为什么采用某来源 | 项目 `literature/SOURCES.tsv` 或既有等价物 | INDEX/QUERY_MAP 只做检索视图 |
| 某个外部 claim 的精确核验 | `LITERATURE_CLAIMS.tsv` + 精确位置 note | 稿件只能在相同或更窄范围复用 |
| 实验协议和科学解释 | 实验卡 | 索引只保存当前状态与指针 |
| 数值和不确定性 | 原始 artifact + 精确提取代码/config/commit | 表格、图和 prose 是派生呈现 |
| 实验当前五轴状态 | 项目 `EXPERIMENTS.tsv` 或一个明确映射的既有机器源 | 旧 `EXPERIMENT_INDEX.*` 可作 authority 或 generated view，不能同时编辑 |
| 跨会话 canonical evidence | 共享 result registry 指向卡片/raw source | 不复制成第二份实验卡或数字表 |
| 当前项目阶段、blocker 和下一动作 | 项目 HANDOFF | 链接证据，不保存结果日记 |
| 论文主张 | claim-evidence map | 绑定内部证据或已核验外部 claim |
| 稿件主线和改写范围 | `academic-manuscript-writing` 选定的 stage contract | 专门 Skill 返回有界产物，由写作 owner 集成 |

## 项目文献双轴

文献阅读深度与具体 claim 核验必须分开：

- `reading_depth`: `metadata_only / abstract_checked / full_read`
- `verification_status`: `needs_verification / claim_verified / contradicted / superseded`

读完一篇论文不等于核验了其中每句话。只有记录 Source ID、版本、页/节/表/图位置、可支持措辞、协议边界、禁止外推和核验时间后，单个 LiteratureClaim 才能成为 `claim_verified`。

全局 PDF、题录、版本关系、去重和 BibTeX 不复制进项目目录；项目只保存 Source-ID 视图、标签、用途、reading depth、精确 claim note 和下游链接。

## 实验五轴与状态转换

默认把以下五个字段分开：

| 轴 | 默认值 |
|---|---|
| Lifecycle stage | `idea_exploration / minimal_probe / formal_experiment / result_analysis / paper_writing / submission_prepare / maintenance` |
| Experiment status | `designed / running / partial / complete / stopped / superseded` |
| Evidence status | `not_assessed / verified / pending_artifact / protocol_mismatch / unverifiable` |
| Claim strength | `main_claim / trend_only / diagnostic_only / negative_boundary / internal_exploration / unsupported` |
| Direction decision | `continue / redirect / reference_only / stop / needs_literature` |

`complete` 只表示预期运行 artifact 和 execution provenance 存在，不自动等于 `verified`、`promoted`、paper-facing 或科学上“成功”。有效的失败、空结果和负对照仍是证据。

旧值可渐进映射：`stop` → `stopped`，`session_result_pending_artifact` → `pending_artifact`。旧 experiment status `needs_verification` 不能机械改名；应先保留真实运行状态，再按缺失原因选择 `pending_artifact` 或 `unverifiable`。项目有更严格 vocabulary 时保留，并通过审计器的 `--allow-value FIELD=VALUE` 显式登记；影响 completion/verification/claim gate 的别名再用 `--map-value FIELD=ALIAS:CANONICAL` 声明语义，不能仅靠名称猜测。

项目最小闭环是：

```text
raw result -> experiment card -> project current-state index/query route
```

只有证据成为跨会话 canonical answer、改变 paper-facing claim、替代旧权威或改变重要 warning 时，才更新共享 registry。只有阶段、中心问题、blocker、活跃执行、canonical route 或下一动作变化时，才更新 HANDOFF。

## 两个跨库交接门

文献到实验：先生成 source-grounded brief，分开论文证据与项目假设，并冻结变量、控制、混杂、成功/失败门和最小验证；有可证伪要求后才分配实验 ID。

证据到稿件：只传递 claim ID/允许措辞/强度、canonical card/raw source、精确外部 claim note、协议和选择边界、反证、冻结图表来源及未决 gap。稿件出现新 claim 或扩大范围时，必须退回证据 owner 核验。

## 稿件七阶段

`academic-manuscript-writing` 每次只选择一个阶段：

```text
initial_draft
manuscript_polish
pre_submission_audit
major_revision_preserving
minor_revision_local
final_submission_audit
proof_correction
```

阶段决定允许的 mutation。初稿可搭建完整论证；polish 只能在不改变科学含义的前提下统一结构和语言；pre-submission audit 只读；大修/小修必须绑定原提交稿、审稿意见和 mainline；final audit 冻结内容；proof 只修生产错误。

## Typed handback

调用专门 Skill 前，owner 必须声明：输入 artifact/ID、允许动作、禁止状态变化、输出类型和返回位置。handback 至少包含 source path、已核验范围、限制和建议状态变化。

专门 Skill 不得自行：

- 晋升 evidence 或扩大 claim；
- 改变项目路线或稿件 stage；
- 并行修改 canonical manuscript；
- 把渲染文件当成新的科学事实源；
- 执行未经授权的移动、删除、发布、上传或最终提交。

## 路径和 CLI 兼容

旧项目常使用：

```text
PROJECT_HANDOFF.md
research_workspace/experiments/
research_workspace/paper/
research_workspace/literature/
EXPERIMENT_INDEX.csv/.md
```

这些路径继续可读。现有模板继续保留，旧写作 reference 路径改为指向阶段化规范的兼容入口。`audit_workspace.py` 继续支持 `--no-git` 和 `--skip-required-entrypoints`；实验生成器继续拒绝覆盖；新研究库审计器支持显式指定 literature、experiments、projects 和 PDF inventory 根目录。

## 审计与最终提交边界

- `audit_research_libraries.py` 检查 Source ID、alias、reading depth、LiteratureClaim、五轴实验索引和 canonical registry 的结构/指针，不替代科学解释或数值复算。
- `scan_external_disclosures.py` 扫描支持的文本、OOXML/ODF、PDF、图片和压缩包成员；退出码 `2` 表示不完整，必须补扫或人工核验。退出码 `0` 也不构成作者批准。
- 最终提交审核依次检查科学/回复一致性、对外披露、文件与渲染、元数据/声明、package/portal 副本身份及作者不可逆动作确认。
- 上传、发布、费用/条款接受和最终提交始终需要与具体动作匹配的授权。

## 发布兼容承诺

- 维持仓库名和 8 个公开 Skill ID。
- 不把可选外部 Skill 变成核心依赖。
- 核心自动测试只使用 Python 标准库；PDF 文本提取和图片 OCR 是披露扫描的可选系统能力，缺失时返回不完整而不是假装通过。
- 不强制批量迁移已有 schema、路径或历史卡片。
- 删除、破坏性迁移、发布和不可逆提交需要明确授权。
