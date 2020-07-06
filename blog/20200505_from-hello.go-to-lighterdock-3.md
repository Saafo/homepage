# 从hello.go到lighterDOCK（三）知识准备和项目配置

这篇文章会比较水，主要是教程链接和学习路线指引。

对`Docker`源码做出修改，我们需要一些基本的能力，以下给出一些资料和教程。

## Go 语法相关

*   [The Way to Go](https://github.com/unknwon/the-way-to-go_ZH_CN)
*   [Go 语言教程 - 菜鸟教程](https://www.runoob.com/go/go-tutorial.html)

推荐有时间的同学尽量去看一遍`The Way to Go`，菜鸟教程的语法知识点并不是很详细。只需要看前半部分基础语法，第四章看完，能看懂基本的语法就好了。之后遇到了看不懂的语法再去用查字典的方式去看。

## Docker 相关

需要对`Docker`有一些基本的概念和使用经验。

*   [Docker 教程 - 菜鸟教程](https://www.runoob.com/docker/docker-tutorial.html)

需要对以下`Docker`相关的概念和运作方式有了解：

### 容器的概念

*   [容器基础：重新认识Docker容器 - hurt-- - CSDN](https://blog.csdn.net/weixin_40907382/article/details/84399275)

### Export & save, import & load 的区别

*   [docker save load export import的区别 - Chen-ky - CSDN](https://blog.csdn.net/guizaijianchic/article/details/78324646)

### Layer 的概念

*   [理解Docker镜像分层 - Ryan Miao - cnblogs](https://www.cnblogs.com/woshimrf/p/docker-container-lawyer.html)

### Registry 的概念和运作方式

*   [浅谈docker中镜像和容器在本地的存储 - Helios - 知乎](https://zhuanlan.zhihu.com/p/95900321)
*   [手把手教你搭建Docker Registry私服 - yoogurt - 掘金](https://juejin.im/post/5b0f4364f265da08f215d9e8)

### Docker 隔离性及其问题相关（选看）

*   [docker之容器隔离 - Liu Kevin](https://blog.liu-kevin.com/2019/03/15/1-shen-ru-pou-xi-k8s/)
*   [Docker资源隔离和限制实现原理 - LionHeart](http://lionheartwang.github.io/blog/2018/03/18/dockerzi-yuan-ge-chi-he-xian-zhi-shi-xian-yuan-li/)
*   [Docker容器实战(六) - 容器的隔离与限制 - 知乎](https://zhuanlan.zhihu.com/p/85528062)
*   [浅谈Docker隔离性和安全性 - Roger_Wu - DELL]([https://www.dell.com/community/%E6%95%B0%E6%8D%AE%E5%AD%98%E5%82%A8%E5%92%8C%E4%BF%9D%E6%8A%A4-%E8%B5%84%E6%96%99%E6%96%87%E6%A1%A3/%E6%B5%85%E8%B0%88Docker%E9%9A%94%E7%A6%BB%E6%80%A7%E5%92%8C%E5%AE%89%E5%85%A8%E6%80%A7/ta-p/7181817](https://www.dell.com/community/数据存储和保护-资料文档/浅谈Docker隔离性和安全性/ta-p/7181817))

## Docker & moby 编译相关

*   [我的docker随笔12：docker源码编译 - 李迟 - CSDN](https://blog.csdn.net/subfate/article/details/97577018)
*   [我的docker随笔13：docker源码编译进阶篇 - 李迟 - CSDN](https://blog.csdn.net/subfate/article/details/97577041)

两篇结合着看，虽然13中作者宣称与前文(12)相同，但其实内容是不一样的。

### Makefile 相关

*   [Make 命令教程 - 阮一峰的网络日志](http://www.ruanyifeng.com/blog/2015/02/make.html) 

## Docker 源码分析相关

### Docker 命令流程分析

*   [docker源码1-命令的调用流程 - wangwDavid - 简书](https://www.jianshu.com/p/9900ec52f2c1)
*   [【docker 17 源码分析】docker pull image 源码分析 - 张忠琳 - CSDN](https://blog.csdn.net/zhonglinzhang/article/details/53484799)

## 工程相关

### Docker-ce 项目的包管理方式

*   建议学习 go package 的管理方式，虽然`Docker-ce`用的不是最新的方案(`vendor`)，在有时间的情况下大概了解一下还是有好处的，特别是一定要搞懂`vendor`。参考[从 goinstall 到 module —— golang 包管理的前世今生 - Wolfogre](https://blog.wolfogre.com/posts/golang-package-history/)。

*   需要理解`$GOPATH`是什么，在现代的工程中如何处理`$GOPATH`和工程的关系。[一个例子](https://segmentfault.com/q/1010000010846304/#answer-1020000010846783)

### 项目的包管理配置

`Docker-ce`的项目主要由两个部分构成，`/components/cli`和`/components/engine`，分别对应[`docker-cli`](https://github.com/docker/cli)项目和[`moby`](https://github.com/moby/moby)项目。这两个项目相对独立发展，`docker-ce`将它们合并在一起。因此，`cli`和`engine`的包管理也是相对独立的。我们可以在`cli`和`engine`各自的根目录下看到`vendor`文件夹。

但是，实测在`Goland`中，`vendor`的要求是在`$GOPATH/src/[domain]/[name]/[repo]/vendor`下才能识别，并且因为在`go modules`之前的 go 包管理方式还无法解决项目名字更换之后，`import`项目本身某部分必须改名字的问题，~~所以我们需要做一个全局替换。~~实测全局替换涉及到的问题过于复杂，最终我采取了以下策略：

我们需要加两个软链接，将`[yourrepo]/components/cli`和`[yourrepo]/components/engine`两个文件夹创建软连接到`docker`目录下。

以我的环境为例，我从`github.com/docker/docker-ce` fork 到了`github.com/saafo/lighter-docker` ， `domain=github.com`,  `yourname=saafo`, `yourrepo=lighter-docker`。

* 执行以下命令来创建软链接：

```bash
cd $GOPATH/src/github.com
mkdir docker
ln -s ./saafo/lighter-docker/components/cli ./docker/cli
ln -s ./saafo/lighter-docker/components/engine ./docker/docker
```

这样之后，`Goland`就应该能识别`vendor`文件夹，`import`段也不会报错了（当然，可能会提示要不要重新排序，这个看自己吧）。

稍微总结一下，我们创建软链接的时候，目的只是为了方便`Goland`识别相关依赖，不至于产生大面积的`import报错`。而我们在构建编译的时候，如果是远程编译，只需要将项目本身deploy到编译机器上，在项目内进行操作即可。这个时候软链接其实并不会用上。编译过程大概是先构建一个构建`docker`的镜像，然后将项目内的`cli`和`engine`导入镜像内的`$GOPATH/src/github.com/docker/cli`和`$GOPATH/src/github.com/docker/docker`，所以我们其实并不需要改项目名字，`github.com`上的`docker/cli`和`docker/docker`的内容其实并不会影响我们。

