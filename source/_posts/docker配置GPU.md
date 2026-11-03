---
title: docker配置GPU
date: 2024-08-01 21:11:09
tags:
- 实用工具
categories:
- docker
---

## docker 配置 GPU

### 1. 配置库

```sh
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
  && curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
    sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
    sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list
```

### 2. 更新源

```sh
sudo apt-get update
```

### 3. 安装 NVIDIA Container Toolkit

```sh
sudo apt-get install -y nvidia-container-toolkit
```

