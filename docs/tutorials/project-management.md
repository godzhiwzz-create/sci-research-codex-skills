# 项目管理教程：按证据接续科研工作

本教程对应 `main` 的按需工作流。目标是低成本找回问题和证据，不是给每次讨论建立完整项目，也不是把一次失败解释成整个方向无价值。

## 1. 从当前任务进入

| 任务 | 入口 | 何时结束 |
|---|---|---|
| 讨论新方向 | `sci-research-manager` | 回答问题、指出可检验差别和不确定性；不自动下载或运行 |
| 给已知论文入库 | `sci-literature-manager` | 查重、验证缺失身份信息、登记增量 |
| 核对一个数字 | `sci-result-auditor` | 读决定性原始结果和协议，报告冲突；不自行修复 |
| 记录已批准的实验 | `sci-experiment-manager` | 协议、结果、卡片和当前索引闭环 |
| 改一段稿件 | `academic-manuscript-writing` | 按已有阶段完成局部改动；不自动重做全稿审核 |

这里的负责人是当前执行者承担的职责，不要求额外启动代理或让简单任务在多个 Skill 间往返。只有改变项目方向、证据权威或稿件阶段时，才进入对应的集成流程。

## 2. 沿用项目入口，按变化读取

已有项目先遵循自己的 `AGENTS.md` 和目录约定。读取当前任务需要的 HANDOFF、相关索引和卡片；已在当前上下文中完整读过、仍可用且未变的资料不重复加载。适用规则要求重新读取、文件变化或上下文缺失时再补读。

已给出 raw path 或 claim ID 的窄任务可以直接查证；索引用于定位，不是每次必经的仪式。摘要不能替代决定性的原文、原始结果和冻结协议。

```text
Use sci-research-manager to resume this project.
Find the current question and only the evidence needed for the next decision.
Preserve existing records and mark missing evidence as needs_verification.
Do not run experiments or reorganize files.
```

新建长期项目时，按实际需要逐步增加入口：

```text
HANDOFF.md                 # 当前阶段、blocker、下一动作
experiments/
  EXPERIMENTS.tsv           # 一个当前状态机器源
  cards/                   # 已接受并授权的实验
literature/
  SOURCES.tsv              # 项目采用的来源，不复制全局论文库
paper/
  CLAIM_EVIDENCE_MAP.md     # 有 paper-facing claim 时再维护
```

这不是初始化清单。讨论可以只留在回答中；不要为未来可能需要的状态预建空文件。兼容旧 `PROJECT_HANDOFF.md`、`research_workspace/` 和 `EXPERIMENT_INDEX.*`，不强制迁移；若已有索引权威，不再手工维护第二份同义索引。

## 3. 方向审查：结论不超过证据

例如用户问：“这些结果支持继续当前路线吗？”可以返回紧凑证据表：

| 证据 | 支持什么 | 不支持什么 |
|---|---|---|
| E041，冻结协议下的主比较 | 当前任务上的预设 gate 已达到 | 任意任务、设置都有效 |
| F120-D01，负对照 | 当前解释 A 不能独立说明差异 | 原始研究问题没有价值 |
| 最近先例的特定表格/方法节 | 当前方案与已有工作的重合 | 尚未测试差别的结果 |

接着区分已证实原因和竞争解释，给出 `continue / redirect / reference_only / stop / needs_literature` 的依据、边界与下一步。例如：“停止重复当前接口；保留问题，若仍在授权范围内，用一个能区分 A/B 的最小检查决定是否推进。”

`do-not-do-next` 应针对已被证据排除的重复动作，不应变成通用的“不加 seed、不跑消融、不调参数”。预定的统计重复、公平对照和决定性核验照常保留。最近先例要在为新提案投入下载或准备分析前影响决策，但不要求穷尽文献或证明完整因果链才允许小实验。

## 4. 只维护发生变化的记录

实验结果的最小闭环是：

```text
原始结果 + 协议/provenance → 实验卡 → 项目当前状态索引
```

共享结果登记只在证据晋升、替代权威、改变论文 claim 或重要警告时更新；HANDOFF 只在阶段、问题、blocker、活跃任务或下一动作变化时更新。无需另建同义的计划、日报、交接和审计记录。

同一方向的多次实验可以用现有 family card 或索引中的一个综合段落链接起来，写清假设、子实验、反证和仍未测试的边界。默认保留子卡片与原始文件的位置和内容；实际移动/归档需要单独匹配的授权与可恢复方案。

下载或 SSH 任务暂时没有输出时，沿用一个监控负责人和同一任务身份，按工具能力等待通知或有界退避检查。连接退出不等于远端任务结束；状态不明先查原任务，不重复启动。持续等待要有业务期限或明确下一次检查条件，不能无限空转。

## 5. 从证据到稿件

存在论文主张时，把它绑定到已核验证据：

| Claim ID | Claim | Evidence | Claim strength | Evidence status |
|---|---|---|---|---|
| C001 | 方法在冻结任务上达到预设目标 | E041 | main_claim | verified |
| C002 | 方法可推广到任意设置 | F120-D01 | unsupported | verified |

证据已核验，不等于主张获支持。新增或扩大 claim 时核对内部 raw/protocol 或外部论文的精确位置；只修改拼写或格式不需要重启整个证据链。

```text
Use sci-result-auditor to verify the specified claim against its raw result and protocol.
Return findings without modifying evidence.
```

当用户要求实际写作，再由 `academic-manuscript-writing` 按稿件阶段使用该证据。局部任务完成不等于整个阶段完成；全稿转换、最终提交或对外发布才执行匹配范围的完整门控。上传和不可逆提交仍需对应授权。

## 6. 最小可用方式

先给一个具体问题和已有入口，不必先补齐历史库。完成当前问题后，仅在有跨会话价值的状态变化时更新既有记录。缺少能力或决定性证据就报告具体缺口，不自动安装工具、扩大团队或把未知写成否定结论。
