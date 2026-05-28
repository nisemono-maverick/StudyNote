---
title: 频率派与贝叶斯派及高斯分布 MLE
source: https://www.yuque.com/bystander-wg876/yc5f72/hu0291
date: 2026-05-28
---

## 1. 记号约定

对观测集采用如下记号：

$$
X_{N \times p} = (x_1, x_2, \cdots, x_N)^T, \quad x_i = (x_{i1}, x_{i2}, \cdots, x_{ip})^T
$$

这个记号表示有 $N$ 个样本，每个样本都是 $p$ 维向量。其中每个观测都是由 $p(x \mid \theta)$ 生成的。

---

## 2. 频率派的观点

$p(x \mid \theta)$ 中的 $\theta$ 是一个**常量**。对于 $N$ 个观测来说，观测集的概率为：

$$
p(X \mid \theta) \stackrel{\text{iid}}{=} \prod_{i=1}^{N} p(x_i \mid \theta)
$$

为了求 $\theta$ 的大小，我们采用**最大对数似然（MLE）**的方法：

$$
\theta_{\text{MLE}} = \arg\max_{\theta} \log p(X \mid \theta) \stackrel{\text{iid}}{=} \arg\max_{\theta} \sum_{i=1}^{N} \log p(x_i \mid \theta)
$$

---

## 3. 贝叶斯派的观点

贝叶斯派认为 $p(x \mid \theta)$ 中的 $\theta$ **不是一个常量**。这个 $\theta$ 满足一个预设的先验分布 $\theta \sim p(\theta)$。于是根据贝叶斯定理，依赖观测集参数的后验可以写成：

$$
p(\theta \mid X) = \frac{p(X \mid \theta) \cdot p(\theta)}{p(X)} = \frac{p(X \mid \theta) \cdot p(\theta)}{\int_{\theta} p(X \mid \theta) \cdot p(\theta) \, d\theta}
$$

为了求 $\theta$ 的值，我们要最大化这个参数后验（**MAP**）：

$$
\theta_{\text{MAP}} = \arg\max_{\theta} p(\theta \mid X) = \arg\max_{\theta} p(X \mid \theta) \cdot p(\theta)
$$

其中第二个等号是由于分母和 $\theta$ 没有关系。求解这个 $\theta$ 值后计算：

$$
p(\theta \mid X) = \frac{p(X \mid \theta) \cdot p(\theta)}{\int_{\theta} p(X \mid \theta) \cdot p(\theta) \, d\theta}
$$

就得到了参数的后验概率。其中 $p(X \mid \theta)$ 叫**似然**，是我们的模型分布。得到了参数的后验分布后，我们可以将这个分布用于预测——**贝叶斯预测**：

$$
p(x_{\text{new}} \mid X) = \int_{\theta} p(x_{\text{new}} \mid \theta) \cdot p(\theta \mid X) \, d\theta
$$

其中积分中的被乘数是**模型**，乘数是**后验分布**。

---

## 4. 小结

频率派和贝叶斯派分别给出了一系列的机器学习算法：

- **频率派**的观点导出了一系列的**统计机器学习算法**
- **贝叶斯派**导出了**概率图理论**

在应用频率派的 MLE 方法时，**最优化理论**占有重要地位。而贝叶斯派的算法，无论是后验概率的建模还是应用这个后验进行推断时，**积分**占有重要地位。因此采样积分方法如 **MCMC** 有很多应用。

---

## 5. Math Basics

### 5.1 高斯分布

#### 一维情况 MLE

高斯分布在机器学习中占有举足轻重的作用。在 MLE 方法中：

$$
\theta = (\mu, \Sigma) = (\mu, \sigma^2), \quad \theta_{\text{MLE}} = \arg\max_{\theta} \log p(X \mid \theta) \stackrel{\text{iid}}{=} \arg\max_{\theta} \sum_{i=1}^{N} \log p(x_i \mid \theta)
$$

一般地，高斯分布的概率密度函数（PDF）写为：

$$
p(x \mid \mu, \Sigma) = \frac{1}{(2\pi)^{p/2} |\Sigma|^{1/2}} e^{-\frac{1}{2}(x - \mu)^T \Sigma^{-1} (x - \mu)}
$$

带入 MLE 中，我们考虑一维的情况：

$$
\log p(X \mid \theta) = \sum_{i=1}^{N} \log p(x_i \mid \theta) = \sum_{i=1}^{N} \log \frac{1}{\sqrt{2\pi}\sigma} \exp\left(-\frac{(x_i - \mu)^2}{2\sigma^2}\right)
$$

