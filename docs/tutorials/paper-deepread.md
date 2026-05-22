# 论文精读教程：从 PDF 到中文深度理解包

这个教程展示 `sci-paper-reader` 的 deep reader 工作流。目标不是生成一份“摘要翻译”，而是生成一份让没读过论文的人也能快速理解论文问题、方法、证据、图表、局限和文献关系的阅读包。

成品示例可以先看：[Attention Is All You Need 精读演示包](examples/attention-is-all-you-need/README.md)。

## 1. 一句话使用方式

把 PDF 或论文链接给 Codex：

```text
Use sci-literature-manager and sci-paper-reader.
Read this paper deeply in Chinese.
First create a Markdown understanding packet, then create a visual HTML packet.
Include abstract screenshot, abstract interpretation, method route, figure/table proof cards, limitations, relation to other papers, and a dated project attachment.
```

## 2. 推荐文件结构

```text
literature/
  <论文分类_English_Category>/
    <论文题目_English_Title>/
      paper.pdf
      paper_understanding_20260522.md
      paper_visual_20260522.html
      assets/
        abstract_crop.png
        figure_1_overview.png
        figure_2_method.png
        assistant_drawn_mechanism.png
      README.md
```

原则：

- MD 是源文件；
- HTML / PPT / Word 是派生展示；
- 论文主体先讲论文本身；
- 项目启发放最后，并写日期，避免污染未来项目阅读。

## 3. 精读包效果预览

### 3.1 开头不是普通摘要，而是“论文身份 + 摘要解读”

```markdown
# Learning Example Representations for Scientific Vision
## 用结构化表示改进科学图像理解

## 论文身份

- Authors: ...
- Venue / Journal: verified venue or journal, 20XX
- Paper type: method paper
- Source status: PDF verified
- Journal partition: conference paper, JCR/CAS journal partition not applicable

## 摘要截图

![abstract](assets/abstract_crop.png)

## 摘要解读

这篇论文的摘要其实在讲三件事：

第一，它认为现有方法把 A 和 B 混在一起，因此在跨域场景中会失败。
第二，它提出的核心不是一个简单模块，而是把表示拆成 ...
第三，它声称在 ... 上有提升，但摘要没有证明 ...
```

### 3.2 方法不是列模块，而是讲清路线

```mermaid
flowchart LR
  A["输入图像 / 数据"] --> B["基础表示"]
  B --> C["关键因子分解"]
  C --> D["训练目标"]
  D --> E["推理输出"]
  E --> F["论文主张的收益"]
```

正文应解释：

- 为什么需要这个中间表示；
- 它解决前人方法的哪个具体缺口；
- 哪个模块是真创新，哪个只是实现工具；
- 训练目标和最终 claim 如何对应。

### 3.3 图表不是贴图，而是 proof card

```markdown
### Figure 2：方法总览

What it shows:
这张图展示了方法从输入到输出的完整路径。

What to look at:
重点看中间的 factorization / alignment / calibration 部分，
它是论文区别于 baseline 的地方。

Comparison/control:
如果后面消融表显示去掉这个部分会下降，Figure 2 就是机制图，
Table 3 则是证明它有贡献的证据。

What it proves:
它证明作者的方法结构确实包含论文声称的关键机制。

What it does not prove:
它本身不证明性能提升，也不证明机制一定有效。
```

这能避免“图放上去了，但读者不知道看什么”。

### 3.4 证据线是整篇论文的骨架

```text
problem
-> claimed cause
-> method principle
-> architecture/mechanism
-> main result
-> ablation
-> robustness
-> limitation
-> relation to other papers
-> project-facing validation requirement
```

如果这条线写不出来，说明还没读懂，不应该急着做 PPT 或实验。

## 4. HTML 视觉包应该有什么

`sci-paper-reader` 已内置 HTML deep reader 规范：

- 英文标题 + 中文副标题；
- 论文身份卡；
- 摘要截图 + 详细摘要解读；
- 阅读路线导航；
- 方法流程图；
- assistant-drawn 机制图；
- 原论文关键图表 crop；
- proof cards；
- limitations；
- relation-to-other-papers map；
- 日期校准的 project attachment。

生成 HTML 后检查本地图像：

```bash
python3 ~/.codex/skills/sci-paper-reader/scripts/check_html_assets.py paper_visual_20260522.html
```

这个脚本会检查 HTML 引用的本地图像是否缺失或为空。

## 5. 和项目的关系要写在最后

项目挂接模块示例：

```markdown
## Project Attachment: 当前项目名

- Date: 2026-05-22
- Current project stage: idea_exploration
- Why this paper matters:
  它提供了一个区分 A/B 因子的建模思路。
- What it supports:
  可以启发一个 no-training diagnostic。
- What it does not support:
  不能直接证明我们的数据集上会提升。
- Suggested validation:
  比较 factor A、factor B、shuffle control、metadata baseline。
- Evidence boundary:
  literature_reference_only, not project evidence.
```

这样做有两个好处：

1. 这篇论文未来给别的项目读时仍然干净；
2. 当前项目不会把文献结论误写成自己的实验证据。

## 6. 常见错误

| 错误 | 正确做法 |
|---|---|
| 只翻译摘要 | 写 abstract interpretation，解释承诺、假设和未证明内容 |
| 只列模块 | 写 method principle 和每个模块存在的原因 |
| 图表只贴不讲 | 每张关键图表写 proof card |
| 读完马上设计实验 | 先输出 literature-to-experiment brief |
| 用当前项目视角重写整篇论文 | 主体讲论文，项目启发放最后 |
| 重要句子全翻译成中文失去精度 | 可以短引原句，但解释用中文 |

## 7. 最小提示词

```text
Use sci-paper-reader.
Create a Chinese paper understanding packet for this PDF.
Do not make it a short summary.
Explain the abstract, problem, method route, key figures/tables, evidence spine,
limitations, relation to other papers, and a dated project attachment.
If you create HTML, preserve figure aspect ratios and run the HTML asset checker.
```

这个提示词已经足够触发 deep reader，而不是普通摘要器。
