# LeetCode@Swift - Vol.12 剪枝

剪枝的本质思想就是在递归/DFS的过程中，在进入分支之前加入判断，在遍历的过程中就先排除一些不可能的分支。

## 括号生成

[括号生成 - 力扣括号生成](https://leetcode-cn.com/problems/generate-parentheses/)

> 数字 n 代表生成括号的对数，请你设计一个函数，用于能够生成所有可能的并且 有效的 括号组合。

### 剪枝

```swift
class Solution {
    func generateParenthesis(_ n: Int) -> [String] {
        return gen("", 0, 0, 2 * n)
    }
    func gen(_ preStr: String, _ leftPars: Int,_ rightPars: Int, _ n: Int) -> [String] {
        guard n > 0 else { return [preStr] }
        var results: [String] = []
        if leftPars < (leftPars + rightPars + n) / 2 {
            results += gen(preStr + "(", leftPars + 1, rightPars, n - 1) // left
        }
        if leftPars > rightPars {
            results += gen(preStr + ")", leftPars, rightPars + 1, n - 1) // right
        }
        return results
    }
}
```

执行用时：24 ms 内存消耗：21.5 MB

初始版本如上。但原来的文章中我们测试过，用inout比用return的速度要快一些，我们来替换测试一下：

```swift
class Solution {
    func generateParenthesis(_ n: Int) -> [String] {
        var results: [String] = []
        gen("", 0, 0, 2 * n, &results)
        return results
    }
    func gen(_ preStr: String, _ left: Int,_ right: Int, _ n: Int, _ results: inout [String]) {
        guard n > 0 else { results.append(preStr);return }
        if left < (left + right + n) / 2 {
            gen(preStr + "(", left + 1, right, n - 1, &results) // left
        }
        if left > right {
            gen(preStr + ")", left, right + 1, n - 1, &results) // right
        }
    }
}
```

执行用时：16 ms 内存消耗：21.1 MB

还可以去掉参数`n`：

```swift
class Solution {
  func generateParenthesis(_ n: Int) -> [String] {
    var results: [String] = []
    gen("", n, n, &results)
    return results
  }
  func gen(_ preStr: String, _ left: Int,_ right: Int, _ results: inout [String]) {
    if right > 0 {
      if left > 0 {
        gen(preStr + "(", left - 1, right, &results) // left
      }
      if left < right {
        gen(preStr + ")", left, right - 1, &results) // right
      }
    } else {
      results.append(preStr)
    }
  }
}
```

执行用时：12 ms 内存消耗：20.9 MB

## N皇后

[N皇后 - 力扣](https://leetcode-cn.com/problems/n-queens/)

> n 皇后问题研究的是如何将 n 个皇后放置在 n×n 的棋盘上，并且使皇后彼此之间不能相互攻击。
> 
> 给定一个整数 n，返回所有不同的 n 皇后问题的解决方案。
> 
> 每一种解法包含一个明确的 n 皇后问题的棋子放置方案，该方案中 'Q' 和 '.' 分别代表了皇后和空位。

### 剪枝

```swift
class Solution {
  var results: [[String]] = []
  func solveNQueens(_ n: Int) -> [[String]] {
    var board: [[Int]] = Array(repeating: Array(repeating: 0, count: n), count: n)
    recursive(board, n)
    return results
  }
  func recursive(_ board: [[Int]], _ row: Int) {
    let n = board.count
    var flag = false
    for (index, cell) in board[n - row].enumerated() {
      var board = board
      if cell == 0 {
        flag = true
        board[n - row][index] = 1
        for r in (n - row + 1)..<n {
          board[r][index] -= 1
          if index - (r - (n - row)) >= 0 {
            board[r][index - (r - (n - row))] -= 1
          }
          if index + (r - (n - row)) < n {
            board[r][index + (r - (n - row))] -= 1
          }
        }
        guard flag == true else { return }
        if row == 1 {
          var result: [String] = []
          for boardRow in board {
            for (index, cell) in boardRow.enumerated() {
              if cell == 1 {
                result.append(
                  String(repeating: ".", count: index) + "Q" + String(repeating: ".", count: n - index - 1)
                )
                break
              }
            }
          }
          results.append(result)
          return
        }
        recursive(board, row - 1)
      }
    }
  }
}
```

执行用时：88 ms 内存消耗：21.3 MB

因为使用`enumerated()`都是对于`[Int]`来使用的，所以去掉之后性能会再高一点：

```swift
class Solution {
  var results: [[String]] = []
  func solveNQueens(_ n: Int) -> [[String]] {
    var board: [[Int]] = Array(repeating: Array(repeating: 0, count: n), count: n)
    recursive(board, n)
    return results
  }
  func recursive(_ board: [[Int]], _ row: Int) {
    let n = board.count
    var flag = false
    for index in 0..<n {
      var board = board
      if board[n - row][index] == 0 {
        flag = true
        board[n - row][index] = 1
        for r in (n - row + 1)..<n {
          board[r][index] = -1
          if index - (r - (n - row)) >= 0 {
            board[r][index - (r - (n - row))] = -1
          }
          if index + (r - (n - row)) < n {
            board[r][index + (r - (n - row))] = -1
          }
        }
        guard flag == true else { return }
        if row == 1 {
          var result: [String] = []
          for boardRow in board {
            for index in 0..<n {
              if boardRow[index] == 1 {
                result.append(
                  String(repeating: ".", count: index) + "Q" + String(repeating: ".", count: n - index - 1)
                )
                break
              }
            }
          }
          results.append(result)
          return
        }
        recursive(board, row - 1)
      }
    }
  }
}
```

执行用时：32 ms 内存消耗：21.3 MB

## 有效的数独

[有效的数独 - 力扣](https://leetcode-cn.com/problems/valid-sudoku/)

> 判断一个 9x9 的数独是否有效。只需要根据以下规则，验证已经填入的数字是否有效即可。
> 
> 数字 1-9 在每一行只能出现一次。
> 
> 数字 1-9 在每一列只能出现一次。
> 
> 数字 1-9 在每一个以粗实线分隔的 3x3 宫内只能出现一次。

这道题是和剪枝没多大关系，主要是引出下面一道题

### 三次循环

```swift
class Solution {
  func isValidSudoku(_ board: [[Character]]) -> Bool {
    //每行检测
    for row in board {
      var list: [Character] = []
      for char in row {
        guard char != "." else { continue }
        guard !list.contains(char) else { return false }
        list.append(char)
      }
    }
    //每列检测
    for col in 0..<9 {
      var list: [Character] = []
      for row in 0..<9 {
        let char = board[row][col]
        guard char != "." else { continue }
        guard !list.contains(char) else { return false }
        list.append(char)
      }
    }
    //九宫格检测
    for horizontal in 0..<3 {
      for vertical in 0..<3 {
        var list: [Character] = []
        for row in (horizontal * 3)..<((horizontal + 1) * 3) {
          for col in (vertical * 3)..<((vertical + 1) * 3) {
            let char = board[row][col]
            guard char != "." else { continue }
            guard !list.contains(char) else { return false }
            list.append(char)
          }
        }
      }
    }
    return true
  }
}
```

执行用时：196 ms 内存消耗：20.6 MB

三次循环可以合并为一次循环，相应的，内存用量会增加一些：

### 一次循环

```swift
class Solution {
  func isValidSudoku(_ board: [[Character]]) -> Bool {
    var rows: [Set<Character>] = Array(repeating: [], count: 9)
    var cols: [Set<Character>] = Array(repeating: [], count: 9)
    var sqrs: [Set<Character>] = Array(repeating: [], count: 9)
    //一遍循环，每个格子同时放到三个数组记录中
    for row in 0..<9 {
      for col in 0..<9 {
        let char = board[row][col]
        guard char != "." else { continue }
        guard !rows[row].contains(char) else { return false }
        guard !cols[col].contains(char) else { return false }
        guard !sqrs[row / 3 + col / 3 * 3].contains(char) else { return false }
        rows[row].insert(char)
        cols[col].insert(char)
        sqrs[row / 3 + col / 3 * 3].insert(char)
      }
    }
    return true
  }
}
```

执行用时：176 ms 内存消耗：21.2 MB

## 解数独

[解数独 - 力扣](https://leetcode-cn.com/problems/sudoku-solver/)

> 编写一个程序，通过已填充的空格来解决数独问题。
> 
> 一个数独的解法需遵循如下规则：
> 
> 数字 1-9 在每一行只能出现一次。
> 
> 数字 1-9 在每一列只能出现一次。
> 
> 数字 1-9 在每一个以粗实线分隔的 3x3 宫内只能出现一次。
> 
> 空白格用 '.' 表示

### 递归剪枝

```swift
class Solution {
  func solveSudoku(_ board: inout [[Character]]) {
    let container: [Set<Character>] = Array(repeating: [], count: 9)
    //先将题目限制存进containers
    var rows = container, cols = container, sqrs = container
    for x in 0..<9 {
      for y in 0..<9 {
        if board[x][y] != "." {
          let num = board[x][y]
          rows[x].insert(Character(String(num)))
          cols[y].insert(Character(String(num)))
          sqrs[x / 3 + y / 3 * 3].insert(Character(String(num)))
        }
      }
    }
    DFS(rows, cols, sqrs, 0, 0, &board)
  }
  func DFS(_ rows: [Set<Character>], _ cols: [Set<Character>], _ sqrs: [Set<Character>],
            _ x: Int, _ y: Int, _ board: inout [[Character]]) -> Bool {
    guard x < 9 else { return true } //结束
    guard board[x][y] == "." else {
      return DFS(rows, cols, sqrs, y == 8 ? x + 1 : x, y == 8 ? 0 : y + 1, &board)
    }
    for num in 1...9 {
      //剪枝
      guard !rows[x].contains(Character(String(num))) && !cols[y].contains(Character(String(num))) &&
        !sqrs[x / 3 + y / 3 * 3].contains(Character(String(num))) else { continue }
      var rows = rows; rows[x].insert(Character(String(num)))
      var cols = cols; cols[y].insert(Character(String(num)))
      var sqrs = sqrs; sqrs[x / 3 + y / 3 * 3].insert(Character(String(num)))
      var tempBoard = board
      tempBoard[x][y] = Character(String(num))
      if DFS(rows, cols, sqrs, y == 8 ? x + 1 : x, y == 8 ? 0 : y + 1, &tempBoard) == true {
        board = tempBoard
        return true
      }
    }
    return false
  }
}
```

执行用时：308 ms 内存消耗：21.4 MB

### 非递归剪枝

```swift
class Solution {
  func solveSudoku(_ board: inout [[Character]]) {
    let container: [Set<Character>] = Array(repeating: [], count: 9)
    // 先将题目限制存进containers
    var rows = container, cols = container, sqrs = container
    var fixs: [Set<Int>] = Array(repeating: [], count: 9) // 题目的点集
    for x in 0..<9 {
      for y in 0..<9 {
        if board[x][y] != "." {
          let num = board[x][y]
          rows[x].insert(Character(String(num)))
          cols[y].insert(Character(String(num)))
          sqrs[x / 3 + y / 3 * 3].insert(Character(String(num)))
          fixs[x].insert(y)
        }
      }
    }
    var x = 0, y = 0
    var reversing = false
    while x < 9 { // 手动循环，不用for-in因为可能有回溯
      if reversing == true { // dealing with reverse
        if !fixs[x].contains(y) && board[x][y] != "9" {
          for num in (Int(String(board[x][y]))! + 1)...9 {
            guard !rows[x].contains(Character(String(num))) && !cols[y].contains(Character(String(num))) &&
              !sqrs[x / 3 + y / 3 * 3].contains(Character(String(num))) else { continue }
            rows[x].remove(board[x][y])
            cols[y].remove(board[x][y])
            sqrs[x / 3 + y / 3 * 3].remove(board[x][y])
            rows[x].insert(Character(String(num)))
            cols[y].insert(Character(String(num)))
            sqrs[x / 3 + y / 3 * 3].insert(Character(String(num)))
            board[x][y] = Character(String(num))
            reversing = false
            break
          }
        }
      }
      if reversing == false && board[x][y] == "." {
        reversing = true // flag
        for num in 1...9 { // 剪枝
          guard !rows[x].contains(Character(String(num))) && !cols[y].contains(Character(String(num))) &&
            !sqrs[x / 3 + y / 3 * 3].contains(Character(String(num))) else { continue }
          rows[x].insert(Character(String(num)))
          cols[y].insert(Character(String(num)))
          sqrs[x / 3 + y / 3 * 3].insert(Character(String(num)))
          board[x][y] = Character(String(num))
          reversing = false // flag = true
          break
        }
      }
      if reversing == false {
        x = y == 8 ? x + 1 : x
        y = y == 8 ? 0 : y + 1
      } else {
        if !fixs[x].contains(y) {
          rows[x].remove(board[x][y])
          cols[y].remove(board[x][y])
          sqrs[x / 3 + y / 3 * 3].remove(board[x][y])
          board[x][y] = "."
        }
        x = y == 0 ? x - 1 : x
        y = y == 0 ? 8 : y - 1 // reverse
      }
    }
  }
}
```

执行用时：176 ms 内存消耗：21.4 MB
