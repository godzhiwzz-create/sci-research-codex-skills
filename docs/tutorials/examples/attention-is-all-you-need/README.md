# Attention Is All You Need 精读演示包

这是 `sci-paper-reader` 的公开演示样例。它展示一个完整 paper deep-read packet 应该如何组织，而不是把论文压缩成几条摘要。

## 文件

```text
Attention_Is_All_You_Need_understanding_20260522.md
Attention_Is_All_You_Need_visual_20260522.html
assets/
  source_card.svg
  paper_crop_abstract_frontpage.png
  paper_crop_figure1_transformer_architecture.png
  paper_crop_figure2_attention.png
  paper_crop_table1_complexity.png
  paper_crop_table2_results.png
  paper_crop_table3_ablation.png
  transformer_flow.svg
  attention_mechanism.svg
  evidence_spine.svg
```

## 来源

- arXiv: [Attention Is All You Need, 1706.03762v7](https://arxiv.org/abs/1706.03762)
- Proceedings: [NeurIPS paper page](https://papers.nips.cc/paper/7181-attention-is-all-you-need)
- Access date: 2026-05-22

## 演示重点

- 英文标题 + 中文副标题。
- 论文身份和来源验证。
- 首页摘要区原文截图 + 摘要解读，但不在正文转载完整长摘要。
- 新手预备知识：任务、token、encoder/decoder、baseline、BLEU、parallelization。
- 关键原文图表截图：Figure 1、Figure 2、Table 1、Table 2、Table 3。
- 自绘 Transformer 架构图。
- 自绘 scaled dot-product / multi-head attention 机制图。
- 图表 proof cards：每张关键图表说明“第一眼看到什么、怎么看、证明什么、不能证明什么”。
- 证据线：problem -> cause -> method principle -> proof object -> limitation。
- 新手 FAQ：解释 Attention/Transformer、RNN/CNN、multi-head、BLEU 的常见误解。
- 项目挂接模块只作为公开教程演示，不绑定任何私有项目。

## 如何查看 HTML

在线渲染版：

- [GitHub Pages HTML 演示](https://godzhiwzz-create.github.io/sci-research-codex-skills/tutorials/examples/attention-is-all-you-need/)

本地直接打开：

```text
Attention_Is_All_You_Need_visual_20260522.html
```

或在仓库根目录运行资产检查：

```bash
python3 skills/sci-paper-reader/scripts/check_html_assets.py docs/tutorials/examples/attention-is-all-you-need/Attention_Is_All_You_Need_visual_20260522.html
```
