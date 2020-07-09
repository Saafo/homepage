# LeetCode@Swift - Vol.3 链表

链表的题目，对于思维的难度（除开部分题的递归解法）要求不算高，主要考察的是代码的实现能力，尽量做到简洁。

## 反转链表

[反转链表 - 力扣](https://leetcode-cn.com/problems/reverse-linked-list/)

> 反转一个单链表。
> 
> 示例:
> 
> 输入: 1->2->3->4->5->NULL
> 输出: 5->4->3->2->1->NULL
> 进阶:
> 你可以迭代或递归地反转链表。你能否用两种方法解决这道题？

已知单链表结构：

```swift
//Definition for singly-linked list.
public class ListNode {
    public var val: Int
    public var next: ListNode?
    public init(_ val: Int) {
        self.val = val
        self.next = nil
    }
}
 ```

### 递归法

首先是胡乱写的第一版

```swift
class Solution {
    func reverseList(_ head: ListNode?) -> ListNode? {
        var newHead: ListNode?
        if head?.next?.next != nil {
            //recursive execute
            newHead = reverseList(head?.next)
        } else {
            if head?.next == nil {
                // when chain.count == 1
                return head
            }
            // at the tail of the chain, newHead == nil
            newHead = head?.next
        }
        head?.next?.next = head
        head?.next = nil
        return newHead
    }
}
```

执行用时：24 ms 内存消耗：23.5 MB

但其实这样面临的选择分支太多，在执行效率上有一定的折扣，尝试优化一下：

```swift
class Solution {
    func reverseList(_ head: ListNode?) -> ListNode? {
        //recursive execute
        return reverse(head!, prev: nil)
    }
    private func reverse(_ head: ListNode?, prev: ListNode?) -> ListNode? {
        var newHead: ListNode?
        if head!.next == nil {
            head
            return head
        }
        newHead = reverse(head!.next, prev: head)
        head!.next = prev
        return newHead
    }
}
```

但其实这样有致命的问题，如果队列本身为空，在第一次执行到`if head!.next == nil`的时候，就会出错，`head!`无法unwrap导致fatal error。修正后的版本如下：

```swift
class Solution {
    func reverseList(_ head: ListNode?) -> ListNode? {
        //recursive execute
        return reverse(head, prev: nil)
    }
    private func reverse(_ head: ListNode?, prev: ListNode?) -> ListNode? {
        if head == nil {
            return prev
        }
        var newHead: ListNode?
        newHead = reverse(head!.next, prev: head)
        head!.next = prev
        return newHead
    }
}
```

执行用时：20 ms 内存消耗：22.5 MB

优化的代价就是要拆成两个函数。因为在递归的过程中必须用到前一个节点的信息。

但其实，到这里去看了一下题解，原来是第一版的条件筛选没写好：

```swift
class Solution {
    func reverseList(_ head: ListNode?) -> ListNode? {
        guard head?.next != nil else { return head }
        let newHead = reverseList(head!.next)
        head!.next!.next = head
        head!.next = nil
        return newHead
    }
}
```

执行用时：24 ms 内存消耗：22.9 MB

总结一下，链表不要一开始就`head?.next?.next`向后管太宽了，这样完全就是作茧自缚。

### 迭代法

递归法的内存消耗肯定会比循环多，一个经典的题解如下：

```swift
class Solution {
    func reverseList(_ head: ListNode?) -> ListNode? {
        var cur: ListNode? = head
        var prev: ListNode?
        while cur != nil {
            (cur!.next, prev, cur) = (prev, cur!, cur!.next)
        }
        return cur
    }
}
```

执行用时：20 ms 内存消耗：21.7 MB

## 两两交换链表中的节点

[两两交换链表中的节点 - 力扣](https://leetcode-cn.com/problems/swap-nodes-in-pairs/)

> 给定一个链表，两两交换其中相邻的节点，并返回交换后的链表。
> 
> 你不能只是单纯的改变节点内部的值，而是需要实际的进行节点交换。
> 
> 示例:
> 
> 给定 1->2->3->4, 你应该返回 2->1->4->3.

### 循环解法

```swift
class Solution {
    func swapPairs(_ head: ListNode?) -> ListNode? {
        guard head?.next != nil else { return head }
        var cur = head
        let newPrev: ListNode? = ListNode(-1)
        newPrev?.next = head
        var prev = newPrev
        while cur?.next != nil {
            prev!.next = cur!.next
            cur!.next = cur!.next!.next
            prev!.next!.next = cur
            
            prev = cur
            cur = cur!.next
        }
        return newPrev?.next
    }
}
```

执行用时：12 ms 内存消耗：20.8 MB

### 递归解法

在题解中看到的神仙递归法，虽然内存消耗大一点，简洁无比。

```swift
class Solution {
    func swapPairs(_ head: ListNode?) -> ListNode? {
        guard head?.next != nil else { return head }
        let cur = head
        let next = head!.next
        cur?.next = swapPairs(next?.next)
        next?.next = cur
        return next
    }
}
```

执行用时：12 ms 内存消耗：20.9 MB

在递归法中，`prev`被`return`的值替代了。

## 环形链表

[环形链表 - 力扣](https://leetcode-cn.com/problems/linked-list-cycle/)

> 给定一个链表，判断链表中是否有环。
>
> 为了表示给定链表中的环，我们使用整数 pos 来表示链表尾连接到链表中的位置（索引从 0 开始）。 如果 pos 是 -1，则在该链表中没有环。
> 
> 示例 1：
>
> 输入：head = [3,2,0,-4], pos = 1
> 
> 输出：true
> 
> 解释：链表中有一个环，其尾部连接到第二个节点。
> 
> 进阶：
>
> 你能用 O(1)（即，常量）内存解决此问题吗？

此题有三种解法，第一种是无脑法：定一个时间，比如0.5s，看循环能否停下来，停不下来直接返回true。第二种方法是利用`Set`这个数据类型。不过要在Swift中实现，必须先给ListNode加拓展，使其遵循`Hashable`和`Equatable`协议。第三种方法，则是`快慢指针`，即进阶要求中用常量内存的解法。

### 哈希表

```swift
extension ListNode: Hashable, Equatable {
   public func hash(into hasher: inout Hasher) {
       hasher.combine(ObjectIdentifier(self))
   }
   public static func ==(lhs: ListNode, rhs: ListNode) -> Bool {
       return lhs === rhs
   }
}
class Solution {
    func hasCycle(_ head: ListNode?) -> Bool {
        var cur = head
        var set: Set<ListNode> = []
        while cur != nil {
            if set.contains(cur!) {
                return true
            } else {
                set.insert(cur!)
                cur = cur!.next
            }
        }
        return false
    }
}
```

执行用时：88 ms 内存消耗：22.8 MB


这个解法用拓展中的`hash()`函数和`==()`函数给ListNode加了两个遵循的协议，拓展可以以后作为模板参考。

### 快慢指针

```swift
class Solution {
    func hasCycle(_ head: ListNode?) -> Bool {
        var fast = head
        var slow = head
        while fast != nil {
            fast = fast?.next?.next
            slow = slow?.next
            if fast === slow && fast != nil {
                return true
            }
        }
        return false
    }
}
```

执行用时：68 ms 内存消耗：22.6 MB

这里利用了`===`来比较两个节点是否相等。`===`是通过验证两者地址是否一样来判等的，概念和js中类似。Swift中的class是引用变量，所以相同的节点的地址必然一样。排名中有很多人直接用val值来判等，个人认为不可取。

`快慢指针`在这里用来解决外部环境（环形结构）无法提供外部的结束约束时创造的内部约束，除了解决环形问题，以后还会用到查找链表中间节点的题目中用到。

## 环形链表 II

[环形链表 II - 力扣](https://leetcode-cn.com/problems/linked-list-cycle-ii/)

> 给定一个链表，返回链表开始入环的第一个节点。 如果链表无环，则返回>  null。
> 
> 为了表示给定链表中的环，我们使用整数 pos 来表示链表尾连接到链表中的位置（索引从 0 开始）。 如果 pos 是 -1，则在该链表中没有环。
> 
> 说明：不允许修改给定的链表。
> 
> 示例 1：
> 
> 输入：head = [3,2,0,-4], pos = 1
> 
> 输出：tail connects to node index 1
> 
> 解释：链表中有一个环，其尾部连接到第二个节点。
> 
> 进阶：
> 
> 你是否可以不用额外空间解决此题？

### 哈希表

和上一个问题类似，不多解释：

```swift
extension ListNode: Hashable, Equatable {
    public func hash(into hasher: inout Hasher) {
        hasher.combine(ObjectIdentifier(self))
    }
    public static func ==(lhs: ListNode, rhs: ListNode) -> Bool {
        return lhs === rhs
    }
}
class Solution {
    func detectCycle(_ head: ListNode?) -> ListNode? {
        var set: Set<ListNode> = []
        var cur = head
        while cur != nil {
            if set.contains(cur!) {
                return cur
            }
            set.insert(cur!)
            cur = cur!.next
        }
        return nil
    }
}
```

执行用时：80 ms 内存消耗：22.7 MB

### 快慢+后指针（Floyd算法）

这道题的难点在于进阶要求中，不用更多的空间来完成此题。对于这种问题，需要返回交点的位置。第一遍做题的时候实在想不出来。看了评论区发现是利用数学上的原理：慢指针走了b，快指针走了2b，a+b-b=a，快慢指针相遇之后再出发一个新的慢指针，和慢指针相遇时刚好是交点。

```swift
class Solution {
    func detectCycle(_ head: ListNode?) -> ListNode? {
        var fast = head
        var slow = head
        var last = head
        while fast != nil {
            fast = fast?.next?.next
            slow = slow?.next
            if fast === slow && fast != nil {
                while slow !== last {
                    slow = slow!.next
                    last = last!.next
                }
                return last
            }
        }
        return nil
    }
}
```

执行用时：68 ms 内存消耗：22.2 MB

## K个一组翻转链表

[K个一组翻转链表 - 力扣](https://leetcode-cn.com/problems/reverse-nodes-in-k-group/)

> 给你一个链表，每 k 个节点一组进行翻转，请你返回翻转后的链表。
> 
> k 是一个正整数，它的值小于或等于链表的长度。
> 
> 如果节点总数不是 k 的整数倍，那么请将最后剩余的节点保持原有顺序。
> 
> 示例：
> 
> 给你这个链表：1->2->3->4->5
> 
> 当 k = 2 时，应当返回: 2->1->4->3->5
> 
> 当 k = 3 时，应当返回: 3->2->1->4->5
> 
> 说明：
> 
> 你的算法只能使用常数的额外空间。
> 你不能只是单纯的改变节点内部的值，而是需要实际进行节点交换。

其实就是分解成两个部分，一个分组，一个组内交换。两个部分应该循环和递归都可以。

### 递归+循环

```swift
class Solution {
    func reverseKGroup(_ head: ListNode?, _ k: Int) -> ListNode? {
        var next = head
        let cur = head
        for _ in 0..<k - 1 {
            next = next?.next
        }
        guard next != nil else { return cur }
        next = next?.next
        next = reverseKGroup(next, k)
        return reverseK(cur, k, next)
    }
    func reverseK(_ head: ListNode?, _ k: Int, _ next: ListNode?) -> ListNode? {
        var cur = head
        var prev: ListNode? = next
        for _ in 0..<k {
            (cur!.next, cur, prev) = (prev, cur?.next, cur)
        }
        return prev
    }
}
```

执行用时：48 ms 内存消耗：21.6 MB

### 双递归

```swift
class Solution {
    func reverseKGroup(_ head: ListNode?, _ k: Int) -> ListNode? {
        var next = head
        let cur = head
        for _ in 0..<k - 1 {
            next = next?.next
        }
        guard next != nil else { return cur }
        next = next?.next
        next = reverseKGroup(next, k)
        return reverseK(cur, k, next)
    }
    func reverseK(_ head: ListNode?, _ k: Int, _ next: ListNode?) -> ListNode? {
        guard k > 1 else { return head }
        let newHead = reverseK(head?.next, k - 1, next)
        head!.next!.next = head
        head!.next = next
        return newHead
    }
}
```

执行用时：44 ms 内存消耗：21.5 MB

注意这里出的`k-1`和`k>1`的条件。不是普通循环，循环在组内就应该停止，所以要额外注意。
