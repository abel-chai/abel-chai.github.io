---
title: linux常用命令
date: 2024-07-08 11:16:13
tags:
- 小技巧
categories:
- linux
---

## linux常用命令

显示磁盘使用情况

```shell
df -h  # 显示磁盘空间使用情况
du -h --max_depth=1  # 显示当前目录的磁盘使用情况
```

查看指定端口的进程信息

```sh
lsof -i :8888
```

指定显卡用于后台执行程序

```sh
CUDA_VISIBLE_DEVICES=0 nohup python demo.py > out.log 2>&1 &
```

查看进程信息

```sh
ps  # 显示当前用户的所有进程(不包括进程调用的子进程)
ps -aux  # 显示所有用户的进程详细信息

ps -aux | grep xxx  # 查看指定进程信息(如 ps -aux | grep python )

top  # 实时显示系统中各个进程的资源占用情况(所有用户)、q 退出
top -u xxx  # 实时显示系统中各个进程的资源占用情况(指定用户)
top -u xxx | grep yyy  # 实时显示系统中指定进程的资源占用情况(指定用户)
```

压缩包分包以及合并

```shell
split -b 500m test.tar archive.part  # 500MB为每个分包的大小, archive.part是分包的前缀

cat archive.part.* > test.tar  # 合包
```

