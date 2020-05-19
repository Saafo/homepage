# flask框架概念理解及部署方式

>   最近写了一个`flask`项目，在整个学习的过程中走了不少的弯路，但同时对`flask`也有了更深刻的理解。我将我的理解做个简单的记录，同时也是一个指路贴，大家可以对`flask`有一个大概的了解，结合自己的需求找到需要学习的知识点进行更进一步的学习。

## 基本概念

### 最简框架解析

我们先来看一个最简单的例子：

```python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
	return 'Hello, World!'
```

首先：`from flask import Flask`我们从`flask`库中导入了`Flask`模块。

`app = Flask(__name__)`我们创建了一个`Flask类`的实例，这个`app`即是我们创建的`WSGI`应用。关于`WSGI`的概念我会在之后讲到，我们只需要先记住，一般情况下，我们写的整个`Flask`项目是一个`WSGI`应用。

关于`__name__`，直接引用官方文档好了：

>第一个参数是应用模块或者包的名称。如果你使用一个单一模块（就 像本例），那么应当使用 __name__ ，因为名称会根据这个模块是按应用方式使用还是作为一个模块导 入而发生变化（可能是‘__main__’，也可能是实际导入的名称）。这个参数是必需的，这样 Flask 才能 知道在哪里可以找到模板和静态文件等东西。更多内容详见Flask 文档。

然后我们使用了`@app.route('/')`。这是一个装饰器，如果不清楚装饰器的概念请先[去了解](https://www.runoob.com/w3cnote/python-func-decorators.html)。这个装饰器使用的是`app`实例当中的`route`方法，因此当`app`WSGI应用运行时，对应的`url`会解析到这个装饰器下的函数中来。

`def hello_world()`即被装饰器修饰的函数，`app WSGI`匹配到`/`的路径后，将转到被`@app.route('/')`修饰的函数。

### 应用情境

可以简单地认为，一个`url`请求的整个处理过程，对应一个独立的`应用情境`。

### 情境全局变量 g

在我们的`WSGI`应用运行起来后，可能有多个请求同时发起，我们可以用不同的应用情境来处理这些同时发起的请求，这个过程由`flask`自动完成。在每一个请求中，我们可能会临时存储一些公共数据，比如数据库的连接和游标，`flask`为此提供了`g`对象，与应用情境具有相同的应用周期。我们在后面“数据库的使用”中展示`g`的具体用例。

>   Note: g 表示“全局”的意思，但是指的是数据在 情境之中是全局的。g 中的数据在情境结束后丢失，因此 它不是在请求之间存储数据的恰当位置。使用session 或数据库跨请求存储数据。

## 进阶了一点点的玩法

### 数据库的使用

除了`@app.route()`装饰器，我们还应该知道的两个装饰器:

*   `@app.before_request()`
*   `@app.teardown_request()`

*   在每个请求开始时，每个请求对应的、被`@app.route()`修饰的函数执行前，会先执行被`@app.before_request()`修饰的函数。
*   在每个请求结束后，弹出应用情境的最后阶段，会执行被`@app.teardown_request()`修饰的函数。

结合前面的知识，我们可以大致设计如下：

*   将数据库的连接信息直接放在py文件的全局变量中（非g)
*   写一个被`@app.before_request()`修饰的`before_request()`函数，将数据库的连接及初始化过程写在这个函数里。并将连接或/和游标存储在对象`g`中。
*   写一个被@app.teardown_request()修饰的`teardown_request()`函数，将数据库的断开过程写在这个函数里。注意在执行断开过程时，要先判断连接对象是否存在。因为无论`before_request()`是否执行成功，都会执行`teardown_request()`函数。

