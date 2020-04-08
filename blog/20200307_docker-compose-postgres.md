# 用docker-compose部署postgresql和pgAdmin4

> 本来一直在用`docker`部署`postgresql`和`pgAdmin4`，但每次部署起来参数很多很麻烦，而且重启容器或者服务器都很麻烦，索性用`docker-compose`来部署。

## 准备步骤

安装`docker-compose`

```bash
apt install docker-compose
```

确定已经pull好`postgres`和`pgAdmin4`镜像，并且已经创建好docker volume:pgdata,若未完成：

```bash
docker pull postgres
docker pull dpage/pgadmin4
docker volume create pgdata
```

然后在任意目录下新建文件`postgres.yml`:

```bash
touch ./postgres.yml
```

## 配置内容

```yml
version: '3'
services:
  postgres:
    image: postgres:latest
    container_name: postgres_dc
    volumes:
      - pgdata:/var/lib/postgresql/data
    environment:
      POSTGRES_USER: yourusername #在此填写postgres的用户名
      POSTGRES_DB: postgres #在此填写postgres的数据库名，默认是postgres
      POSTGRES_PASSWORD: yourpasswd #在此填写posgres的数据库密码
    ports:
      - "5432:5432"
  pgadmin:
    image: dpage/pgadmin4:latest
    container_name: pgadmin_dc
    environment: 
      PGADMIN_DEFAULT_EMAIL: youremail@yourdomain #在此填写pgAdmin登录账户邮箱
      PGADMIN_DEFAULT_PASSWORD: yourpasswd #在此填写pgAdmin密码
    ports:
      - "5050:80"
volumes:
  pgdata:
```

## 部署

在当前目录下运行：

```bash
docker-compose up -d
```

若需停止运行，在当前目录运行：

```bash
docker-compose down
```

## 连接步骤

打开浏览器，输入`localhost:5050`，登录`pgAdmin4`之后，点击添加新服务器，特别注意，在连接地址IP里应该填写docker路由地址，端口填写5432。

### docker路由地址查看方法

```bash
docker inspect postgres_dc
```

在输出内容中找到`Gateway`，对应的地址即为docker路由地址。