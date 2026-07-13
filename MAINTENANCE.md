# Maintenance Workflow

这是 `sci-research-codex-skills` 的唯一维护流程入口，适用于文档、Skill、脚本、CI、Pages 和 Release。`AGENTS.md` 定义不可越过的行为边界；本文件定义日常更新怎样执行、验证、发布和回滚。

## 不可破坏的保证

- 已发布的标签和 Release 不移动、不复用、不通过强制推送改写。
- 仓库名和 8 个公开 Skill 名称保持兼容；破坏性变化只能进入明确批准的新主版本。
- 维护不改写研究项目中的原始资产、时间戳、实验结果或证据状态。
- 凭据、个人绝对路径、未公开数据、缓存和本地生成物不得进入提交。
- 所有公开变化经分支、Pull Request、CI 和 `main` 合并；不直接在 `main` 上试错。
- `VERSION`、Changelog、README、Pages、标签和 Release 的版本声明必须一致。

## 维护事实源

| 内容 | 唯一事实源 | 同步对象 |
|---|---|---|
| 当前稳定版本 | `VERSION` | README、Pages、Changelog、Git 标签、GitHub Release |
| 未发布变化 | `CHANGELOG.md` 的 `Unreleased` | PR 描述与后续 Release notes |
| Agent/Skill 边界 | `AGENTS.md` 和各 Skill 的 `SKILL.md` | 贡献指南、模板、测试 |
| 自动验证 | `scripts/maintenance_check.py` 和 `tests/` | PR CI、月度巡检 |
| 公开入口 | `README.md` 和 `docs/index.html` | GitHub About、Topics、Pages |
| 历史版本 | 不可移动的 annotated tag | GitHub Release 和源码归档 |

发生冲突时，先保护安全、证据和已发布历史，再修正文档或自动化；不要为了让检查变绿而降低边界。

## 变化分类

| 类型 | 版本处理 | 必须更新 |
|---|---|---|
| 拼写、链接、社区配置、内部维护 | 保持当前版本，记入 `Unreleased` | 相关文档、测试或配置 |
| 向后兼容的错误修复 | 下一个 patch | VERSION、Changelog、README、Pages、Release |
| 向后兼容的新能力 | 下一个 minor | 同上，并补测试与使用说明 |
| 改名、删除、状态语义或行为破坏 | 下一个 major，需明确批准 | 迁移说明、兼容策略、完整前向测试 |
| 安全问题 | 先私密处理，再决定 patch/minor | SECURITY、修复测试、发布说明 |

版本没有固定发布时间；只有经过验证、能够清楚说明兼容边界的变化才进入 Release。

## 日常更新流程

### 1. 恢复现场并确定范围

```bash
git switch main
git pull --ff-only origin main
git status -sb
python scripts/maintenance_check.py check
```

先阅读 `AGENTS.md`、本文件和目标 Skill 的完整 `SKILL.md`。把已有未提交内容视为他人工作；范围混杂时不要使用 `git add -A`。

### 2. 创建单一目的分支

```bash
git switch -c agent/short-description
```

一次 PR 只解决一个可描述的维护目标。用户可见变化立即记入 `CHANGELOG.md` 的 `Unreleased`；日常开发不提前修改 `VERSION` 或已发布条目的日期。

### 3. 实现并验证

最低验证集：

```bash
python scripts/maintenance_check.py check
python -m unittest discover -s tests -v
git diff --check
```

修改 Skill 时再运行官方快速校验：

```bash
VALIDATOR="${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-creator/scripts/quick_validate.py"
for skill in skills/*; do
  test -f "$skill/SKILL.md" && python "$VALIDATOR" "$skill"
done
```

修改协调器、证据语义、实验状态或写入行为时，增加真实但只读的前向测试；修改 Python 时运行类型检查。不要用 mock 结果冒充真实证据。

### 4. 提交、PR 和合并

1. 只暂存确认属于本次范围的文件。
2. 使用简短、可检索的提交标题。
3. 推送 `agent/*` 分支并创建草稿 PR。
4. PR 描述写清变化、原因、用户影响、安全/兼容边界和验证结果。
5. 等待所有 GitHub Actions 成功，再转为 ready 并用普通 merge commit 合并。
6. 合并后确认 `main` 的 tests 与 Pages 均成功，再删除临时分支。

## 发布流程

### 1. 准备发布 PR

1. 按语义化版本确定 `X.Y.Z`。
2. 将 `Unreleased` 内容整理为 `## [X.Y.Z] - YYYY-MM-DD`，保留旧版本日期不动。
3. 更新 `VERSION`、README 的当前版本与 Release 链接、Pages 版本入口和 Changelog 比较链接。
4. 运行日常最低验证集；若涉及 Skill，再运行全部 Skill 快速校验和必要前向测试。
5. 通过独立发布 PR 合并到 `main`。

### 2. 验证 release candidate

同步干净的 `main` 后运行：

```bash
git switch main
git pull --ff-only origin main
python scripts/maintenance_check.py release-candidate
```

此检查要求：工作区干净、当前分支为 `main`、本地与 `origin/main` 一致、版本高于已有标签、目标标签尚不存在，并且版本文档一致。

### 3. 创建不可移动版本

```bash
VERSION="$(tr -d '\n' < VERSION)"
git tag -a "v${VERSION}" -m "SCI Research Codex Skills v${VERSION}"
git push origin "refs/tags/v${VERSION}"
gh release create "v${VERSION}" --verify-tag --title "v${VERSION}" --notes-file RELEASE_NOTES.md
```

`RELEASE_NOTES.md` 只作为本地临时文件，不提交；内容从对应 Changelog 条目整理，必须包含兼容性、安全边界和验证结果。

### 4. 发布后核验

```bash
python scripts/maintenance_check.py verify-tag "v${VERSION}"
gh release view "v${VERSION}"
gh run list --branch main --limit 5
git status -sb
```

确认 Release 为预期版本、标签指向正确提交、CI 与 Pages 成功、工作区干净。发布说明写错时只编辑说明；代码或标签错误时发布新的 patch，不移动旧标签。

`v1.0.0` 是建立本流程前的历史基线；从 `v2.0.0` 开始使用完整版本一致性核验。

## 自动巡检

- 每次 push 和 Pull Request：运行维护一致性检查与完整单元测试矩阵。
- 每月 1 日：定期工作流重新检查仓库一致性、测试和当前稳定标签。
- 每月：Dependabot 检查 GitHub Actions 更新，并以独立 PR 提交。
- 每季度人工检查：仓库 About/Topics、Pages、Releases、私密漏洞报告、未处理 Issue/PR、失效外链和废弃 Action 警告。

定期工作流只读，不自动修改文件、合并 PR、移动标签或创建 Release。

## 回滚与事故处理

- 普通回归：为问题提交创建 `git revert` PR，完整跑 CI 后合并。
- 已发布回归：保留原标签，先在 Release 说明中标记已知问题，再发布修复 patch。
- 安全问题：使用 GitHub 私密漏洞报告，避免在公开 Issue、日志或 PR 中暴露利用细节。
- 凭据误提交：立即轮换凭据；是否重写历史需要单独授权和影响评估，不能把普通回滚当作凭据清除。
- Pages 或 CI 平台故障：记录外部状态，不通过放宽测试或删除安全检查来规避。

## 交接记录

长期维护任务结束时至少留下：

```text
main commit:
current VERSION:
latest Release:
Unreleased summary:
open PR/Issue:
local validation:
GitHub CI/Pages:
known risk or blocker:
next safe action:
```

交接是导航信息，不替代 Git、Changelog、测试结果或 Release 事实。
