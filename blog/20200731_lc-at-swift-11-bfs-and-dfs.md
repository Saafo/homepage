# LeetCode@Swift - Vol.11 深度优先和广度优先

BFS和DFS是比先序中序后序更加常考也更加普遍运用的算法。

BFS一般只采用非递归实现。

DFS可采用递归和非递归实现。

但二者并不一定有严格的界限，有的BFS的题也可以用DFS实现。比如下面这道题：

## 二叉树的层序遍历

[二叉树的层序遍历 - 力扣](https://leetcode-cn.com/problems/binary-tree-level-order-traversal/)

> 给你一个二叉树，请你返回其按 层序遍历 得到的节点值。 （即逐层地，从左到右访问所有节点）。

```swift
//Definition for a binary tree node.
public class TreeNode {
    public var val: Int
    public var left: TreeNode?
    public var right: TreeNode?
    public init(_ val: Int) {
        self.val = val
        self.left = nil
        self.right = nil
    }
}
```

### BFS

```swift
class Solution {
    func levelOrder(_ root: TreeNode?) -> [[Int]] {
        guard root != nil else { return [] }
        var result: [[Int]] = []
        var stack: [TreeNode] = [root!]
        var currentLayerCount = stack.count
        var curNode: TreeNode
        while !stack.isEmpty {
            var currentLayer: [Int] = []
            while currentLayerCount > 0 {
                curNode = stack.removeFirst()
                currentLayerCount -= 1
                currentLayer.append(curNode.val)
                if curNode.left != nil {
                    stack.append(curNode.left!)
                }
                if curNode.right != nil {
                    stack.append(curNode.right!)
                }
            }
            result.append(currentLayer)
            currentLayerCount = stack.count
        }
        return result
    }
}
```

执行用时：20 ms 内存消耗：21.2 MB

在这里，我们的第二层循环仍然是采用的while循环以及一个counter来执行对一层的循环和判定。但我们可以利用`for...in...`来完成这件事。在Swift中，`for...in...`的条件即使被修改，仍然会以第一次遇到条件时的状态（特别是循环次数）为准，所以我们可以改写成以下形式：

```swift
class Solution {
    func levelOrder(_ root: TreeNode?) -> [[Int]] {
        guard root != nil else { return [] }
        var result: [[Int]] = []
        var stack: [TreeNode] = [root!]
        while !stack.isEmpty {
            var currentLayer: [Int] = []
            for curNode in stack {
                stack.removeFirst()
                currentLayer.append(curNode.val)
                if curNode.left != nil {
                    stack.append(curNode.left!)
                }
                if curNode.right != nil {
                    stack.append(curNode.right!)
                }
            }
            result.append(currentLayer)
        }
        return result
    }
}
```

执行用时：12 ms 内存消耗：21.1 MB

继续尝试将所有的`if xxx != nil`改成`if let xxx = xxx`：

```swift
class Solution {
    func levelOrder(_ root: TreeNode?) -> [[Int]] {
        guard let root = root else { return [] }
        var result: [[Int]] = []
        var stack: [TreeNode] = [root]
        while !stack.isEmpty {
            var currentLayer: [Int] = []
            for curNode in stack {
                stack.removeFirst()
                currentLayer.append(curNode.val)
                if let left = curNode.left {
                    stack.append(left)
                }
                if let right = curNode.right {
                    stack.append(right)
                }
            }
            result.append(currentLayer)
        }
        return result
    }
}
```

执行用时：28 ms 内存消耗：21.2 MB

可以发现用时反而多了一些，所以在写起来不麻烦的情况下，还是没有必要全部替换为可选绑定。

### DFS

DFS则是按深度优先的顺序将节点值添加到结果集中，即先建好一个结果集，再添加值进去。

```swift
class Solution {
    func levelOrder(_ root: TreeNode?) -> [[Int]] {
        guard root != nil else { return [] }
        var result: [[Int]] = []
        DFS(root!, &result, 0)
        return result
    }
    func DFS(_ node: TreeNode, _ result: inout [[Int]], _ currentLayer: Int) {
        if result.count <= currentLayer { result.append([]) }
        result[currentLayer].append(node.val)
        if let left = node.left {
            DFS(left, &result, currentLayer + 1)
        }
        if let right = node.right {
            DFS(right, &result, currentLayer + 1)
        }
    }
}
```

执行用时：20 ms 内存消耗：21.4 MB

尝试将inout改为返回值：

```swift
class Solution {
    func levelOrder(_ root: TreeNode?) -> [[Int]] {
        guard root != nil else { return [] }
        // var result: [[Int]] = []
        return DFS(root!, [], 0)
    }
    func DFS(_ node: TreeNode, _ result: [[Int]], _ currentLayer: Int) -> [[Int]] {
        var result = result
        if result.count <= currentLayer { result.append([]) }
        result[currentLayer].append(node.val)
        if let left = node.left {
            result = DFS(left, result, currentLayer + 1)
        }
        if let right = node.right {
            result = DFS(right, result, currentLayer + 1)
        }
        return result
    }
}
```

执行用时：28 ms 内存消耗：24.7 MB

可以发现虽然inout仍然是函数执行完之后复制回去，但返回值比inout还是要更慢一些。以后类似的递归情况还是应该优先考虑用inout而不是返回值。

## 二叉树的最大深度

[二叉树的最大深度 - 力扣](https://leetcode-cn.com/problems/maximum-depth-of-binary-tree/)

> 给定一个二叉树，找出其最大深度。
> 
> 二叉树的深度为根节点到最远叶子节点的最长路径上的节点数。
> 
> 说明: 叶子节点是指没有子节点的节点。

同理，两种遍历方法均可

### BFS

没啥好说的，直接上代码吧

```swift
class Solution {
    func maxDepth(_ root: TreeNode?) -> Int {
        guard root != nil else { return 0 }
        var stack: [TreeNode] = [root!]
        var depth = 0
        while !stack.isEmpty {
            for node in stack {
                if node.left != nil {
                    stack.append(node.left!)
                }
                if node.right != nil {
                    stack.append(node.right!)
                }
                stack.removeFirst()
            }
            depth += 1
        }
        return depth
    }
}
```

执行用时：48 ms 内存消耗：21.5 MB

### DFS

```swift
class Solution {
    func maxDepth(_ root: TreeNode?) -> Int {
        guard root != nil else { return 0 }
        var depth = 1, maxD = 1
        DFS(root!, depth, &maxD)
        return maxD
    }
    func DFS(_ node: TreeNode, _ depth: Int, _ maxD: inout Int) {
        if node.left != nil {
            DFS(node.left!, depth + 1, &maxD)
        }
        if node.right != nil {
            DFS(node.right!, depth + 1, &maxD)
        }
        maxD = max(depth, maxD)
    }
}
```

执行用时：36 ms 内存消耗：21.7 MB

### 递归

囿于DFS和BFS，以及层数自上到下递增的思维，没想到最简单的方法反而是简单的递归：

（其实递归也算是DFS啦，这个算是上面的优化解）

```swift
class Solution {
    func maxDepth(_ root: TreeNode?) -> Int {
        guard root != nil else { return 0 }
        return max(maxDepth(root!.left),maxDepth(root!.right)) + 1
    }
}
```

执行用时：36 ms 内存消耗：21.8 MB

还可以继续优化（狗头

```swift
class Solution {
    func maxDepth(_ root: TreeNode?) -> Int {
        return root == nil ? 0 : max(maxDepth(root!.left),maxDepth(root!.right)) + 1
    }
}
```

执行用时：32 ms 内存消耗：21.8 MB

## 二叉树的最小深度

[二叉树的最小深度 - 力扣](https://leetcode-cn.com/problems/minimum-depth-of-binary-tree/)

> 给定一个二叉树，找出其最小深度。
> 
> 最小深度是从根节点到最近叶子节点的最短路径上的节点数量。
> 
> 说明: 叶子节点是指没有子节点的节点。

### BFS

```swift
class Solution {
    func minDepth(_ root: TreeNode?) -> Int {
        guard root != nil else { return 0 }
        var stack: [TreeNode] = [root!]
        var depth = 1
        while !stack.isEmpty {
            for node in stack {
                if node.left == nil && node.right == nil {
                    return depth
                }
                if node.left != nil {
                    stack.append(node.left!)
                }
                if node.right != nil {
                    stack.append(node.right!)
                }
                stack.removeFirst()
            }
            depth += 1
        }
        return depth
    }
}
```

执行用时：48 ms 内存消耗：21.5 MB

### 递归/DFS

```swift
class Solution {
    func minDepth(_ root: TreeNode?) -> Int {
        guard root != nil else { return 0 }
        if root!.left == nil && root!.right == nil {
            return 1
        }
        else if root!.left == nil {
            return minDepth(root!.right) + 1
        }
        else if root!.right == nil {
            return minDepth(root!.left) + 1
        }
        else {
            return min(minDepth(root!.left), minDepth(root!.right)) + 1
        }
    }
}
```

执行用时：72 ms 内存消耗：22.1 MB

代码可以稍微优化一下：

```swift
class Solution {
    func minDepth(_ root: TreeNode?) -> Int {
        guard root != nil else { return 0 }
        return root!.left == nil || root!.right == nil
            ? minDepth(root!.left) + minDepth(root!.right) + 1
            : min(minDepth(root!.left), minDepth(root!.right)) + 1
    }
}
```

执行用时：52 ms 内存消耗：21.9 MB
