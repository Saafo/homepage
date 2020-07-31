# LeetCode@Swift - Vol.10 贪心算法

适用于贪心算法的场景：

* 问题能够分解成子问题来解决
* 子问题的最优解能递推到全局问题的最优解（此时子问题的最优解为最优子结构）

贪心算法与动态规划的不同在于，它对每个子问题的解决方案都做出选择，不能回退。
动态规划则会保存以前的运算结构，并根据以前的结构对当前进行选择，有回退功能。

## 买卖股票的最佳时机 II

[买卖股票的最佳时机 II - 力扣](https://leetcode-cn.com/problems/best-time-to-buy-and-sell-stock-ii/)

> 给定一个数组，它的第 i 个元素是一支给定股票第 i 天的价格。
> 
> 设计一个算法来计算你所能获取的最大利润。你可以尽可能地完成更多的交易（多次买卖一支股票）。
> 
> 注意：你不能同时参与多笔交易（你必须在再次购买前出售掉之前的股票）。

### DFS

思路是每一天都分为两种情况，买进和卖出，DFS遍历这棵树，时间复杂度为O(2^n)。

### 贪心算法

思路为看当前天是否比前一天高，高就买入。时间复杂度为O(n)。

```swift
class Solution {
    func maxProfit(_ prices: [Int]) -> Int {
        var profit = 0
        for (index, price) in prices[1..<prices.count].enumerated() {
            if price > prices[index] {
                profit += price - prices[index]
            }
        }
        return profit
    }
}
```

执行用时：52 ms 内存消耗：21.2 MB

注意循环中index实际上是从1开始。

### 动态规划

//TODO