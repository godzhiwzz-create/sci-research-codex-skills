# Security Policy

## Supported versions

| Version | Security support |
|---|---|
| 2.x | Supported |
| 1.0.0 | Archived; upgrade to 2.x |

## What to report privately

请私密报告可能导致以下结果的问题：

- 路径越界、任意文件读取或写入；
- 绕过拒绝覆盖或 provenance/mtime 保护；
- 凭据、私有数据或未公开科研结果泄露；
- 未经用户明确授权执行远程命令、提交、发布或昂贵计算；
- 恶意 Skill、模板或项目内容诱导 Agent 绕过安全边界。

## Reporting

使用仓库的 [GitHub private vulnerability reporting](https://github.com/godzhiwzz-create/sci-research-codex-skills/security/advisories/new) 提交报告。请包含受影响版本、最小复现、影响范围和建议缓解措施，但不要附上真实凭据或未公开数据。

如果私密报告入口不可用，请创建一个不含敏感细节的普通 Issue，请求维护者建立私密沟通渠道。不要在公开 Issue、Pull Request 或日志中披露利用细节。

维护者确认问题后会先限制影响范围，再准备修复和发布说明。修复发布前，不会要求报告者公开未解决的细节。
