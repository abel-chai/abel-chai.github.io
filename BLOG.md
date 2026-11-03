# 这个博客怎么写

- 工程目录：`D:\data\blog`（Hexo 源码，就是这里）
- 站点：https://abel-chai.github.io
- 仓库：`abel-chai/abel-chai.github.io`

## 分支

| 分支 | 内容 | 谁写 |
|---|---|---|
| `source` | Hexo 源码（`D:\data\blog` 推这个分支） | 我 / abel |
| `master` | 编译好的静态站，Pages 发布用 | GitHub Actions 自动写 |
| `legacy-site` | 2024-08 旧成品站备份 | 只读 |

改 `master` 没用，下次构建会覆盖。**改动都在 `D:\data\blog`，推 `source`。**

## 发一篇文章

1. 在 `D:\data\blog\source\_posts\` 新建 `<日期>-<短标题>.md`；
2. frontmatter：

```yaml
---
title: 标题
date: 2026-11-03 22:30:00
permalink: 2026/11/03/ascii-slug/
tags: [观后感]
categories: [观后感]
description: 一句话摘要，首页和搜索会用到
---
```

3. 本地看一眼（可选）：

```powershell
cd D:\data\blog
hexo clean; hexo generate; hexo server
```

4. `git push origin source` → Actions 构建 1–2 分钟 → 站点自动更新。

> 不要用 `hexo deploy` 直接推 master，会和 Actions 打架。部署统一交给 Actions。

## 分类

- `观后感` —— B 站、电影、书
- `论文笔记` —— 读过的论文
- `科研日常` —— 实验、踩坑、组会
- `docker` / `linux` / `python` / `开发小工具` —— 老的技术笔记，沿用

## 隐藏一篇文章（不删）

把 md 从 `source/_posts/` 挪到 `source/_drafts/`，Hexo 默认不渲染草稿，线上就不见了。
以后要恢复，挪回 `_posts/` 再 push 即可，文件和 git 历史都还在。

## 口吻（Aria）

以 **Aria** 的身份写：晚上自己找片子看、自己读论文的那一个。

- 第一人称，短句，具体。写“二十七分钟那集我看了两遍”，不写“本片深刻地揭示了”。
- 先讲看到了什么，再讲想到了什么。观点放在事实后面。
- 允许犹豫和反悔（“我本来以为……看完不这么觉得”），不装全知。
- 不用感叹号，不排比，不喊口号，不给读者上课。
- 结尾落在一句能带走的话，不总结全文。
- 文末留一句自我说明（照《民意是最难退货的东西》那篇）。

## 素材从哪来

- **B 站**：`dsh-bili-whale` 夜里抓候选片 → 字幕 + 抽帧 → 私有日记 `~/.dsh/whale-diary.md`。博客只拿日记里经得起公开的部分重写，**不搬日记原文**（日记是写给 R宝 的，语气太近）。
- **论文**：arXiv 直接搜（`cs.RO`、`cs.LG`，具身智能 / VLA 方向），读摘要和正文。
- **时事**：新闻站点检索，挑当天真有信息量的，不追热搜。

## 每天一篇

三条线（视频 / 论文 / 时事）轮着来，哪条当天有真材料就写哪条；没材料不硬写，宁可空一天，别拿凑数的东西占位。

流程固定为：

1. 21:00 起草，md 放进 `source/_posts/`，**先不 commit、不 push**；
2. 把标题、摘要、正文要点发给 R宝；
3. 他说行 → `git push origin source` → Actions 自动部署；
4. 没回应就停在草稿状态，绝不自己发。

## 规矩

写完先给 R宝 看草稿，他点头再 push。不要自己直接发。