**首先对 $\mu$ 求极值：**

$$
\mu_{\text{MLE}} = \arg\max_{\mu} \log p(X \mid \theta) = \arg\max_{\mu} \sum_{i=1}^{N} (x_i - \mu)^2
$$

于是：

$$
\frac{\partial}{\partial \mu} \sum_{i=1}^{N} (x_i - \mu)^2 = 0 \quad \Longrightarrow \quad \mu_{\text{MLE}} = \frac{1}{N} \sum_{i=1}^{N} x_i
$$

**其次对 $\sigma$ 求极值：**

$$
\sigma_{\text{MLE}} = \arg\max_{\sigma} \log p(X \mid \theta) = \arg\max_{\sigma} \sum_{i=1}^{N} \left[-\log \sigma - \frac{1}{2\sigma^2}(x_i - \mu)^2\right] = \arg\min_{\sigma} \sum_{i=1}^{N} \left[\log \sigma + \frac{1}{2\sigma^2}(x_i - \mu)^2\right]
$$

于是：

$$
\frac{\partial}{\partial \sigma} \sum_{i=1}^{N} \left[\log \sigma + \frac{1}{2\sigma^2}(x_i - \mu)^2\right] = 0 \quad \Longrightarrow \quad \sigma_{\text{MLE}}^2 = \frac{1}{N} \sum_{i=1}^{N} (x_i - \mu)^2
$$

**有偏性说明：**

值得注意的是，上面的推导中，首先对 $\mu$ 求 MLE，然后利用这个结果求 $\sigma_{\text{MLE}}$。因此可以预期的是对数据集求期望时，$E_D[\mu_{\text{MLE}}]$ 是**无偏**的：

$$
E_D[\mu_{\text{MLE}}] = E_D\left[\frac{1}{N} \sum_{i=1}^{N} x_i\right] = \frac{1}{N} \sum_{i=1}^{N} E_D[x_i] = \mu
$$

但是当对 $\sigma_{\text{MLE}}$ 求期望的时候，由于使用了单个数据集的 $\mu_{\text{MLE}}$，因此对所有数据集求期望的时候我们会发现 $\sigma_{\text{MLE}}$ 是**有偏**的：

$$
\begin{aligned}
E_D[\sigma_{\text{MLE}}^2] &= E_D\left[\frac{1}{N} \sum_{i=1}^{N} (x_i - \mu_{\text{MLE}})^2\right] \\
&= E_D\left[\frac{1}{N} \sum_{i=1}^{N} (x_i^2 - 2x_i\mu_{\text{MLE}} + \mu_{\text{MLE}}^2)\right] \\
&= E_D\left[\frac{1}{N} \sum_{i=1}^{N} x_i^2 - \mu_{\text{MLE}}^2\right] \\
&= E_D\left[\frac{1}{N} \sum_{i=1}^{N} x_i^2 - \mu^2 + \mu^2 - \mu_{\text{MLE}}^2\right] \\
&= E_D\left[\frac{1}{N} \sum_{i=1}^{N} x_i^2 - \mu^2\right] - E_D[\mu_{\text{MLE}}^2 - \mu^2] \\
&= \sigma^2 - (E_D[\mu_{\text{MLE}}^2] - \mu^2) \\
&= \sigma^2 - (E_D[\mu_{\text{MLE}}^2] - E_D^2[\mu_{\text{MLE}}]) \\
&= \sigma^2 - \text{Var}[\mu_{\text{MLE}}] \\
&= \sigma^2 - \text{Var}\left[\frac{1}{N} \sum_{i=1}^{N} x_i\right] \\
&= \sigma^2 - \frac{1}{N^2} \sum_{i=1}^{N} \text{Var}[x_i] \\
&= \frac{N-1}{N} \sigma^2
\end{aligned}
$$

所以无偏估计为：

$$
\hat{\sigma}^2 = \frac{1}{N-1} \sum_{i=1}^{N} (x_i - \mu)^2
$$

---

#### 多维情况

多维高斯分布表达式为：

$$
p(x \mid \mu, \Sigma) = \frac{1}{(2\pi)^{p/2} |\Sigma|^{1/2}} e^{-\frac{1}{2}(x - \mu)^T \Sigma^{-1} (x - \mu)}
$$

其中 $x, \mu \in \mathbb{R}^p$，$\Sigma \in \mathbb{R}^{p \times p}$，$\Sigma$ 为协方差矩阵，一般而言也是半正定矩阵。这里我们只考虑正定矩阵。

**马氏距离与特征值分解：**

