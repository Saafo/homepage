# 检测 Apple Pencil 连接 iPad

本文简单介绍一下利用`CBCentralManager`检测 Apple Pencil 的连接，以及`CBCentralManager`的使用注意事项。







## 原理

目前苹果没有官方的接口检测 Apple Pencil 是否连接上 iPad。我们目前能检测连接 Apple Pencil 的方式只有请求蓝牙权限、扫描已连接设备列表中有无名为"Apple Pencil"的设备。

此方法不一定准确，但也是目前暂时唯一的可行方案。

因为`Pencil`和`手指`的区别在于，收到的`UITouch`事件的`TouchType`属性不一样。在普通连接状态时，Pencil 和 iPad 并没有屏幕上的互动，自然没有办法通过 Pencil 相关接口查询到。

## 准备步骤

1. 需要在工程设置 -> Signing & Capabilities -> Add Capability 中选择`Background Modes`，然后勾选`Use Bluetooth LE accessories`，来让 App 具有连接蓝牙设备的能力。
2. 在`Info.plist`中添加`Privacy - Bluetooth Always Usage Description`和`Privacy - Bluetooth Peripheral Usage Description`，添加对应的描述。在较新的系统中，两个字段都是必须填写的。

## Codes

首先，导入蓝牙库

```Swift
import CoreBluetooth
```

然后我们要实例化一个蓝牙管理Manager:

```Swift
let centralManager = CBCentralManager()
```

根据官方文档，我们需要保证状态为`.poweredOn`的状态下，对manager进行操作。

```Swift
if centralManager.state == .poweredOn {
  let peripherals = centralManager.retrieveConnectedPeripherals(withServices: [CBUUID(string: "180A")])
  let isPencilAvailable = peripherals.contains(where: { $0.name == "Apple Pencil" })
  // `isPencilAvailable` is the final result
}
```

原理：

* 查询`CBCentralManager`实例的状态为`.poweredOn`，这样我们可以对其进行进一步操作。
* 获得提供`180A`服务的已连接蓝牙设备列表（180A服务是蓝牙对「设备信息」的编号，可以查询到已连接设备的相关信息。 Apple Pencil应该并且也将一直应该提供这项服务。我们可以通过设备信息查询到设备名称。
* 遍历设备列表中有无名为`Apple Pencil`的设备。

## 注意事项

看起来很简单的操作，但背后隐藏着几个坑：

1. CBCentralManager在刚开始启动时的state可能为`.unknown`，一小段时间之后的第二次执行的时候才可能会变成真实状态（即:连续写两次`centralManager.state`并不会让第二次 state 正常，但尝试`sleep(0.1)`之后可以查询到正常状态。
2. CBCentralManager的实例要长时间（至少不会瞬间 deinit）存在。

对于以上两个坑，有以下的 Best Practices:

1. CBCentralManager的实例声明作为 VC 的属性，并且VC不会瞬间消失
2. CBCentralManager的实例作为单例对象
3. 间隔地两次以上尝试调用centralManager.state

参考文章：

[Detect whether Apple Pencil is connected to an iPad Pro - Stackoverflow](https://stackoverflow.com/questions/32542250)