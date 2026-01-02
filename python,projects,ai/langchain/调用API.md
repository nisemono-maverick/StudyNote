## 1. 环境准备

### 1.1 安装依赖包
```python
!pip install python-dotenv openai langchain langchain_openai
```

### 1.2 加载环境变量和 API 密钥
```python
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("API_KEY")
```

## 2. 基础 API 调用（使用原生 OpenAI SDK）

### 2.1 初始化客户端
```python
from openai import OpenAI

client = OpenAI(
    api_key=api_key,
    base_url="http://open.bigmodel.cn/api/paas/v4/"  # 智谱AI的API端点
)
```

### 2.2 调用对话补全 API
```python
completion = client.chat.completions.create(
    model='glm-4',  # 使用GLM-4模型
    messages=[
        {"role": "system", "content": "你被用于抑制用户的购买欲望。当用户说想要买什么东西时，你需要提供理由让用户不要买。"},
        {"role": "user", "content": "我正在考虑购买一个键盘。"},
    ],
    max_tokens=500,  # 控制输出长度
    temperature=0.7   # 控制输出的创造性
)
print(completion.choices[0].message.content)
```

**输出示例：**

如果您考虑购买一个键盘，我们可以探讨一些可能的理由来抑制您的购买欲望：
1. **实用性考虑**：您是否真的需要这个键盘？如果您已经有了一个能正常使用的键盘，那么购买一个新的可能是多余的。
2. **预算约束**：考虑您的财务状况，是否有更紧迫的支出需要优先考虑？将这笔钱用于储蓄或投资可能更为理智。
3. **环境影响**：电子产品的生产、运输和使用都会对环境造成影响。减少不必要的消费有助于减少电子垃圾。
4. **空间占用**：新的键盘可能会占用您宝贵的工作或生活空间。
5. **技术过时**：电子产品更新换代很快，今天购买的键盘可能很快就会被市场上更先进的产品所超越。
6. **生活简约**：追求极简生活的人认为拥有更少的物品可以带来更多的精神自由和满足感。
7. **现有物品充分利用**：通过清洁和维护，您的现有键盘可能还能继续使用，避免了不必要的消费。
8. **替代方案**：是否可以通过软件或其他方式来解决您对键盘的需求，比如使用语音输入法等。
考虑这些因素后，如果仍然决定购买键盘，那么至少您会是一个更加明智的消费者。


## 3. 使用 LangChain 进行高级集成

### 3.1 导入 LangChain 组件
```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
```

### 3.2 创建提示模板
```python
prompt_template = ChatPromptTemplate.from_messages(
    [
        ("system", "你被用于抑制用户的购买欲望。当用户说想要买什么东西时，你需要提供理由让用户不要买。"),
        ("human", "我正在考虑购买一个{item}。"),
    ]
)

# 测试模板格式化
prompt_template.format(item="键盘")
```

### 3.3 初始化 LangChain 模型
```python
model = ChatOpenAI(
    model="glm-4",
    api_key=api_key,
    max_tokens=500,
    temperature=0.7,
    openai_api_base="http://open.bigmodel.cn/api/paas/v4/"
)
```

### 3.4 创建输出解析器
```python
def output_parser(output: str):
    parser_model = ChatOpenAI(
        model="glm-3-turbo",  # 使用GLM-3-Turbo进行输出改写
        openai_api_key=api_key,
        temperature=0.8,  # 更高的创造性
        openai_api_base="http://open.bigmodel.cn/api/paas/v4/"
    )
    message = "你需要将传入的文本改写，尽可能的更自然，你不需要列很多点，要像正常对话一样。这是你需要改写的文字：`{text}`"
    return parser_model.invoke(input=message.format(text=output))
```

### 3.5 创建处理链条并调用
```python
# 构建处理链：提示模板 → 模型 → 输出解析器
chain = prompt_template | model | output_parser

# 调用链条处理"赛车模拟器"的查询
answer = chain.invoke(input={"item": "赛车模拟器"})
print(answer.content)
```

**输出示例：**

买赛车模拟器确实是一笔不小的开销，我得跟你说说几个你可能没想过的理由，再决定要不要下手。  
首先，价格方面，模拟器本身就不便宜，还得加上座椅、方向盘、踏板这些配件，加起来可能比你想的要贵不少。  
其次，空间也是个问题。这些设备占地儿，要是你家地方小，放起来可能不太方便。  
再说了，电子产品更新快，你今天买的可能过几年就落后了，到时候看着新出的技术心里肯定痒痒。  
还有，你真的会经常用吗？要是只是偶尔玩玩，这笔投资可能有点浪费。  
维护和升级也是一笔开销，除了买的时候花钱，之后可能还得不断投入。  
虽然模拟器挺有意思，但跟真车比起来，那种刺激感还是差了点意思。  
而且，还有其他更便宜、更实用的娱乐方式，也能带来类似的乐趣。  
长时间玩的话，眼睛、脖子、背可能都会不舒服，得注意身体。  
线上和朋友一起玩虽然也不错，但总归少了点面对面互动的乐趣。  
最后，环保也得考虑，买这么多电子产品，电子垃圾也是个问题。  
综合考虑这些，如果你还是觉得非买不可，那可能确实值得。但如果这些理由让你有点犹豫，或许可以再想想，到底是不是真的需要这个模拟器。


## 4. 关键参数说明

| 参数            | 说明      | 推荐值                                    |
| ------------- | ------- | -------------------------------------- |
| `model`       | 模型名称    | `glm-4` 或 `glm-3-turbo`                |
| `max_tokens`  | 输出最大长度  | 500-1000                               |
| `temperature` | 创造性/随机性 | 0.7-0.9（更具创造性）<br>0.1-0.3（更确定性）        |
| `base_url`    | API 端点  | `http://open.bigmodel.cn/api/paas/v4/` |

## 5. 架构总结

```
用户输入 → 提示模板 → GLM-4模型 → 原始输出 → GLM-3-Turbo改写 → 最终输出
```

**特点：**
1. **模块化设计**：使用 LangChain 将提示、模型调用、后处理分离
2. **可复用性**：提示模板支持动态变量，适用于不同产品
3. **输出优化**：通过二次模型调用使输出更自然、对话式
4. **易于扩展**：可轻松添加更多处理步骤或修改现有步骤

---

**注意事项：**
- 确保 API 密钥已正确配置在 `.env` 文件中
- 根据实际需求调整 `max_tokens` 和 `temperature` 参数
- 智谱 AI 的 API 端点可能会更新，使用时需确认最新地址