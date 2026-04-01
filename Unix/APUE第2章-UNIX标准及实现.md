# 第 2 章：UNIX 标准及实现

## 2.1 引言

本章回答一个问题：**为什么同样是 UNIX，不同系统（Linux、macOS、FreeBSD）上的程序要重新编译才能运行？**

答案在于：历史上 UNIX 分裂成很多变种，各家自己扩展 API，导致不兼容。为了解决这个问题，业界制定了各种标准。

---

## 2.2 UNIX 标准化

### 2.2.1 ISO C

**ISO C** 是 C 语言本身的标准，和操作系统无关。它规定了：
- 语言语法
- 标准库函数（`printf`、`malloc`、`strlen` 等）

C89 → C99 → C11 → C17 → C23，版本不断演进。

`#include <stdio.h>` 引入的就是 ISO C 标准库。

### 2.2.2 IEEE POSIX

**POSIX**（Portable Operating System Interface）是 IEEE 制定的操作系统接口标准，规定了：
- 系统调用有哪些（`open`、`fork`、`read`...）
- 库函数有哪些
- shell 和工具的行为
- 线程、网络等接口

POSIX 标准让程序可以在不同 UNIX 系统间移植，只需重新编译。

> macOS 通过了 POSIX 官方认证，是正牌 UNIX；Linux 兼容 POSIX 但没有认证。

### 2.2.3 Single UNIX Specification（SUS）

**SUS** 是比 POSIX 更完整的标准，由 The Open Group 维护。通过认证才能叫做「UNIX」商标。

SUSv3 = POSIX.1-2001，SUSv4 = POSIX.1-2008，两者高度重合。

---

## 2.3 UNIX 系统实现

标准是规范，实现是具体的操作系统。主要实现：

| 系统 | 内核 | 备注 |
|------|------|------|
| Linux | Linux | GNU/Linux，最广泛 |
| macOS | XNU（Mach + BSD） | 通过 POSIX 认证 |
| FreeBSD | FreeBSD | 服务器常用 |
| Solaris | illumos | Oracle |

本书以 **Linux** 和 **macOS（Darwin）** 为主要参考平台。

---

## 2.4 标准和实现的关系

```
ISO C 标准
    │
    ▼
POSIX 标准（超集，包含 ISO C，增加系统调用规范）
    │
    ▼
SUS 标准（超集，包含 POSIX，增加更多接口）
    │
    ▼
具体实现（Linux / macOS / FreeBSD）
（可能有各自的扩展，超出标准范围）
```

实现可以在标准之上添加扩展，但这样写的代码就不可移植了。

---

## 2.5 限制

UNIX 系统有两类限制：

### 编译时限制

写死在头文件里的常量，编译时就能知道，不依赖运行环境。

```c
#include <limits.h>
INT_MAX      // int 的最大值，通常 2147483647
PATH_MAX     // 路径最大长度，通常 1024 或 4096

#include <float.h>
DBL_MAX      // double 的最大值
```

### 运行时限制

需要在运行时查询，因为可能因系统配置不同而变化。

```c
#include <unistd.h>

// sysconf 查询系统运行时限制
long clk_tck = sysconf(_SC_CLK_TCK);    // 每秒时钟滴答数
long open_max = sysconf(_SC_OPEN_MAX);  // 最大打开文件数

// pathconf 查询路径相关限制
long name_max = pathconf("/", _PC_NAME_MAX);  // 文件名最大长度
```

```bash
# 命令行查询
getconf OPEN_MAX
getconf PATH_MAX /
```

---

## 2.6 选项

POSIX 定义了很多**可选特性**，不同系统支持情况不同。程序可以在运行时查询：

```c
// 查询系统是否支持某个 POSIX 特性
sysconf(_SC_JOB_CONTROL)   // 是否支持作业控制
sysconf(_SC_SAVED_IDS)     // 是否支持 saved set-user-ID
```

头文件里也有宏定义：
- 定义为 -1：肯定不支持
- 定义为正数：肯定支持
- 未定义：运行时查询

---

## 2.7 功能测试宏

编译时通过宏控制暴露哪些接口：

```c
// 只使用 POSIX.1 接口，屏蔽平台扩展
#define _POSIX_SOURCE

// 使用 POSIX.1 + SUSv4 接口
#define _XOPEN_SOURCE 700

// 使用 GNU 扩展（Linux 特有）
#define _GNU_SOURCE
```

实际用法：编译时传参数：
```bash
gcc -D_POSIX_SOURCE file.c
gcc -D_GNU_SOURCE file.c
```

---

## 2.8 基本系统数据类型

APUE 和 POSIX 定义了一套**平台无关的类型**，不要直接用 `int`、`long`，而用这些：

| 类型 | 含义 | 定义在 |
|------|------|--------|
| `pid_t` | 进程 ID | `<sys/types.h>` |
| `uid_t` | 用户 ID | `<sys/types.h>` |
| `gid_t` | 组 ID | `<sys/types.h>` |
| `time_t` | 日历时间（秒） | `<time.h>` |
| `size_t` | 对象大小（无符号） | `<stddef.h>` |
| `ssize_t` | 带符号大小（可为 -1 表示出错） | `<sys/types.h>` |
| `off_t` | 文件偏移量 | `<sys/types.h>` |
| `mode_t` | 文件权限 | `<sys/types.h>` |

这些类型在 32 位和 64 位系统上实际宽度不同，但用同一个名字，代码就无需改动。

---

## 本章小结

| 概念 | 要点 |
|------|------|
| ISO C | C 语言本身的标准，规定语言和标准库 |
| POSIX | 操作系统接口标准，让程序跨 UNIX 可移植 |
| SUS | 更完整的标准，通过认证才能叫 UNIX |
| 编译时限制 | `<limits.h>` 里的常量 |
| 运行时限制 | `sysconf()`、`pathconf()` 查询 |
| 基本数据类型 | `pid_t`、`time_t`、`size_t` 等，平台无关 |

---

## 思考题

1. `int` 和 `pid_t` 都能存进程 ID，为什么 POSIX 要定义 `pid_t`？

2. 编译时限制和运行时限制各举一个实际例子，说明为什么一个能写死一个不行？

---

## 延伸问题与补充

<!-- 问答中产生的重要内容追加在此 -->
