# 从hello.go到lighterDOCK（二）在国内编译Docker-ce

>   众所周知，由于国内的网络环境，诸如docker.com, github.com, debian.org, golang.org等网站的连接速度并不理想。因为`Docker`的编译并不仅仅是本地编译，而是需要很多的网络依赖包，在编译的过程中需要频繁地从以上网站下载资源。这篇文章详细地讲述了怎样在国内的网络环境编译`Docker`。

## 教程环境

* Ubuntu Server 20.04 (focal)(本文命令为focal的地方，其他版本的同学可以自行替换成对应的代号)
* Docker v19.03.8
* 需要一个socks&http(s)代理，能够通过`export`命令导入运行环境即可。

## 准备知识
首先，我们需要分清`moby`, `docker`, `docker-ce`和`docker-cli`的关系。从`v17.06`版本开始，原来的`docker`项目被改名成了`moby`，`Github`也对`github.com/docker/docker`做了到`github.com/moby/moby`的跳转处理，`moby`会以开源项目的形式继续存在，任何人都可以向其贡献代码。而`Docker`公司将提供`docker-ce`和`docker-ee`两项产品，其中`docker-ce`是面向社区的免费版产品。`docker-ce`和`docker-ee`均以`moby`作为核心，并和其他的部分一起构成整个产品。一般我们指的编译`Docker`，则是指编译`docker-ce`。`docker-ce`包含`moby`(engine)，`cli`和`cli plugins`(可以在/components/packaging/deb目录看出结构)(`rpm`系在/components/packaging/rpm目录)

## 准备工作

**建议全程使用root账户操作，建议使用root账户安装Docker。（因为涉及到将本地文件拷贝到镜像中保留权限的问题）**

### 安装Docker

`Ubuntu 19`及以前的安装方式可以参考[菜鸟教程](https://www.runoob.com/docker/ubuntu-docker-install.html)的安装方式，`Ubuntu 20.04`的安装方式可以参考[这篇文章](https://linuxconfig.org/how-to-install-docker-on-ubuntu-20-04-lts-focal-fossa)来安装。

`Ubuntu 20.04`将Docker纳入了官方仓库，安装Docker会更方便一些：

```bash
apt install docker.io #不使用sudo: 这里建议用root账户安装docker
```

### 安装make

```bash
apt install make
```

### 准备alpine镜像

编译过程中会用到alpine镜像，虽然能自动安装，但好像安装后会卡住，可以尝试先运行

```bash
docker pull alpine
```

来提前准备alpine镜像

### 准备代理

```bash
#不一定这样照做，有等效代理即可
export all_proxy=socks5://[这里写IP地址]:[这里写socks5端口] 
export HTTP_PROXY=socks5://[这里写IP地址]:[这里写socks5端口] 
export HTTPS_PROXY=socks5://[这里写IP地址]:[这里写socks5端口] 
```

### 将docker-ce clone到本地

关于`docker-ce`和`moby`等的关系在前文有详细说明，这里不再赘述。

```bash
git clone https://github.com/docker/docker-ce.git
```

### 配置DNS

针对可能出现的`Temporary failure resolving 'archive.ubuntu.com'`或者无法解析`github.com`地址等问题，可以尝试配置宿主机DNS，这里给出一种办法，其他方法可以参考[官方文档](https://wiki.debian.org/NetworkConfiguration#Defining_the_.28DNS.29_Nameservers)

```bash
vim /etc/network/interfaces #在root模式下，不需要sudo
```

这是一个新文件，我们只需要添加一下内容：

```text
auto eth0
iface eth0 inet static
    dns-nameservers 114.114.114.114 8.8.8.8
```

保存即可。如果还是没有解决问题，重启即可。重启后记得设置代理。

## 源文件操作

### 权限问题

需要注意的是项目从`Github` clone下来之后，要注意权限变动问题。比如我遇到的问题是：我的主力机是`MacBook`，通过`Goland` deploy到远程`Ubuntu Server`上。但需要注意的是，在`Goland -> Tools -> Deployment -> Options...`和`Goland -> Preferences... -> Build, Excution, Deployment -> Options` 里，需要将`Preserve Original file permissions(SFTP Only)`改为`Yes`。这样才能保留文件本身的权限。

如果使用不同的工具，类似的权限问题也需要注意。一个简单的检查方法是，`/components/packaging/deb/gen-deb-ver`文件的权限应该是`755`。

### 修改部分

首先准备一个socks&http(s)代理。然后修改以下文件：

#### 镜像换源

`/components/packaging/deb/ubuntu-focal/Dockerfile`第17排：

```Dockerfile
RUN apt-get update && apt-get install -y curl devscripts equivs git
```

改为

```Dockerfile
RUN sed -i s@/archive.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list \
    && apt-get clean \
    && apt-get update --fix-missing && apt-get install -y curl devscripts equivs git
```

这个部分是将构建镜像中的apt源换成阿里云，方便下载资源。如果访问默认源足够快的同学不需要替换。

## 编译部分

进入目录：

```bash
cd components/packaging/deb
```

执行命令：

```bash
make DOCKER_BUILD_ARGS="--network=host" VERSION=18.10.0-ce-dev ENGINE_DIR=/root/docker-ce/components/engine CLI_DIR=/root/docker-ce/components/cli ubuntu-focal
```

这里我指定了Enging和Cli的绝对地址，和我不同的同学需要自行替换。同时我用的是`Ubuntu 20.04(focal)`版本，最后的`ubuntu-focal`可能也需要根据版本替换。`DOCKER_BUILD_ARGS`是指定Docker使用宿主机的网络，以便代理发挥作用。`VERSION`可以去项目根目录的`VERSION`文件查看你的版本信息。


进行编译，首次编译大概在20分钟左右，具体取决于你的网速和机器性能，后续编译因为有资源缓存，一般在5~10分钟。

期间如果有报错信息，可以自行探索解决方案，报错里是能给出很多有用的信息的。如果是网络相关的报错，只有尽量换一个好一点的代理，多试几次。

## 生成文件

可以看到编译出来的结果在`components/packaging/deb/debbuild/ubuntu-focal`目录。至此，编译结束。如下是我生成的文件：

```bash
root@ubuntu:~/docker-ce/components/packaging/deb# ls debbuild/ubuntu-focal/
docker-ce_0.0.0-20200501212840-43e58e6158-0~ubuntu-focal_amd64.buildinfo  docker-ce_0.0.0-20200501212840-43e58e6158-0~ubuntu-focal.dsc
docker-ce_0.0.0-20200501212840-43e58e6158-0~ubuntu-focal_amd64.changes    docker-ce_0.0.0-20200501212840-43e58e6158-0~ubuntu-focal.tar.gz
docker-ce_0.0.0-20200501212840-43e58e6158-0~ubuntu-focal_amd64.deb        docker-ce-cli_0.0.0-20200501212840-43e58e6158-0~ubuntu-focal_amd64.deb
```

使用命令

```bash
dpkg -i docker-ce_0.0.0-20200501212840-43e58e6158-0~ubuntu-focal_amd64.deb
```

进行安装。

如果是对`Docker`要做修改并反复编译，可以参考[这篇文章](https://blog.csdn.net/subfate/article/details/97577041)修改`/components/engine/hack/dockerfile/`下的`*.installer`文件来避免重复下载部分文件。