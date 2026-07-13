# v2 架构与兼容说明

## 一个中枢，七个专门入口

v2 沿用全部原有 Skill 名称，但把跨领域共同纪律收敛到 `sci-research-manager`：

- 用户授权和只读/写入边界；
- 项目启动读取顺序；
- 生命周期阶段；
- 证据层级和冲突仲裁；
- 方向 promotion/stop gate；
- claim 强度；
- Git、时间、迁移和归档保护；
- 收尾与 HANDOFF 更新。

其余 Skill 只维护文献、精读、实验、审计、论文、资产或写作领域的独有流程。这样既保留旧触发名，也减少重复规则和互相覆盖。

## 五个正交字段

旧项目常把阶段、结果好坏、论文用途和证据可信度混在一个 `status` 中。v2 将其拆开：

1. `stage`：当前任务处于研究生命周期哪一段；
2. `experiment status`：实验是否设计、运行、完成、停止或待核验；
3. `evidence status`：artifact 是否 verified、pending、mismatch 或 unsupported；
4. `claim strength`：结果能以多强的语言进入论文；
5. `direction decision`：continue、redirect、reference_only、stop 或 needs_literature。

已有项目有稳定 schema 时继续沿用，并在 handoff 中记录映射，不批量改历史卡片。

## 路径兼容

v1 示例默认使用：

```text
PROJECT_HANDOFF.md
research_workspace/experiments/
research_workspace/paper/
research_workspace/literature/
```

v2 仍能读取这些路径，但 Skill 不再把它们当唯一结构。脚本接受 `--root`、`--cards-dir`、`--index-csv`、`--claim-map` 等显式参数。

## 迁移建议

1. 不移动原始结果、日志、checkpoint、投稿包或 Git worktree。
2. 先增加 README/HANDOFF/QUERY_MAP 导航层。
3. 把会话结果标成 `session_result_pending_artifact`，直到找回 raw artifact。
4. 把协议冲突标成 `protocol_mismatch`，不要用新文档覆盖旧事实。
5. 新实验采用 v2 模板；旧卡只在需要时渐进补字段。
6. 生成索引先写 `.generated.md/.generated.csv`，人工核验后再晋升 canonical。
7. 路径迁移前后用 `provenance_guard.py` 记录并核验时间、大小和可选 hash。

## v1 脚本行为变化

- `generate_experiment_card.py` 继续兼容原来的位置参数，同时新增 F-family ID、`--root`、`--cards-dir`、`--template` 和 `--dry-run`；已存在卡片返回非零且不覆盖。
- `update_experiment_index.py` 同时生成 `.generated.md` 和 `.generated.csv`，不再暗示可直接覆盖人工 canonical index。
- `collect_results.py` 默认输出 `master_results.generated.csv`，并为每行记录 `source_path`。
- `check_project_consistency.py` 默认把报告写到 stdout；只有显式传入 `--output` 才创建报告文件。
- 所有路径参数都可显式指定，旧 `research_workspace/` 只是兼容默认值。

## 发布兼容承诺

- 维持 8 个公开 Skill 名称。
- 不把可选外部 Skill 变成核心依赖。
- 核心测试只使用 Python 标准库。
- 删除或破坏性迁移永远需要明确用户授权。
