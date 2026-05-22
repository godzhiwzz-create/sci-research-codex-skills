# 项目管理教程：让 Codex 接管长期 SCI 论文研究记忆

这个教程适合已经有很多实验、文献、报告和草稿的项目。目标不是把文件夹“摆好看”，而是让 Codex 能低成本找回主线、判断证据、解释失败原因，并阻止你把一个失败方向继续调参。

## 1. 先建立项目骨架

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

result_analysis / route_review

## Current Central Question

当前路线真正要回答的是：某个信号是否能解释目标任务失败，而不是它能否被塞进某个 head。

## Evidence Ledger

| Evidence | What it supports | What it does not support |
|---|---|---|
| E003 | 主方法在目标设置中有稳定收益 | 不证明所有域都优于 RGB |
| F012-D01 | 当前一致性目标不成立 | 不否定该研究信号本身 |
| F018-D02 | 当前辅助头有正则化效应 | 不证明目标机制已经成立 |

## Failure Cause

- signal mismatch：信号测到的是 A，但任务需要 B。
- interface mismatch：信号被放进了直接决策层。
- control failure：shuffle / metadata / detector-native statistics 解释了增益。

## Do Not Do Next

- 不加 epoch。
- 不加 seed。
- 不调 loss weight。
- 不再换一个小 head。
- 不把成熟框架的小优化当主贡献。

## Decision

redirect：保留问题，停止当前接口，先做 no-training cause diagnostic。
```

这个输出的重点是“为什么”，不是“又跑什么”。

## 4. 多个实验怎么合并

如果一个方向下有很多小实验，不要让 active 目录塞满几十张卡。用 family card 收束：

```text
cards/
  F012_direction_exploration.md
  _archive/
    F012/
      F012_D01_old_probe.md
      F012_D02_old_probe.md
```

family card 负责记录：

- 方向假设；
- 子实验表；
- 哪些支持；
- 哪些被 control 解释掉；
- 哪些不能再重复；
- 最终 go / redirect / stop。

## 5. 项目管理和论文写作怎么连起来

实验卡只说明实验。论文 claim 还要进入：

```text
research_workspace/paper/CLAIM_EVIDENCE_MAP.md
```

例子：

```markdown
| Claim ID | Claim | Evidence | Strength | Status |
|---|---|---|---|---|
| C001 | 方法解决了某类 shortcut | E001, E006 | strong | supported |
| C002 | 该信号能作为通用任务先验 | F012-D01, F018-D02 | weak | unsupported |
```

写论文前先让 Codex 做：

```text
Use sci-paper-manager and sci-result-auditor.
Audit CLAIM_EVIDENCE_MAP before I write the introduction.
```

## 6. 常见错误

| 错误 | 这套 skills 怎么拦住 |
|---|---|
| 失败后继续调参 | `sci-research-manager` 要求先输出 failure cause 和 do-not-do-next |
| 文件夹越整越乱 | `sci-experiment-manager` 用 family card 合并路线 |
| 论文 claim 先写后补证据 | `sci-paper-manager` 要求 claim-evidence map |
| 项目公开时泄漏隐私 | `sci-asset-manager` 先做 delete / release review |
| 强框架跑得好就当自己贡献 | direction layer 标记为 reference track，不自动变主线 |

## 7. 最小可用流程

如果你只想先用起来：

```text
1. Initialize PROJECT_HANDOFF / QUERY_MAP / EXPERIMENT_INDEX.
2. 把已有实验补成 cards。
3. 让 Codex 用 sci-research-manager 做一次 route review。
4. 把结论写入 DECISION_LOG。
5. 写论文前用 sci-result-auditor 审计 claim map。
```

这就足够把一个长期项目从“凭记忆推进”变成“按证据推进”。
