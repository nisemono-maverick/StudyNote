## 1. What is Compression?

Compression reduces file size while preserving information.

**Lossless Compression**: No information is lost (C must be injective: if A ≠ B, then C(A) ≠ C(B)).

**Example**: `mobydick.txt` (643KB) → `mobydick.zip` (261KB), deflated 59%.

---

## 2. Information Theory (Shannon Entropy)

### Key Insight
The more predictable data is, the less information it contains → the better we can compress it.

**Example**: 
- 10 random characters: hard to memorize (high entropy)
- 10000 'A's: easy to memorize (low entropy)

### Shannon Entropy Definition
Measures how predictable a dataset is:
- Formula: `E(-log₂(p(X)))`
- English text: ~1 bit of entropy per character
- Random English letters: ~4.7 bits per character

**Implication**: A 47-char English string (~47 bits entropy) can theoretically be compressed to 47 bits (87% reduction from 376 bits).

---

## 3. Prefix-Free Codes

### The Problem with Morse Code
Morse code is ambiguous without pauses:
- `--•--•` could be MEME, GG, MATE, or MAN

### Prefix-Free Solution
No codeword is a prefix of another.

**Example**:
```
Tree representation:
      start
     0/   \1
     E     space(111)
    0/\1
   I   A(1011)
  ...
```

Encoding "I ATE": `1000` + `111` + `1101` + `1011` = `10001111101101011` (unambiguous!)

---

## 4. Shannon-Fano Coding

**Approach**: Split symbols into halves of roughly equal frequency, recursively.

| Symbol | Frequency | Code |
|--------|-----------|------|
| 三 | 0.35 | 00 |
| 点 | 0.17 | 01 |
| 一 | 0.17 | 10 |
| 四 | 0.16 | 110 |
| 円 | 0.15 | 111 |

Average: **2.31 bits/symbol**

**Problem**: Not optimal. There's always a better code.

---

## 5. Huffman Coding (Optimal)

### Core Algorithm
1. Count frequency of each symbol
2. Create a node for each symbol with its frequency
3. Repeatedly merge the two smallest nodes into a parent node
4. Result: Binary tree where path = codeword

**Example** (same symbols):
```
      (1.0)
     0/   \1
   三(0.35) (0.65)
           0/   \1
        (0.34) (0.31)
        0/  \1  0/  \1
       点   一  四   円
```

| Symbol | Frequency | Huffman Code | Bits |
|--------|-----------|--------------|------|
| 三 | 0.35 | 0 | 1 |
| 点 | 0.17 | 100 | 3 |
| 一 | 0.17 | 101 | 3 |
| 四 | 0.16 | 110 | 3 |
| 円 | 0.15 | 111 | 3 |

Average: **2.3 bits/symbol** (better than Shannon-Fano!)

### Efficiency Calculation
```
(0.35 × 1) + (0.17 + 0.17 + 0.16 + 0.15) × 3 = 2.3 bits/symbol

vs. 32-bit Unicode: 14× improvement!
```

---

## 6. Data Structures for Huffman

### Encoding (symbol → codeword)
Use `Array<BitSequence>` or **` HashMap<Character, BitSequence>`**
- Array: Faster (O(1) direct access), more memory if alphabet is sparse
- HashMap: Less memory for sparse alphabets

### Decoding (codeword → symbol)
Use **Trie** (prefix tree)
- Walk down the tree using bits: 0 = left, 1 = right
- When reaching a leaf: output symbol, restart from root

---

## 7. Huffman in Practice

### Two Approaches

**Approach 1: Corpus-based**
- Build one Huffman tree per input type (English, Chinese, images...)
- **Pros**: No overhead for tree
- **Cons**: Suboptimal for specific files

**Approach 2: Per-file tree** ✅ (Used in practice)
- Create unique code for each file
- Store the tree at the beginning of compressed file
- **Pros**: Optimal compression
- **Cons**: Tree overhead (insignificant for large files)

### File Format
```
[X.huf]
| Decoding Trie | Codeword for symbol 1 | Codeword for symbol 2 | ... |
```

---

## 8. Compression Theory

### Universal Compression is Impossible

**Argument 1**: If any algorithm could compress by 50%, we could compress repeatedly down to 1 bit — impossible.

**Argument 2 (Pigeonhole Principle)**:
- 2^1000 possible 1000-bit sequences
- Only 2^501 - 1 sequences of length ≤ 500
- Can't fit 2^1000 things into 2^501 places!

### No Free Lunch Theorem
No compression algorithm can compress below the **Shannon Entropy** of a dataset.

- **Trade-off**: To make some strings shorter, others must get longer
- **Good news**: Real data (English, images) is low-entropy, so compressible
- **Bad news**: Random data will get slightly larger

---

## 9. LZW Compression (Extra)

**Key Idea**: Each codeword represents multiple symbols.

**Algorithm**:
1. Start with trivial table (ASCII symbol → codeword)
2. When codeword X is used, add new entry: X + next symbol
3. Output codewords instead of raw symbols

**Neat Property**: Decoder can reconstruct the table from compressed data alone (no need to send it).

**Usage**: `.gif`, `.zip` files (patent expired in 2003).

---

## Summary

| Concept | Key Point |
|---------|-----------|
| Compression | Reduce size while preserving info |
| Entropy | Predictability = compressibility |
| Prefix-Free | No codeword is prefix of another |
| Huffman | Optimal prefix-free coding |
| Data Structures | Array/HashMap for encode, Trie for decode |
| Theory | Can't beat entropy; universal compression impossible |
