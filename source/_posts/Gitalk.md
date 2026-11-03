---
title: Gitalk
date: 2024-01-13 17:12:02
tags: 
- 插件
categories:
- 开发小工具
---

## Gitalk

Gitalk 是一个基于 Github Issue 和 Preact 开发的评论插件。详情请访问官网 [Gitalk](https://github.com/gitalk/gitalk)

### 安装

---

- npm 安装

```
npm i gitalk  --save 
```

### 使用

---

1. 需要选择一个公共 github 存储库用于存储评论；然后创建 [Github Application](https://github.com/settings/applications/new)，并填写相关信息
2. 应用到页面上

```vue
<template>
    <div id="gitalk-container"></div>
</template>


<script>
   import 'gitalk/dist/gitalk.css'
   import Gitalk from 'gitalk' 
   
    
    var gitalk = new Gitalk({
  	    clientID: 'GitHub Application Client ID',
  		clientSecret: 'GitHub Application Client Secret',
  		repo: 'GitHub repo',
  		owner: 'GitHub repo owner',
  		admin: ['GitHub repo owner and collaborators'],
  		id: location.pathname,  // Ensure uniqueness and length less than 50
  		distractionFreeMode: false  // Facebook-like distraction free mode
	})

	gitalk.render('gitalk-container')
</script>

```

