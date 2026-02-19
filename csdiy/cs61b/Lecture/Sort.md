A comprehensive guide to fundamental sorting algorithms, their implementations, and complexity analysis.

---

## Table of Contents

- [1. Selection Sort](#1-selection-sort)
- [2. Heapsort](#2-heapsort)
- [3. Mergesort](#3-mergesort)
- [4. Insertion Sort](#4-insertion-sort)
- [5. Quicksort](#5-quicksort)
- [6. Sorting Stability](#6-sorting-stability)
- [7. Radix Sort](#7-radix-sort)
- [8. Algorithm Comparison](#8-algorithm-comparison)
- [9. Java Implementation](#9-java-implementation)

---

## 1. Selection Sort

### Core Idea
Selection sort works by repeatedly finding the minimum element from the unsorted portion and putting it at the beginning.

### Algorithm
```
For each position i from 0 to N-1:
    Find the smallest item in the unsorted portion (i to N-1)
    Swap it with the item at position i
```

### Complexity Analysis
| Case    | Time Complexity | Space Complexity |
| ------- | --------------- | ---------------- |
| Best    | Θ(N²)           | Θ(1)             |
| Worst   | Θ(N²)           | Θ(1)             |
| Average | Θ(N²)           | Θ(1)             |

**Note:** Selection sort always performs ~N²/2 comparisons regardless of input order.

---

## 2. Heapsort

### 2.1 Naive Heapsort

**Approach:**
1. Insert all items into a max heap
2. Repeatedly delete the largest item and place it at the end of the output array

**Complexity:**
- Time: Θ(N log N)
- Space: Θ(N) - requires extra space for the heap

### 2.2 In-Place Heapsort

**Key Insight:** Treat the input array itself as a heap using **bottom-up heapification**.

**Algorithm:**
1. **Heapify Phase:** Convert array into a max heap
   - Sink nodes in reverse level order (from N/2 down to 0)
   - After sinking at position k, the tree rooted at k is a valid heap
   
2. **Sort Phase:** Repeatedly extract maximum
   - Swap root (max) with last item in heap
   - Heapify the reduced heap
   - Repeat until heap is empty

### Complexity Analysis
| Phase | Time Complexity |
|-------|----------------|
| Bottom-up Heapification | Θ(N) |
| N delete-max operations | Θ(N log N) |
| **Total** | **Θ(N log N)** |
| **Space** | **Θ(1)** |

**Note:** The worst-case time complexity of Heapsort is Θ(N log N), making it very predictable.

---

## 3. Mergesort

### Core Idea
Divide and conquer: Split the array into halves, recursively sort each half, then merge the sorted halves.

### Algorithm
```
Mergesort(arr, left, right):
    if left >= right: return
    mid = (left + right) / 2
    Mergesort(arr, left, mid)
    Mergesort(arr, mid+1, right)
    Merge(arr, left, mid, right)
```

### Merge Operation
The merge operation combines two sorted subarrays into one sorted array:
- Compare elements from both subarrays
- Copy the smaller element to the target array
- Continue until all elements are processed

**Merge Runtime:** Θ(N)

### Complexity Analysis
| Case | Time Complexity | Space Complexity |
|------|----------------|------------------|
| Best | Θ(N log N) | Θ(N) |
| Worst | Θ(N log N) | Θ(N) |
| Average | Θ(N log N) | Θ(N) |

**Characteristics:**
- Stable sort (preserves relative order of equal elements)
- Guaranteed O(N log N) performance
- Not in-place (requires O(N) auxiliary space)

---

## 4. Insertion Sort

### Core Idea
Build the final sorted array one item at a time by inserting each new element into its proper position among the previously sorted elements.

### In-Place Algorithm
```
For i from 0 to N-1:
    Designate item i as the "traveling item"
    While traveler < item to its left:
        Swap traveler leftward
```

### When Insertion Sort Excels

**Almost Sorted Arrays:**
- Define an "almost sorted" array as one with ≤ cN inversions
- Runtime: Θ(N + K), where K is the number of inversions
- When K = O(N), insertion sort runs in linear time

### Complexity Analysis
| Case | Time Complexity | Space Complexity |
|------|----------------|------------------|
| Best (already sorted) | Θ(N) | Θ(1) |
| Worst (reverse sorted) | Θ(N²) | Θ(1) |
| Average | Θ(N²) | Θ(1) |

**Characteristics:**
- Stable sort
- Excellent for small or nearly sorted arrays
- In-place (no extra memory needed)

---

## 5. Quicksort

### Core Idea
Partition the array around a pivot element such that:
- All elements left of pivot are ≤ pivot
- All elements right of pivot are ≥ pivot
- Recursively sort both partitions

### Algorithm
```
Quicksort(arr, left, right):
    if left >= right: return
    pivot_index = Partition(arr, left, right)
    Quicksort(arr, left, pivot_index - 1)
    Quicksort(arr, pivot_index + 1, right)
```

### Hoare Partitioning

**Two-Pointer Approach:**
- **L pointer:** Starts at left, moves right. Stops on elements ≥ pivot.
- **R pointer:** Starts at right, moves left. Stops on elements ≤ pivot.
- When both stop, swap elements and continue
- When pointers cross, partitioning is complete

### Quicksort LTHS (Leftmost + Tony Hoare + Shuffle)

The "fastest" version of Quicksort combines:
1. **Pivot Selection:** Leftmost element
2. **Partition Algorithm:** Tony Hoare's two-pointer method
3. **Worst-case Avoidance:** Shuffle the array before sorting

### Complexity Analysis
| Case | Time Complexity | Space Complexity |
|------|----------------|------------------|
| Best | Θ(N log N) | Θ(log N) |
| Worst (unbalanced partitions) | Θ(N²) | Θ(N) |
| Average | Θ(N log N) | Θ(log N) |

### QuickSelect

Use partitioning to find the k-th smallest element in expected linear time.

**Algorithm:**
1. Partition the array
2. If pivot position == k: return pivot
3. If pivot position > k: recurse on left partition
4. If pivot position < k: recurse on right partition

**Average Runtime:** Θ(N)

---

## 6. Sorting Stability

### Definition
A sorting algorithm is **stable** if it preserves the relative order of equal elements.

### Stability of Common Algorithms
| Algorithm | Stable? |
|-----------|---------|
| Selection Sort | No |
| Heapsort | No |
| Mergesort | Yes |
| Insertion Sort | Yes |
| Quicksort | No |
| Counting Sort | Yes |
| LSD Radix Sort | Yes |

**Why Stability Matters:**
- When sorting records by multiple keys (e.g., sort by name, then by age)
- In database operations and data processing pipelines

---

## 7. Radix Sort

### Two Key Ideas

#### 1. Digit-by-Digit Sorting
Sort integers by processing digits from least significant to most significant (LSD) or vice versa (MSD).

#### 2. Counting Sort (as subroutine)
Counting sort works when keys are integers in a small range [0, R-1]:
1. Count occurrences of each key
2. Compute prefix sums to determine positions
3. Place elements in output array (stable)

**Counting Sort Complexity:**
- Time: Θ(N + R)
- Space: Θ(N + R)

### LSD (Least Significant Digit) Radix Sort

**Algorithm:**
1. For each digit position from right to left:
   - Perform stable counting sort on that digit

**Runtime:** Θ(WN + WR)
- W = number of digits
- N = number of elements
- R = radix (base, typically 10)

### MSD (Most Significant Digit) Radix Sort

**Algorithm:**
1. Sort by most significant digit
2. Recursively sort each bucket separately

**Runtime:**
- Best case: Θ(N + R)
- Worst case: Θ(WN + WR)

**Advantage:** Can terminate early when buckets are small (switch to insertion sort).

---

## 8. Algorithm Comparison

| Algorithm | Best Case | Worst Case | Space | Stable? | Notes |
|-----------|-----------|------------|-------|---------|-------|
| **Selection Sort** | Θ(N²) | Θ(N²) | Θ(1) | No | Simple, always N² comparisons |
| **Heapsort** | Θ(N) | Θ(N log N) | Θ(1) | No | Guaranteed O(N log N) |
| **Mergesort** | Θ(N log N) | Θ(N log N) | Θ(N) | Yes | Stable, predictable |
| **Insertion Sort** | Θ(N) | Θ(N²) | Θ(1) | Yes | Fast for small/nearly sorted arrays |
| **Quicksort** | Θ(N log N) | Θ(N²) | Θ(log N) | No | Fastest in practice (with optimizations) |
| **Counting Sort** | Θ(N + R) | Θ(N + R) | Θ(N + R) | Yes | Integer keys only |
| **LSD Radix Sort** | Θ(WN) | Θ(WN + WR) | Θ(N + R) | Yes | Fixed-width keys |
| **MSD Radix Sort** | Θ(N + R) | Θ(WN + WR) | Θ(N + WR) | Yes | Variable-width keys |

### Summary of Core Ideas

| Algorithm | Core Idea |
|-----------|-----------|
| Selection Sort | Find the smallest item and put it at the front |
| Heapsort | Use max-heap to repeatedly find and remove max |
| Mergesort | Merge two sorted halves into one sorted whole |
| Insertion Sort | Insert current item into its proper position |
| Quicksort | Partition items around a pivot |
| Radix Sort | Sort digit by digit using stable subroutine |

---

## 9. Java Implementation

```java
import java.util.Random;

public class Sort {
    
    private static final Random rand = new Random();
    
    /* ==================== Selection Sort ==================== */
    
    /**
     * Selection Sort: Find the minimum element and place it at the beginning
     * Time: O(N²), Space: O(1)
     */
    public int[] selectionSort(int[] arr) {
        int[] sortArr = arr.clone();
        int n = sortArr.length;
        
        for (int i = 0; i < n; i++) {
            int minIdx = i;
            for (int j = i + 1; j < n; j++) {
                if (sortArr[j] < sortArr[minIdx]) {
                    minIdx = j;
                }
            }
            swap(sortArr, i, minIdx);
        }
        return sortArr;
    }
    
    /* ==================== Heapsort ==================== */
    
    /**
     * In-place Heapsort using bottom-up heapification
     * Time: O(N log N), Space: O(1)
     */
    public int[] heapSort(int[] arr) {
        int[] sortArr = arr.clone();
        int n = sortArr.length;
        
        // Bottom-up heapification
        for (int i = n / 2 - 1; i >= 0; i--) {
            sink(sortArr, n, i);
        }
        
        // Extract elements from heap
        for (int i = n - 1; i > 0; i--) {
            swap(sortArr, 0, i);      // Move max to end
            sink(sortArr, i, 0);       // Restore heap property
        }
        return sortArr;
    }
    
    private void sink(int[] arr, int size, int i) {
        while (2 * i + 1 < size) {
            int left = 2 * i + 1;
            int right = 2 * i + 2;
            int largest = i;
            
            if (left < size && arr[left] > arr[largest]) {
                largest = left;
            }
            if (right < size && arr[right] > arr[largest]) {
                largest = right;
            }
            
            if (largest == i) break;
            swap(arr, i, largest);
            i = largest;
        }
    }
    
    /* ==================== Mergesort ==================== */
    
    /**
     * Mergesort: Divide and conquer with merging
     * Time: O(N log N), Space: O(N)
     */
    public int[] mergeSort(int[] arr) {
        if (arr == null || arr.length <= 1) return arr.clone();
        
        int[] sortArr = arr.clone();
        int[] temp = new int[sortArr.length];
        mergeSortHelper(sortArr, 0, sortArr.length - 1, temp);
        return sortArr;
    }
    
    private void mergeSortHelper(int[] arr, int left, int right, int[] temp) {
        if (left >= right) return;
        
        int mid = left + (right - left) / 2;
        mergeSortHelper(arr, left, mid, temp);
        mergeSortHelper(arr, mid + 1, right, temp);
        merge(arr, left, mid, right, temp);
    }
    
    private void merge(int[] arr, int left, int mid, int right, int[] temp) {
        // Copy to temp array
        System.arraycopy(arr, left, temp, left, right - left + 1);
        
        int i = left, j = mid + 1, k = left;
        
        while (i <= mid && j <= right) {
            if (temp[i] <= temp[j]) {
                arr[k++] = temp[i++];
            } else {
                arr[k++] = temp[j++];
            }
        }
        
        while (i <= mid) arr[k++] = temp[i++];
        while (j <= right) arr[k++] = temp[j++];
    }
    
    /* ==================== Insertion Sort ==================== */
    
    /**
     * Insertion Sort: Build sorted array one element at a time
     * Time: O(N²) worst, O(N) best, Space: O(1)
     */
    public int[] insertionSort(int[] arr) {
        int[] sortArr = arr.clone();
        int n = sortArr.length;
        
        for (int i = 1; i < n; i++) {
            int key = sortArr[i];
            int j = i - 1;
            
            // Move elements greater than key one position ahead
            while (j >= 0 && sortArr[j] > key) {
                sortArr[j + 1] = sortArr[j];
                j--;
            }
            sortArr[j + 1] = key;
        }
        return sortArr;
    }
    
    /* ==================== Quicksort ==================== */
    
    /**
     * Quicksort with random shuffle and Hoare partitioning
     * Average Time: O(N log N), Space: O(log N)
     */
    public int[] quickSort(int[] arr) {
        if (arr == null || arr.length <= 1) return arr.clone();
        
        int[] sortArr = arr.clone();
        shuffle(sortArr);  // Prevent worst-case
        quickSortHelper(sortArr, 0, sortArr.length - 1);
        return sortArr;
    }
    
    private void quickSortHelper(int[] arr, int left, int right) {
        if (left >= right) return;
        
        int pivotIdx = hoarePartition(arr, left, right);
        quickSortHelper(arr, left, pivotIdx);
        quickSortHelper(arr, pivotIdx + 1, right);
    }
    
    private int hoarePartition(int[] arr, int left, int right) {
        int pivot = arr[left];
        int i = left - 1, j = right + 1;
        
        while (true) {
            do { i++; } while (arr[i] < pivot);
            do { j--; } while (arr[j] > pivot);
            if (i >= j) return j;
            swap(arr, i, j);
        }
    }
    
    /**
     * QuickSelect: Find k-th smallest element (0-indexed)
     * Average Time: O(N), Worst: O(N²)
     */
    public int quickSelect(int[] arr, int k) {
        if (arr == null || k < 0 || k >= arr.length) {
            throw new IllegalArgumentException("Invalid k");
        }
        
        int[] sortArr = arr.clone();
        shuffle(sortArr);
        
        int left = 0, right = sortArr.length - 1;
        while (left < right) {
            int pivotIdx = hoarePartition(sortArr, left, right);
            if (pivotIdx < k) {
                left = pivotIdx + 1;
            } else {
                right = pivotIdx;
            }
        }
        return sortArr[left];
    }
    
    /* ==================== Radix Sort (LSD) ==================== */
    
    /**
     * LSD Radix Sort for non-negative integers
     * Time: O(W * N), Space: O(N + R)
     */
    public int[] radixSort(int[] arr) {
        if (arr == null || arr.length <= 1) return arr.clone();
        
        int[] sortArr = arr.clone();
        int max = getMax(sortArr);
        
        // Do counting sort for every digit
        for (int exp = 1; max / exp > 0; exp *= 10) {
            countingSortByDigit(sortArr, exp);
        }
        return sortArr;
    }
    
    private void countingSortByDigit(int[] arr, int exp) {
        int n = arr.length;
        int[] output = new int[n];
        int[] count = new int[10];
        
        // Count occurrences
        for (int value : arr) {
            count[(value / exp) % 10]++;
        }
        
        // Compute prefix sums (starting positions)
        for (int i = 1; i < 10; i++) {
            count[i] += count[i - 1];
        }
        
        // Build output array (stable - iterate from end)
        for (int i = n - 1; i >= 0; i--) {
            int digit = (arr[i] / exp) % 10;
            output[--count[digit]] = arr[i];
        }
        
        // Copy back
        System.arraycopy(output, 0, arr, 0, n);
    }
    
    private int getMax(int[] arr) {
        int max = arr[0];
        for (int num : arr) {
            if (num > max) max = num;
        }
        return max;
    }
    
    /* ==================== Utility Methods ==================== */
    
    private void swap(int[] arr, int i, int j) {
        int temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }
    
    private void shuffle(int[] arr) {
        for (int i = arr.length - 1; i > 0; i--) {
            int j = rand.nextInt(i + 1);
            swap(arr, i, j);
        }
    }
    
    /* ==================== Main for Testing ==================== */
    
    public static void main(String[] args) {
        Sort sorter = new Sort();
        int[] test = {64, 34, 25, 12, 22, 11, 90};
        
        System.out.println("Original: " + java.util.Arrays.toString(test));
        System.out.println("Selection: " + java.util.Arrays.toString(sorter.selectionSort(test)));
        System.out.println("Heapsort: " + java.util.Arrays.toString(sorter.heapSort(test)));
        System.out.println("Mergesort: " + java.util.Arrays.toString(sorter.mergeSort(test)));
        System.out.println("Insertion: " + java.util.Arrays.toString(sorter.insertionSort(test)));
        System.out.println("Quicksort: " + java.util.Arrays.toString(sorter.quickSort(test)));
        System.out.println("Radixsort: " + java.util.Arrays.toString(sorter.radixSort(test)));
        System.out.println("QuickSelect (3rd smallest): " + sorter.quickSelect(test, 2));
    }
}
```

---

## Key Takeaways

1. **No single "best" sorting algorithm** - choose based on your constraints:
   - Small/Nearly sorted data → Insertion Sort
   - Guaranteed performance → Mergesort or Heapsort
   - General-purpose fast sorting → Quicksort (with optimizations)
   - Integer keys with small range → Radix Sort

2. **Trade-offs are inevitable:**
   - Time vs Space (Mergesort)
   - Average vs Worst case (Quicksort)
   - Comparisons vs Restricted keys (Comparison-based vs Radix)

3. **Practical considerations:**
   - Hybrid approaches (e.g., Quicksort switching to Insertion Sort for small subarrays)
   - Stability requirements for multi-key sorting
   - Cache efficiency and real-world performance
