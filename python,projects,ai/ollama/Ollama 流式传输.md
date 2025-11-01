
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
