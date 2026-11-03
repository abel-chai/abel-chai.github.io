---
title: docekr安装
date: 2024-08-01 20:50:24
tags:
- 实用工具
categories:
- docker
---

## 基于 Ubuntu20.04 安装 docker

### 1. 卸载旧版本 docker

```sh
# 卸载旧版本
sudo apt-get purge docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin docker-ce-rootless-extras
# 清除旧版 docker 占用的内存
sudo apt-get remove --auto-remove docker
# 删除无用的相关的配置文件
dpkg -l |grep ^rc|awk '{print $2}' |sudo xargs dpkg -P 
# 删除相关目录
rm -rf /etc/systemd/system/docker.service.d
rm -rf /var/lib/docker  # docker 数据存储地址
# 更新系统源 
sudo apt-get update
```

### 2. 配置安装环境

```sh
sudo apt-get install apt-transport-https ca-certificates curl gnupg-agent software-properties-common
```

### 3. 添加阿里云的 docekr GPG 密钥

```sh
curl -fsSL http://mirrors.aliyun.com/docker-ce/linux/ubuntu/gpg | sudo apt-key add -
```

### 4. 添加阿里镜像源

```sh
sudo add-apt-repository "deb [arch=amd64] http://mirrors.aliyun.com/docker-ce/linux/ubuntu $(lsb_release -cs) stable" 
```

### 5. 查看 docker 版本

```sh
apt-cache madison docker-ce
apt-cache madison docker-ce-cli
```

### 6. 安装最新版 / 指定版本 docker

```sh
#安装最新版 
sudo apt-get install -y docker-ce docker-ce-cli
#安装5:20.10.21~3-0~ubuntu-kinetic版 
sudo apt-get install -y docker-ce=5:27.1.0-1~ubuntu.20.04~focal docker-ce-cli=5:27.1.0-1~ubuntu.20.04~focal
```

### 7. 重启 docker

```sh
sudo systemctl restart docker
```

### 8. 运行 hello-world 验证 docker 是否安装成功

```sh
docker run hello-world
```

