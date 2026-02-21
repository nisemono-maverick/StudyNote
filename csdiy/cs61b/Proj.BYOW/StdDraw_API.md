# StdDraw API 文档

> 来源：[Princeton CS - StdDraw](https://introcs.cs.princeton.edu/java/stdlib/javadoc/StdDraw.html)
> 
> `StdDraw` 类提供了创建绘图程序的静态方法，支持点、线、几何图形、文本、颜色、图片、动画以及键盘鼠标交互。

---

## 目录

1. [快速开始](#快速开始)
2. [基础图形绘制](#基础图形绘制)
3. [填充图形](#填充图形)
4. [圆弧与多边形](#圆弧与多边形)
5. [画笔设置](#画笔设置)
6. [画布设置](#画布设置)
7. [文本与图片](#文本与图片)
8. [动画与双缓冲](#动画与双缓冲)
9. [键盘与鼠标输入](#键盘与鼠标输入)
10. [文件保存](#文件保存)
11. [预定义颜色常量](#预定义颜色常量)
12. [完整方法列表](#完整方法列表)

---

## 快速开始

### 环境配置
- 确保 `StdDraw.class` 在 Java classpath 中
- 或下载 [stdlib.jar](https://introcs.cs.princeton.edu/java/stdlib/stdlib.jar) 添加到 classpath
- 或下载 [StdDraw.java](https://introcs.cs.princeton.edu/java/stdlib/StdDraw.java) 放在工作目录

### Hello World 示例

```java
public class TestStdDraw {
    public static void main(String[] args) {
        // 设置画笔粗细
        StdDraw.setPenRadius(0.05);
        
        // 设置画笔颜色并画点
        StdDraw.setPenColor(StdDraw.BLUE);
        StdDraw.point(0.5, 0.5);
        
        // 画线
        StdDraw.setPenColor(StdDraw.MAGENTA);
        StdDraw.line(0.2, 0.2, 0.8, 0.2);
    }
}
```

---

## 基础图形绘制

### 点与线

| 方法 | 描述 |
|------|------|
| `point(double x, double y)` | 在 (x, y) 位置画点 |
| `line(double x1, double y1, double x2, double y2)` | 画线段，从 (x1, y1) 到 (x2, y2) |

> **注意**: 默认坐标系中 x 和 y 必须在 0 到 1 之间，否则图形不可见。

### 圆形与椭圆

| 方法                                                                        | 描述                                               |
| ------------------------------------------------------------------------- | ------------------------------------------------ |
| `circle(double x, double y, double radius)`                               | 画圆，中心 (x, y)，半径 radius                           |
| `ellipse(double x, double y, double semiMajorAxis, double semiMinorAxis)` | 画椭圆，中心 (x, y)，长半轴 semiMajorAxis短半轴 semiMinorAxis |
| `square(double x, double y, double halfLength)`                           | 画正方形，中心 (x, y)，半边长 halfLength                    |
| `rectangle(double x, double y, double halfWidth, double halfHeight)`      | 画矩形                                              |

---

## 填充图形

| 方法 | 描述 |
|------|------|
| `filledCircle(double x, double y, double radius)` | 填充圆 |
| `filledEllipse(double x, double y, double semiMajorAxis, double semiMinorAxis)` | 填充椭圆 |
| `filledSquare(double x, double y, double halfLength)` | 填充正方形 |
| `filledRectangle(double x, double y, double halfWidth, double halfHeight)` | 填充矩形 |

---

## 圆弧与多边形

### 圆弧

```java
arc(double x, double y, double radius, double angle1, double angle2)
```

- 绘制从 angle1 到 angle2 的圆弧（角度制，逆时针从 x 轴正方向开始）
- 例如：`arc(0.0, 0.0, 1.0, 0, 90)` 绘制从 3 点钟到 12 点钟的 1/4 圆弧

### 多边形

| 方法 | 描述 |
|------|------|
| `polygon(double[] x, double[] y)` | 画多边形轮廓 |
| `filledPolygon(double[] x, double[] y)` | 画填充多边形 |

**示例**: 画填充菱形
```java
double[] x = { 0.1, 0.2, 0.3, 0.2 };
double[] y = { 0.2, 0.3, 0.2, 0.1 };
StdDraw.filledPolygon(x, y);
```

---

## 画笔设置

### 画笔粗细

```java
setPenRadius(double radius)
```

- 默认半径: `0.002`（约画布宽度的 1/500）
- 线条厚度 = `2 * radius`
- 设置为 `0.0` 可获得最小像素点

**示例**: 
```java
StdDraw.setPenRadius(0.01);  // 5倍粗细
```

### 画笔颜色

| 方法 | 描述 |
|------|------|
| `setPenColor(Color color)` | 设置画笔颜色（Color 类型） |
| `setPenColor(int red, int green, int blue)` | 设置 RGB 颜色（0-255） |
| `setPenColor()` | 重置为默认黑色 |

**获取当前颜色**:
```java
Color c = StdDraw.getPenColor();
Color bg = StdDraw.getBackgroundColor();
```

---

## 画布设置

### 窗口标题

```java
setTitle(String windowTitle)  // 默认: "Standard Draw"
```

### 画布大小

```java
setCanvasSize(int width, int height)  // 默认: 512×512 像素
```

> 通常在程序开头调用一次，会清空当前画布。

### 坐标系统

| 方法 | 描述 |
|------|------|
| `setXscale(double xmin, double xmax)` | 设置 X 轴范围 |
| `setYscale(double ymin, double ymax)` | 设置 Y 轴范围 |
| `setScale(double min, double max)` | 同时设置 X 和 Y 轴范围 |

**示例**:
```java
// 保留边距
StdDraw.setScale(-0.05, 1.05);

// 自定义坐标系
StdDraw.setXscale(0, 100);
StdDraw.setYscale(0, 100);
```

> 注意：如果 X 和 Y 比例不同，圆形会变椭圆，正方形会变矩形。

---

## 文本与图片

### 文本

| 方法 | 描述 |
|------|------|
| `text(double x, double y, String text)` | 在 (x, y) 居中显示文本 |
| `text(double x, double y, String text, double degrees)` | 旋转文本 |
| `textLeft(double x, double y, String text)` | 左对齐文本 |
| `textRight(double x, double y, String text)` | 右对齐文本 |

### 字体设置

```java
setFont(Font font)  // 默认: Sans Serif, 16pt
setFont()           // 重置为默认字体
```

**示例**:
```java
import java.awt.Font;

Font font = new Font("Arial", Font.BOLD, 60);
StdDraw.setFont(font);
StdDraw.text(0.5, 0.5, "Hello, World");
```

### 图片

| 方法 | 描述 |
|------|------|
| `picture(double x, double y, String filename)` | 显示图片（居中） |
| `picture(double x, double y, String filename, double degrees)` | 旋转图片 |
| `picture(double x, double y, String filename, double w, double h)` | 缩放图片 |
| `picture(double x, double y, String filename, double w, double h, double degrees)` | 旋转+缩放 |

**支持的格式**: JPEG, PNG, GIF, TIFF, BMP

> 图片会被缓存，重复绘制同一图片不会降低性能。

---

## 动画与双缓冲

### 双缓冲方法

| 方法 | 描述 |
|------|------|
| `enableDoubleBuffering()` | 启用双缓冲（动画必备） |
| `disableDoubleBuffering()` | 禁用双缓冲（默认） |
| `show()` | 将离屏缓冲复制到屏幕 |
| `pause(int t)` | 暂停 t 毫秒 |

### 动画循环模式

```java
// 1. 启用双缓冲
StdDraw.enableDoubleBuffering();

// 2. 动画循环
for (double t = 0.0; true; t += 0.02) {
    // 清空画布
    StdDraw.clear();
    
    // 绘制对象
    double x = Math.sin(t);
    double y = Math.cos(t);
    StdDraw.filledCircle(x, y, 0.1);
    
    // 显示并暂停
    StdDraw.show();
    StdDraw.pause(20);  // 20ms = 50 FPS
}
```

### 清屏

| 方法 | 描述 |
|------|------|
| `clear()` | 清屏为白色背景 |
| `clear(Color color)` | 清屏为指定颜色 |

```java
StdDraw.clear(StdDraw.LIGHT_GRAY);      // 灰色背景
StdDraw.clear(StdDraw.TRANSPARENT);     // 透明背景
```

---

## 键盘与鼠标输入

### 鼠标

| 方法 | 返回值 | 描述 |
|------|--------|------|
| `isMousePressed()` | `boolean` | 鼠标是否被按下 |
| `mouseX()` | `double` | 鼠标 X 坐标 |
| `mouseY()` | `double` | 鼠标 Y 坐标 |

**示例**:
```java
while (true) {
    if (StdDraw.isMousePressed()) {
        double x = StdDraw.mouseX();
        double y = StdDraw.mouseY();
        System.out.println("Mouse at: " + x + ", " + y);
    }
    StdDraw.pause(50);
}
```

### 键盘

| 方法 | 返回值 | 描述 |
|------|--------|------|
| `hasNextKeyTyped()` | `boolean` | 是否有未处理的按键 |
| `nextKeyTyped()` | `char` | 获取下一个按键字符 |
| `isKeyPressed(int keycode)` | `boolean` | 检查特定键是否被按下 |

**示例**:
```java
// 处理字符输入
if (StdDraw.hasNextKeyTyped()) {
    char c = StdDraw.nextKeyTyped();
    System.out.println("Pressed: " + c);
}

// 检查功能键 (需要 import java.awt.event.KeyEvent)
if (StdDraw.isKeyPressed(KeyEvent.VK_LEFT)) {
    // 左箭头被按下
}
```

> `KeyEvent` 定义在 `java.awt.event` 包中，包含 `VK_UP`, `VK_DOWN`, `VK_LEFT`, `VK_RIGHT`, `VK_SPACE` 等常量。

---

## 文件保存

```java
save(String filename)
```

- **支持格式**: `.jpg`, `.png`, `.gif`, `.bmp`, `.tif`
- **推荐**: 几何图形用 PNG，含照片用 JPEG
- JPEG 不支持透明背景

---

## 预定义颜色常量

| 常量 | RGB 值 | 颜色 |
|------|--------|------|
| `BLACK` | (0, 0, 0) | 黑色 |
| `WHITE` | (255, 255, 255) | 白色 |
| `RED` | (255, 0, 0) | 红色 |
| `GREEN` | (0, 128, 0) | 绿色 |
| `BLUE` | (0, 0, 255) | 蓝色 |
| `CYAN` / `AQUA` | (0, 255, 255) | 青色 |
| `MAGENTA` / `FUSCIA` | (255, 0, 255) | 品红 |
| `YELLOW` | (255, 255, 0) | 黄色 |
| `LIME` | (0, 255, 0) | 亮绿 |
| `MAROON` | (128, 0, 0) | 栗色 |
| `NAVY` | (0, 0, 128) | 海军蓝 |
| `OLIVE` | (128, 128, 0) | 橄榄绿 |
| `GRAY` | (128, 128, 128) | 灰色 |
| `DARK_GRAY` | (64, 64, 64) | 深灰 |
| `LIGHT_GRAY` | (192, 192, 192) | 浅灰 |
| `BOOK_BLUE` | - | 教材蓝色 |
| `BOOK_LIGHT_BLUE` | - | 教材浅蓝色 |
| `BOOK_RED` | - | 教材红色 |

---

## 完整方法列表

### 绘图方法

| 方法 | 参数说明 |
|------|----------|
| `point(double x, double y)` | 画点 |
| `line(double x0, double y0, double x1, double y1)` | 画线 |
| `circle(double x, double y, double radius)` | 画圆 |
| `filledCircle(double x, double y, double radius)` | 填充圆 |
| `ellipse(double x, double y, double semiMajorAxis, double semiMinorAxis)` | 画椭圆 |
| `filledEllipse(double x, double y, double semiMajorAxis, double semiMinorAxis)` | 填充椭圆 |
| `arc(double x, double y, double radius, double angle1, double angle2)` | 画圆弧 |
| `square(double x, double y, double halfLength)` | 画正方形 |
| `filledSquare(double x, double y, double halfLength)` | 填充正方形 |
| `rectangle(double x, double y, double halfWidth, double halfHeight)` | 画矩形 |
| `filledRectangle(double x, double y, double halfWidth, double halfHeight)` | 填充矩形 |
| `polygon(double[] x, double[] y)` | 画多边形 |
| `filledPolygon(double[] x, double[] y)` | 填充多边形 |

### 文本与图片

| 方法 | 参数说明 |
|------|----------|
| `text(double x, double y, String text)` | 居中文字 |
| `text(double x, double y, String text, double degrees)` | 旋转文字 |
| `textLeft(double x, double y, String text)` | 左对齐文字 |
| `textRight(double x, double y, String text)` | 右对齐文字 |
| `picture(double x, double y, String filename)` | 显示图片 |
| `picture(double x, double y, String filename, double degrees)` | 旋转图片 |
| `picture(double x, double y, String filename, double scaledWidth, double scaledHeight)` | 缩放图片 |
| `picture(double x, double y, String filename, double scaledWidth, double scaledHeight, double degrees)` | 旋转+缩放 |

### 设置方法

| 方法 | 参数说明 |
|------|----------|
| `setPenRadius(double radius)` | 设置画笔半径 |
| `setPenColor(Color color)` | 设置画笔颜色 |
| `setPenColor(int red, int green, int blue)` | 设置 RGB 颜色 |
| `setPenColor()` | 重置画笔颜色 |
| `setFont(Font font)` | 设置字体 |
| `setFont()` | 重置字体 |
| `setTitle(String title)` | 设置窗口标题 |
| `setCanvasSize(int width, int height)` | 设置画布大小 |
| `setXscale(double xmin, double xmax)` | 设置 X 轴范围 |
| `setYscale(double ymin, double ymax)` | 设置 Y 轴范围 |
| `setScale(double min, double max)` | 设置坐标范围 |

### 获取方法

| 方法 | 返回值 |
|------|--------|
| `getPenColor()` | `Color` - 当前画笔颜色 |
| `getBackgroundColor()` | `Color` - 当前背景颜色 |
| `getPenRadius()` | `double` - 当前画笔半径 |
| `getFont()` | `Font` - 当前字体 |

### 动画与显示

| 方法 | 参数说明 |
|------|----------|
| `clear()` | 清屏（白色） |
| `clear(Color color)` | 清屏（指定颜色） |
| `enableDoubleBuffering()` | 启用双缓冲 |
| `disableDoubleBuffering()` | 禁用双缓冲 |
| `show()` | 显示离屏缓冲 |
| `pause(int t)` | 暂停 t 毫秒 |
| `save(String filename)` | 保存到文件 |

### 输入方法

| 方法                          | 返回值       | 说明      |
| --------------------------- | --------- | ------- |
| `isMousePressed()`          | `boolean` | 鼠标是否按下  |
| `mouseX()`                  | `double`  | 鼠标 X 坐标 |
| `mouseY()`                  | `double`  | 鼠标 Y 坐标 |
| `hasNextKeyTyped()`         | `boolean` | 是否有按键   |
| `nextKeyTyped()`            | `char`    | 下一个按键   |
| `isKeyPressed(int keycode)` | `boolean` | 特定键是否按下 |

---

## 异常与注意事项

1. **参数检查**: 所有方法会对 `null`、NaN、Infinity 进行检查，不符合会抛出 `IllegalArgumentException`
2. **数组长度**: `polygon` 方法要求 x[] 和 y[] 长度相同
3. **负值检查**: 半径、半长宽等参数不能为负
4. **越界绘制**: 绘制超出画布的对象是允许的，但只有画布内的部分可见
5. **浮点问题**: 坐标值过大（如 10^308）可能导致显示问题

---

## 性能优化建议

1. **双缓冲**: 绘制大量静态对象时，先 `enableDoubleBuffering()`，绘制完成后调用 `show()`
2. **动画帧率**: 每帧只调用一次 `show()`，不要在每个对象绘制后都调用
3. **图片缓存**: 重复绘制相同图片会自动缓存，无需担心性能

---

## 参考

- 教材: *Computer Science: An Interdisciplinary Approach* - Robert Sedgewick & Kevin Wayne
- 章节: Section 1.5
