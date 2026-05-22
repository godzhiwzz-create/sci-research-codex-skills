---
name: sci-paper-reader
description: Deep-read academic papers into a fast, intuitive "I understand this paper" artifact for SCI/CVPR projects. Use when the user gives a paper and wants an MD/PPT/HTML/Word-style explanation that makes the paper's problem, idea, method, evidence, figures, results, limitations, and relation to other papers clear as if they had spent serious time reading it. Also supports project-facing mechanism extraction and experiment-design handoff while keeping literature separate from experiment evidence.
---

# sci-paper-reader

## Core Principle

Read papers so the user can quickly understand the paper as if they had spent
serious time with it.

This skill is not for generic summaries or bullet-note dumps.  It converts a
paper into a **Paper Understanding Packet**:

- what the paper is about;
- why the problem matters;
- what gap it attacks;
- the paper's core idea in plain language;
- how the method works step by step;
- how to read the main figures/tables;
- what evidence supports the claim;
- what the limitations and hidden assumptions are;
- how it relates to other papers;
- what it means for the current project.

Literature is the ground, but it is not experiment evidence.  A paper can
inspire a hypothesis; only project experiments can support project claims.

## Default Deliverable

Unless the user asks for a specific format, produce a Markdown file:

```text
paper_understanding.md
```

For projects that prefer Chinese reading artifacts, the default language is
**Chinese**.
Important definition sentences, claims, or paper-original phrases may be quoted
briefly in the original language when they help precision, but the explanation,
route, figure guide, and project implication should be written in Chinese.

It should be readable by someone who has not read the paper.  The default is
not a short abstract summary.  It is a compact, complete understanding artifact.

Optional output formats:

- `paper_understanding.md`: default, fastest, easiest to edit.
- `paper_understanding.html`: when the user wants browser-style visual
  reading with diagrams, navigation, proof cards, and self-drawn architecture
  / mechanism figures.
- `paper_understanding_obsidian.md`: when the user wants an Obsidian-friendly
  structure with callouts, Mermaid diagrams, backlinks, tags, and block-level
  notes.
- `paper_understanding.docx`: when the user wants a polished document.
- `paper_deepread.pptx`: when the user wants a teaching/report deck.

The content standard is the same across formats: clear route, plain-language
explanation, figure guidance, and relation to other papers.

## Storage And Production Order

For long-term literature libraries, store each paper as:

```text
<paper_category>/<paper_title_slug>/
  <paper_title_slug>.pdf
  <paper_title_slug>_understanding_<YYYYMMDD>.md
  <paper_title_slug>_visual_<YYYYMMDD>.html
  assets/
    figure_table_crops.png
    assistant_drawn_diagrams.png
    render_previews.png
  README.md
```

Always write the Markdown understanding file first.  Build HTML, PPT, Word, or
Obsidian derivatives from that Markdown logic.  A visual artifact may improve
layout and add diagrams, but it must not invent a different proof route from the
Markdown.

The main artifact must explain the paper itself before connecting to the current
project.  Put project-specific interpretation at the end under an explicitly
dated module, for example:

```markdown
## Project Attachment: <project/topic name>

- Date: YYYY-MM-DD
- Current project stage:
- Why this paper matters for this project:
- What it supports:
- What it does not support:
- Hypotheses or diagnostics suggested:
- Evidence boundary:
```

Do not let the current project lens dominate the paper body.  Project-specific
implications belong in the final project attachment unless the user explicitly
asks for a project-only reading.  The paper body should remain useful to a
future project with a different topic.

For visual HTML / Obsidian outputs, do not create a text-only dump.  Include
at least:

1. the original English paper title as the main title, followed by a clear
   Chinese subtitle/translation;
2. a paper identity opening block covering authors, venue/year, paper type,
   source status, and journal/partition notes.  If the paper is a conference
   paper, explicitly say that journal JCR/CAS partitions do not apply;
3. an abstract/front-page screenshot when available, plus a Chinese abstract
   interpretation that explains the problem, core idea, hidden assumptions,
   outputs, and what the abstract does **not** prove;
4. a reading route / navigation structure;
5. a method-flow diagram;
6. a mechanism or architecture diagram drawn by the assistant when useful;
7. selected original paper figure/table crops when they materially improve
   understanding, preserving aspect ratio and using layout that adapts to the
   crop instead of stretching the image;
8. figure/table proof cards explaining what each paper figure proves;
9. project-facing implication cards;
10. clear distinction between paper evidence and project evidence.

Compression standard: "精炼" means removing redundancy and preserving the
evidence route; it does **not** mean making the artifact so short that the user
must return to the original paper to understand the main claim, method, figures,
limitations, and project implications.

## Deep Reader Support Files

For a serious visual deep-read packet, keep this `SKILL.md` as the coordinator
and load only the needed support file:

- Read `references/packet_schema.md` when building a full Markdown-first paper
  understanding packet.
