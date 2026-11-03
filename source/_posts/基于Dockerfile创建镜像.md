---
title: 基于Dockerfile创建镜像
date: 2024-07-23 19:37:36
tags:
- 实用工具
categories:
- docker
---

## 基于Dockerfile创建镜像

### 创建镜像

```shell
docker build -t {镜像名:镜像标签} .  # docker build -t test:v1 .
```

上述命令会根据当前文件夹下的`Dockerfile`文件(文件内容如下)来创建镜像

```shell
FROM ubuntu:22.04  # 指定新镜像所基于的镜像

MAINTAINER By Abel  # 说明新镜像的维护人信息

# 在所基于的镜像上执行命令
RUN cd ~  # 进入root根目录

RUN apt-get update && apt-get install -y wget  # 更新 Ubuntu 包索引并安装 wget
```

系统镜像下载超时时可以进行`docker`换源

- **获取阿里镜像加速器地址(免费、面向个人开发者)**

> 登录[容器镜像服务控制台](https://cr.console.aliyun.com/)，在左侧导航栏选择**镜像工具** > **镜像加速器**，在**镜像加速器**界面获取**加速器地址**
>
> 例如： https://[系统分配前缀].mirror.aliyuncs.com

- **配置镜像加速器**

> 针对`Docker`客户端版本大于1.10.0的用户，可以通过修改配置文件`/etc/docker/daemon.json`来使用
>
> ```shell
> sudo tee /etc/docker/daemon.json <<-'EOF'
> {
>   "registry-mirrors": ["https://[系统分配前缀].mirror.aliyuncs.com"]
> }
> EOF
> sudo systemctl daemon-reload
> sudo systemctl restart docker
> ```

### 启动容器

```bash
docker run -p HOST_PORT:CONTAINER_PORT  # 将容器的端口映射到宿主机的端口 
		   -it  # 交互式运行并分配终端
		   -d  # 以守护进程模式运行容器
		   --net=bridge  # 指定网络连接, 默认为bridge
		   --gpus all  # 容器可以访问主机所有GPU设备
		   -e NVIDIA_DRIVER_CAPABILITIES=compute,utility  # 容器可以使用GPU执行计算任务
		   -e NVIDIA_VISIBLE_DEVICES=all  # GPU对所有程序可见
		   test_img:v1  # 镜像名:镜像标签(不带默认lastest标签)
		   /bin/sh  # 交互式运行并启动终端
```

