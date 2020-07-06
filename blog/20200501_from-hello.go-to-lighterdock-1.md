# 从hello.go到lighterDOCK（一）在国内编译moby

>   众所周知，由于国内的网络环境，诸如docker.com, github.com, debian.org, golang.org等网站的连接速度并不理想。因为`moby`的编译并不仅仅是本地编译，而是需要很多的网络依赖包，在编译的过程中需要频繁地从以上网站下载资源。这篇文章详细地讲述了怎样在国内的网络环境编译`moby`。

## 教程环境

* Ubuntu Server 20.04
* Docker v19.03.8, build afacb8b7f0
* Go v1.13.8 linux/amd64
* Moby v19.03.8 [commit f6163d3](https://github.com/moby/moby/tree/f6163d3f7a10c5d01a92bc8b86e204d784b2f6d6)
* 需要一个socks&http(s)代理，能够通过`export`命令导入运行环境即可。

## 准备工作

### 安装Docker

`Ubuntu 19`及以前的安装方式可以参考[菜鸟教程](https://www.runoob.com/docker/ubuntu-docker-install.html)的安装方式，`Ubuntu 20.04`的安装方式可以参考[这篇文章](https://linuxconfig.org/how-to-install-docker-on-ubuntu-20-04-lts-focal-fossa)来安装。

`Ubuntu 20.04`将Docker纳入了官方仓库，安装Docker会更方便一些：

```bash
sudo apt install docker.io
```

### 将moby clone到本地

`moby`是构建`docker`的核心开源部分，任何人都能在[官方仓库](https://github.com/moby/moby)贡献代码。

```bash
git clone https://github.com/moby/moby.git
```

## 修改部分

### 权限修改

一些脚本需要修改权限，这里列举一些我遇到的脚本：

```bash
sudo chmod a+x ./contrib/download-frozen-image-v2.sh
sudo chmod a+x ./hack/dockerfile/install/install.sh
```

### 代理配置

首先准备一个socks&http(s)代理。然后修改以下文件

`./makefile`文件大概第278排，需要添加一行`--build-arg ALL_PROXY=xxxxx`：

```makefile
bundles/buildx: bundles ## build buildx CLI tool
	docker build -f $${BUILDX_DOCKERFILE:-Dockerfile.buildx} -t "moby-buildx:$${BUILDX_COMMIT:-latest}" \
		--build-arg BUILDX_COMMIT \
		--build-arg BUILDX_REPO \
		--build-arg ALL_PROXY=socks5://[这里写IP地址]:[这里写socks5端口] \  # by saafo
		--build-arg GOOS=$$(if [ -n "$(GOOS)" ]; then echo $(GOOS); else go env GOHOSTOS || uname | awk '{print tolower($$0)}' || true; fi) \
		--build-arg GOARCH=$$(if [ -n "$(GOARCH)" ]; then echo $(GOARCH); else go env GOHOSTARCH || true; fi) \
		.
```

`./hack/dockerfile/install/install.sh`文件，在开头部分添加三个proxy配置：

```bash
set -e #原来就有的
set -x #原来就有的

export all_proxy=socks5://[这里写IP地址]:[这里写socks5端口] # by saafo
export http_proxy=http://[这里写IP地址]:[这里写http端口] # by saafo
```

## 编译部分

### 构建编译Docker的环境

在仓库根目录使用命令

```bash
export all_proxy=socks5://[这里写IP地址]:[这里写socks5端口] #导入一次即可
make build DOCKER_BUILD_ARGS="--network=host"
```

进行编译。

这个部分的速度取决于你的代理速度，我的垃圾代理大概花了110分钟完成。完成之后可以使用`docker images`查看刚创建的`docker-dev`镜像，于是我们便有了编译docker源码的环境了。如果前一个部分编译过慢，可以尝试在[这里](https://hub.docker.com/repository/docker/saafo/docker-dev)下载我编译好的镜像。

### 编译Docker

一个脚本需要修改权限：

```bash
sudo chmod a+x ./hack/make.sh
```

在仓库根目录使用命令

```bash
make binary DOCKER_BUILD_ARGS="--network=host"
```

进行编译，大概两分钟就编译好了。

可以看到编译出来的结果在`./bundles/binary-daemon`目录。至此，编译结束。