- Read `references/evidence_spine.md` when the paper's proof route, figure
  logic, or relation to other papers is unclear.
- Read `references/html_visual_guidelines.md` before creating a visual HTML
  artifact with screenshots, assistant-drawn diagrams, and figure proof cards.
- After creating HTML, run
  `python scripts/check_html_assets.py <paper_understanding.html>` to catch
  missing local images and zero-byte visual assets.

The deep reader workflow is embedded here.  Do not create a separate standalone
paper-reading skill unless the user explicitly asks for a portable export.

## Relationship To Other Skills

Use this skill as the coordinator for serious paper reading.

- Use `sci-literature-manager` for paper discovery, library indexing, source
  verification queues, and reading-route maps.
- Use `nature-reader` when the user needs a full bilingual/source-grounded
  Markdown reader.
- Use `deckforge-paper2ppt` when the user needs a serious evidence-spine PPT
  with beginner-readable narration and screenshot QA.
- Use `nature-paper2ppt` only for quick lightweight decks.
- Use `sci-research-manager` when the paper changes the research direction.
- Use `sci-experiment-manager` only after this skill produces an
  experiment-facing literature brief.

## Stage Detection

Classify the task first:

- `paper_triage`: decide whether a paper is worth reading.
- `paper_understanding_packet`: create the default "I understand this paper"
  artifact.
- `single_paper_deep_read`: deeply read one paper.
- `multi_paper_synthesis`: compare a paper set.
- `problem_driven_reading`: read papers to solve a project bottleneck.
- `ppt_deep_reading`: create a teaching deck.
- `experiment_literature_handoff`: turn reading into validation requirements.
- `maintenance`: update reading indexes, skill routes, or cleanup.

## Startup For Projects With A Literature Layer

If the project has a `research_workspace/literature/` layer, first read:

1. `PROJECT_HANDOFF.md`
2. `research_workspace/literature/索引与队列_Index_and_Queues/LITERATURE_QUERY_MAP.md`
3. `research_workspace/literature/索引与队列_Index_and_Queues/LITERATURE_INDEX.md`
4. matching literature manifest / paper card / source PDF

Read experiment cards only when the user asks to connect literature to project
evidence or design an experiment.

## Reading Modes

### Mode A — Paper Understanding Packet

Use this as the default when the user says:

- "读一下这篇论文";
- "快速了解这篇论文";
- "做成 md / ppt / html / word";
- "让我像读完一样知道它在讲什么";
- "讲清楚它和其他论文的关系".

Required output structure:

```markdown
# Paper Understanding Packet

## 0. 一分钟讲明白
- 这篇论文在解决什么问题
- 它为什么需要一个新想法
- 核心想法是什么
- 主要证据是什么
- 最重要的局限是什么

## 1. 论文身份
- 标题 / 作者 / 会议年份 / 来源状态
- 论文类型：方法 / 数据集 / 理论 / benchmark / review
- 它属于哪条研究线

## 2. 这篇论文为什么会出现
- 用中文讲背景
- 前人方法解决不了什么
- 这个问题为什么重要

## 3. 核心命题
- 论文主张什么
- 它认为问题的根因是什么
- 它提出的新原则 / 新方法是什么

## 4. 方法路线图
- 输入是什么
- 主要步骤 / 模块是什么
- 训练 / 监督 / 目标是什么
- 输出是什么
- 哪些是真创新，哪些是借用已有工具

## 5. 图表阅读指南
- Figure 1：看什么，证明什么
- Figure 2：看什么，证明什么
- 关键表格：哪些数字重要，为什么重要

## 6. 证据链
- 主结果
- 消融 / 诊断
- 鲁棒性 / 泛化
- 失败案例 / 局限证据

## 7. 和其他论文的关系
- 继承了什么
- 改了什么
- 和谁竞争
- 启发了哪些后续论文 / 项目方向

## 8. 最该记住什么
- 3-5 条耐用结论
- 不能过度声称什么
- 什么时候该用这篇论文

## 9. 对当前项目的启发
- 它提示我们的问题是什么
- 它提供哪些变量 / 控制 / 诊断思路
- 它支持 continue / redirect / reference_only / stop 哪种决策
```

For a project paper, the packet must make the user feel:

```text
I know what this paper is trying to solve, how it solves it, why the evidence
matters, where it sits in the literature, and what I can use from it.
```

### Mode B — Fast triage

Use when deciding whether a paper belongs in the library.

Output:

1. bibliographic status and source;
2. problem addressed;
3. mechanism in one paragraph;
4. relevance to current project;
5. read / defer / reject decision;
6. verification gaps.

### Mode C — Project-facing deep read

Use for papers that may affect direction or experiment design.

Output shape:

```markdown
# Paper Reading Brief

## 1. Source and verification
## 2. Paper problem
## 3. Claimed cause / mechanism
## 4. Method principle
## 5. Evidence spine
## 6. Key figures / tables to inspect
## 7. What this changes for our project
## 8. Variables and controls to extract
## 9. Risks, confounds, and non-transferable parts
## 10. Experiment-facing validation requirements
## 11. Decision: use / reference_only / verify_more / reject
```

