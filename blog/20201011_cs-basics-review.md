# 计算机基础知识复习提纲

核心专业课学完了，来面向面经整理一下计算机基础的知识点提纲。







## 操作系统

### 进程管理

#### 进程和线程

知识点&问题

* 进程、线程、协程的概念？
* 进程和线程的区别？
* 为什么会有线程？
* 多线程的意义？
* 多线程会不会导致程序崩溃？

答案

* 进程、线程、协程的概念？
  * 进程是资源分配和管理的基本单位，线程是调度的基本单位。
  * 协程的调度由程序员控制：避免无意义切换，但也失去使用多CPU的能力。适合I/O密集任务。(async/await)
* 进程和线程的区别？
  * 共享空间资源、健壮性、性能
* 为什么会有线程？
  * 性能
* 多线程的意义？
  * 防止单线程阻塞；利用硬件
* 多线程会不会导致程序崩溃？
  * 死锁、内存泄漏导致占用过高

#### 进程调度

知识点&问题

* 进程状态转换图？
  * 长程中程短程？
  * 任务队列？
* 进程调度策略？
* 进程间通信：信号、死锁、同步方式？
* 上下文切换？
* 内核态用户态？
* 锁的类型？

答案

* 进程状态转换图：new, ready(suspend), running, blocked(suspend), exit
  * 长程(new -> ready(suspend))，中程(suspend ->)，短程调度(ready -> running)
  * ready(suspend), blocked(suspend) 队列
