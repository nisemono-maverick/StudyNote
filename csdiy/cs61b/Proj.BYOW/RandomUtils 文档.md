`RandomUtils` 是一个伪随机数生成工具库，提供了多种分布的随机数生成方法以及数组打乱、排列等功能。  
  
**包路径**: `utils.RandomUtils`  
  
**来源**: 改编自普林斯顿大学 [StdRandom](https://introcs.cs.princeton.edu/java/22library/StdRandom.java.html)  
  
---  
  
## 目录  
  
1. [均匀分布 (Uniform)](#1-均匀分布-uniform)  
2. [伯努利分布 (Bernoulli)](#2-伯努利分布-bernoulli)  
3. [高斯分布 (Gaussian)](#3-高斯分布-gaussian)  
4. [几何分布 (Geometric)](#4-几何分布-geometric)  
5. [泊松分布 (Poisson)](#5-泊松分布-poisson)  
6. [帕累托分布 (Pareto)](#6-帕累托分布-pareto)  
7. [柯西分布 (Cauchy)](#7-柯西分布-cauchy)  
8. [指数分布 (Exponential)](#8-指数分布-exponential)  
9. [离散分布 (Discrete)](#9-离散分布-discrete)  
10. [数组打乱 (Shuffle)](#10-数组打乱-shuffle)  
11. [随机排列 (Permutation)](#11-随机排列-permutation)  
  
---  
  
## 1. 均匀分布 (Uniform)  
  
### `uniform(Random random)`  
  
返回一个在 `[0, 1)` 范围内均匀分布的随机实数。  
  
| 项目 | 说明 |  
|------|------|  
| **参数** | `random` - `java.util.Random` 实例 |  
| **返回值** | `double` - 范围 `[0, 1)` 的随机实数 |  
| **异常** | 无 |  
  
```java  
double r = RandomUtils.uniform(random);  // 例如: 0.4721  
```  
  
---  
  
### `uniform(Random random, int n)`  
  
返回一个在 `[0, n)` 范围内均匀分布的随机整数。  
  
| 项目 | 说明 |  
|------|------|  
| **参数** | `random` - `java.util.Random` 实例<br>`n` - 整数范围的上限（不包含） |  
| **返回值** | `int` - 范围 `[0, n)` 的随机整数 |  
| **异常** | `IllegalArgumentException` - 如果 `n <= 0` |  
  
```java  
int r = RandomUtils.uniform(random, 10);  // 例如: 7 (范围 0-9)  
```  
  
---  
  
### `uniform(Random random, long n)`  
  
返回一个在 `[0, n)` 范围内均匀分布的随机长整数。  
  
| 项目 | 说明 |  
|------|------|  
| **参数** | `random` - `java.util.Random` 实例<br>`n` - 长整数范围的上限（不包含） |  
| **返回值** | `long` - 范围 `[0, n)` 的随机长整数 |  
| **异常** | `IllegalArgumentException` - 如果 `n <= 0` |  
  
```java  
long r = RandomUtils.uniform(random, 10000000000L);  
```  
  
---  
  
### `uniform(Random random, int a, int b)`  
  
返回一个在 `[a, b)` 范围内均匀分布的随机整数。  
  
| 项目 | 说明 |  
|------|------|  
| **参数** | `random` - `java.util.Random` 实例<br>`a` - 左端点（包含）<br>`b` - 右端点（不包含） |  
| **返回值** | `int` - 范围 `[a, b)` 的随机整数 |  
| **异常** | `IllegalArgumentException` - 如果 `b <= a` 或 `b - a >= Integer.MAX_VALUE` |  
  
```java  
int r = RandomUtils.uniform(random, 5, 10);  // 例如: 7 (范围 5-9)  
```  
  
---  
  
### `uniform(Random random, double a, double b)`  
  
返回一个在 `[a, b)` 范围内均匀分布的随机实数。  
  
| 项目 | 说明 |  
|------|------|  
| **参数** | `random` - `java.util.Random` 实例<br>`a` - 左端点（包含）<br>`b` - 右端点（不包含） |  
| **返回值** | `double` - 范围 `[a, b)` 的随机实数 |  
| **异常** | `IllegalArgumentException` - 如果 `!(a < b)` |  
  
```java  
double r = RandomUtils.uniform(random, 10.0, 20.0);  // 例如: 15.67  
```  
  
---  
  
## 2. 伯努利分布 (Bernoulli)  
  
### `bernoulli(Random random, double p)`  
  
根据成功概率 `p` 返回一个伯努利分布的随机布尔值。  
  
| 项目 | 说明 |  
|------|------|  
| **参数** | `random` - `java.util.Random` 实例<br>`p` - 返回 `true` 的概率，范围 `[0.0, 1.0]` |  
| **返回值** | `boolean` - 以概率 `p` 返回 `true`，以概率 `1-p` 返回 `false` |  
| **异常** | `IllegalArgumentException` - 如果 `p` 不在 `[0.0, 1.0]` 范围内 |  
  
```java  
boolean success = RandomUtils.bernoulli(random, 0.3);  // 30% 概率为 true  
```  
  
---  
  
### `bernoulli(Random random)`  
  
返回一个公平硬币抛掷结果（成功概率 0.5）。  
  
| 项目 | 说明 |  
|------|------|  
| **参数** | `random` - `java.util.Random` 实例 |  
| **返回值** | `boolean` - 以 50% 概率返回 `true` 或 `false` |  
| **异常** | 无 |  
  
```java  
boolean heads = RandomUtils.bernoulli(random);  // 公平硬币  
```  
  
---  
  
## 3. 高斯分布 (Gaussian)  
  
### `gaussian(Random random)`  
  
返回一个标准高斯分布（正态分布）的随机实数，均值为 0，标准差为 1。  
  
使用 **Box-Muller 变换的极坐标形式** 实现。  
  
| 项目 | 说明 |  
|------|------|  
| **参数** | `random` - `java.util.Random` 实例 |  
| **返回值** | `double` - 标准正态分布的随机值 |  
| **异常** | 无 |  
  
```java  
double r = RandomUtils.gaussian(random);  // 例如: -0.52 (大部分值在 -3 到 3 之间)  
```  
  
---  
  
### `gaussian(Random random, double mu, double sigma)`  
  
返回一个高斯分布的随机实数，指定均值和标准差。  
  
| 项目 | 说明 |  
|------|------|  
| **参数** | `random` - `java.util.Random` 实例<br>`mu` (μ) - 均值<br>`sigma` (σ) - 标准差 |  
| **返回值** | `double` - 均值为 `mu`，标准差为 `sigma` 的正态分布随机值 |  
| **异常** | 无 |  
  
```java  
// 生成身高数据（均值 170cm，标准差 10cm）  
double height = RandomUtils.gaussian(random, 170.0, 10.0);  
```  
  
---  
  
## 4. 几何分布 (Geometric)  
  
### `geometric(Random random, double p)`  
  
返回一个几何分布的随机整数，表示获得第一次成功所需的试验次数。  
  
使用 **Knuth 算法** 实现。  
  
| 项目 | 说明 |  
|------|------|  
| **参数** | `random` - `java.util.Random` 实例<br>`p` - 每次试验的成功概率，范围 `(0.0, 1.0]` |  
| **返回值** | `int` - 获得第一次成功所需的试验次数；如果 `p` 接近 1.0，返回 `Integer.MAX_VALUE` |  
| **异常** | `IllegalArgumentException` - 如果 `p` 不在 `[0.0, 1.0]` 范围内 |  
  
```java  
// 掷骰子直到出现 6，需要多少次？  
int rolls = RandomUtils.geometric(random, 1.0/6.0);  // 例如: 4  
```  
  
---  
  
## 5. 泊松分布 (Poisson)  
  
### `poisson(Random random, double lambda)`  
  
返回一个泊松分布的随机整数，均值为 `lambda`。  
  
使用 **Knuth 算法** 实现。  
  
| 项目 | 说明 |  
|------|------|  
| **参数** | `random` - `java.util.Random` 实例<br>`lambda` (λ) - 分布的均值，必须为正数 |  
| **返回值** | `int` - 泊松分布的随机值 |  
| **异常** | `IllegalArgumentException` - 如果 `lambda <= 0.0` 或为无穷大 |  
  
```java  
// 某服务台每小时平均来 4 个顾客，这个小时来多少人？  
int customers = RandomUtils.poisson(random, 4.0);  // 例如: 3  
```  
  
---  
  
## 6. 帕累托分布 (Pareto)  
  
### `pareto(Random random)`  
  
返回一个标准帕累托分布的随机实数（形状参数 α = 1.0）。  
  
帕累托分布描述"80-20法则"等现象，即大部分结果来自少数原因。  
  
| 项目 | 说明 |  
|------|------|  
| **参数** | `random` - `java.util.Random` 实例 |  
| **返回值** | `double` - 标准帕累托分布的随机值 |  
| **异常** | 无 |  
  
```java  
double r = RandomUtils.pareto(random);  
```  
  
---  
  
### `pareto(Random random, double alpha)`  
  
返回一个帕累托分布的随机实数，指定形状参数。  
  
| 项目 | 说明 |  
|------|------|  
| **参数** | `random` - `java.util.Random` 实例<br>`alpha` (α) - 形状参数，必须为正数 |  
| **返回值** | `double` - 形状参数为 `alpha` 的帕累托分布随机值 |  
| **异常** | `IllegalArgumentException` - 如果 `alpha <= 0.0` |  
  
```java  
// alpha 越小，尾部越重（极端值越多）  
double r = RandomUtils.pareto(random, 2.0);  
```  
  
---  
  
## 7. 柯西分布 (Cauchy)  
  
### `cauchy(Random random)`  
  
返回一个柯西分布的随机实数。  
  
柯西分布具有"厚尾"特性，均值和方差都不存在。  
  
| 项目 | 说明 |  
|------|------|  
| **参数** | `random` - `java.util.Random` 实例 |  
| **返回值** | `double` - 柯西分布的随机值 |  
| **异常** | 无 |  
  
```java  
double r = RandomUtils.cauchy(random);  // 可能产生很大的值  
```  
  
---  
  
## 8. 指数分布 (Exponential)  
  
### `exp(Random random, double lambda)`  
  
返回一个指数分布的随机实数，速率为 `lambda`。  
  
指数分布描述独立随机事件发生的时间间隔，如顾客到达间隔。  
  
| 项目 | 说明 |  
|------|------|  
| **参数** | `random` - `java.util.Random` 实例<br>`lambda` (λ) - 速率参数，必须为正数 |  
| **返回值** | `double` - 指数分布的随机值 |  
| **异常** | `IllegalArgumentException` - 如果 `lambda <= 0.0` |  
  
```java  
// 平均每小时来 2 个顾客，下一个顾客多久后到？（小时）  
double waitTime = RandomUtils.exp(random, 2.0);  // 例如: 0.23  
```  
  
---  
  
## 9. 离散分布 (Discrete)  
  
### `discrete(Random random, double[] probabilities)`  
  
根据给定的概率分布返回一个随机整数索引。  
  
| 项目 | 说明 |  
|------|------|  
| **参数** | `random` - `java.util.Random` 实例<br>`probabilities` - 概率数组，`probabilities[i]` 是返回 `i` 的概率 |  
| **返回值** | `int` - 以指定概率返回对应的索引 |  
| **异常** | `IllegalArgumentException` - 如果数组为 `null`、概率和不为 1.0、或有负概率 |  
  
```java  
// 掷一个不均匀的骰子  
double[] probs = {0.1, 0.1, 0.1, 0.1, 0.1, 0.5};  // 6 点概率 50%int roll = RandomUtils.discrete(random, probs);  // 例如: 5 (即 6 点)  
```  
  
---  
  
### `discrete(Random random, int[] frequencies)`  
  
根据给定的频数分布返回一个随机整数索引。  
  
| 项目 | 说明 |  
|------|------|  
| **参数** | `random` - `java.util.Random` 实例<br>`frequencies` - 频数数组，`frequencies[i]` 是返回 `i` 的相对频率 |  
| **返回值** | `int` - 以与频数成比例的概率返回对应的索引 |  
| **异常** | `IllegalArgumentException` - 如果数组为 `null`、全为 0、有负数、或总和超过 `Integer.MAX_VALUE` |  
  
```java  
// 从奖池中抽奖  
int[] frequencies = {10, 5, 1};  // 奖项 A 10 张，B 5 张，C 1 张  
int prize = RandomUtils.discrete(random, frequencies);  // 例如: 0 (奖项 A)  
```  
  
---  
  
## 10. 数组打乱 (Shuffle)  
  
### `shuffle(Random random, Object[] a)`  
  
将对象数组随机打乱（Fisher-Yates 洗牌算法）。  
  
| 项目 | 说明 |  
|------|------|  
| **参数** | `random` - `java.util.Random` 实例<br>`a` - 要打乱的数组 |  
| **返回值** | 无（原地修改） |  
| **异常** | `IllegalArgumentException` - 如果数组为 `null` |  
  
```java  
String[] cards = {"A", "2", "3", "4", "5"};RandomUtils.shuffle(random, cards);  
// cards 现在可能是: ["3", "A", "5", "2", "4"]  
```  
  
---  
  
### `shuffle(Random random, double[] a)` / `shuffle(Random random, int[] a)` / `shuffle(Random random, char[] a)`  
  
将基本类型数组随机打乱。  
  
| 项目 | 说明 |  
|------|------|  
| **参数** | `random` - `java.util.Random` 实例<br>`a` - 要打乱的数组 |  
| **返回值** | 无（原地修改） |  
| **异常** | `IllegalArgumentException` - 如果数组为 `null` |  
  
---  
  
### `shuffle(Random random, Object[] a, int lo, int hi)` / `shuffle(Random random, double[] a, int lo, int hi)` / `shuffle(Random random, int[] a, int lo, int hi)`  
  
只打乱数组的指定子范围 `[lo, hi)`。  
  
| 项目 | 说明 |  
|------|------|  
| **参数** | `random` - `java.util.Random` 实例<br>`a` - 要打乱的数组<br>`lo` - 左端点（包含）<br>`hi` - 右端点（不包含） |  
| **返回值** | 无（原地修改） |  
| **异常** | `IllegalArgumentException` - 如果数组为 `null` 或索引越界 |  
  
```java  
int[] arr = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};  
RandomUtils.shuffle(random, arr, 3, 7);  
// 只有索引 3,4,5,6 被打乱，其他位置不变  
```  
  
---  
  
## 11. 随机排列 (Permutation)  
  
### `permutation(Random random, int n)`  
  
返回 `0` 到 `n-1` 的一个均匀随机排列。  
  
| 项目 | 说明 |  
|------|------|  
| **参数** | `random` - `java.util.Random` 实例<br>`n` - 元素个数 |  
| **返回值** | `int[]` - 长度为 `n` 的随机排列数组 |  
| **异常** | `IllegalArgumentException` - 如果 `n` 为负数 |  
  
```java  
int[] perm = RandomUtils.permutation(random, 5);  
// 可能是: [3, 0, 4, 1, 2]  
```  
  
---  
  
### `permutation(Random random, int n, int k)`  
  
返回从 `0` 到 `n-1` 中均匀随机选择 `k` 个元素的排列。  
  
| 项目 | 说明 |  
|------|------|  
| **参数** | `random` - `java.util.Random` 实例<br>`n` - 总元素个数<br>`k` - 选择的元素个数 |  
| **返回值** | `int[]` - 长度为 `k` 的随机排列数组 |  
| **异常** | `IllegalArgumentException` - 如果 `n` 为负数，或 `k` 不在 `[0, n]` 范围内 |  
  
```java  
// 从 52 张牌中随机发 5 张  
int[] hand = RandomUtils.permutation(random, 52, 5);  
// 例如: [23, 5, 48, 11, 37]  
```  
  
---  
  
## 使用示例  
  
### 基础用法  
  
```java  
import utils.RandomUtils;  
import java.util.Random;  
  
public class Example {  
    public static void main(String[] args) {        // 使用种子确保可重复  
        Random random = new Random(12345L);        // 随机整数 [0, 10)        int dice = RandomUtils.uniform(random, 1, 7);  // 掷骰子  
        // 随机布尔（50%）  
        boolean coin = RandomUtils.bernoulli(random);        // 打乱数组  
        String[] names = {"Alice", "Bob", "Carol", "David"};        RandomUtils.shuffle(random, names);        // 随机选择  
        double[] weights = {0.5, 0.3, 0.2};        int choice = RandomUtils.discrete(random, weights);    }}  
```  
  
### 在游戏开发中的使用  
  
```java  
// 随机生成游戏世界  
public class WorldGenerator {  
    private Random random;        public WorldGenerator(long seed) {  
        this.random = new Random(seed);    }        public void generate() {  
        // 随机决定房间数量（10-20个）  
        int roomCount = RandomUtils.uniform(random, 10, 21);        // 随机决定是否生成宝藏（30%概率）  
        boolean hasTreasure = RandomUtils.bernoulli(random, 0.3);        // 随机房间大小（正态分布）  
        int roomWidth = (int) RandomUtils.gaussian(random, 8, 2);        // 从敌人类型池中随机选择  
        String[] enemyTypes = {"Goblin", "Orc", "Dragon", "Skeleton"};        String enemy = enemyTypes[RandomUtils.uniform(random, enemyTypes.length)];    }}  
```  
  
---  
  
## 注意事项  
  
1. **种子可重复性**: 使用相同的种子创建 `Random` 实例，可以获得完全相同的随机数序列  
2. **线程安全**: `RandomUtils` 本身不是线程安全的，多线程环境下建议使用 `ThreadLocalRandom`  
3. **性能**: 对于大量随机数生成，考虑使用 `SplittableRandom`（Java 8+）  
4. **异常处理**: 注意检查参数范围，避免 `IllegalArgumentException`