# Repository Agent Rules

Scope: the entire `sci-research-codex-skills` repository.

## Start

1. Read `README.md` and the target skill's complete `SKILL.md`.
2. Preserve the repository name and existing public skill folder names unless a breaking rename is explicitly approved.
3. Inspect `git status -sb` before editing; never overwrite unrelated work.

## Skill design

- Keep YAML frontmatter to `name` and `description` only.
- Keep each `SKILL.md` under 500 lines and use imperative instructions.
- Put reusable detail one level below the skill in `references/`; link every reference directly from `SKILL.md`.
- Put deterministic, tested automation in `scripts/` and reusable output material in `templates/` or `assets/`.
- Do not add README, changelog, or installation files inside individual skill folders.
- Keep `sci-research-manager` as lifecycle route owner. Specialist skills may add narrow workflows but must not override project-local rules or promote unsupported evidence.
- Keep project-specific paths, metrics, credentials, datasets, and headline numbers out of portable skills.

## Safety and compatibility

- Default audit tools to read-only output or clearly named generated files.
- Never delete, move, publish, submit, or start remote/expensive work without explicit user authorization.
- Preserve original file timestamps and Git worktree state during maintenance workflows.
- Keep the public names `sci-research-manager`, `sci-literature-manager`, `sci-paper-reader`, `sci-experiment-manager`, `sci-paper-manager`, `sci-result-auditor`, `sci-asset-manager`, and `academic-manuscript-writing` compatible.

## Releases and repository front

- Treat `VERSION` as the canonical release number and keep it aligned with `README.md`, `CHANGELOG.md`, Pages, tags, and GitHub Releases.
- Use semantic version tags on commits reachable from `main`; create annotated tags and never move or reuse a published tag.
- Keep `v1.0.0` immutable as the pre-v2 compatibility baseline.
- Update public-facing version claims, maintenance links, and release notes in the same release change.
- Keep repository description, homepage, topics, issue forms, pull request template, contribution guide, and security policy current.
- Publish a release only after the corresponding commit has passed repository tests and GitHub Actions.

## Validation

Before commit:

1. Run `python -m unittest discover -s tests -v`.
2. Run the system `quick_validate.py` against every skill when available.
3. Compile every Python script without leaving `__pycache__` in the repository.
4. Inspect Markdown links and `agents/openai.yaml` metadata.
5. Forward-test meaningful coordinator changes on realistic read-only tasks.

Do not commit generated test fixtures, caches, local manifests, or credentials.