首先处理指数上的数字，指数上的数字可以记为 $x$ 和 $\mu$ 之间的**马氏距离**。对于对称的协方差矩阵可进行特征值分解：

$$
\Sigma = U\Lambda U^T = (u_1, u_2, \cdots, u_p) \, \text{diag}(\lambda_i) \, (u_1, u_2, \cdots, u_p)^T = \sum_{i=1}^{p} u_i \lambda_i u_i^T
$$

于是：

$$
\Sigma^{-1} = \sum_{i=1}^{p} u_i \frac{1}{\lambda_i} u_i^T
$$

$$
\Delta = (x - \mu)^T \Sigma^{-1} (x - \mu) = \sum_{i=1}^{p} (x - \mu)^T u_i \frac{1}{\lambda_i} u_i^T (x - \mu) = \sum_{i=1}^{p} \frac{y_i^2}{\lambda_i}
$$

我们注意到 $y_i$ 是 $x - \mu$ 在特征向量 $u_i$ 上的投影长度，因此上式就是 $\Delta$ 取不同值时的**同心椭圆**。

**多维高斯模型的两个问题：**

1. **参数自由度太高**：参数 $\Sigma, \mu$ 的自由度为 $O(p^2)$，对于维度很高的数据其自由度太高。
   - **解决方案**：高自由度的来源是 $\Sigma$ 有 $\frac{p(p+1)}{2}$ 个自由参数，可以假设其是对角矩阵，甚至在各向同性假设中假设其对角线上的元素都相同。前一种的算法有 **Factor Analysis**，后一种有 **概率 PCA（p-PCA）**。

2. **单峰限制**：单个高斯分布是单峰的，对有多个峰的数据分布不能得到好的结果。
   - **解决方案**：**高斯混合模型（GMM）**。

---

### 5.2 高斯分布的常用定理

我们记 $x = (x_1, x_2, \cdots, x_p)^T = (x_{a,m \times 1}, x_{b,n \times 1})^T$，$\mu = (\mu_{a,m \times 1}, \mu_{b,n \times 1})$，

$$
\Sigma = \begin{pmatrix} \Sigma_{aa} & \Sigma_{ab} \\ \Sigma_{ba} & \Sigma_{bb} \end{pmatrix}
$$

已知 $x \sim \mathcal{N}(\mu, \Sigma)$。

**定理：** 已知 $x \sim \mathcal{N}(\mu, \Sigma)$，$y = Ax + b$，那么 $y \sim \mathcal{N}(A\mu + b, A\Sigma A^T)$。

**证明：**

$$
E[y] = E[Ax + b] = AE[x] + b = A\mu + b
$$

$$
\text{Var}[y] = \text{Var}[Ax + b] = \text{Var}[Ax] = A \cdot \text{Var}[x] \cdot A^T
$$

下面利用这个定理得到 $p(x_a)$、$p(x_b)$、$p(x_a \mid x_b)$、$p(x_b \mid x_a)$ 这四个量。

**1. 边缘分布 $p(x_a)$：**

$$
x_a = \begin{pmatrix} I_{m \times m} & O_{m \times n} \end{pmatrix} \begin{pmatrix} x_a \\ x_b \end{pmatrix}
$$

代入定理中得到：

$$
E[x_a] = \begin{pmatrix} I & O \end{pmatrix} \begin{pmatrix} \mu_a \\ \mu_b \end{pmatrix} = \mu_a
$$

$$
\text{Var}[x_a] = \begin{pmatrix} I & O \end{pmatrix} \begin{pmatrix} \Sigma_{aa} & \Sigma_{ab} \\ \Sigma_{ba} & \Sigma_{bb} \end{pmatrix} \begin{pmatrix} I \\ O \end{pmatrix} = \Sigma_{aa}
$$

所以：

$$
x_a \sim \mathcal{N}(\mu_a, \Sigma_{aa})
$$

**2. 边缘分布 $p(x_b)$：**

同理：

$$
x_b \sim \mathcal{N}(\mu_b, \Sigma_{bb})
$$

**3. 条件分布 $p(x_b \mid x_a)$：**

引入三个量：

$$
\begin{aligned}
x_{b \cdot a} &= x_b - \Sigma_{ba} \Sigma_{aa}^{-1} x_a \\
\mu_{b \cdot a} &= \mu_b - \Sigma_{ba} \Sigma_{aa}^{-1} \mu_a \\
\Sigma_{bb \cdot a} &= \Sigma_{bb} - \Sigma_{ba} \Sigma_{aa}^{-1} \Sigma_{ab}
\end{aligned}
$$

