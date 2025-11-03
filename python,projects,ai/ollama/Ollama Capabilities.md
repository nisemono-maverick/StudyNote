## Ollama 流式传输
### 概述

1. 流式传输允许您在模型生成文本时实时渲染输出内容。
2. 在REST API中，流式传输功能默认开启，但在SDK中默认处于关闭状态。
3. 若要在SDK中启用流式传输，只需将`stream`参数设置为`True`。

### 核心概念解析

1. 对话交互：可流式接收部分助理消息。每个数据块均包含`content`字段，使您能够实时呈现动态生成的消息。
2. 思考过程：具备思考能力的模型会在每个数据块中同时传递`thinking`字段与常规内容。通过检测流数据中的该字段，可在最终答案生成前展示或隐藏推理轨迹。
3. 工具调用：实时观察每个数据块中的`tool_calls`字段，执行请求的工具操作，并将工具执行结果追加回对话流程。

## 流数据块处理要点

必须持续累积部分字段以维护对话记录的完整性。这一点在工具调用场景中尤为重要——模型的思考过程、触发的工具调用及执行结果都必须在下一次请求中完整回传给模型。
```python
from ollama import chat

stream = chat(
	model = 'gwen3',
	messages = [{'role': 'user', 'content': '天为什么是蓝的?'}],
	stream = True,
	think = True
)

in_thinking = False
content = ''
thinking = ''

for chunk in stream:
	if chunk.message.thinking:
		if not in_thinking:
			in_thinking = True
			print('Thinking:\n', end='', flush=True)
		print(chunk.message.thinking, end='', flush=True)
		# accumulate the partial thinking
		thinking += chunk.message.thinking
	elif chunk.message.content:
		if in_thinking:
			in_thinking = False
			print('\n\nAnswer:\n', end='', flush=True)
		print(chunk.message.content, end='', flush=True)
		# accumulate the partial content
		content += chunk.message.content
	# append the accumulated fields to the messages for the next request
	new_messages = [{ 'role': 'assistant', 'thinking': thinking, 'content': content }]
```

## Ollama 深度思考

### 概述
支持思考能力的模型会输出 `thinking` 字段，将推理过程与最终答案分离。

**主要用途**：
- 审核模型推理步骤
- 在UI中展示模型"思考"过程
- 仅显示最终答案（隐藏推理过程）

### 支持的模型
- **Qwen 3**
- **GPT-OSS**（使用 `low`/`medium`/`high` 级别，无法完全禁用推理过程）
- **DeepSeek-v3.1**
- **DeepSeek R1**
- 更多模型可在 [thinking models](https://ollama.com/search?c=thinking) 中查找

### API 调用启用思考

### 基本配置
- 大多数模型：设置 `think: true` 或 `think: false`
- GPT-OSS：必须使用 `"low"`、`"medium"`、`"high"` 级别

### 响应字段
- **推理过程**：`message.thinking`（chat）或 `thinking`（generate）
- **最终答案**：`message.content`（chat）或 `response`（generate）

### 示例代码
#### cURL
```bash
curl http://localhost:11434/api/chat -d '{
  "model": "gpt-oss",
  "messages": [{
    "role": "user",
    "content": "How many letter r are in strawberry?"
  }],
  "think": true,
  "stream": false
}'
```

#### python
```python
from ollama import chat

response = chat(
  model='gpt-oss',
  messages=[{'role': 'user', 'content': '问题内容'}],
  think=True,
  stream=False,
)

print('思考过程:', response.message.thinking)
print('最终答案:', response.message.content)
```

### 流式传输推理过程

#### 处理逻辑
- 推理令牌在答案令牌之前交错传输
- 检测到第一个 `thinking` chunk 时开始渲染"思考"部分
- 当 `message.content` 到达时切换到最终回复

#### Python 示例
```python
stream = chat(model='qwen3', messages=[...], think=True, stream=True)

in_thinking = False
for chunk in stream:
    if chunk.message.thinking and not in_thinking:
        in_thinking = True
        print('思考过程:\n', end='')
    
    if chunk.message.thinking:
        print(chunk.message.thinking, end='')
    elif chunk.message.content:
        if in_thinking:
            print('\n\n答案:\n', end='')
            in_thinking = False
        print(chunk.message.content, end='')
```

### CLI 快速参考

#### 基本命令
```bash
# 启用思考
ollama run deepseek-r1 --think "你的问题"

# 禁用思考
ollama run deepseek-r1 --think=false "你的问题"

# 隐藏思考过程（仍使用思考模型）
ollama run deepseek-r1 --hidethinking "你的问题"

# GPT-OSS 特殊语法
ollama run gpt-oss --think=low "你的问题"
```

#### 交互式会话
- 启用思考：`/set think`
- 禁用思考：`/set nothink`

### 注意事项
- 对于支持的模型，思考功能在 CLI 和 API 中默认启用
- GPT-OSS 不接受布尔值，必须使用思考级别
- 流式传输时需要正确处理思考过程和最终答案的切换
