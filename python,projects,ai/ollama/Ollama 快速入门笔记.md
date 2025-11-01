
### 第一步：下载安装
访问 [ollama download](https://ollama.com/download) 下载对应操作系统的版本（支持 macOS、Windows 和 Linux）

### 第二步：运行模型

#### 方法一：命令行界面 (CLI)
```bash
ollama run gemma3
```

#### 方法二：cURL
1. 先下载模型：
```bash
ollama pull gemma3
```

2. 与模型对话：
```bash
curl http://localhost:11434/api/chat -d '{
  "model": "gemma3",
  "messages": [{
    "role": "user",
    "content": "Hello there!"
  }],
  "stream": false
}'
```

#### 方法三：Python
1. 下载模型：
```bash
ollama pull gemma3
```

2. 安装 Python 库：
```bash
pip install ollama
pip install 'httpx[socks]'
```

3. 与模型对话：
```python
from ollama import chat
from ollama import ChatResponse

response: ChatResponse = chat(model='gemma3', messages=[
  {
    'role': 'user',
    'content': 'Why is the sky blue?',
  },
])
print(response['message']['content'])
# 或者直接访问响应对象的字段
print(response.message.content)
```

#### 方法四：JavaScript
1. 下载模型：
```bash
ollama pull gemma3
```

2. 安装 JavaScript 库：
```bash
npm i ollama
```
3. 初始化项目

```bash
npm init -y
```
4. 编辑`package.json`

```json
{
  "type": "module"
}
```

5. 与模型对话：
```javascript
import ollama from 'ollama'

const response = await ollama.chat({
  model: 'gemma3',
  messages: [{ role: 'user', content: 'Why is the sky blue?' }],
})
console.log(response.message.content)
```

6. 运行对话
```bash
node chat.js
```

### 可用模型
查看所有可用模型请访问：[https://ollama.com/models](https://ollama.com/models)