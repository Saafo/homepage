# LeetCode@Swift - Vol.1 数组和字典的查找

最近开始接触Swift和LeetCode。这个系列的每一期主要是展示一道题的解法，然后逐步优化，顺便整理Swift相关语法。

[两数之和](https://leetcode-cn.com/problems/two-sum)

> 给定一个整数数组 nums 和一个目标值 target，请你在该数组中找出和为目标值的那 两个 整数，并返回他们的数组下标。
>
> 你可以假设每种输入只会对应一个答案。但是，数组中同一个元素不能使用两遍。
>
> 示例:
>
> 给定 nums = [2, 7, 11, 15], target = 9
>
> 因为 nums[0] + nums[1] = 2 + 7 = 9
> 所以返回 [0, 1]

## 无脑法

> 这是我刷的第一道题，啥都不会的时候只有用无脑法了。

```swift
class Solution {
    func twoSum(_ nums: [Int], _ target: Int) -> [Int] {
        for i in 0..<nums.count-1 {
            for j in i+1..<nums.count {
                if nums[i] + nums[j] == target {
                    return [i, j]
                }
            }
        }
        return []
    }
}
```

执行时间608ms, 内存消耗21.2MB。

执行时间较长，但内存消耗是所有方法中消耗最少的。

## 哈希表

看评论区可以用哈希表进行优化。

在Swift中，`Dictionary`是基于`hashable`协议的，`key`都是必须`hashable`的。带来的好处是，`hashable`是基于`equable`协议的，这样能保证`key`不重复。其次，我们可以用到`contains()函数`来快速查找`key`的存在。有两种具体的实现方式：

* dict.keys.contains(wantedKey)
* dict[wantedKey]

其中，`contains()`在官方文档中的时间复杂度为O(n)。但是在各种教程或者笔记中，这里的`contains()`似乎都被当成了O(1)。~~这是为什么啊？？~~<!-- TODO here -->

### 基于contains()的方案

```swift
class Solution {
    func twoSum(_ nums: [Int], _ target: Int) -> [Int] {
        var hashDict:[Int: Int] = [:]
        for i in 0..<nums.count {
            hashDict[nums[i]] = i
        }
        for i in 0..<nums.count-1 {
            if( hashDict.keys.contains(target - nums[i])) {
                if let location = hashDict[target - nums[i]] {
                    if (i != location) {
                        return [i, location]
                    }
                }
            }
        }
        return []
    }
}
```

执行用时40ms 内存消耗23MB。

但这里有三个优化点。其一，用了个大循环：先存入了所有数字到字典中，再进行遍历。此题的测试用例中可能数组长度较短。但在数组长度较长的情况下，我们完全可以避免多余的循环：将字典的创建放进后一个循环中。

```swift
class Solution {
    func twoSum(_ nums: [Int], _ target: Int) -> [Int] {
        var hashDict:[Int: Int] = [:]

        for i in 0..<nums.count {
            if( hashDict.keys.contains(target - nums[i])) {
                if let location = hashDict[target - nums[i]] {
                    if (i != location) {
                        return [i, location]
                    }
                }
            }
            hashDict[nums[i]] = i
        }
        return []
    }
}
```
执行用时：48 ms 内存消耗：22.9 MB

其二，先用`contains()`之后又要取一次`hashDict[]`的值，在这个具体问题下，我们不如直接取值。并且带来的一个优点是，`contains()`的复杂度其实是O(n)，但如果用字典直接查询key值,由于字典key本身哈希化的优化，其时间复杂度为O(1)。

其三，我们可以借助`enumerated()方法`来更方便地完成遍历，精简代码。最终代码如下：

```swift
class Solution {
    func twoSum(_ nums: [Int], _ target: Int) -> [Int] {
        var hashDict:[Int: Int] = [:]
        for (i, num) in nums.enumerated() {
            if let location = hashDict[target - num] {
                if (i != location) {
                    return [i, location]
                }
            }
            hashDict[nums[i]] = i
        }
        return []
    }
}
```
执行用时：40 ms 内存消耗：21.4 MB