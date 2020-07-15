# LeetCode@Swift - Vol.6 滑动窗口

滑动窗口算得上面试中的非常高频的题型。

## 滑动窗口最大值

[滑动窗口最大值 - 力扣](https://leetcode-cn.com/problems/sliding-window-maximum/)

> 给定一个数组 nums，有一个大小为 k 的滑动窗口从数组的最左侧移动到数组的最右侧。你只可以看到在滑动窗口内的 k 个数字。滑动窗口每次只向右移动一位。
> 
> 返回滑动窗口中的最大值。
> 
> 进阶：
> 
> 你能在线性时间复杂度内解决此题吗？
> 
> 示例:
> 
> 输入: nums = [1,3,-1,-3,5,3,6,7], 和 k = 3
> 输出: [3,3,5,5,6,7] 
>  
> 提示：
> 
> 1 <= nums.length <= 10^5
> 
> -10^4 <= nums[i] <= 10^4
> 
> 1 <= k <= nums.length

这道题的思路，一个是可以维持一个大顶堆，不过首先时间复杂度上来说是log n的复杂度，另一个，在窗口离开的时候，删除节点也是挺麻烦的一件事情。

### 原始方法

这道题我首先采用了滑动窗口，将新来的元素与窗口中的元素一一比较，如果窗口中的元素比新来的元素小，则直接除籍。然后，无论如何也让新元素加进窗口。代码如下：

```swift
class Solution {
    func maxSlidingWindow(_ nums: [Int], _ k: Int) -> [Int] {
        var indexStack: [Int] = []
        var result: [Int] = []
        for i in 0..<k {
            if indexStack.isEmpty { indexStack.append(i) }
            else {
                indexStack.removeAll() {nums[$0] < nums[i] }
                indexStack.append(i)
            }
        }
        result.append(nums[indexStack[0]])
        for i in 0..<nums.count - k {
            if indexStack[0] == i { indexStack.removeFirst() }
            if indexStack.isEmpty { indexStack.append(i + k) }
            else {
                indexStack.removeAll() { nums[$0] < nums[i + k] }
                indexStack.append(i + k)
            }
            result.append(nums[indexStack[0]])
        }
        return result
    }
}
```

执行用时：792 ms 内存消耗：26.4 MB

这个解法用到了`removeAll(where: <closure>)`函数。之前一直采用的是这样的方法：

```swift
for indexOfIndex in 0..<indexStack.count {
    if nums[indexStack[indexOfIndex]] < nums[i + k] {
        indexStack.remove(at: indexOfIndex)
    }
}
```

但有个很明显的错误就是，在删除之后，原数组的index会更新，最终会出现index out of range的错误。所以按条件删除，还是用自带的removeAll()函数比较安全。

不过很明显的问题就是，耗时太久了。只击败了5.83%的用户。

### 双端队列Deque

把原始方法中的`removeAll(where: <closure>)`换成规范的双端队列操作即可，即换成：

```swift
while !indexStack.isEmpty && nums[indexStack.last!] < nums[i or i + k] {
    indexStack.popLast()
}
```

完整代码：

```swift
class Solution {
    func maxSlidingWindow(_ nums: [Int], _ k: Int) -> [Int] {
        var indexStack: [Int] = []
        var result: [Int] = []
        for i in 0..<k {
            if indexStack.isEmpty { indexStack.append(i) }
            else {
                while !indexStack.isEmpty && nums[indexStack.last!] < nums[i] {
                    indexStack.popLast()
                }
                indexStack.append(i)
            }
        }
        result.append(nums[indexStack[0]])
        for i in 0..<nums.count - k {
            if indexStack[0] == i { indexStack.removeFirst() }
            if indexStack.isEmpty { indexStack.append(i + k) }
            else {
                while !indexStack.isEmpty && nums[indexStack.last!] < nums[i + k] {
                    indexStack.popLast()
                }
                indexStack.append(i + k)
            }
            result.append(nums[indexStack[0]])
        }
        return result
    }
}
```

执行用时：464 ms 内存消耗：26.5 MB

所耗内存增加了一点点，但时间减少了接近一半，算是正常范围了。

我们能发现两个循环大概是一致的，可以合并一下：

```swift
class Solution {
    func maxSlidingWindow(_ nums: [Int], _ k: Int) -> [Int] {
        var indexStack: [Int] = []
        var result: [Int] = []
        for i in 0..<nums.count {
            if !indexStack.isEmpty && indexStack[0] == i - k { indexStack.removeFirst() }
            while !indexStack.isEmpty && nums[indexStack.last!] < nums[i] {
                indexStack.popLast()
            }
            indexStack.append(i)
            if i >= k - 1 {
                result.append(nums[indexStack[0]])
            }
        }
        return result
    }
}
```

执行用时：472 ms 内存消耗：25.9 MB

### 动态规划

这个解法为官方的第三种解法，具体思路可以参考官方题解，甚为巧妙。

```swift
class Solution {
    func maxSlidingWindow(_ nums: [Int], _ k: Int) -> [Int] {
        guard nums.count * k != 0 else { return [] }
        guard k != 1 && nums.count != 1 else { return nums }
        var left = [Int](repeating: -1, count: nums.count)
        var right = [Int](repeating: -1, count: nums.count)
        var result: [Int] = []
        
        for i in 0..<nums.count {
            if (i + 1) % k == 1 {
                left[i] = nums[i]
            } else {
                left[i] = max(left[i - 1], nums[i])
            }
            let j = nums.count - 1 - i
            if (j + 1) % k == 0 || i == 0 {
                right[j] = nums[j]
            } else {
                right[j] = max(right[j + 1], nums[j])
            }
        }
        for i in 0...nums.count - k {
            result.append(max(right[i], left[i + k - 1]))
        }
        return result
    }
}
```

执行用时：412 ms 内存消耗：25.7 MB
