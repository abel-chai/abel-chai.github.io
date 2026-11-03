---
title: docker常用命令
date: 2024-07-23 21:01:12
tags:
- 小技巧
categories:
- docker
---

## docker常用命令

显示当前正在运行的`docker`容器

```shell
docker ps  # -a / --all: 显示所有容器
```

显示本地主机上的镜像

```shell
docker images
```

开启指定容器的交互式终端

```shell
docker exec -it 容器id /bin/bash
```

获取容器长`ID`

```
docker inspect -f '{{.ID}}' 容器名
```

拷贝主机文件到容器中

```
docker cp 主机文件路径 容器长ID:docker容器路径
```

拷贝容器文件到主机中

```
docker cp 容器长ID:docker容器路径 主机文件路径 
```

提交容器副本使之成为一个新镜像

```shell
docker commit -m="提交的描述信息" -a="作者" 容器ID 要创建的目标镜像名:[tag]
```

导出镜像

```shell
docker save -o test.tar 镜像名:[tag]
```

导入镜像

```shell
docker load -i test.tar  # 此时镜像名与标签不变
```

