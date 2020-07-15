# LeetCode@Swift - Vol.7 map和set

`map`和`set`的具体实现方式有`hashMap`、`treeMap`、`hashSet`和`treeSet`。具体的实现过程清楚原理即可，不在此赘述。

对应到语言中，map的一般实现方式，在Swift和Python中都是用`hashMap`来实现的，Java中可以指定hash/tree。set一般都有原生的类型。

## 有效的字母异位词

[有效的字母异位词 - 力扣](https://leetcode-cn.com/problems/valid-anagram/)

> 给定两个字符串 s 和 t ，编写一个函数来判断 t 是否是 s 的字母异位词。
> 
> 示例 1:
> 
> 输入: s = "anagram", t = "nagaram"
> 
> 输出: true
> 
> 示例 2:
> 
> 输入: s = "rat", t = "car"
> 
> 输出: false
> 
> 说明:
> 
> 你可以假设字符串只包含小写字母。
> 
> 进阶:
> 
> 如果输入字符串包含 unicode 字符怎么办？你能否调整你的解法来应对这种情况？

### 排序法

一开始是直接去想后一种方法了，忘了本身也可以通过排序来解决。可以采用快排来进行排序。这里直接用内置排序函数。

```swift
class Solution {
    func isAnagram(_ s: String, _ t: String) -> Bool {
        return s.sorted() == t.sorted()
    }
}
```

执行用时：596 ms 内存消耗：21.9 MB

### map法

```swift
class Solution {
    func isAnagram(_ s: String, _ t: String) -> Bool {
        guard s.count == t.count else { return false }
        var map: [Character: Int] = [:]
        for char in s {
            map[char] = map[char] != nil ? map[char]! + 1 : 1
        }
        for char in t {
            if map[char] != nil && map[char]! > 0 {
                map[char]! -= 1
            } else {
                return false
            }
        }
        for key in map.keys {
            if map[key] != 0 {
                return false
            }
        }
        return true
    }
}
```

执行用时：112 ms 内存消耗：21 MB

不过这里需要注意的是，首先可以在最前面验证两个字符串的长度，如果不相等就可以直接不比较了。其次，因为之后保证了两个字符串相等，所以最后一个For循环验证其实可以去掉...如此：

```swift
class Solution {
    func isAnagram(_ s: String, _ t: String) -> Bool {
        guard s.count == t.count else { return false }
        var map: [Character: Int] = [:]
        for char in s {
            map[char] = map[char] != nil ? map[char]! + 1 : 1
        }
        for char in t {
            if map[char] != nil && map[char]! > 0 {
                map[char]! -= 1
            } else {
                return false
            }
        }
        return true
    }
}
```

执行用时：116 ms 内存消耗：21.2 MB

其实还有更简单的方式，如果字符串值只包括26个小写字母，那么直接用一个长度26的数组也够了。在这里就不详写了。

## 两数之和

请见[LeetCode@Swift - Vol.1 数组和字典的查找 - 两数之和](https://blog.mintsky.xyz/20200630_lc-at-swift-01-finding-in-arrays-and-dicts#tip1)

## 三数之和

[三数之和 - 力扣](https://leetcode-cn.com/problems/3sum/)

三种方法，第一种是暴力法，在此省略。第二种是基于哈希表的O(n2)解法。第三种是排序后再用双指针前后夹逼法。

### 哈希表

先得到一个基本框架：

```swift
class Solution {
    func threeSum(_ nums: [Int]) -> [[Int]] {
        var result: [[Int]] = []
        for i in 0..<nums.count - 1 {
            for j in i+1..<nums.count {
                if nums[j...].contains(-nums[i] - nums[j]) {
                    result.append([nums[i], nums[j], -nums[i] - nums[j]])
                }
            }
        }
        return result
    }
}
```

但是这样的算法有个很严重的问题：一旦数据中出现了重复数据，那么带来的重复答案就没法剔除。因此，我们需要进行去重。显然，如果对产生后的答案进行去重的时间会非常多，因此去重需要在添加进结果集之前就做去重。具体的实现方式是对数据集先排序。

```swift
class Solution {
    func threeSum(_ nums: [Int]) -> [[Int]] {
        guard nums.count >= 3 else { return [] }
        var result: [[Int]] = []
        let data = nums.sorted()
        for i in 0..<data.count - 2 {
            if i - 1 >= 0 && data[i - 1] == data[i] { continue }
            for j in i+1..<data.count - 1 {
                if j - 1 >= i + 1 && data[j - 1] == data[j] { continue }
                if data[(j + 1)...].contains(-data[i] - data[j]) {
                    result.append([data[i], data[j], -data[i] - data[j]])
                }
            }
        }
        return result
    }
}
```

这样能过前310/313个用例。但在311个用例时会超出时间显示，所以可能只能采用双指针的解法。

### 排序 + 双指针

```swift
class Solution {
    func threeSum(_ nums: [Int]) -> [[Int]] {
        guard nums.count >= 3 else { return [] }
        var result: [[Int]] = []
        let data = nums.sorted()
        for i in 0..<data.count - 2 {
            if i - 1 >= 0 && data[i - 1] == data[i] { continue }
            var j = i + 1
            var k = data.count - 1
            while j < k {
                if data[i] + data[j] + data[k] < 0 {
                    repeat { j += 1 } while data[j - 1] == data[j] && j != k
                }
                else if data[i] + data[j] + data[k] > 0 {
                    repeat { k -= 1 } while data[k + 1] == data[k] && j != k
                }
                else {
                    result.append([data[i], data[j], data[k]])
                    repeat { j += 1 } while data[j - 1] == data[j] && j != k
                    if j == k { break }
                    repeat { k -= 1 } while data[k + 1] == data[k] && j != k
                }
            }
        }
        return result
    }
}
```

执行用时：300 ms 内存消耗：23.7 MB

稍微精简一下逻辑：

```swift
class Solution {
    func threeSum(_ nums: [Int]) -> [[Int]] {
        guard nums.count >= 3 else { return [] }
        var result: [[Int]] = []
        let data = nums.sorted()
        for i in 0..<data.count - 2 {
            if i - 1 >= 0 && data[i - 1] == data[i] { continue }
            var j = i + 1
            var k = data.count - 1
            while j < k {
                let sum = data[i] + data[j] + data[k]
                if sum < 0 { j += 1 }
                else if sum > 0 { k -= 1}
                else {
                    result.append([data[i], data[j], data[k]])
                    repeat { j += 1 } while j < k && data[j - 1] == data[j]
                    repeat { k -= 1 } while j < k && data[k + 1] == data[k]
                }
            }
        }
        return result
    }
}
```

执行用时：268 ms 内存消耗：23.7 MB

## 四数之和

[四数之和 - 力扣](https://leetcode-cn.com/problems/4sum/)

> 给定一个包含 n 个整数的数组 nums 和一个目标值 target，判断 nums 中是否存在四个元素 a，b，c 和 d ，使得 a + b + c + d 的值与 target 相等？找出所有满足条件且不重复的四元组。
> 
> 注意：
> 
> 答案中不可以包含重复的四元组。
> 
> 示例：
> 
> 给定数组 nums = [1, 0, -1, 0, -2, 2]，和 target = 0。
> 
> 满足要求的四元组集合为：
> [
>   [-1,  0, 0, 1],
> 
>   [-2, -1, 1, 2],
> 
>   [-2,  0, 0, 2]

思路与`三数之和`相同，多一层循环，复杂度为O(n3)

```swift
class Solution {
    func fourSum(_ nums: [Int], _ target: Int) -> [[Int]] {
        guard nums.count >= 4 else { return [] }
        var result: [[Int]] = []
        let data = nums.sorted()
        for p in 0..<data.count - 3 {
            guard p - 1 < 0 || data[p - 1] != data[p] else { continue }
            for i in (p+1)..<data.count - 2 {
                guard i - 1 < p + 1 || data[i - 1] != data[i] else { continue }
                var j = i + 1
                var k = data.count - 1
                while j < k {
                    let sum = data[p] + data[i] + data[j] + data[k]
                    if sum < target { j += 1 }
                    else if sum > target { k -= 1}
                    else {
                        result.append([data[p], data[i], data[j], data[k]])
                        repeat { j += 1 } while j < k && data[j - 1] == data[j]
                        repeat { k -= 1 } while j < k && data[k + 1] == data[k]
                    }
                }
            }
        }
        return result
    }
}
```