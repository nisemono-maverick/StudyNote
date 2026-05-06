# LaTeX 常用命令速查表

## 文档结构

```latex
\documentclass[选项]{类}          % 文档类：article, report, book, beamer
\usepackage{包名}                 % 导入宏包
\begin{document}                  % 文档开始
\end{document}                    % 文档结束
```

### 常用文档类选项
| 选项 | 说明 |
|------|------|
| `10pt/11pt/12pt` | 正文字号 |
| `a4paper/letterpaper` | 纸张大小 |
| `twoside/oneside` | 单双面打印 |
| `titlepage/notitlepage` | 标题页 |

---

## 常用宏包

```latex
\usepackage[utf8]{inputenc}       % 编码
\usepackage[UTF8]{ctex}            % 中文支持
\usepackage{amsmath, amssymb}      % 数学公式
\usepackage{graphicx}              % 插入图片
\usepackage{geometry}              % 页面布局
\usepackage{hyperref}              % 超链接
\usepackage{listings}              % 代码高亮
\usepackage{booktabs}              % 三线表
\usepackage{enumitem}              % 列表定制
\usepackage{xcolor}                % 颜色
```

---

## 章节命令

```latex
\part{部分}                       % 仅 book/report
\chapter{章}                      % 仅 book/report
\section{节}
\subsection{小节}
\subsubsection{小小节}
\paragraph{段落}
\subparagraph{子段落}

\tableofcontents                   % 生成目录
\listoffigures                     % 图目录
\listoftables                      % 表目录
```

---

## 文本格式

```latex
\textbf{粗体}                     % bold
\textit{斜体}                     % italic
\underline{下划线}                % underline
\texttt{等宽字体}                 % typewriter
\textsf{无衬线}                   % sans-serif
\emph{强调}                       % emphasis（通常是斜体）

\small \large \Large \huge        % 字号变化
\centering \raggedright           % 对齐方式
```

---

## 数学公式

### 行内公式
```latex
$...$ 或 \(...\)                  % 行内公式，如 $E=mc^2$
```

### 独立公式
```latex
\[...\] 或 $$...$$               % 无编号
\begin{equation}                 % 有编号
\end{equation}
\begin{equation*}                % 无编号
\end{equation*}
```

### 常用符号
```latex
上标：x^2    下标：x_i    分数：\frac{a}{b}
根号：\sqrt{x}  \sqrt[n]{x}
求和：\sum_{i=1}^{n}    积分：\int_{a}^{b}
极限：\lim_{x \to \infty}
向量：\vec{a}  矩阵：\begin{pmatrix} a & b \\ c & d \end{pmatrix}
```

### 希腊字母
```latex
\alpha \beta \gamma \delta \epsilon \varepsilon
\Gamma \Delta \Theta \Lambda \Pi \Sigma
```

### 常用符号
```latex
\pm \times \div \cdot \infty \partial \nabla
\leq \geq \neq \approx \equiv \sim
\in \notin \subset \supset \cup \cap
\forall \exists \Rightarrow \Leftarrow \Leftrightarrow
```

### 多行公式
```latex
\begin{align}
  a &= b + c \\
  d &= e + f
\end{align}

\begin{cases}
  x = 1, & y = 2 \\
  x = 3, & y = 4
\end{cases}
```

---

## 列表环境

```latex
\begin{itemize}                   % 无序列表
  \item 项目
  \item 项目
\end{itemize}

\begin{enumerate}                 % 有序列表
  \item 第一项
  \item 第二项
\end{enumerate}

\begin{description}               % 描述列表
  \item[关键词] 解释
\end{description}
```

---

## 表格

```latex
\begin{table}[htbp]
  \centering
  \caption{表标题}
  \begin{tabular}{|l|c|r|}        % l左齐 c居中 r右齐 |竖线
    \hline
    左 & 中 & 右 \\
    \hline
    1 & 2 & 3 \\
    \hline
  \end{tabular}
\end{table}

% 三线表（推荐）
\begin{table}[htbp]
  \centering
  \caption{三线表}
  \begin{tabular}{lcr}
    \toprule
    左 & 中 & 右 \\
    \midrule
    1 & 2 & 3 \\
    \bottomrule
  \end{tabular}
\end{table}
```

**位置参数**: `h` here, `t` top, `b` bottom, `p` 单独页, `!` 强制

---

## 图片

```latex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.8\textwidth]{图片名}
  \caption{图标题}
  \label{fig:label}
\end{figure}

% 并排图片
\begin{figure}[htbp]
  \centering
  \subfigure[子图1]{\includegraphics[width=0.45\textwidth]{fig1}}
  \subfigure[子图2]{\includegraphics[width=0.45\textwidth]{fig2}}
  \caption{总标题}
\end{figure}
```

---

## 交叉引用

```latex
\label{sec:intro}                 % 设置标签
\ref{sec:intro}                   % 引用编号
\pageref{sec:intro}               % 引用页码
\eqref{eq:emc2}                   % 公式引用（带括号）
\cite{key}                        % 文献引用
\footnote{脚注内容}               % 脚注
```

---

## 参考文献

```latex
\begin{thebibliography}{99}
  \bibitem{key1} 作者, 标题, 期刊, 年份.
  \bibitem{key2} 作者, \emph{书名}, 出版社, 年份.
\end{thebibliography}

% 或使用 BibTeX/BibLaTeX
\bibliographystyle{plain}
\bibliography{references}
```

---

## 常用环境

```latex
\begin{quote}                    % 引用环境
\begin{quotation}                % 带缩进的引用
\begin{abstract}                 % 摘要
\begin{appendix}                 % 附录
\begin{verbatim}                 % 原样输出
\begin{lstlisting}               % 代码（需listings包）
```

---

## 页面设置

```latex
\usepackage{geometry}
\geometry{a4paper, margin=2.5cm}
% 或
\geometry{left=2cm, right=2cm, top=2.5cm, bottom=2.5cm}

\newpage                         % 分页
\clearpage                       % 分页并清空浮动体
\thispagestyle{empty}            % 本页无页眉页脚
```

---

## 自定义命令

```latex
\newcommand{\cmd}{定义}          % 定义新命令
\newcommand{\cmd}[1]{使用#1}      % 带一个参数
\renewcommand{\cmd}{新定义}       % 重定义命令
```

---

## 常用技巧

| 需求 | 命令 |
|------|------|
| 换行 | `\\` |
| 新段 | 空一行 |
| 水平空格 | `\quad` `\qquad` `\,` `\:` `\;` |
| 省略号 | `\dots` `\cdots` `\vdots` `\ddots` |
| 度符号 | `$45^\circ$` |
| 百分号 | `\%` |
| 注释 | `% 注释内容` |
| 非断行空格 | `~` |

---

## 编译流程

```bash
# 简单文档
pdflatex main.tex

# 含交叉引用
pdflatex main.tex
pdflatex main.tex

# 含参考文献
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex

# 或直接用 latexmk
latexmk -pdf main.tex
```
