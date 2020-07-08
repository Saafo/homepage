# LeetCode@Swift - Vol.3 链表

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

[两两交换链表中的节点](https://leetcode-cn.com/problems/swap-nodes-in-pairs/)

> 给定一个链表，两两交换其中相邻的节点，并返回交换后的链表。
> 
> 你不能只是单纯的改变节点内部的值，而是需要实际的进行节点交换。
> 
> 示例:
> 
> 给定 1->2->3->4, 你应该返回 2->1->4->3.