# LeetCode@Swift - Vol.9 递归和分治

递归的基本用法在之前的文章中已经有提到也有过不少的应用。对于分治，Divide & Conquer，很重要的一点在于`Divide`，比如接下来的这一题。

## Pow(x, n)

[Pow(x, n) - 力扣](https://leetcode-cn.com/problems/powx-n/)

> 实现 pow(x, n) ，即计算 x 的 n 次幂函数。

### 递归法

递归法第一时间想到的是n = n - 1这样递归下去。但n大一点的用例会直接爆内存。这里的`Divide`，应该采取按奇偶两种情况分成两部分或三部分，相等的两部分直接计算其中一个即可。

```swift
class Solution {
    func myPow(_ x: Double, _ n: Int) -> Double {
        guard n != 0 else { return 1 }
        if n < 0 {
            return myPow(1/x, -n)
        } else {
            if n % 2 == 0 {
                let temp = myPow(x, n / 2)
                return temp * temp
            } else {
                let temp = myPow(x, n / 2)
                return temp * temp * x
            }
        }
    }
}
```

执行用时：4 ms 内存消耗：20.8 MB

## 多数元素

[多数元素 - 力扣](https://leetcode-cn.com/problems/majority-element/)

> 给定一个大小为 n 的数组，找到其中的多数元素。多数元素是指在数组中出现次数大于 ⌊ n/2 ⌋ 的元素。
> 
> 你可以假设数组是非空的，并且给定的数组总是存在多数元素。

### 哈希表

遍历数组，按key存入map，存入时如果发现已经超过一半（题目有保证一定存在）则直接返回

```swift
class Solution {
    func majorityElement(_ nums: [Int]) -> Int {
        var dict: [Int: Int] = [:]
        let length = nums.count
        for item in nums {
            if dict[item] == nil { dict[item] = 0 }
            dict[item]! += 1
            if dict[item]! > length / 2 {
                return item
            }
        }
        return -1
    }
}
```

执行用时：240 ms 内存消耗：21 MB

### 递归法

递归法在这里的思路是，将数组递归平分，如果左边出现最多的数和右边出现最多的数相等，则直接返回这个数，如果不相等，则去统计这两个数在这两个部分中分别出现过多少次，返回出现较多的数。

```swift
class Solution {
    func majorityElement(_ nums: [Int]) -> Int {
        if nums.count == 1 { return nums[0] }
        let leftMajor = majorityElement(Array(nums[0..<nums.count/2]))
        let rightMajor = majorityElement(Array(nums[nums.count/2..<nums.count]))
        if leftMajor == rightMajor {
            return leftMajor //or rightMajor
        } else {
            var leftCount = 0, rightCount = 0
            for item in nums {
                if item == leftMajor {
                    leftCount += 1
                }
                else if item == rightMajor {
                    rightCount += 1
                }
            }
            return leftCount < rightCount ? rightMajor : leftMajor
        }
    }
}
```

执行用时：936 ms 内存消耗：21.4 MB

### 摩尔投票法

对于这道题来说，其实最高效的办法还是摩尔投票法，原理即为，多数元素比其他所有元素加起来还要多。

```swift
class Solution {
    func majorityElement(_ nums: [Int]) -> Int {
        var count = 0
        var result: Int = -1
        for item in nums {
            guard count != 0 else {
                result = item
                count += 1
                continue
            }
            if item == result {
                count += 1
            } else {
                count -= 1
            }
        }
        return result
    }
}
```

执行用时：164 ms 内存消耗：21.2 MB

可以稍微优化一下：

```swift
class Solution {
    func majorityElement(_ nums: [Int]) -> Int {
        var count = 0, result = -1
        for item in nums {
            if count == 0 { result = item }
            count += item == result ? 1 : -1
        }
        return result
    }
}
```

### 排序法

排序法，虽迟但到。

排好序，中间的数字肯定是多数元素。（在保证一定有多数元素存在的前提下）

```swift
class Solution {
    func majorityElement(_ nums: [Int]) -> Int {
        var sorted = nums.sorted()
        return sorted[nums.count/2]
    }
}
```

执行用时：204 ms 内存消耗：21.3 MB

思路和代码足够简单，但时间就不足够快了。

## 求众数 II

[求众数 II - 力扣](https://leetcode-cn.com/problems/majority-element-ii/)

> 给定一个大小为 n 的数组，找出其中所有出现超过 ⌊ n/3 ⌋ 次的元素。
> 
> 说明: 要求算法的时间复杂度为 O(n)，空间复杂度为 O(1)。

再跑一下题，本题是和前一道题类似，不过和分治没太多关系的一道题，仅为个人做题顺序。

### 哈希表

思路和前一道题相同，时间表现不算最佳但尚可。

```swift
class Solution {
    func majorityElement(_ nums: [Int]) -> [Int] {
        var dict: [Int: Int] = [:]
        var result: Set<Int> = []
        for item in nums {
            if dict[item] == nil { dict[item] = 0 }
            dict[item]! += 1
            if dict[item]! > nums.count / 3 {
                result.insert(item)
            }
        }
        return Array(result)
    }
}
```

执行用时：160 ms 内存消耗：23 MB

### 摩尔投票改进版☆

超过n/3的元素最多有两个。

注意，题目并没有保证一定存在，所以最后有一遍校验。

```swift
class Solution {
    func majorityElement(_ nums: [Int]) -> [Int] {
        guard nums.count != 0 else { return [] }
        var num1 = nums[0], num2 = nums[0]
        var count1 = 0, count2 = 0
        for item in nums {
            if item == num1 {
                count1 += 1
            }
            else if item == num2 {
                count2 += 1
            }
            else if count1 == 0 {
                num1 = item
                count1 += 1
            }
            else if count2 == 0 {
                num2 = item
                count2 += 1
            } else {
                count1 -= 1
                count2 -= 1
            }
        }
        count1 = 0
        count2 = 0
        for item in nums {
            if item == num1 {
                count1 += 1
            }
            else if item == num2 {
                count2 += 1
            }
        }
        var result: [Int] = []
        if count1 > nums.count / 3 {
            result.append(num1)
        }
        if count2 > nums.count / 3 {
            result.append(num2)
        }
        return result
    }
}
```

执行用时：112 ms 内存消耗：21.5 MB