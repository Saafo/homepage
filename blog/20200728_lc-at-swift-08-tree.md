# LeetCode@Swift - Vol.8 树

树是算法中很重要的一个结构，通常需要掌握先序/中序/后序的递归/非递归算法，以及BFS/HFS算法。常见的题目有二叉树、二叉搜索树相关的题型。







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

## 验证二叉搜索树

[验证二叉搜索树 - 力扣](https://leetcode-cn.com/problems/validate-binary-search-tree/)

> 给定一个二叉树，判断其是否是一个有效的二叉搜索树。
> 
> 假设一个二叉搜索树具有如下特征：
> 
> 节点的左子树只包含小于当前节点的数。
> 
> 节点的右子树只包含大于当前节点的数。
> 
> 所有左子树和右子树自身必须也是二叉搜索树。

### 排序法

第一种方法是中序遍历成数列，然后看是否为升序数列即可。省略。

### 递归

递归需要注意的是，不仅仅要在每个节点确保`存在的左节点` < `本节点` < `存在的右节点`，本节点需要大于`整个左子树最大的节点`，小于`整个右子树最小的节点`。

在本解法（递归）和下面一种非递归的解法，我们都不需要把所有的节点存下来，只需要一个prev变量，验证现在的节点比之前一个节点大就行了。

```swift
class Solution {
    func isValidBST(_ root: TreeNode?) -> Bool {
        guard root != nil else { return true }
        var prev: Int?
        return validate(root, &prev)
    }
    func validate(_ root: TreeNode?, _ prev: inout Int?) -> Bool {
        guard root != nil else { return true }
        guard validate(root!.left, &prev) == true else { return false }
        if prev != nil {
            guard prev! < root!.val else { return false }
        }
        prev = root!.val
        guard validate(root!.right, &prev) == true else { return false }
        return true
    }
}
```

执行用时：60 ms 内存消耗：21.7 MB

### 非递归

非递归采用一个栈来保存还未遍历的节点。

```swift
class Solution {
    func isValidBST(_ root: TreeNode?) -> Bool {
        var stack: [TreeNode] = []
        var cur: TreeNode? = root
        var prev: Int?
        while !stack.isEmpty || cur != nil {
            if cur != nil {
                stack.append(cur!)
                cur = cur!.left
            } else {
                cur = stack.popLast()
                if prev != nil {
                    guard prev! < cur!.val else { return false }
                }
                prev = cur!.val
                cur = cur!.right
            }
        }
        return true
    }
}
```

执行用时：60 ms 内存消耗：21.3 MB

可以看出递归和循环在时间上是大致相同的，不过在内存消耗上就有差距了，显而易见的是循环需要的内存会更少。

### 递归优化版

```swift
class Solution {
    func isValidBST(_ root: TreeNode?) -> Bool {
        // let result: Bool
        let (result, _, _) = validate(root)
        return result
    }
    func validate(_ root: TreeNode?) -> (Bool, Int?, Int?) {
        guard let root = root else { return (true, nil, nil) }
        // let min, max: Int
        let (leftResult, leftMin, leftMax) = validate(root.left)
        guard leftResult == true && (leftMax == nil || leftMax! < root.val) else {
            return (false, nil, nil)
        }
        let (rightResult, rightMin, rightMax) = validate(root.right)
        guard rightResult == true && (rightMin == nil || rightMin! > root.val) else {
            return (false, nil, nil)
        }
        return (true, leftMin ?? root.val, rightMax ?? root.val)
    }
}
```

执行用时：52 ms 内存消耗：21.7 MB

我也说不清为啥这个就要快一点，主要原理是在递归的时候就加入min和max值的记录，比较的时候直接比较，（不用反复修改一个inout的prev？）

## 二叉搜索树的最近公共祖先☆

[二叉搜索树的最近公共祖先 - 力扣](https://leetcode-cn.com/problems/lowest-common-ancestor-of-a-binary-search-tree/)

> 给定一个二叉搜索树, 找到该树中两个指定节点的最近公共祖先。
> 
> 百度百科中最近公共祖先的定义为：“对于有根树 T 的两个结点 p、q，最近公共祖先表示为一个结点 x，满足 x 是 p、q 的祖先且 x 的深度尽可能大（一个节点也可以是它自己的祖先）。”

### 链路比较法

最简单的方法：从根节点开始遍历到两个给定的节点，记录两条路径，比较两条路径上相同的最后一个节点即可。因为二叉搜索树的特性，我们可以在遍历的时候和每个节点比较大小就能知道需要找的节点在左子树还是右子树。代码如下：

```swift
class Solution {
    func lowestCommonAncestor(_ root: TreeNode?, _ p: TreeNode?, _ q: TreeNode?) -> TreeNode? {
        guard let p = p, let q = q else { return nil }
        var pPath: [TreeNode?] = []
        var qPath: [TreeNode?] = []
        var cur: TreeNode? = root
        while cur != nil && cur!.val != p.val {
            pPath.append(cur)
            cur = p.val < cur!.val ? cur!.left : cur!.right
        }
        pPath.append(cur)
        cur = root
        while cur != nil && cur!.val != q.val {
            qPath.append(cur)
            cur = q.val < cur!.val ? cur!.left : cur!.right
        }
        qPath.append(cur)
        var result: TreeNode?
        for i in 0..<min(pPath.count, qPath.count) {
            if pPath[i]!.val != qPath[i]!.val {
                return result
            }
            result = pPath[i]
        }
        return result
    }
}
```

执行用时：152 ms 内存消耗：21.9 MB

比较惊讶的是思路简单的同时用时还不多，理论耗时在3log2n，也就是O(logn)的复杂度。

### 递归法

递归法的思路是：利用二叉搜索树的特性，从根节点开始递归，如果p和q都小于当前节点，那么继续找左子树（因为p,q肯定在左子树上），反之则寻找右子树，如果都不是，说明p,q在此节点分叉，也即最近公共祖先。那么就可以直接返回当前节点了。

```swift
class Solution {
    func lowestCommonAncestor(_ root: TreeNode?, _ p: TreeNode?, _ q: TreeNode?) -> TreeNode? {
        guard root != nil else { return root }
        if root!.val > p!.val && root!.val > q!.val {
            return lowestCommonAncestor(root!.left, p, q)
        }
        else if root!.val < p!.val && root!.val < q!.val {
            return lowestCommonAncestor(root!.right, p, q)
        }
        return root
    }
}
```

执行用时：156 ms 内存消耗：21.9 MB

我们可以发现这种遍历方法，如果给定的树非空；并且p,q都存在于树中，那么其实可以删掉函数第一行root != nil的校验。

### 非递归法

模仿递归的思路，我们可以很容易地写出非递归法。

```swift
class Solution {
    func lowestCommonAncestor(_ root: TreeNode?, _ p: TreeNode?, _ q: TreeNode?) -> TreeNode? {
        guard let p = p, let q = q else { return nil }
        var root = root
        while root != nil {
            if p.val < root!.val && root!.val > q.val {
                root = root!.left
            }
            else if p.val > root!.val && root!.val < q.val {
                root = root!.right
            } else {
                return root
            }
        }
        return nil
    }
}
```

执行用时：160 ms 内存消耗：21.5 MB

## 二叉树的最近公共祖先☆

[二叉树的最近公共祖先 - 力扣](https://leetcode-cn.com/problems/lowest-common-ancestor-of-a-binary-tree/)

> 给定一个二叉树, 找到该树中两个指定节点的最近公共祖先。
>
> 百度百科中最近公共祖先的定义为：“对于有根树 T 的两个结点 p、q，最近公共祖先表示为一个结点 x，满足 x 是 p、q 的祖先且 x 的深度尽可能大（一个节点也可以是它自己的祖先）。”

本题没有了搜索树的性质，如果再继续使用链路比较法，则会花费过多的时间用于节点的寻找上。故本题主要采用递归的方法。

### 递归法

递归法的具体思路是：对于一个节点，

* 如果本身是空/p/q，则返回自己
* 如果左子树是nil，则返回右子树
* 如果右子树是nil，则返回左子树
* 如果两个子树都不是nil，则返回自己

非常巧妙，建议多多回味。

```swift
class Solution {
    func lowestCommonAncestor(_ root: TreeNode?, _ p: TreeNode?, _ q: TreeNode?) -> TreeNode? {
        guard root != nil && root!.val != p!.val && root!.val != q!.val else { return root }
        let left = lowestCommonAncestor(root!.left, p, q)
        let right = lowestCommonAncestor(root!.right, p, q)
        return left == nil ? right : right == nil ? left : root
    }
}
```

执行用时：92 ms 内存消耗：28.3 MB

这里可以改进的地方是，对于TreeNode这种class引用值的比较可以使用`===`和`!==`来判断是否指向同一个class，如下：

```swift
class Solution {
    func lowestCommonAncestor(_ root: TreeNode?, _ p: TreeNode?, _ q: TreeNode?) -> TreeNode? {
        guard root != nil && root !== p && root !== q else { return root }
        let left = lowestCommonAncestor(root!.left, p, q)
        let right = lowestCommonAncestor(root!.right, p, q)
        return left == nil ? right : right == nil ? left : root
    }
}
```