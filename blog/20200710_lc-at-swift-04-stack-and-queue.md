# LeetCode@Swift - Vol.4 栈和队列

栈和队列在众多语言中已经有了成熟的实现，面试的时候也一般不会让手写一个栈或者队列。不用太关注底层实现，直接用就行了。

栈->数组/单链表

队列->数组/双链表

## 比较含退格的字符串

[比较含退格的字符串 - 力扣](https://leetcode-cn.com/problems/backspace-string-compare/)

> 给定`S`和`T`两个字符串，当它们分别被输入到空白的文本编辑器后，判断二者是否相等，并返回结果。`#`代表退格字符。
> 
> 注意：如果对空文本输入退格字符，文本继续为空。
> 示例 1：
> 
> 输入：S = "ab#c", T = "ad#c"
> 
> 输出：true
> 
> 解释：S 和 T 都会变成 “ac”。
> 
> 提示：
> 
> 1 <= S.length <= 200
> 
> 1 <= T.length <= 200
> 
> S 和 T 只含有小写字母以及字符 '#'。
> 
> 进阶：
> 
> 你可以用 O(N) 的时间复杂度和 O(1) 的空间复杂度解决该问题吗？

### 构造字符串，占用额外空间
```swift
class Solution {
    func backspaceCompare(_ S: String, _ T: String) -> Bool {
        var s: String = ""
        var t: String = ""
        for i in S {
            if i == "#" {
                s.popLast()
            } else {
                s.append(i)
            }
        }
        for i in T {
            if i == "#" {
                t.popLast()
            } else {
                t.append(i)
            }
        }
        return s == t
    }
}
```

执行用时：4 ms 内存消耗：20.7 MB

非常简单，唯一需要注意的一点是，注意诸如`###ab`这种情况，当然Swift中的`popLast()`返回的是Optional类型，很好地避免了crash。如果用`removeLast()`就需要先判断栈是否是空了。

但是，在具体的实现上，其实出现了重复代码，可以稍微优化一下：

```swift
class Solution {
    func backspaceCompare(_ S: String, _ T: String) -> Bool {
        return build(S) == build(T)
    }
    func build(_ string: String) -> String {
        var s = ""
        for i in string {
            if i == "#" {
                s.popLast()
            } else {
                s.append(i)
            }
        }
        return s
    }
}
```

执行用时：4 ms 内存消耗：20.7 MB

### 双指针

```swift
class Solution {
    func backspaceCompare(_ S: String, _ T: String) -> Bool {
        var sIndex = S.count - 1
        var tIndex = T.count - 1
        while sIndex >= 0 && tIndex >= 0 {
            sIndex = indexCalc(S, sIndex)
            tIndex = indexCalc(T, tIndex)
            guard sIndex >= 0 && tIndex >= 0 else {
                return sIndex == -1 && tIndex == -1
            }
            if S[S.index(S.startIndex, offsetBy: sIndex)] !=
               T[T.index(T.startIndex, offsetBy: tIndex)] {
                return false
            }
            sIndex -= 1
            tIndex -= 1
        }
        sIndex = indexCalc(S, sIndex)
        tIndex = indexCalc(T, tIndex)//确保值稳定
        return sIndex == -1 && tIndex == -1
    }
    func indexCalc(_ string: String, _ i: Int) -> Int {
        var index = i
        while index >= 0 {
            if string[string.index(string.startIndex, offsetBy: index)] == "#" {
                index = indexCalc(string, index - 1) - 1
            } else {
                break
            }
        }
        return index > -1 ? index : -1//处理溢出
    }
}
```

执行用时：20 ms 内存消耗：20.6 MB

## 用栈实现队列

[用栈实现队列 - 力扣](https://leetcode-cn.com/problems/implement-queue-using-stacks/)

> 使用栈实现队列的下列操作：
> 
> push(x) -- 将一个元素放入队列的尾部。
> 
> pop() -- 从队列首部移除元素。
> 
> peek() -- 返回队列首部的元素。
> 
> empty() -- 返回队列是否为空。
> 
> 示例:
> 
> MyQueue queue = new MyQueue();
> 
> queue.push(1);
> 
> queue.push(2);  
> 
> queue.peek();  // 返回 1
> 
> queue.pop();   // 返回 1
> 
> queue.empty(); // 返回 false
>  
> 
> 说明:
> 
> 你只能使用标准的栈操作 -- 也就是只有 `push to top`, `peek/pop from top`, `size`, 和 `is empty` 操作是合法的。
> 
> 你所使用的语言也许不支持栈。你可以使用 list 或者 deque（双端队列）来模拟一个栈，只要是标准的栈操作即可。
> 
> 假设所有操作都是有效的 （例如，一个空的队列不会调用 pop 或者 peek 操作）。

```swift
class MyQueue {
    var queueIn: [Int]
    var queueOut: [Int]
    /** Initialize your data structure here. */
    init() {
        queueIn = []
        queueOut = []
    }
    
    /** Push element x to the back of queue. */
    func push(_ x: Int) {
        queueIn.append(x)
    }
    
    /** Removes the element from in front of queue and returns that element. */
    func pop() -> Int {
        if queueOut.isEmpty {
            for _ in queueIn {
                queueOut.append(queueIn.popLast()!)
            }
        }
        return queueOut.popLast()!
    }
    
    /** Get the front element. */
    func peek() -> Int {
        if queueOut.isEmpty {
            for _ in queueIn {
                queueOut.append(queueIn.popLast()!)
            }
        }
        return queueOut.last!
    }
    
    /** Returns whether the queue is empty. */
    func empty() -> Bool {
        return queueIn.isEmpty && queueOut.isEmpty
    }
}

/**
 * Your MyQueue object will be instantiated and called as such:
 * let obj = MyQueue()
 * obj.push(x)
 * let ret_2: Int = obj.pop()
 * let ret_3: Int = obj.peek()
 * let ret_4: Bool = obj.empty()
 */
```

执行用时：4 ms 内存消耗：21.4 MB

本题和下面的一道题，都是用栈或队列来实现彼此。基本思路都是`负负得正`的思维。最初虽然想到了（也就是官方题解的方法一），但没有想到优化的方式，即每次pop之后不用再归还回去，等out栈没有了再从in栈倒过来。后面这种方法在pop的时候，就可以达到`摊还复杂度O(1)`的时间复杂度了。

在这道题之后，还顺便测试了`for...in...`语句中`in`后面的`iteratable thing`，即使在循环的过程中变化，但`for...in...`语句仍然会按照最初运行的时候来循环。在本题中，我们只是恰好需要循环栈元素个数次数，所以也并无大碍。

## 用队列实现栈

[用队列实现栈 - 力扣](https://leetcode-cn.com/problems/implement-stack-using-queues/)

> 使用队列实现栈的下列操作：
> 
> push(x) -- 元素 x 入栈
> 
> pop() -- 移除栈顶元素
> 
> top() -- 获取栈顶元素
> 
> empty() -- 返回栈是否为空
> 
> 注意:
> 
> 你只能使用队列的基本操作-- 也就是 `push to back`, `peek/pop from front`, `size`, 和 `is empty` 这些操作是合法的。
> 
> 你所使用的语言也许不支持队列。 你可以使用 list 或者 deque（双端队列）来模拟一个队列 , 只要是标准的队列操作即可。
> 
> 你可以假设所有操作都是有效的（例如, 对一个空的栈不会调用 pop 或者 top 操作）。

这道题主要有两种思路，第一种就是利用两个队列的空间，牺牲push或者pop的时间复杂度，这里只列举牺牲push的情况；第二种则只利用一个队列的空间，牺牲push的复杂度，只是每次push的时候将队列前面已有的元素重新添加到尾部一遍。

### 双队列，牺牲push

```swift
class MyStack {
    var stackIn: [Int]
    var stackOut: [Int]
    /** Initialize your data structure here. */
    init() {
        stackIn = []
        stackOut = []
    }
    
    /** Push element x onto stack. */
    func push(_ x: Int) {
        stackIn.append(x)
        for _ in stackOut {
            stackIn.append(stackOut.removeFirst())
        }
        (stackIn, stackOut) = (stackOut, stackIn)
    }
    
    /** Removes the element on top of the stack and returns that element. */
    func pop() -> Int {
        return stackOut.removeFirst()
    }
    
    /** Get the top element. */
    func top() -> Int {
        return stackOut.first!
    }
    
    /** Returns whether the stack is empty. */
    func empty() -> Bool {
        return stackOut.isEmpty
    }
}

/**
 * Your MyStack object will be instantiated and called as such:
 * let obj = MyStack()
 * obj.push(x)
 * let ret_2: Int = obj.pop()
 * let ret_3: Int = obj.top()
 * let ret_4: Bool = obj.empty()
 */
```

执行用时：8 ms 内存消耗：21.4 MB

### 单队列解法

```swift
class MyStack {
    var stack: [Int]
    /** Initialize your data structure here. */
    init() {
        stack = []
    }
    
    /** Push element x onto stack. */
    func push(_ x: Int) {
        stack.append(x)
        for _ in 0..<stack.count - 1 {
            stack.append(stack.removeFirst())
        }
    }
    
    /** Removes the element on top of the stack and returns that element. */
    func pop() -> Int {
        return stack.removeFirst()
    }
    
    /** Get the top element. */
    func top() -> Int {
        return stack.first!
    }
    
    /** Returns whether the stack is empty. */
    func empty() -> Bool {
        return stack.isEmpty
    }
}

/**
 * Your MyStack object will be instantiated and called as such:
 * let obj = MyStack()
 * obj.push(x)
 * let ret_2: Int = obj.pop()
 * let ret_3: Int = obj.top()
 * let ret_4: Bool = obj.empty()
 */
```

执行用时：12 ms 内存消耗：21.3 MB

理论上复杂度和前者一样，执行用时就不纠结了吧，内存消耗确实少了一些。但最重要的还是开阔思维。

## 有效的括号

[有效的括号 - 力扣](https://leetcode-cn.com/problems/valid-parentheses/)

> 给定一个只包括 `'('`，`')'`，`'{'，'}'`，`'['，']'` 的字符串，判断字符串是否有效。
> 
> 有效字符串需满足：
> 
> 左括号必须用相同类型的右括号闭合。
> 
> 左括号必须以正确的顺序闭合。
> 
> 注意空字符串可被认为是有效字符串。

这道题没有太多的解法，都是实现一个栈，通过入栈出栈的方式来解题。核心的考点在于具体实现上充分利用语言的特性来优化代码。

### map映射

```swift
class Solution {
    func isValid(_ s: String) -> Bool {
        let map: [Character:Character] = [")":"(", "]":"[", "}":"{"]
        var stack: [Character] = []
        for i in s {
            if map.values.contains(i) {
                stack.append(i)
            }
            else if stack.isEmpty || map[i] != stack.popLast() {
                return false
            }
        }
        return stack.isEmpty
    }
}
```

执行用时：8 ms 内存消耗：21.8 MB

需要注意的就是Swift语法，一个是在用`For...in...`来遍历字符串的时候，每次返回的值是`'String.Element' (aka 'Character')`，所以在声明map的时候要注意声明`Character`，单个字符默认会被当做String。或者也可以使用description来将字符转为字符串。第二点是`popLast()`方法，也即Python中的pop()方法，用来将数组中最后一个元素返回并删除。这个解法的主要关注点还是在于代码的精炼，特别是else if的条件写法。

### 子字符串替换

题解中有人用Python给出了另类的解法，即不断替换字符串中的`()`、`[]`、`{}`来验证字符串是否匹配。这里给出了Swift版：

```swift
import Foundation
class Solution {
    func isValid(_ s: String) -> Bool {
        var string = s
        var len = 0
        while len != string.count {
            len = string.count
            string = string.replacingOccurrences(of: "()", with: "")
                .replacingOccurrences(of: "[]", with: "")
                .replacingOccurrences(of: "{}", with: "")
        }
        return string.isEmpty
    }
}
```

执行用时：1236 ms 内存消耗：21.7 MB

可以看出，这种算法的时间复杂度平均高达O(n2)，并且可能由于`replaceOccurrences`需要导入Foundation库，整体的耗时非常长。不推荐，只是作为一种思路的开阔来学习。
