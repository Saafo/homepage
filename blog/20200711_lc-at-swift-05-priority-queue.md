# LeetCode@Swift - Vol.5 优先队列

优先队列也不用太去关注底层实现，一般的语言都已经有了成熟的实现。对于优先队列来说，一般其实现机制有：堆（二叉堆、二项式堆、斐波那契堆）、二叉搜索树。

关于堆的各种具体实现的时间复杂度，可以参考[维基百科](https://en.wikipedia.org/wiki/Heap_(data_structure)#Comparison_of_theoretic_bounds_for_variants),需要熟记。

## 数据流中的第K大元素

[数据流中的第K大元素 - 力扣](https://leetcode-cn.com/problems/kth-largest-element-in-a-stream/)

> 设计一个找到数据流中第K大元素的类（class）。注意是排序后的第K大元素，不是第K个不同的元素。
> 
> 你的`KthLargest`类需要一个同时接收整数`k`和整数数组`nums`的构造器，它包含数据流中的初始元素。每次调用`KthLargest.add`，返回当前数据流中第K大的元素。
> 
> 示例:
> 
> int k = 3;
> 
> int[] arr = [4,5,8,2];
> 
> KthLargest kthLargest = new KthLargest(3, arr);
> 
> kthLargest.add(3);   // returns 4
> 
> kthLargest.add(5);   // returns 5
> 
> kthLargest.add(10);  // returns 5
> 
> kthLargest.add(9);   // returns 8
> 
> kthLargest.add(4);   // returns 8
> 
> 说明:
> 
> 你可以假设 nums 的长度≥ k-1 且k ≥ 1。

```swift
class KthLargest {
    var heap: [Int]
    let k: Int
    init(_ k: Int, _ nums: [Int]) {
        if k <= nums.count {
            self.heap = Array(nums.sorted(by: <)[Int(nums.count - k)...])
        } else {
            self.heap = nums
        }
        self.k = k
    }
    
    func add(_ val: Int) -> Int {
        return heap.kAdd(val, k)
    }
}
extension Array where Element == Int {
    mutating func kAdd(_ add: Int, _ k: Int) -> Int {
        if self.count < k {
            self.insert(add, at: self.startIndex)
        }
        guard add >= self[0] else { return self[0] }
        self[0] = add
        var i = 0
        while i * 2 + 1 < self.count {
            if i * 2 + 2 < self.count {
                if self[i * 2 + 1] > self[i * 2 + 2] {
                    if self[i] > self[i * 2 + 2] {
                        (self[i], self[i * 2 + 2]) = (self[i * 2 + 2], self[i])
                        i = i * 2 + 2
                        continue
                    } else {
                        break
                    }
                }
            }
            if self[i] > self[i * 2 + 1] {
                (self[i], self[i * 2 + 1]) = (self[i * 2 + 1], self[i])
                i = i * 2 + 1
            } else {
                break
            }
        }
        return self[0]
    }
}
```

执行用时：220 ms 内存消耗：22.3 MB

这个解法是利用`extension`来实现的插入功能。就是逻辑上需要注意比如初始输入`k=2, nums=[1]`这种尚未填充完整的情况，题目说明的是初始数组长度大于k - 1，尤其需要注意这一点。

【更多题目待更新】