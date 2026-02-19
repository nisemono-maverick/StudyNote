## 1. Introduction to Tries

A **Trie** (pronounced "try") is a tree-like data structure designed for efficient retrieval of string keys. Unlike binary search trees, each node in a trie stores characters of keys along paths from the root, making them ideal for string operations.

## 2. Special Case: Character-Keyed Map

For keys limited to ASCII characters, a simple array-based approach works:

```java
public class DataIndexedCharMap<V> {
    private V[] items;
    
    public DataIndexedCharMap(int R) {
        items = (V[]) new Object[R];
    }
    
    public void put(char c, V val) {
        items[c] = val;
    }
    
    public V get(char c) {
        return items[c];
    }
}
```

## 3. Trie Fundamentals

### 3.1 Basic Structure
- Each node represents a single character
- Nodes can be shared by multiple keys
- Path from root to a node spells out a key or prefix

### 3.2 Node Design
```java
private static class Node {
    private char ch;           // Optional - can be inferred from position
    private boolean isKey;     // Marks end of complete key
    private DataIndexedCharMap<Node> next;
}
```

### 3.3 Time Complexity
- **Insert**: Θ(L) where L = key length
- **Search**: O (L)
- For fixed alphabets (like ASCII): O (1) per operation

## 4. Trie Implementations

### 4.1 Array-Based Trie (Fixed Alphabet)
```java
public class ArrayTrie {
    private static final int R = 128; // ASCII
    private Node root;
    
    private static class Node {
        private boolean isKey;
        private Node[] next = new Node[R];
    }
}
```

### 4.2 BST-Based Trie (Space Efficient)
```java
public class BSTTrie {
    private Node root;
    
    private static class Node {
        private boolean isKey;
        private TreeMap<Character, Node> next = new TreeMap<>();
    }
}
```

### 4.3 HashTable-Based Trie
```java
public class HashTrie {
    private Node root;
    
    private static class Node {
        private boolean isKey;
        private HashMap<Character, Node> next = new HashMap<>();
    }
}
```

## 5. Complete Trie Implementation (BST-Based)

```java
import java.util.*;

public class TrieSet {
    private static class Node {
        private boolean isKey;
        private Map<Character, Node> next;
        
        private Node(boolean b) {
            isKey = b;
            next = new TreeMap<>();
        }
    }
    
    private Node root;
    
    public TrieSet() {
        root = new Node(false);
    }
    
    // Insert a word into the trie
    public void insert(String word) {
        Node curr = root;
        for (char c : word.toCharArray()) {
            if (!curr.next.containsKey(c)) {
                curr.next.put(c, new Node(false));
            }
            curr = curr.next.get(c);
        }
        curr.isKey = true;
    }
    
    // Check if word exists
    public boolean contains(String word) {
        Node curr = root;
        for (char c : word.toCharArray()) {
            if (!curr.next.containsKey(c)) return false;
            curr = curr.next.get(c);
        }
        return curr.isKey;
    }
    
    // Get all keys in the trie
    public List<String> collect() {
        List<String> result = new ArrayList<>();
        for (Character c : root.next.keySet()) {
            colHelp(String.valueOf(c), result, root.next.get(c));
        }
        return result;
    }
    
    private void colHelp(String s, List<String> x, Node n) {
        if (n.isKey) x.add(s);
        for (Character c : n.next.keySet()) {
            colHelp(s + c, x, n.next.get(c));
        }
    }
    
    // Get all keys with given prefix
    public List<String> keysWithPrefix(String prefix) {
        List<String> result = new ArrayList<>();
        Node curr = root;
        
        // Traverse to the node representing the prefix
        for (char c : prefix.toCharArray()) {
            if (!curr.next.containsKey(c)) return result;
            curr = curr.next.get(c);
        }
        
        // Collect all keys from this node
        colHelp(prefix, result, curr);
        return result;
    }
    
    // Check if any key starts with prefix
    public boolean startsWith(String prefix) {
        Node curr = root;
        for (char c : prefix.toCharArray()) {
            if (!curr.next.containsKey(c)) return false;
            curr = curr.next.get(c);
        }
        return true;
    }
    
    // Find longest key that is a prefix of given word
    public String longestPrefixOf(String word) {
        StringBuilder sb = new StringBuilder();
        Node curr = root;
        
        for (char c : word.toCharArray()) {
            if (!curr.next.containsKey(c)) break;
            sb.append(c);
            curr = curr.next.get(c);
        }
        return sb.toString();
    }
}
```

## 6. Key Operations Explained

### 6.1 `collect()`
Retrieves all keys in the trie:
1. Start with empty result list
2. For each child of root, recursively traverse and collect keys
3. Time complexity: O (N) where N = total nodes visited

### 6.2 `keysWithPrefix(String prefix)`
1. Find node corresponding to the prefix
2. Collect all keys from that node
3. Efficient for autocomplete applications

### 6.3 `longestPrefixOf(String word)`
Finds the longest key that is a prefix of the input word.
Useful for routing applications and text processing.

## 7. Applications

### 7.1 Autocomplete
- Efficient prefix matching
- Fast retrieval of suggestions

### 7.2 Spell Checking
- Quick dictionary lookups
- Prefix-based suggestions

### 7.3 IP Routing
- Longest prefix matching for routing tables

### 7.4 Text Processing
- Word games (Boggle, Scrabble)
- Pattern matching

## 8. Trade-offs

### Advantages:
- **Fast prefix searches**: O (L) for operations
- **Space efficiency**: Shared prefixes reduce storage
- **Ordered iteration**: Natural alphabetical ordering
- **No hash collisions**: Deterministic performance

### Disadvantages:
- **Memory overhead**: Each node stores multiple pointers
- **Cache inefficiency**: Non-contiguous memory access
- **Complex implementation**: More complex than hash tables

## 9. Performance Comparison

| Operation | Trie (BST-based) | Hash Table | Notes |
|-----------|-----------------|------------|-------|
| Insert    | O (L log R)      | O (L)       | R = alphabet size |
| Search    | O (L log R)      | O (L)       |       |
| Prefix Search | O (L log R)  | O (N)       | Trie excels here |
| Memory    | Moderate        | High       | Trie shares prefixes |

## 10. Optimizations（un-implement）

### 10.1 Compressed Tries
- Merge nodes with single children
- Store strings instead of single characters

### 10.2 Ternary Search Tries
- Each node has three children: left, middle, right
- More memory efficient than standard tries

### 10.3 Double-Array Tries
- Use two arrays for base and check
- Memory efficient but complex

