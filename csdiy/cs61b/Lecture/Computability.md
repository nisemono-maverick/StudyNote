# Lecture 39: Complexity and P = NP

## 1. Problem Reductions: The Knapsack Problem

### Three Versions of Knapsack
Given items with weights and values, and a weight limit:

1. **Optimization (List)**: Return the list of items to steal for max value
2. **Optimization (Value)**: Return the maximum value achievable
3. **Decision**: Return True/False if you can steal at least target value

### Reductions Between Versions
All three are **equivalent under Turing Reduction** (solve one → solve all):

| From | To | Method |
|------|-----|--------|
| Decision | Value | Binary search on target value (Θ(log V)) |
| Value | List | Test each item: remove it, check if max value drops |
| List | Value | Sum the values of returned items |

**Key Insight**: Reductions show relative difficulty. If A reduces to B, B is "at least as hard" as A.

---

## 2. Turing Machines

### What is a Turing Machine?
A theoretical model of computation:
- Infinite memory (unlike real computers)
- Can simulate any computer program
- Forms the basis of complexity analysis

**Turing-Complete**: A language that can simulate any Turing Machine.
- Examples: Python, Java, C++, JavaScript
- Surprising example: Minecraft Redstone

### Deterministic Turing Machine (DTM)
- No randomness/guessing allowed
- **Class P**: Decision problems solvable by DTM in polynomial time

**Examples in P**:
- Is array sorted? O(N)
- Minimum spanning tree < X weight? O(E log V)
- Is N-bit number prime? O(N^12) — proven in 2002!

### Nondeterministic Turing Machine (NTM)
- Has a magic `guess()` operation
- Returns True if **ANY** guess pattern leads to True
- Returns False only if **ALL** guess patterns return False

**Class NP**: Decision problems solvable by NTM in polynomial time

---

## 3. NP Problems

### Equivalent Definition of NP
NP = problems whose solution can be **verified** in polynomial time by a DTM.

**Process**:
1. Nondeterministically guess a solution
2. Deterministically verify the solution

If verification is poly-time → problem is in NP.

### Example: Sudoku (n² × n²)
**NTM Solution**:
1. Guess values for all n⁴ empty cells (creates exponentially many "universes")
2. Check if rows, columns, and boxes contain 1-n²

**Runtime**: Θ(n⁴) — poly-time → Sudoku ∈ NP

### Example: Knapsack Decision Problem
**NTM Solution**:
1. Guess a subset of items (2^N universes)
2. Verify: total weight ≤ limit AND total value ≥ target

**Runtime**: Θ(N) → Knapsack ∈ NP

### More NP Problems
- Logic puzzles: Minesweeper, Tetris, Rubik's Cube
- Graph: Longest Path, Independent Set
- Math: Prime Factorization
- Crypto: Decryption

### NOT in NP (currently)
- Chess/Go (perfect play)
- Halting Problem (undecidable)

---

## 4. NP-Hard and NP-Complete

### NP-Hard
A problem is **NP-Hard** if **every problem in NP** reduces to it.
- "At least as hard as everything in NP"
- May or may not be in NP itself

### NP-Complete
A problem is **NP-Complete** if:
1. It is in NP
2. It is NP-Hard

**Cook-Levin Theorem (1971-73)**: **SAT is NP-Complete**

**SAT Problem**: Given a boolean formula (e.g., "x && (y || !z)"), is there an assignment making it True?

### The Web of Reductions
SAT reduces to 3-SAT reduces to Graph Coloring reduces to Exact Cover reduces to Knapsack...

**Result**: All NP-Complete problems are **equivalent**!
- Solving Knapsack = Solving Sudoku = Solving SAT
- Thousands of problems across different fields are actually the same problem

### Reductions Graph
```
    Longest Path    Independent Set    Sudoku    Knapsack
          \              |              /          /
           \             |             /          /
            \            |            /          /
             ========== SAT =========           /
                       /                       /
            Prime Factorization (not known to be NP-complete)
            
    [Green]: In P        [Pink]: NP-Complete
```

---

## 5. The P = NP Question

### The Million Dollar Question
Is there a polynomial-time algorithm for any NP-Complete problem?
- **If YES** → P = NP (all NP problems collapse to P)
- **If NO** → P ≠ NP

### Current Consensus (2019 Poll)
- **89%** believe P ≠ NP
- **11%** believe P = NP
- **3%** believe it's impossible to prove either way

### Why P ≠ NP?
- "Someone would have found a polynomial algorithm by now"
- Creating solutions seems harder than verifying them (philosophically)

### Why P = NP might still be possible?
- NP is surprisingly close to P:
  - Knapsack: poly-time if N = total weight (pseudo-polynomial)
  - Approximation algorithms exist
  - SAT solvers work fast in practice

### Consequences if P = NP
Even with Θ(n^1,000,000) algorithm:
- All modern cryptography breaks (RSA, AES, etc.)
- Optimization becomes trivial
- Mathematics becomes "mechanical" (proofs easy to find)

### Consequences if P ≠ NP
- New branch of complexity theory
- Cryptography remains secure
- Still many unsolved problems in the complexity hierarchy

### Millennium Prize Problem
P = NP is one of the 7 **Clay Mathematics Institute** $1,000,000 prize problems.

---

## Summary

| Concept | Definition |
|---------|------------|
| **P** | Decision problems solvable in poly-time by DTM |
| **NP** | Decision problems solvable in poly-time by NTM (or verifiable in poly-time) |
| **NP-Hard** | At least as hard as every problem in NP |
| **NP-Complete** | Both in NP and NP-Hard |
| **Reduction** | Transform problem A into problem B (A ≤ B means B is harder) |
| **P = NP?** | Unsolved. $1M prize. Most believe P ≠ NP. |

**Key Theorem**: SAT is NP-Complete (Cook-Levin).

**Implication**: All NP-Complete problems are equivalent. Solve one in poly-time → solve them all.