[这是一个连接SQLite3的示例](http://docs.jinkan.org/docs/flask/patterns/sqlite3.html)，[这是一个用`Psycopg2`连接`PostgreSQL`的示例](https://github.com/Saafo/feed-my-fit-be/blob/master/app.py)。

### 双重装饰器

有的时候，在`app.route()`装饰器之外，我们还想再套一层装饰器，比如，在数据库发生错误的时候,我们可以通过自己定义的装饰器来处理数据库错误，并且回滚数据。一个例子：

装饰器定义：

```python
def handle_database_exception():
    def handle(f):
        @wraps(f) #需要from functools import wraps
        def wrapper(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except (DataError, InternalError):
                g.conn.rollback()
                return returnmsg.error("Database Error", 403) #尝试SQL注入或数据不规范时会引发数据库异常，返回异常信息。
        return wrapper
    return 
```

双重装饰器：

```python
@app.route('/user/register') #用户注册
@handle_database_exception()
def register_route():
    return registerlogin.registerlogin(g.cur, g.conn, request.args)
```

注意，两个装饰器一定要注意顺序，自己的处理装饰器一般会写在路径装饰器之后。[代码实例](https://github.com/Saafo/feed-my-fit-be/blob/master/app.py)

### 蓝图和工厂函数

这次比较遗憾的一点是在项目几乎完工的时候才有好好了解一下`蓝图`和`工厂函数`两个概念。

蓝图，即是在中大型项目中组织路由的一种更好的方式，可以让整个项目的架构更加优美。具体实现是，可以把原来集中在一个文件里的`app.route()`分散到不同的文件中，具体使用可以参考[这篇文章](https://spacewander.github.io/explore-flask-zh/7-blueprints.html)

[工厂函数](https://www.runoob.com/design-pattern/factory-pattern.html)，是一个设计模式。这个设计模式运用到`flask`项目中，可以很方便地同时创建多个配置不同的`WSGI`实例。

## 部署方式

### 虚拟环境

各种教程的开篇都在提到“虚拟环境”，无论是Python 2.x还是3.x，都在让先配置虚拟环境。但我认为，如果只是完成简单的项目，并且对系统本身的环境没有洁癖，没有太大的必要去配置虚拟环境。我的情况是，开发机使用了`Anaconda`，宿主机用`Docker`部署，所以没有使用虚拟环境。虚拟环境还是结合实际情况来配置吧。

### 配置导入方式

`flask`提供了多种配置的导入方式，比较方便地，我们可以在创建`app`实例之后，通过

```python
app.config.from_pyfile('config.py')
```

使用`config.py`来加载缺省配置。所有配置都可以直接写在`config.py`文件中，因为看`from_pyfile()`的源码我们可以发现，具体的执行方式是直接运行`config.py`，因此`config.py`本身也可以运行其他的命令。

[一个例子](https://github.com/Saafo/feed-my-fit-be/blob/master/config.py)，在`config.py`中读取`config.json`中的配置。

### WSGI, app.run(), flask run 和 uWSGI

>   Flask应用是一个符合WSGI规范的Python应用，不能独立运行（类似app.run的方式仅适合开发模式），需要依赖其他的组件提供服务器功能。

WSGI是一种规范，具体的介绍可以见[这篇文章](https://zhuanlan.zhihu.com/p/95942024)。

通过将整个项目构成一个WSGI应用，我们可以方便地用专业的服务器来启动这个应用。也就是说，在整个项目中，在调试阶段尽量以`app.run()`作为程序入口，或者用`flask run`来启动项目。尽量避免先运行一段代码，在代码当中调用`app.run()`的项目结构。

`app.run()`或`flask run`可以视为一个简单的开发调试服务器，在开发调试的过程中，用`app.run()`来启动应用足够简单，也可以直接加入`port`、`host`、`debug`等参数。

但你会发现，在使用`app.run()`或`flask run`启动项目时，控制台会有这样的一行警告：

```bash
WARNING: This is a development server. Do not use it in a production deployment.
```

因为`app.run()`和`flask run`仅仅是能处理简单场景的请求，对于一般生产环境如高并发等场景并不完全擅长，所以在开发完毕准备上线时，我们应该用更专业的服务器来启动我们构建的`WSGI`应用。

我们可以安装`uWSGI`，用`uWSGI`来启动项目。`uWSGI`，请自行查阅相关文档博客，本文主要介绍docker部署的方法。

### docker部署

我采用`Docker` + `Docker-compose`的方式来部署到线上。

服务器，我采用的是 `Gunicorn` + `gevent` + `Nginx`的组合。其中`Nginx`是安装在宿主机中，`Gunicorn`和`gevent`是写在镜像中。我们只需提前安装配置好`Nginx`就好。给一个简单的介绍：

*   `Gunicorn`：和`uWSGI`是同一种角色：启动`WSGI`应用的服务器，各有优劣。
*   `gevent`："gunicorn 默认使用同步阻塞的网络模型(-k sync)，对于大并发的访问可能表现不够好，我们可以很方便地顺手套一个gevent来增加并发量"

我们首先将项目依赖写进`./requirements.txt`中，可以用

```bash
pip freeze > requirements.txt
```

来生成当前环境的依赖，但为了缩小镜像大小和缩短构建时间，我们只需要把项目相关的依赖库保留在`./requirements.txt`就好。记得把`gunicorn`和`gevent`也写入文件，构建时作为服务器用。

在项目根目录新建`Dockerfile`来构建镜像文件：

```dockerfile
FROM python:3.8
WORKDIR /build

COPY . .
RUN pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple

CMD ["gunicorn", "app:app", "-k", "gevent", "-b", "0.0.0.0:80"]
```

解释一下最后一行的含义：

*   运行`gunicorn`（我们已经在`./requirements.txt`中写入了`gunicorn`和`gevent`，构建的时候会自动下载安装。
*   启动的`WSGI`应用是在`app.py`文件中的`app`实例。
*   将默认的`sync`库替换成`gevent`库，支持异步处理请求，提高吞吐量。
*   端口绑定容器中的`80`端口，向外界开放。

在项目根目录新建`docker-compose.yml`来描述服务：

```yaml
version: '3'
services:
  {your_service_name}:
    image: {your_image_name}:latest
    container_name: {your_container_name}
    ports:
      - "10800:80"
```

之后将整个项目`deploy`或者复制到服务器上，服务器安装好`Docker`和`docker-compose`之后，进入项目根目录，执行命令：

```bash
docker build -t {your_image_name} .
docker-compose up -d
```

将`Nginx`端口配置好，`proxy_pass`到`localhost:10800`即完成部署。



### 参考文章

[uWSGI安装配置](https://www.runoob.com/python3/python-uwsgi.html)

[Flask + Docker 无脑部署新手教程](https://zhuanlan.zhihu.com/p/78432719)

如果想看语言更技术化的风格，可以参考[这篇文章](https://www.cnblogs.com/zxpo/p/9728899.html)