* 调度策略：
  * First Come First Served
  * Shortest Job First
  * Shortest Remaining Time Next
  * Round Robin (名字来源：round ribbon, [法国农民圆形签字](http://songkun.me/2018/11/14/2018-11-14-round-robin/)23333)
* 线程同步方式？
  * 临界区Critical Section、互斥量Mutex、信号量Semaphore、事件对象Event
* 经典问题：生产者消费者、哲学家、读写者优先
* 死锁条件？
  * 互斥、持有和等待、非抢占、环路等待
* 基本策略？
  * 鸵鸟策略
  * 检测和恢复：抢占、回滚、进程终止
  * 避免：安全状态、银行家算法（预先演算、按时归还）
* 锁的类型？
  * 自旋锁spinlock 反复循环尝试获取
    * 自旋锁一般适用于线程持有锁的时间比较短，锁的获取和释放频繁的情况。
  * 阻塞锁mutex
  * 互斥锁 条件锁
* 锁策略？
  * 独占锁exclusive lock
  * 共享锁shared lock
  * 可重入锁
  * 公平锁、非公平锁

### 内存管理

知识点&问题

* 连续内存分配
* 虚拟内存
  * 原理？
  * 概念？
  * 存在问题？
  * 策略？
  * 分页分段区别？
  * 优点？
* 堆和栈？

答案

* 连续内存分配
  * 固定分区/动态分区 内零头/外零头
* 虚拟内存
  * 原理：局部性原理
    * 时间上的局部性：最近被访问的页在不久的将来还会被访问
    * 空间上的局部性：内存中被访问的页周围的页也很可能被访问
  * 概念：Page <-> Page Frame, 抽象|中间层：Memory Manage Unit
  * 问题：
    * 缓存 - Tranlation Lookaside Buffer
    * 页数太多 - 反转页表(Inverted Page Table - Hash Table)
    * 颠簸 - 修改算法/程序太多/增加物理内存
  * 策略：分页替换算法
    * Optimal Page Replacement
    * FIFO
    * Least Recently Used
    * Clock Policy / Second Chance
  * 应用：分页和分段的区别
  * 优点：虚拟内存的好处
    * 共享内存，内存保护，按需加载，Copy-On-Write...
* 堆和栈的区别
  * 手动/自动管理
  * 生长方向：底 Data BSS 堆 -> <- 栈 顶

### 文件管理

#### 文件和磁盘


知识点&问题

* 磁盘结构
  * 时延？
  * IOPS?

答案

* 时延：寻道时延、旋转时间、传输延迟
* IOPS: I/O Per Second
* 调度算法
  * FCFS
  * Shortest Seek TIme First
  * SCAN: Elevator algorithm

#### I/O

* DMA

#### 文件系统

知识点&问题

* i-Node作用？

答案：

* i-Node作用？
  * 转换文件的逻辑结构和物理结构

## 计网

### 应用层

知识点&问题

* HTTP
  * Get和Post有何不同,可以反过来用吗？
  * 常见状态码？
    * 200 302 204 400 401 403 404 500 503
  * 条件Get
  * 持久连接
  * Pipeline
  * 会话跟踪：Session和Cookie (Session Storage, Local Storage)
  * 跨站攻击CSRF和XSS
  * HTTP 1.0 1.1 2.0
  * **HTTP和HTTPS**
* [DNS及为什么使用UDP](https://draveness.me/whys-the-design-dns-udp-tcp/)
* SMTP/POP3/IMAP
* JSONP?如何实现跨域
* socket通信过程？
* WebSocket特点？
* RSA公私钥互换？

答案

* Get和Post有何不同,可以反过来用吗？
  * 参数位置，安全性，浏览器支持；可以反过来但需要服务端支持。
* 常见状态码？
  * 200 OK 客户端请求成功
  * 302 Moved Temporarily 请求重定向
  * 304 Not Modified 文件未修改，可以直接使用缓存的文件。
  * 400 Bad Request 由于客户端请求有语法错误，不能被服务器所理解。
  * 401 Unauthonzed 请求未经授权。这个状态代码必须和WWW-Authenticate报头域一起使用
  * 403 Forbidden 服务器收到请求，但是拒绝提供服务。服务器通常会在响应正文中给出不提供服务的原因
  * 404 Not Found 请求的资源不存在，例如，输入了错误的URL
  * 500 Internal Server Error 服务器发生不可预期的错误，导致无法完成客户端的请求。
  * 503 Service Unavailable 服务器当前不能够处理客户端的请求，在一段时间之后，服务器可能会恢复正常。
* 条件Get
  * If-Modified-Since - 304 Not Modified
* 持久连接
  * keep-alive
* Pipeline
  * 性能提升、时间缩短
  * 默认未启用，将被multiplexing替代
  * 一些代理服务器不能正确的处理 HTTP Pipelining。
  * 正确的流水线实现是复杂的。
  * Head-of-line Blocking 连接头阻塞
* 会话跟踪的方式？
  * URL参数、隐藏表单域、Session、Cookie
* 如何抵御跨站攻击CSRF？
  * 合理使用POST，检查Referer，一次性随机Token
* HTTP 1.0 1.1 2.0
  * 1.1 默认长连接 支持Pipeline
  * 2.0 multiplexing多路复用 二进制分帧 首部压缩 服务端推送
* JSONP?如何实现跨域
  * script标签
* socket通信过程？
  * server: socket(), bind(), listen(), accept()
  * client: socket(), connect()
* WebSocket特点？
  * 双向通信
  * 二进制传输
  * 有状态
* RSA公私钥互换？
  * 私钥加密公钥解密用来签名验证，公钥加密私钥解密则用来加密数据
  * 從 RSA 的數學原理上來說，交換使用在功能上是沒有任何問題的。但是，但是，一般的 RSA 實現中，公鑰的生成選擇的 Modular Multiplicative Inverse 都會是一個較小的數值，目的是降低 Hamming Weight，也就是體現在你看到的公鈅比私鈅短很多這上面。這就導致了，如果有人拿到了私鈅，就可以較爲輕鬆地計算出一個有效的公鈅。所以永遠不要把私鈅公開出去。[--Rix Tox](https://www.zhihu.com/question/31602509/answer/52621918)

### 运输层

知识点&问题

* 首部格式
  * 伪首部
* TCP握手挥手
  * 为什么三次握手？
  * 握手挥手状态图全解：[面试必考 | TCP 协议（第一弹）](https://mp.weixin.qq.com/s/RI6QZAKLEDqa9vMKpaLpoQ)
  * SYN Flood
* TCP如何可靠传输？
* TCP滑动窗口(ARQ)
* TCP流量控制
* TCP拥塞控制 快速重传机制
* TCP拆包 | UDP不拆包
* TCP心跳检测
* TCP & UDP 区别

答案

* 首部格式
  * 
* [SYN Flood & SYN cookie](https://segmentfault.com/a/1190000019292140)
* [TCP为什么三次握手？](https://draveness.me/whys-the-design-tcp-three-way-handshake/)
  * 确保连接有效
  * 确认双方的序列号
* TCP如何可靠传输？
  * 校验和、累计确认和重传机制
* TCP粘包？
  * 伪概念，应用层按终结符/长度声明作为标识
* TCP滑动窗口
  * 超时重传、累计确认
* [TCP流量控制、拥塞控制](https://zhuanlan.zhihu.com/p/37379780) 快速重传机制
  * TCP Tahoe Reno ssthresh
* TCP心跳检测
  * 应用层自己开个低级别线程，实现小心跳包
  * TCP KeepAlive
* TCP & UDP 区别
  * 有连接 / 无连接
  * 流控拥控 / 无
  * 可靠 / 不可靠
  * 头部长 / 短
  * 面向流 / 数据包

### 网络层

知识点&问题

* BGP OSPF RIP
* IP首部格式
* DHCP过程？为什么四个包而不是两个？
* MTU & Path MTU Discovery

答案

* DHCP过程？
  * (discover, offer, request, ack)
* 为什么DHCP要用四个包而不是两个？
  * 局域网内有时候不止一台dhcp服务器，有时候会有很多台，如果使用两个报文，就会出现一台client收到多个offer的问题了

### 数据链路层

* ARP
  * 懂的都懂，不懂的也没有办法。我只能说...

## 数据结构

* 排序算法
  * 归并
  * 快排
  * 堆排
* 红黑树 // TODO
* B树 // TODO
* 优先队列 // TODO
* 布隆过滤器

## Linux

知识点&问题

* [epoll](https://imageslr.github.io/2020/02/27/select-poll-epoll.html)
* 如何直接操作物理内存？

答案

* 如何直接操作物理内存？
  * /dev/mem 物理内存镜像
  * /dev/kmem kernel看到的虚拟内存全镜像

## iOS

### Swift基础

1. UTF-8, index单独计算

```swift
let s = "🐂🍺" // s.count = 2
```

2. UInt和Int 等长

```swift
UInt32.max
Int32.max
```

3. 类型转换Optional

```swift
Int(3.14) // Non-optional
Int("234") // Optional
```

4. 隐式解析可选类型 implicitly unwrapped optionals

```swift
let assumedString: String! = "A String"
let implicitString: String = assumedString // 不需要感叹号
let optionalString = assumedString // typeof(optionalString) == String?
```

5. 断言和先决条件？？

```swift
assert(3 > 4, "wrong")
precondition(3 > 5, "error")
```

6. Struct和class的区别？

7. Switch - 基于模式匹配~=，重载于Equatable, optionals, range, interval

8. MVVM与MVC // TODO

9. Property: 存储属性、计算属性、属性观察器、属性包装器、全局和局部变量、类型属性

10. Optional 是一个泛型枚举，大致定义如下:

```
enum Optional<Wrapped> {
  case none
  case some(Wrapped)
}
```

1.   

**需要记的代码**
* 正则模板

```swift
string.range(of: #"regex"#, options: .regularexpression) == string.startIndex..<string.endIndex
```
* Equatable&Hashable

```swift
extension blabla: Hashable, Equatable {
  public func hash(into hasher: inout Hasher) {
    hasher.combine(ObjectIdentifier(self))
  }
  public static func ==(lhs: blabla, rhs: blabla) {
    return lhs === rhs
  }
}
```
* random

```swift
list.randomElement()!
Int.random(in: 0..<10)
```

* unicodeScalar

```swift
UnicodeScalar("u").value // "u" must be of type String
for i in "saafo".unicodeScalars
```

### iOS App

知识点&问题

* iOS Runloop?
* iOS界面渲染流程？
* 闭包：如何捕获？释放？weak&unowned?
* escaping? autoclosure?
* UIView 和 CALayer 的区别？
* 响应链？

答案

* iOS Runloop?
  * 与线程绑定，默认启动主线程的Runloop
  * Runloop Mode 以下三种状态切换
    * Source:
      * Input Source
        * Port-Based Sources(系统底层Port事件)
        * Custom Input Sources
        * Cocoa Perform Selector Sources
      * Timer Source
    * Runloop Observer 监控自身状态
    * 
* 闭包：循环引用、ARC
  * weak: var optional, unowned：保证不为空
  * **闭包是self的属性时才会发生循环引用！**
* UIView 和 CALayer 的区别？
  * UIView 是 CALayer 的 delegate，UIView 可以响应事件，而 CALayer 则不能。
* 响应链
  * UILabel/UITextField/UIButton -> UIView -> UIView -> UIVC -> UIWindow ->UIApplication ->UIAppDelegate

### iOS 设计模式

* Creational 创建型 5
  * Factory Method 工厂方法模式
  * Abstract Factory 抽象工厂模式
  * Singleton 单例模式
  * Builder 建造者模式
  * Prototype 原型模式
* Structural 结构型 7
  * Adapter 适配器模式
  * Decorator 装饰者模式
  * Proxy 代理模式
  * Facade 外观模式
  * Bridge 桥接模式
  * Composite 组合模式
  * Flyweight 享元模式
* Behavioral 行为型 11
  * Strategy 策略模式
  * Template Method 模板方法模式
  * Observer 观察者模式
  * Iterator 迭代器模式
  * Chain of responsibility 责任链模式
  * Command 命令模式
  * Memento 备忘录模式
  * State 状态模式
  * Visitor 访问者模式
  * Mediator 中介者模式
  * Interpreter 解释器模式

六大原则

* 开闭原则
* 里氏代换原则
* 依赖倒转原则
* 接口隔离原则
* 迪米特法则（最少知道原则）
* 合成复用原则

## 数据库

## 编译技术