# Golang 在 VSCode 中的调试配置

（解决Golang在VSCode中调试时无法接收标准输入(stdin)的问题）

> 最近开始接触Go语言，但在配置VSCode的调试文件的时候发现VSCode中的官方GO插件调试时用的是调试控制台(debug console)而非终端(terminal)，找了很多设置也没有类似于`terminal`或者`internalTerminal`或者`externalTerminal`的配置项。最终在`vscode-go`仓库的[issue](https://github.com/microsoft/vscode-go/issues/219)里找到了问题所在。鉴于目前还没有国内的博客帖子总结该问题，在这里总结一下问题原因及解决方案。

### 问题起因

最开始以为是`vscode-go`插件的锅，但在相关问题的[issue](https://github.com/microsoft/vscode-go/issues/219)里，`vscode-go`的开发团队给出的回复是，由于`delve`调试器本身在普通模式运行时就无法直接接受命令行标准输入(stdin)，导致配套的相关插件也无法正常工作。本来`delve`自身加上支持接受命令行输入的功能即可彻底解决这个问题，但似乎`delve`开发团队的人员[并不对此感兴趣](https://github.com/go-delve/delve/issues/1274/#issuecomment-406981956)，不少开发者也同样也对此表示[无奈](https://github.com/microsoft/vscode-go/issues/219/#issuecomment-455968894),只有用目前其他开发者给出的[折中的解决办法](https://github.com/microsoft/vscode-go/issues/219/#issuecomment-530933960)。

### 解决方案

虽然`delve`在普通模式下不能接受标准输入(stdin)，但其在`headless`模式下是可以接受标准输入的。在`VSCode`中我们也可以借助这个特性来实现Golang的调试时输入功能。

以下是开发者`HowieLiuX`给出的参考配置：

tasks.json
```
{
    // See https://go.microsoft.com/fwlink/?LinkId=733558
    // for the documentation about the tasks.json format
    "version": "2.0.0",
    "tasks": [
        {
            "label": "echo",
            "type": "shell",
            "command": "cd ${fileDirname} && dlv debug --headless --listen=:2345 --log --api-version=2",
            "problemMatcher": [],
            "group": {
                "kind": "build",
                "isDefault": true
            }
        }
    ]
}
```
launch.json
```
{
    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Connect to server",
            "type": "go",
            "request": "launch",
            "mode": "remote",
            "remotePath": "${fileDirname}",
            "port": 2345,
            "host": "127.0.0.1",
            "program": "${fileDirname}",
            "env": {},
            "args": []
        }
    ]
}
```

然而，我在macOS平台尝试以以上配置启动调试时却先后遇到了  
`zsh:cd:1: too many arguments`、  
`zsh:1: command not found: dlv`  
`Request type of 'launch' with mode 'remote' is deprecated, please use request type 'attach' with mode 'remote' instead.`  
这些问题。

在大半天的折腾之后，总结下来问题1是由于路径中含有特殊符号（如空格），需要将`cd ${fileDirname}`改为`cd \"${fileDirname}\"`；问题2是由于PATH似乎并没有被自动添加到启动的终端中。我的解决方案是在执行命令之前执行`source /etc/profile`命令。问题3则应该将`launch.json`中`"request": "launch"`改为`"request": "attach"`

以下是我现在使用的配置

tasks.json
```
{
    // See https://go.microsoft.com/fwlink/?LinkId=733558
    // for the documentation about the tasks.json format
    "version": "2.0.0",
    "tasks": [
        {
            "label": "echo",
            "type": "shell",
            "command": "cd \"${fileDirname}\" && source /etc/profile && ~/Applications/Go/bin/dlv debug --headless --listen=:2346 --api-version=2",
            "problemMatcher": [],
            "group": {
                "kind": "build",
                "isDefault": true
            }
        }
    ]
}
```

launch.json
```
{
    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Connect to server",
            "type": "go",
            "request": "attach",
            "mode": "remote",
            "remotePath": "${workspaceFolder}",
            "port": 2346,
            "host": "127.0.0.1",
            "internalConsoleOptions": "neverOpen"
        }
    ]
}
```

### 调试步骤
因为tasks.json中已经将当前配置isDefault为true,只需要按快捷键`cmd`+`shift`+`B`先启动build任务，再按调试键，即可正常调试。

以上为macOS的推荐配置，Windows用户可以尝试[Windows的推荐解决方案](https://github.com/microsoft/vscode-go/issues/219/#issuecomment-370159866)