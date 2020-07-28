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

## 无重复字符的最长子串

[无重复字符的最长子串 - 力扣](https://leetcode-cn.com/problems/longest-substring-without-repeating-characters/)

> 给定一个字符串，请你找出其中不含有重复字符的 最长子串 的长度。
> 
> 示例 1:
> 
> 输入: "abcabcbb"
> 
> 输出: 3 
> 
> 解释: 因为无重复字符的最长子串是 "abc"，所以其长度为 3。
> 
> 示例 2:
> 
> 输入: "bbbbb"
> 
> 输出: 1
> 
> 解释: 因为无重复字符的最长子串是 "b"，所以其长度为 1。
> 
> 示例 3:
> 
> 输入: "pwwkew"
> 
> 输出: 3
> 
> 解释: 因为无重复字符的最长子串是 "wke"，所以其长度为 3。
> 请注意，你的答案必须是 子串 的长度，"pwke" 是一个子序列，不是子串。

### 滑动窗口

考虑滑动窗口解法，先上原始代码：

```swift
class Solution {
    func lengthOfLongestSubstring(_ s: String) -> Int {
        guard s.count > 1 else { return s.count }
        var maxLen = 0
        var stack: [Character] = []
        for top in s {
            while stack.contains(top) {
                stack.removeFirst()
            }
            stack.append(top)
            maxLen = max(maxLen, stack.count)
        }
        return maxLen
    }
}
```

执行用时：560 ms 内存消耗：21 MB

可以看出用的时间非常多，所以需要优化一下。

我们知道`contains()`方法对普通的数组的时间复杂度是O(n)，所以我们可以避免每次都用`contains()`来查询字符串中是否还有top元素，一旦发现有之后，每次直接去找第一个元素。代码如下：

```swift
class Solution {
    func lengthOfLongestSubstring(_ s: String) -> Int {
        guard s.count > 1 else { return s.count }
        var maxLen = 0
        var stack: [Character] = []
        for top in s {
            if stack.contains(top) {
                while stack[0] != top {
                    stack.removeFirst()
                }
                stack.removeFirst()
            }
            stack.append(top)
            maxLen = max(maxLen, stack.count)
        }
        return maxLen
    }
}
```

执行用时：120 ms 内存消耗：20.9 MB

可以看出执行时间有了非常大的提升，以后在使用contains()的方法的时候，应该主注意**如果在对非Hashable对象**使用时，避免过多地循环使用（此时时间复杂度为O(n))。

### 滑动窗口改进版

不过即使做了一定的改进，我们仍然需要通过一个一个removeFirst的方式来确定窗口左边界的位置。我们完全可以用一个map来记录每种元素出现过的最后一个位置，代码如下：

```swift
class Solution {
    func lengthOfLongestSubstring(_ s: String) -> Int {
        guard s.count > 1 else { return s.count }
        var characters = Array(s)
        var start = 0, ans = 0
        var dict:[Character: Int] = [:]
        for (end, item) in characters.enumerated() {
            if let position = dict[item] {
                start = max(start, position + 1)
            }
            dict[item] = end
            ans = max(ans, end - start + 1)
        }
        return ans
    }
}
```

执行用时：68 ms 内存消耗：21.2 MB

这里需要特别注意的是两个max()的用处。

## 最小覆盖子串

