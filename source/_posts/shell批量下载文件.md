---
title: shell批量下载文件
date: 2024-07-07 12:06:25
tags:
- 小技巧
categories:
- linux
---

## shell 批量下载文件

使用 shell 脚本可以批量下载文件(以 wget 命令为例)

```shell
#!/bin/bash

# 文件数组
files=("https://example.com/1.txt" "https://example.com/1.txt")

# 下载目录
download_dir="/download/"

for url in "${files[@]}"
do
  # 提取文件名
  filename=$(basename "$url")
  
  # 下载文件
  echo "正在下载文件: $filename"
  wget "$url" -o "$download_dir" --progress=bar:force
  
  # 检查是否下载成功
  if [ $? -eq 0 ] 
  then
    echo "$filename 下载成功"
  else
    echo "$filename 下载失败"
  fi
done
```