### Mode D — Multi-paper synthesis

Use when several papers must answer one project question.

Do not summarize each paper independently and stop.  Build a comparison:

| Paper | Problem | Mechanism | Useful variable | Control / risk | Project role |

Then synthesize:

1. where papers agree;
2. where they conflict;
3. what they do not answer;
4. what the project must test itself;
5. which direction should continue, redirect, or stop.

### Mode E — Full paper reader

Use when the user wants complete bilingual or source-grounded reading.

Follow `nature-reader`:

- preserve original/translation alignment;
- keep page/block anchors;
- place figures/tables near discussion;
- produce `paper.md`, `source_map.json`, and assets when needed.

Still add a short project-facing brief at the top or as a companion file.

### Mode F — Deep PPT

Use when the user wants a paper-to-PPT deck that teaches the paper.

Follow `deckforge-paper2ppt`:

- write an evidence spine before slide design;
- begin with abstract screenshot and abstract promise map when useful;
- use claim -> proof object -> explanation -> implication;
- preserve screenshot aspect ratio;
- render/QA the deck;
- keep enough visible explanation and speaker notes for a reader who has not
  read the paper.

The deck must not replace the reading brief.  A good PPT comes from a good
evidence spine.

### Mode G — HTML or Word explainer

Use when the user wants a more visual or shareable explanation but not a PPT.

HTML should include:

- a top-level thesis box;
- section navigation;
- figure/table explanation blocks;
- relation-to-other-papers map;
- project implication box.

Word/docx should include:

- clean heading hierarchy;
- figure/table callouts;
- compact relation table;
- final takeaways and project-use section.

Use document/presentation tooling as needed, but keep the intellectual structure
from the Paper Understanding Packet.

## Evidence Spine Contract

For any serious read, build this before outputs:

```text
paper problem
-> paper's claimed cause
-> method principle
-> proof objects
-> result / ablation interpretation
-> limitation
-> project implication
-> next validation requirement
```

If the spine is unclear, do not make slides or experiment plans yet.

## Reader Empathy Rules

Write as if the reader is smart but has not read the paper.

Do:

- explain prerequisite terms before using them heavily;
- say why a figure/table matters before interpreting details;
- distinguish "paper claims" from "paper proves";
- narrate the logic, not just the section order;
- show what is new, what is inherited, and what is only engineering.

Do not:

- paste abstract-level paraphrases as the whole answer;
- list modules without explaining why they exist;
- cite results without explaining what comparison makes them meaningful;
- say "improves performance" without saying against what and why;
- bury the relation to other papers at the end as a vague paragraph.

## Project-facing Question Template

When reading for a project bottleneck, ask:

1. Does the paper explain the current failure mode or only provide a tool?
2. Does it define a cleaner physical/statistical/algorithmic factor than the
   project's current cue?
3. Does it distinguish the relevant factors instead of mixing them into one
   scalar or module?
4. Does it propose a role for the signal: condition, target, context,
   diagnostic, calibration, or decision?
5. What controls would prevent another plug-in or shortcut mistake?
6. Does it transfer to the target domain, or only source/synthetic settings?
7. What minimal no-training diagnostic follows?

## Experiment Handoff Contract

Before handing off to `sci-experiment-manager`, produce:

```markdown
## Literature-to-Experiment Brief

Hypothesis:
Theory:
Papers used:
Variables / cues:
Required controls:
Minimal validation:
Success criteria:
Failure criteria:
Risks:
Do-not-do-next:
Recommended stage:
```

Do not create experiment IDs, configs, runs, or result files in this skill.

## Verification Rules

- Do not invent titles, authors, venues, DOIs, arXiv IDs, datasets, metrics, or
  code repositories.
- Mark uncertain items as `needs verification`.
- Prefer official publisher, arXiv, OpenReview, CVF, project pages, or cached
  PDFs.
- Do not cite exact numbers unless source/page/table is verified.
- Do not let a paper override project negative evidence.

## Output Locations

For projects with a literature layer, place outputs under project-specific
folders such as:

- `research_workspace/literature/method_cards/` for stable method cards;
- `research_workspace/literature/research_routes/<route_name>/` for
  problem-driven reading briefs and routes;
- `research_workspace/literature/tooling/` or a project-specific subfolder for
  PPT/HTML tooling outputs;
- `research_workspace/literature/archive/` for superseded generated packages.

Update literature indexes when adding durable outputs.

## Do Not

- Do not produce shallow bullet summaries for important papers.
- Do not start with PPT layout before reading.
- Do not turn a mature method's built-in mechanism into the user's contribution
  without a new project-specific hypothesis.
- Do not use paper claims as project claims.
- Do not create experiment records from literature-only work.
- Do not batch-read a whole library unless the user explicitly asks.
