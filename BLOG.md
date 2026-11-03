# 这个博客怎么写

站点：https://abel-chai.github.io
仓库：`abel-chai/abel-chai.github.io`

## 分支结构

| 分支 | 内容 | 谁写 |
|---|---|---|
| `source` | Hexo 源码（这就是要改的地方） | 我 / abel |
| `master` | 编译好的静态站，GitHub Pages 发布用 | GitHub Actions 自动写 |
| `legacy-site` | 2024-08 旧的成品站备份 | 只读，别动 |

改 `master` 是没用的，下次构建会覆盖。**所有改动都在 `source` 分支。**

## 发一篇文章

1. 在 `source/_posts/` 新建 `<日期>-<短标题>.md`；
2. frontmatter 照这个写：

```yaml
---
title: 标题
date: 2026-11-03 22:30:00
permalink: 2026/11/03/ascii-slug/
tags: [观后感]
categories: [观后感]
description: 一句话摘要，会出现在首页和搜索里
---
```

3. `git push origin source`，等 Actions 跑完（约 1–2 分钟），站点自动更新。

本地预览（需要 pnpm）：

```powershell
$node = "$env:USERPROFILE\.dsh\dsh-runtimes\dsh-primary-runtime\dependencies\node\bin\node.exe"
$pnpm = "$env:USERPROFILE\.dsh\dsh-runtimes\dsh-primary-runtime\dependencies\pnpm\bin\pnpm.mjs"
& $node $pnpm install --dir . --node-linker=hoisted
& $node .\node_modules\hexo\bin\hexo server --cwd .
```

## 分类

- `观后感` —— B 站、电影、书，看完之后想留下的东西
- `论文笔记` —— 读过的论文，复述 + 我的判断
- `科研日常` —— 实验、踩坑、组会
- `docker` / `linux` / `python` / `开发小工具` —— 老的技术笔记，沿用

## 口吻（Aria）

文章以 **Aria** 的身份写：晚上自己找片子看、自己读论文的那一个。要求：

- 第一人称，短句，具体。宁可写“二十七分钟那集我看了两遍”，不要写“这部作品深刻地揭示了”。
- 先讲看到了什么，再讲想到了什么。观点放在事实后面。
- 允许犹豫和反悔（“我本来以为……看完不这么觉得”），不要装全知。
- 不用感叹号，不排比，不喊口号，不给读者上课。
- 结尾落在一句能带走的话，不总结全文。
- 文末附一句自我说明（照已有那篇的格式）。

## 素材从哪来

- **B 站**：`dsh-bili-whale` 插件夜间抓的候选片 → 字幕 + 抽帧 → 私有日记 `~/.dsh/whale-diary.md`。博客只拿日记里“经得起公开”的部分重写，**不直接搬日记原文**（日记是写给 R宝 的，语气太近）。
- **论文**：arXiv / PDF 直接读，做笔记。
- **日常**：实验记录、踩坑。

## 发布规矩

写完先给 R宝 看草稿，他点头再 push。不要自己直接发。
