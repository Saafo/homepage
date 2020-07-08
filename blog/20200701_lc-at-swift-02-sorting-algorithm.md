# LeetCode@Swift - Vol.2 排序算法

## 寻找两个正序数组的中位数

[寻找两个正序数组的中位数 - 力扣](https://leetcode-cn.com/problems/median-of-two-sorted-arrays/)

> 给定两个大小为 m 和 n 的正序（从小到大）数组 nums1 和 nums2。
> 
> 请你找出这两个正序数组的中位数，并且要求算法的时间复杂度为 O(log(m + n))。
> 
> 你可以假设 nums1 和 nums2 不会同时为空。
> 
>  
> 
> 示例 1:
> 
> nums1 = [1, 3]
> nums2 = [2]
> 
> 则中位数是 2.0
> 示例 2:
> 
> nums1 = [1, 2]
> nums2 = [3, 4]
> 
> 则中位数是 (2 + 3)/2 = 2.5

### 无脑法

按惯例，来一波无脑法，直接用Swift内置的sort()方法（复杂度恰好就是O(nlogn)）:

```swift
import Foundation
class Solution {
    func findMedianSortedArrays(_ nums1: [Int], _ nums2: [Int]) -> Double {
        var nums: [Int] = nums1 + nums2
        nums.sort()
        let len: Int = nums.count
        if len % 2 == 0 {
            return Double(nums[len / 2 - 1] + nums[len / 2]) / 2
        }
        return Double(nums[(len - 1) / 2])
    }
}
```
执行用时：128 ms, 内存消耗：21.4 MB

#### sort()函数

Swift有很强大的`sort()`函数，借这道题的机会，我们来总结一下Swift的`sort()`函数。

> You can sort any mutable collection of elements that conform to the Comparable protocol by calling this method. Elements are sorted in ascending order.
> 
> The sorting algorithm is not guaranteed to be stable. A stable sort preserves the relative order of elements that compare equal.
> 
> Complexity: O(n log n), where n is the length of the collection.
> 
> 以上内容来自官方文档对于`sort()`函数的说明。

在使用方法上，sort可以跟`by: >`参数来实现降序排列，也可以`by: {闭包函数}`来实现自定类型的排序。具体使用方法可参考相关文档博客。

我们来了解一下关于`sort()`函数本身：

在`Swift 5`之前，Swift的排序算法是一个融合了快排、堆排、插排优点的混合算法`Introsort`。

在`Swift 5`之后，一个2018年10月将sort()算法从Introsort更改为[`修改过的Timsort`](https://github.com/apple/swift/blob/master/stdlib/public/core/Sort.swift)的PR被合并。

[参考来源](https://swiftrocks.com/introsort-timsort-swifts-sorting-algorithm.html)

Swift 5中排序的稳定性，官方宣称“不保证稳定”，具体解释看[这里](https://forums.swift.org/t/is-sort-stable-in-swift-5/21297/10)。

`Timsort`是Python默认的排序方法，在JDK1.7中也被引入。这两种方法不属于常用的基础算法。所以在这里也不展开讲。

## Swift基础排序算法

借这道题的机会我们来写一遍基础算法

### 冒泡排序

```swift
func bubbleSort(array: [Int]) -> [Int] {
    var result = array
    var temp: Int
    for i in 0..<result.count - 1 {
        for j in i+1..<result.count {
            if result[i] > result[j] {
                temp = result[j]
                result[j] = result[i]
                result[i] = temp
            }
        }
    }
    return result
}
```

修改原数组版：

```swift
func bubbleSort(array: inout [Int]) {
    var temp: Int
    for i in 0..<array.count - 1 {
        for j in i+1..<array.count {
            if array[i] > array[j] {
                temp = array[j]
                array[j] = array[i]
                array[i] = temp
            }
        }
    }
}
```

### 快速排序

按照C语言的逻辑我们先来写个草稿：

```swift
func quickSort(array: [Int]) -> [Int] {
    var sorted: [Int] = array
    guard sorted.count > 1 else {
        return sorted
    }
    let temp: Int = sorted[0]
    var i:Int = 0
    var j:Int = sorted.count-1
    while i != j {
        while sorted[j] > temp && i != j {
            j -= 1
        }
        if i != j {
            sorted[i] = sorted[j]
            i += 1
        }
        while sorted[i] < temp && i != j {
            i += 1
        }
        if i != j {
            sorted[j] = sorted[i]
            j -= 1
        }
    }
    sorted[i] = temp
    let left = quickSort(array: Array(sorted[..<i]))
    let right = quickSort(array: Array(sorted[i+1..<sorted.count]))
    let middle:[Int] = [sorted[i]]
    return left + middle + right
}
```

需要注意的是，Swift中的`inout`使用的`&`符号，很容易让有C或C++使用背景的人有一种传递引用的印象。但事实并非如此。`inout`做的事情是通过值传递，然后再复制回来，并不是传递引用。测试了一下快排在500个数据的情况下，inout复制整个数组的方案，比上面的方案慢一倍左右。

如果要使用指针，可以尝试[`Unsafe Swift - 手动内存管理`](https://developer.apple.com/documentation/swift/swift_standard_library/manual_memory_management)

### 选择排序

```swift
func selectionSort(array: inout [Int]) {
    var minIndex: Int
    for i in 0..<array.count {
        minIndex = i
        for selector in i..<array.count {
            if array[selector] < array[minIndex] {
                minIndex = selector
            }
        }
        (array[minIndex], array[i]) = (array[i], array[minIndex])
    }
}
```

### 插入排序

```swift
func insertionSort(array: inout [Int]) {
    var index: Int
    for i in 0..<array.count {
        index = i - 1
        while index >= 0 && array[index] > array[index + 1] {
            (array[index], array[index + 1]) = (array[index + 1], array[index])
            index -= 1
        }
    }
}
```

插入排序的时间复杂度虽然很高，但排列比较整齐的数列的时候效率很高。有两种优化排序：希尔和二分。

### 希尔排序

```swift
func shellSort(array: inout [Int]) {
    var gap: Int = array.count / 2
    while gap != 0 {
        for i in gap..<array.count {//思考为什么不是 in 0..<gap
            for index in stride(from: i - gap, through: i % gap, by: -gap) {
                if(array[index] > array[index + gap]) {
                    (array[index + gap], array[index]) = (array[index], array[index + gap])
                }
            }
        }
        gap /= 2
    }
}
```

### 堆排序

```swift
func heapSort(array: inout [Int]) {
    for j in (0..<array.count).reversed() {
        var i = j
        while(i > 0) {
            if i == array.count - 1 {
                if i % 2 == 1 {
                    if array[i] > array[(i - 1)/2] {//处理单独子叶
                        (array[i], array[(i - 1)/2]) = (array[(i - 1)/2], array[i])
                        i -= 1
                        continue
                    }
                }
            }
            if array[i] >= array[i - 1] {//>=:稳定性
                if array[i] > array[(i - 1)/2] {
                    (array[i], array[(i - 1)/2]) = (array[(i - 1)/2], array[i])
                }
            } else {
                if array[i - 1] > array[(i - 1)/2] {
                    (array[i - 1], array[(i - 1)/2]) = (array[(i - 1)/2], array[i - 1])
                }
            }
            i -= 2
        }
        (array[0], array[j]) = (array[j], array[0])
    }
}
```

### 归并排序

```swift
func mergeSort(array: [Int]) -> [Int] {
    guard array.count > 1 else { return array }
    let middle = array.count / 2
    let left = mergeSort(array: Array(array[0..<middle]))
    let right = mergeSort(array: Array(array[middle..<array.count]))
    //merge left & right
    var merge: [Int] = []
    var leftIndex = 0
    var rightIndex = 0
    while leftIndex < left.count || rightIndex < right.count {
        while leftIndex != left.count && rightIndex != right.count {
            if left[leftIndex] <= right[rightIndex] {
                merge.append(left[leftIndex])
                leftIndex += 1
            } else {
                merge.append(right[rightIndex])
                rightIndex += 1
            }
        }
        if leftIndex == left.count {
            merge.append(right[rightIndex])
            rightIndex += 1
        } else {
            merge.append(left[leftIndex])
            leftIndex += 1
        }
    }
    return merge
}
```

### 基数排序

```swift
func radixSort(array: inout [Int]) {
    var bucket:[[Int]] = [[]]
    for _ in 0...9 {
        let row: [Int] = []
        bucket.append(row)
    }
    var temp: Int! = array.max()
    var digits = 0
    while temp != 0 {
        temp /= 10
        digits += 1
    }
    for digit in 0..<digits {
        var temp: Int
        temp = NSDecimalNumber(decimal: pow(10, digit)).intValue
        for number in array {
            bucket[number/temp%10].append(number)
        }
        array.removeAll()
        for i in 0...9 {
            array += bucket[i]
            bucket[i].removeAll()
        }
    }
}
```

## 时间复杂度

### 排序算法时间复杂度

![排序算法时间复杂度比较](https://raw.githubusercontent.com/SunshineBrother/LeetCodeStudy/master/sort.png)

### 常用算法时间复杂度

| 算法             | 时间复杂度   |
| ---------------- | ------------ |
| 二分查找         | O(log n)     |
| 二叉树遍历       | O(n)         |
| 排序二维矩阵查找 | O(n)         |
| 归并排序         | O(n * log n) |