[最小覆盖子串 - 力扣](https://leetcode-cn.com/problems/minimum-window-substring/)

> 给你一个字符串 S、一个字符串 T，请在字符串 S 里面找出：包含 T 所有字符的最小子串。
> 
> 示例：
> 
> 输入: S = "ADOBECODEBANC", T = "ABC"
> 
> 输出: "BANC"
> 
> 说明：
> 
> 如果 S 中不存这样的子串，则返回空字符串 ""。
> 
> 如果 S 中存在这样的子串，我们保证它是唯一的答案。

### 滑动窗口

还是先采用普通的滑动窗口方法:

```swift
class Solution {
    func minWindow(_ s: String, _ t: String) -> String {
        guard s.count > 0 && s.count >= t.count else { return "" }
        var dict: [Character: Int] = [:]
        var start = 0, match = 0, tdif = 0
        var result: (Int, Int) = (-1, -1)
        var midResult: (Int, Int) = (-1, -1)
        for c in t {
            if dict[c] == nil { tdif += 1 }
            dict[c] = dict[c] == nil ? -1 : dict[c]! - 1
        }
        for (end, char) in s.enumerated() {
            guard dict[char] != nil else { continue }
            dict[char]! += 1
            if dict[char] == 0 {
                match += 1
                if match == tdif { //刚刚匹配上
                    while true {
                        midResult = (start, end)
                        let firstChar = s[s.index(s.startIndex, offsetBy: start)]
                        start += 1
                        guard dict[firstChar] != nil else { continue }
                        dict[firstChar]! -= 1
                        if dict[firstChar]! < 0 { 
                            match -= 1
                            break
                        }
                    }
                    
                }
                
            }
            if midResult.0 != -1 {
                if result.0 == -1 {
                    result = midResult
                } else {
                    if result.1 - result.0 > midResult.1 - midResult.0 {
                        result = midResult
                    }
                }
            }
        }
        return result.0 == -1 ? "" : String(s[s.index(s.startIndex, offsetBy: result.0)...s.index(s.startIndex, offsetBy: result.1)])
    }
}
```

不过这样发现运行超时，超时的用例中字符串和匹配的字符串长度都非常长。于是尝试将字符串先转换成`[Character]`，如下：

```swift
class Solution {
    func minWindow(_ s: String, _ t: String) -> String {
        guard s.count > 0 && s.count >= t.count else { return "" }
        var S = Array(s)
        var T = Array(t)
        var dict: [Character: Int] = [:]
        var start = 0, match = 0, tdif = 0
        var result: (Int, Int) = (-1, -1)
        var midResult: (Int, Int) = (-1, -1)
        for c in T {
            if dict[c] == nil { tdif += 1 }
            dict[c] = dict[c] == nil ? -1 : dict[c]! - 1
        }
        for end in 0..<S.count {
            let char = S[end]
            guard dict[char] != nil else { continue }
            dict[char]! += 1
            if dict[char] == 0 {
                match += 1
                if match == tdif { //刚刚匹配上
                    while true {
                        midResult = (start, end)
                        let firstChar = S[start]
                        start += 1
                        guard dict[firstChar] != nil else { continue }
                        dict[firstChar]! -= 1
                        if dict[firstChar]! < 0 { 
                            match -= 1
                            break
                        }
                    }
                    
                }
                
            }
            if midResult.0 != -1 {
                if result.0 == -1 {
                    result = midResult
                } else {
                    if result.1 - result.0 > midResult.1 - midResult.0 {
                        result = midResult
                    }
                }
            }
        }
        return result.0 == -1 ? "" : String(S[result.0...result.1])
    }
}
```

执行用时：200 ms 内存消耗：21.8 MB

果然顺利通过，以后做字符串相关的题目，还是先转换成\[Character\]吧。

探究了一下原因，主要在于String中每个字符的长度不同，所以计算Index的时间复杂度其实是O(n)，如果大量地计算index值会非常花时间。有关Swift字符串的相关原理可以参考[这篇文章](https://juejin.im/post/5da1ddfbe51d45782e6039e5)。

本题还有更高效的解法，暂时不做讨论。//TODO

## 找到字符串中所有字母异位词

[找到字符串中所有字母异位词 - 力扣](https://leetcode-cn.com/problems/find-all-anagrams-in-a-string/)

> 给定一个字符串 s 和一个非空字符串 p，找到 s 中所有是 p 的字母异位词的子串，返回这些子串的起始索引。
> 
> 字符串只包含小写英文字母，并且字符串 s 和 p 的长度都不超过 20100。
> 
> 说明：
> 
> 字母异位词指字母相同，但排列不同的字符串。
> 
> 不考虑答案输出的顺序。

### 滑动窗口

暂时只提供滑动窗口常规解法

```swift
class Solution {
    func findAnagrams(_ s: String, _ p: String) -> [Int] {
        guard s.count > 0 && s.count >= p.count else { return [] }
        let S = Array(s)
        let P = Array(p)
        var dict: [Character: Int] = [:]
        var result: [Int] = []
        var left = 0, right = 0, pDiff = 0, match = 0
        for i in P {
            if dict[i] == nil { pDiff += 1 }
            dict[i] = dict[i] == nil ? -1 : dict[i]! - 1
        }
        outer: while left <= S.count - P.count {
            var tempDict = dict
            for index in 0..<0+P.count {
                let item = S[left + index]
                guard tempDict[item] != nil else {
                    left += index + 1
                    continue outer
                }
                tempDict[item]! += 1
                if tempDict[item]! > 0 {
                    left += 1
                    continue outer
                }
            }
            result.append(left)
            match = pDiff
            right = left + P.count //加速！
            while right < S.count && tempDict[S[right]] != nil {
                tempDict[S[right]]! += 1
                if tempDict[S[right]] == 0 { match += 1 }
                tempDict[S[left]]! -= 1
                if tempDict[S[left]] == -1 { match -= 1 }
                left += 1
                right += 1
                if match == pDiff { result.append(left) }
            }
            left = right + 1
        }
        return result
    }
}
```

执行用时：160 ms 内存消耗：22.3 MB

## 水果成篮

[水果成篮 - 力扣](https://leetcode-cn.com/problems/fruit-into-baskets/)

> 在一排树中，第 i 棵树产生 tree[i] 型的水果。
> 
> 你可以从你选择的任何树开始，然后重复执行以下步骤：
> 
> 把这棵树上的水果放进你的篮子里。如果你做不到，就停下来。
> 
> 移动到当前树右侧的下一棵树。如果右边没有树，就停下来。
> 
> 请注意，在选择一颗树后，你没有任何选择：你必须执行步骤 1，然后执行步骤 2，然后返回步骤 1，然后执行步骤 2，依此类推，直至停止。
> 
> 你有两个篮子，每个篮子可以携带任何数量的水果，但你希望每个篮子只携带一种类型的水果。
> 
> 用这个程序你能收集的水果总量是多少？

### 滑动窗口

```swift
class Solution {
    func totalFruit(_ tree: [Int]) -> Int {
        guard tree.count > 2 else { return tree.count }
        var result = 0
        var left = 0
        var dict: [Int:Int] = [:]
        for (right, item) in tree.enumerated() {
            guard !dict.keys.contains(item) else {
                dict[item] = right
                result = max(result, right - left + 1)
                continue
                }
            if dict.count < 2 {
                dict[item] = right
                continue
            } else {
                result = max(result, right - left)
                let minValue = dict.values.min()!
                let minKey: Int? = {
                    for (key, value) in dict {
                        if value == minValue {
                            return key
                        }
                    }
                    return nil
                }()
                left = right - 1
                while tree[left] == tree[left - 1] {
                    left -= 1
                }
                dict[minKey!] = nil
                dict[item] = right
            }
        }
        return result
    }
}
```

执行用时：1280 ms 内存消耗：22.9 MB

## 和相同的二元子数组

[和相同的二元子数组 - 力扣](https://leetcode-cn.com/problems/binary-subarrays-with-sum/)

> 在由若干 0 和 1  组成的数组 A 中，有多少个和为 S 的非空子数组。

自己写得太拉胯了，以后再整理更好的解法。//TODO

参考文章：[一文带你AC十道题【滑动窗口】- lucifer210](https://cloud.tencent.com/developer/article/1600147)