特别的，最后一个式子叫做 $\Sigma_{bb}$ 的 **Schur 补（Schur Complementary）**。

可以看到：

$$
x_{b \cdot a} = \begin{pmatrix} -\Sigma_{ba} \Sigma_{aa}^{-1} & I_{n \times n} \end{pmatrix} \begin{pmatrix} x_a \\ x_b \end{pmatrix}
$$

所以：

$$
E[x_{b \cdot a}] = \begin{pmatrix} -\Sigma_{ba} \Sigma_{aa}^{-1} & I_{n \times n} \end{pmatrix} \begin{pmatrix} \mu_a \\ \mu_b \end{pmatrix} = \mu_{b \cdot a}
$$

$$
\text{Var}[x_{b \cdot a}] = \begin{pmatrix} -\Sigma_{ba} \Sigma_{aa}^{-1} & I_{n \times n} \end{pmatrix} \begin{pmatrix} \Sigma_{aa} & \Sigma_{ab} \\ \Sigma_{ba} & \Sigma_{bb} \end{pmatrix} \begin{pmatrix} -\Sigma_{aa}^{-1} \Sigma_{ba}^T \\ I_{n \times n} \end{pmatrix} = \Sigma_{bb \cdot a}
$$

利用这三个量可以得到 $x_b = x_{b \cdot a} + \Sigma_{ba} \Sigma_{aa}^{-1} x_a$。因此：

$$
E[x_b \mid x_a] = \mu_{b \cdot a} + \Sigma_{ba} \Sigma_{aa}^{-1} x_a
$$

$$
\text{Var}[x_b \mid x_a] = \Sigma_{bb \cdot a}
$$

**4. 条件分布 $p(x_a \mid x_b)$：**

同理，引入：

$$
\begin{aligned}
x_{a \cdot b} &= x_a - \Sigma_{ab} \Sigma_{bb}^{-1} x_b \\
\mu_{a \cdot b} &= \mu_a - \Sigma_{ab} \Sigma_{bb}^{-1} \mu_b \\
\Sigma_{aa \cdot b} &= \Sigma_{aa} - \Sigma_{ab} \Sigma_{bb}^{-1} \Sigma_{ba}
\end{aligned}
$$

所以：

$$
E[x_a \mid x_b] = \mu_{a \cdot b} + \Sigma_{ab} \Sigma_{bb}^{-1} x_b
$$

$$
\text{Var}[x_a \mid x_b] = \Sigma_{aa \cdot b}
$$

---

### 5.3 线性模型求解

**已知：**

$$
p(x) = \mathcal{N}(\mu, \Lambda^{-1}), \quad p(y \mid x) = \mathcal{N}(Ax + b, L^{-1})
$$

**求解：** $p(y)$、$p(x \mid y)$

**解：**

令 $y = Ax + b + \epsilon$，$\epsilon \sim \mathcal{N}(0, L^{-1})$，所以：

$$
E[y] = E[Ax + b + \epsilon] = A\mu + b
$$

$$
\text{Var}[y] = A\Lambda^{-1}A^T + L^{-1}
$$

因此：

$$
p(y) = \mathcal{N}(A\mu + b, L^{-1} + A\Lambda^{-1}A^T)
$$

引入 $z = \begin{pmatrix} x \\ y \end{pmatrix}$，我们可以得到：

$$
\text{Cov}(x, y) = E[(x - E[x])(y - E[y])^T]
$$

对于这个协方差可以直接计算：

$$
\text{Cov}(x, y) = E[(x - \mu)(Ax - A\mu + \epsilon)^T] = E[(x - \mu)(x - \mu)^T A^T] = \text{Var}[x] A^T = \Lambda^{-1} A^T
$$

注意到协方差矩阵的对称性，所以：

$$
p(z) = \mathcal{N}\left(\begin{pmatrix} \mu \\ A\mu + b \end{pmatrix}, \begin{pmatrix} \Lambda^{-1} & \Lambda^{-1} A^T \\ A\Lambda^{-1} & L^{-1} + A\Lambda^{-1}A^T \end{pmatrix}\right)
$$

根据之前的公式，我们可以得到：

$$
E[x \mid y] = \mu + \Lambda^{-1} A^T (L^{-1} + A\Lambda^{-1}A^T)^{-1} (y - A\mu - b)
$$

$$
\text{Var}[x \mid y] = \Lambda^{-1} - \Lambda^{-1} A^T (L^{-1} + A\Lambda^{-1}A^T)^{-1} A \Lambda^{-1}
$$
