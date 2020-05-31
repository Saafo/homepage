# 配置 Docker TLS 连接

> 在远程管理`Docker`的时候，例如用`Portainer`来连接远程`Docker`时，默认的方式是在`2375`端口上连接。但`2375`上没有任何的鉴权，所以我们需要用更安全的方式来连接远程`Docker`。
> 
> 本文主要介绍的是通过`TLS CA certificate`, `TLS certificate`和`TLS key`来远程连接`Docker`。 

## 生成 TLS 证书和秘钥

生成证书秘钥可以通过`openssl`，如果不熟悉`openssl`，在这里介绍一种新的工具：`cfssl`

### cfssl
`cfssl` 即 `toolkit for everything TLS/SSL`，能够用简单的命令，通过配置文件来快速生成证书及秘钥。

安装cfssl

```bash
apt install golang-cfssl
```

简单配置，我们只需要两种证书：客户端证书、服务器证书。

首先进入一个独立文件夹：

```bash
mkdir ~/.docker
cd ~/.docker
```

### 初始化CA

```bash
cfssl print-defaults config > ca-config.json
cfssl print-defaults csr > ca-csr.json
```

编辑 ca-config.json:

```json
{
    "signing": {
        "default": {
            "expiry": "168h"
        },
        "profiles": {
            "server": {
                "expiry": "8760h",
                "usages": [
                    "signing",
                    "key encipherment",
                    "server auth"
                ]
            },
            "client": {
                "expiry": "8760h",
                "usages": [
                    "signing",
                    "key encipherment",
                    "client auth"
                ]
            }
        }
    }
}
```

编辑 ca-csr.json:

```json
{
    "CN": "Own CA",
    "key": {
        "algo": "rsa",
        "size": 2048
    },
    "names": [
        {
            "C": "CN",
            "ST": "SC",
            "L": "CD",
            "O": "SynX"
        }
    ]
}
```

### 创建CA证书

```bash
cfssl gencert -initca ca-csr.json | cfssljson -bare ca -
```

可以看到我们生成了三个文件：

* ca-key.pem 私钥(**一定要保存好)
* ca.csr 证书请求文件
* ca.pem CA证书

### 创建服务器证书

```bash
cfssl print-defaults csr > server.json
```

vim server.json:

```jsonc
{
    "CN": "Your Server Name Here",
    "hosts": [
        "192.168.0.136"//Your Server IP here
    ],
    "key": {
        "algo": "rsa",
        "size": 2048
    },
    "names": [
        {
            "C": "CN",
            "ST": "SC",
            "L": "CD",
            "O": "SynX"
        }
    ]
}
```

好了,通过CA证书,私钥,我们来生成服务器证书和密钥

```bash
cfssl gencert -ca=ca.pem \
    -ca-key=ca-key.pem \
    -config=ca-config.json \
    -profile=server server.json \
    | cfssljson -bare server
```

我们可以看到生成了三个文件

```bash
server-key.pem
server.csr
server.pem
```

### 生成客户端证书

```bash
cfssl print-defaults csr > client.json
```

修改 client.json,其中，注意修改以下内容

```json
    "CN": "client",
    "hosts": [""],
```

执行命令：

```bash
cfssl gencert -ca=ca.pem -ca-key=ca-key.pem -config=ca-config.json -profile=client client.json | cfssljson -bare client
```

## 文件处理

至此，我们得到了以下文件：

```bash
root@saafoserver:/etc/docker# ls
ca-config.json  ca-csr.json  ca.pem      client.json     client.pem  server.csr   server-key.pem
ca.csr          ca-key.pem   client.csr  client-key.pem      server.json  server.pem
```

修改文件名：

```bash
mv server-key.pem key.pem
mv server.pem cert.pem
```

将以下文件复制回客户端：

```bash
ca.pem #TLS CA certificate
client.pem #TLS certificate
client-key.pem #TLS key
```

## 启用Docker TLS模式

首先停止运行当前的`Docker`

```bash
systemctl stop docker
```

在这里提供两种简单的`Docker TLS`开启方式：

1. 临时开启

```bash
dockerd --tlsverify \
    --tlscacert=ca.pem \
    --tlscert=cert.pem \
    --tlskey=key.pem \
    -H=0.0.0.0:2376
```

2. 修改配置文件

~~因为懒得写就贴链接了~~

可以参考[这篇文章](https://my.oschina.net/ykbj/blog/1920021)，提供了证书生成脚本和修改Docker配置文件的方式。