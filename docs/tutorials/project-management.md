# 项目管理教程：让 Codex 接管长期 SCI 论文研究记忆

这个教程适合已经有很多实验、文献、报告和草稿的项目。目标不是把文件夹“摆好看”，而是让 Codex 能低成本找回主线、判断证据、解释失败原因，并阻止你把一个失败方向继续调参。

## 1. 先建立项目骨架

下面是兼容 v1 的示例结构，不是 v2 的硬编码要求。已有项目应优先沿用自己的 `AGENTS.md`、README/HANDOFF 和目录约定；新脚本也支持显式指定路径。

在项目根目录建立：

```text
PROJECT_HANDOFF.md
AGENTS.md
research_workspace/
  experiments/
    QUERY_MAP.md
    EXPERIMENT_INDEX.md
    EXPERIMENT_INDEX.csv
    cards/
  literature/
  paper/
    PAPER_STATUS.md
    CLAIM_EVIDENCE_MAP.md
  project/
    DECISION_LOG.md
    STAGE_PLAN.md
    PROJECT_PLAN.md
```

新项目可将 `EXPERIMENTS.tsv` 作为五轴当前状态的唯一 editable 机器源，并在项目 `literature/` 中使用 `SOURCES.tsv` 与 `LITERATURE_CLAIMS.tsv`。旧 `EXPERIMENT_INDEX.*` 可以继续作为 authority 或 generated view，但不要和 `EXPERIMENTS.tsv` 同时手工维护。

推荐对 Codex 说：

```text
Use sci-research-manager.
Initialize the project memory files for my SCI paper project.
Keep uncertain information marked as needs verification.
```

## 2. 让 Codex 每次按低 token 路线读取

在 `AGENTS.md` 写明：

```markdown
Before starting a research task, read:

1. PROJECT_HANDOFF.md
2. research_workspace/experiments/QUERY_MAP.md
3. research_workspace/experiments/EXPERIMENT_INDEX.md
4. relevant experiment cards only

Do not scan all logs, runs, results, or checkpoints by default.
```

这样 Codex 每次不会一上来扫全项目，而是先看轻量记忆，再按问题进入相关实验卡。

## 3. 项目管理输出长什么样

当你说：

```text
现在实验太乱了，帮我整理主线，告诉我哪些该停，哪些还能继续。
```

理想输出应该像这样：

```markdown
## Stage

result_analysis

## Operating Mode

direction_review

## Current Central Question

当前路线真正要回答的是：某个信号是否能解释目标任务失败，而不是它能否被塞进某个 head。

## Evidence Ledger

| Evidence | What it supports | What it does not support |
|---|---|---|
| E041 | 预注册主比较达到预设 gate | 不证明其他任务或设置也成立 |
| F120-D01 | 候选解释 A 未通过对照 | 不否定原始研究问题 |
| F121-D02 | 辅助信号只呈现有限诊断作用 | 不支持把它提升为主贡献 |

## Failure Cause

- signal mismatch：信号测到的是 A，但任务需要 B。
- interface mismatch：信号被放进了直接决策层。
- control failure：随机化检查或简单对照解释了表面差异。

## Do Not Do Next

- 不加 epoch。
- 不加 seed。
- 不调 loss weight。
- 不再换一个小 head。
- 不把成熟框架的小优化当主贡献。

## Decision

redirect：保留问题，停止当前接口，先做最小的区分性 probe。
```

这个输出的重点是“为什么”，不是“又跑什么”。

## 4. 多个实验怎么合并

如果一个方向下有很多小实验，不要让 active 目录塞满几十张卡。用 family card 收束：

```text
cards/
  F120_direction_exploration.md
  _archive/
    F120/
      F120_D01_old_probe.md
      F120_D02_old_probe.md
```

family card 负责记录：

- 方向假设；
- 子实验表；
- 哪些支持；
- 哪些被 control 解释掉；
- 哪些不能再重复；
- 建议的 continue / redirect / reference_only / stop / needs_literature。

family card 保存科学综合；`sci-research-manager` 接收 handback 后再集成最终方向决定和共享 registry 状态。

## 5. 项目管理和论文写作怎么连起来

实验卡只说明实验。论文 claim 还要进入：

```text
research_workspace/paper/CLAIM_EVIDENCE_MAP.md
```

例子：

```markdown
| Claim ID | Claim | Evidence | Claim strength | Evidence status |
|---|---|---|---|---|
| C001 | 方法在预注册任务上达到目标 | E021, E041 | main_claim | verified |
| C002 | 该机制可推广到任意设置 | F120-D01, F121-D02 | unsupported | verified |
```

第二行刻意展示：证据已核验，不等于 claim 获得支持；五个状态轴不能互相替代。

写论文前先让 Codex 做：

```text
Use sci-research-manager and sci-result-auditor.
Audit CLAIM_EVIDENCE_MAP and return a bounded evidence packet.
Then use academic-manuscript-writing to select the manuscript stage before editing prose.
```

## 6. 常见错误

| 错误 | 这套 skills 怎么拦住 |
|---|---|
| 失败后继续调参 | `sci-research-manager` 要求先输出 failure cause 和 do-not-do-next |
| 文件夹越整越乱 | `sci-experiment-manager` 用 family card 合并路线 |
| 论文 claim 先写后补证据 | `sci-research-manager` 要求 claim-evidence map 与 evidence packet |
| 对外包中夹带未审核披露或本地材料 | 最终提交门运行披露候选扫描并阻断 incomplete scan |
| 强框架跑得好就当自己贡献 | direction decision 标记为 `reference_only`，不自动变主线 |

## 7. 最小可用流程

如果你只想先用起来：

```text
1. Initialize HANDOFF / QUERY_MAP and one authoritative experiment current-state index.
2. 把已有实验补成 cards。
3. 让 Codex 用 sci-research-manager 做一次 route review。
4. 把结论写入 DECISION_LOG。
5. 写论文前用 sci-result-auditor 审计 claim map，再由 academic-manuscript-writing 选择阶段。
```

这就足够把一个长期项目从“凭记忆推进”变成“按证据推进”。
