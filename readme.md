# My Homepage

[Mintsky's Homepage](http://mintsky.xyz)

>人类的本质是造轮子。

我的博客和随之诞生的辣鸡博客模板

## 技术架构

### 依赖：

* [jQuery](https://jquery.com)
* [marked.js](https://marked.js.org/)
* [hightlight.js](http://highlightjs.org/)
* [github-markdown-css](https://sindresorhus.com/github-markdown-css/)
* [Python-Markdown](https://python-markdown.github.io/)
* [utterances](https://utteranc.es/)

### 结构：

* `index.html`和`rss.xml`为`generator.py`根据原始`index.html`和`/blog`文件夹下的`markdown`文件生成的文件。每次添加新博客后需要手动运行。
* `blog-template.html`为所有博客页面的框架页面，客户端通过读取服务器上的`markdown博客文件`和`blog-template.html`实时渲染出博客页面。
* `/blog文件夹`存放博客。
* 评论系统由[utterances](https://utteranc.es/)提供。

## 使用方法

* clone this repository
* 全文搜索`mintsky.xyz`替换为您的域名，并将有必要修改的地方都修改掉。这是基于我的需求创建的仓库，所以没有做分离，鲁棒性不好。
* pip install markdown
* `nginx`配置：
  ```
  server{
                listen 80;
                server_name blog.mintsky.xyz;
                location = / {
                        return 301 http://mintsky.xyz;
                }
                location / {
                        root (这里放homepage文件夹目录);
                        try_files $uri /blog-template.html =404;
                }
        }
  ```
* 每次更新博客时将`markdown文件`放入`/blog文件夹`，然后运行`generator.py`。

## 注意事项

* 与`Github Pages`不兼容。如果要在其上使用需要修改js文件。
* `utterances`使用第三方cookies导致[401报错的问题](https://github.com/utterance/utterances/issues/123)