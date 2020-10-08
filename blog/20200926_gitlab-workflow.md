# GitLab工作流说明

使用GitLab工作流可以让我们更充分地使用GitLab，提高团队协作效率。

本文会描述一个完整的GitLab + Xcode工作流。





## Gitlab工作流

1. 在`议题/issue`中创建一个`新议题/New issue`

* 标题应该为小任务的总结性概括，可以在下方的`Description`中**列出本次需要解决的任务**。
* `Assignee`为任务的指派人，如果是自己的任务，请指派给自己。
* `Milestore`为任务里程碑。会在后面讲述。
* `Labels`为Issue的标签，常见的标签有：
  * BUG
  * Doing
  * Enhance
  * Important
  * New Feature
  * Not Important
  * To Do
  * Under Discussion

应该选中合适的标记。其中`Important`和`Not Important`、`To Do`和`Doing`、`BUG` `Enhance`和`New Feature`应该互斥。
* `Due date`为截止日期。为了提高效率，请**设定**一个解决完此issue的**截止日期**。

2. 在issue页面，点击`Create merge request`**右边的箭头**，更改好合适的分支名称（小写字母统一用减号分隔，以自己名字结尾），然后点`创建合并请求/Create Merge Request`

3. 接下来会跳转到新开的MR页面。注意，此时的名字为`WIP: `开头。有此前缀时说明此MR还没有准备好。具体解释可以点下方`This is a Work in Progess`右侧的问号查看详情。简介中的`Closes #x`表示当此MR被合并时，会自动关闭`issue #x`。

4. 回到Xcode，点击`Source Control`中的`Pull`或者按`⌥⌘X`拉取最新远端仓库。

5. 按`⌘2`切换到`Source Control Navigator`，在`Remotes->origin`中可以看见刚刚自己新建的分支，右键，`Checkout...`，即可切换到新分支进行开发。

6. 开发结束后，提交所有更改。可以按`⌥⌘C`来提交更改。提交时请养成多次少量Commit的习惯。每次Commit时请逐个检查更改的地方，避免混入错误。最后一次Commit时可以勾上左下角`Push to remote`来将更改推送到远端的自己的分支。

7. 在修改好自己的代码之后，要确保和此刻的master没有冲突。可以在Xcode中先checkout 到master，然后pull。如果没有新的提交，可以忽略本步接下来的操作。如果其他人有新的提交，应该再次切换到自己的分支，然后在master上右键，选择`Merge master into <自己的分支>`。如果有冲突，先解决红色的冲突部分。然后再Push到远端。

8. 所有更改结束后，回到MR页面。此时在`Discussion`界面应该有之前的Commit信息。在准备合并之前，可以点击右上角的`Edit`，在`Description`中加入对此次MR的描述（更改了什么，新增了什么）（注意，不要删掉了`Closes #x`，除非不想关闭该issue）

9. 回到MR页面，点击`Resolve WIP status`，此时MR已经准备好被合并。

10.  在右侧的`Assignee`中找到负责合并的Maintainer，指派给他，他会收到邮件。在被合并之后，MR页面还有删除源分支的选项，可以选择删除源分支。同时在Xcode中切换至master，pull新的提交，并且删除本地自己的分支。

## Commit信息建议

之前翻看了不少现存的项目代码，看到不少的 Commit Message 写得比较简单，例如一连串的 "update", "fix"，从这些 Commit Message 中完全看不出做了什么改动，想想如果之后想要定位之前的某个改动，该从哪里下手。

目前 Commit Message 规范比较常见的有 Angular 团队的规范，并由此衍生出了 Conventional Commits Specification，可以参照此 Specification 约定 Commit Message 格式规范。

```txt
<type>(<scope>): <subject>
<BLANK LINE>
<body>
<BLANK LINE>
<footer>
```

大体分三行：

【标题行】必填, 描述主要修改类型和内容。

【主题内容】描述为什么修改, 做了什么样的修改, 以及这么做的思路等等。

【页脚注释】放 Breaking Changes 或 Closed Issues

其中 type 是 Commit 的类型，可以有以下取值：

```txt
feat：新特性
fix：修改 bug
refactor：代码重构
docs：文档更新
style：代码格式修改
test：测试用例修改
chore：其他修改, 比如构建流程, 依赖管理
```

其中 scope 表示的是 Commit 影响的范围，比如 ui，utils，build 等，是一个可选内容。

其中 subject 是 Commit 的概述，body 是 Commit 的具体内容。

例如：

```txt
fix: correct minor typos in code

see the issue for details on typos fixed.

Refs #133
```

参考：[如何有效地进行代码Review? - 腾讯大讲堂](https://mp.weixin.qq.com/s/ICl-IBgR3aVQi4ObsB0-ww)

## Milestone的使用

Milestone是里程碑的意思。在issue和MR中都可以选择是否属于某个里程碑。属于这个里程碑的所有issue和MR会被汇总在里程碑的页面，同时会有一个进度条，展示完成的issue和MR占所有issue和MR的进度。