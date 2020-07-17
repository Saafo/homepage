# LeetCode@Swift - Vol.6 滑动窗口

## 滑动窗口题型总结

滑动窗口算得上面试中的非常高频的题型。

滑动窗口主要用来处理连续问题。比如题目求解“连续子串...”、“连续子数组...”，这时就应该能想到滑动窗口。

从类型上，滑动窗口主要有以下三种题型：

* 固定窗口大小
* 窗口大小不固定，求解最大的满足条件的窗口
* 窗口大小不固定，求解最小的满足条件的窗口

后两种都称之为`可变窗口`。当然，基本思路都是一样的。

### 固定窗口大小

对于固定窗口，只需要固定初始化左右指针`l`和`r`，分别表示窗口的左右定点，注意：

* `l`初始化为0
* 初始化`r`，使得`r - l + 1`等于窗口大小
* 同时移动`l`和`r`
* 判断窗口内的连续元素是否满足题目限定的条件

一个可行的思路是，将`窗口内的元素是否满足条件`转化为`窗口边缘的两个元素是否满足条件`。具体可以建立辅助数组来实现。[滑动窗口最大值](#滑动窗口最大值)的第三种解法即使如此。

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

## 长度最小的子数组

[长度最小的子数组 - 力扣](https://leetcode-cn.com/problems/minimum-size-subarray-sum/)

> 给定一个含有 n 个正整数的数组和一个正整数 s ，找出该数组中满足其和 ≥ s 的长度最小的 连续 子数组，并返回其长度。如果不存在符合条件的子数组，返回 0。
> 
> 示例：
> 
> 输入：s = 7, nums = [2,3,1,2,4,3]
> 
> 输出：2
> 
> 解释：子数组 [4,3] 是该条件下的长度最小的子数组。
> 
> 进阶：
> 
> 如果你已经完成了 O(n) 时间复杂度的解法, 请尝试 O(n log n) 时间复杂度的解法。

### 可变窗口

```swift
class Solution {
    func minSubArrayLen(_ s: Int, _ nums: [Int]) -> Int {
        guard nums.count > 0 else { return 0 }
        var minLen = Int.max
        var i = 0
        var j = 0
        var sum = nums[0]
        while i <= j && j < nums.count {
            if sum < s {
                guard j < nums.count - 1 else { break }
                j += 1
                sum += nums[j]
            }
            else {
                minLen = min(minLen, j - i + 1)
                sum -= nums[i]
                i += 1
            }
        }
        return minLen == Int.max ? 0 : minLen
    }
}
```

执行用时：72 ms 内存消耗：21 MB

看了下题解，可以优化的有几点：

* 出现num\[index\]当前数据为目标值，直接return 1
* 出现当前计算的区域长度为1且满足条件，直接结束循环，return 1

优化后代码

```swift
class Solution {
    func minSubArrayLen(_ s: Int, _ nums: [Int]) -> Int {
        guard nums.count > 0 else { return 0 }
        var minLen = Int.max
        var i = 0
        var sum = 0
        for (j, item) in nums.enumerated() {
            guard item != s else { return 1 }
            sum += item
            while sum >= s {
                guard i != j else { return 1 }
                minLen = min(minLen, j - i + 1)
                sum -= nums[i]
                i += 1
            }
        }
        return minLen == Int.max ? 0 : minLen
    }
}
```

执行用时：72 ms 内存消耗：21.1 MB（说明：尝试提交过多次，在72~108之前飘动，感觉纠结这一点时间意义不大）

参考文章：[一文带你AC十道题【滑动窗口】- lucifer210](https://cloud.tencent.com/developer/article/1600147)