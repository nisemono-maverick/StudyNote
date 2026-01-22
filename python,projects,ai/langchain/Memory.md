This notebook demonstrates multiple methods for adding memory to a chatbot using **LangChain**, enabling the model to remember previous interactions in a conversation.

## 1. **Setup & Environment**
Load environment variables and configure the language model.

```python
from dotenv import load_dotenv
import os
load_dotenv()
api_key = os.getenv("API_KEY")
```

The model used is **ChatOpenAI** (GLM-4) with a custom API base for increased token limits and controlled randomness.

```python
model = ChatOpenAI(
    model="glm-4",
    api_key=api_key,
    max_tokens=500,
    temperature=0.7,
    openai_api_base="http://open.bigmodel.cn/api/paas/v4/"
)
```

---

## 2. **Basic Memory Using `ChatPromptTemplate`**
### 2.1 Without Memory
A simple prompt template with no memory:

```python
prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You are a chatbot."),
    ("human", "{new_message}")
])
```

### 2.2 With Memory via `MessagesPlaceholder`
Add conversation history using `MessagesPlaceholder`:

```python
prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You are a chatbot."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{new_message}")
])
```

The history is passed as a list of messages with `role` and `content`.

---

## 3. **Chat Loop with Manual Memory Management**
A simple function to maintain conversation history:

```python
history = []

def chat_with_memory(new_message):
    global history
    response = chain.invoke({
        "history": history,
        "new_message": new_message
    })
    history.append({"role": "human", "content": new_message})
    history.append({"role": "ai", "content": response.content})
    return response.content
```

This manually appends each exchange to the `history` list.

---

## 4. **Using LangChain’s Built-in Memory Module**
### 4.1 `ChatMessageHistory`
A more structured way to store messages:

```python
from langchain_community.chat_message_histories import ChatMessageHistory
chat_history = ChatMessageHistory()
chat_history.add_user_message("Hello! I'm maverick.")
chat_history.add_ai_message("Hello maverick! How can I help you today?")
```

### 4.2 `RunnableWithMessageHistory`
LangChain provides a runnable wrapper to automatically manage history:

```python
from langchain_core.runnables.history import RunnableWithMessageHistory

chat_with_memory = RunnableWithMessageHistory(
    runnable=chain,
    get_session_history=lambda config: chat_history,
    input_messages_key="new_message",
    history_messages_key="history"
)
```

This simplifies memory handling by automatically injecting history into prompts.

---

## 5. **Handling Long Conversations**
### 5.1 Trimming Messages
To prevent token overflow, we can keep only the most recent messages:

```python
def trim_messages(chain_input):
    stored_messages = chat_history.messages
    if len(stored_messages) > 2:
        chat_history.clear()
        for message in stored_messages[-2:]:
            chat_history.add_message(message)
    return chain_input
```

### 5.2 Summarization-Based Memory
When the conversation grows, we can summarize older messages and store the summary:

```python
def summarize_messages(chain_input):
    stored_messages = chat_history.messages
    if len(stored_messages) >= 6:
        summary_prompt = ChatPromptTemplate.from_messages([
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "Summarize the conversation briefly")
        ])
        summarize_chain = summary_prompt | model
        summary = summarize_chain.invoke({"chat_history": stored_messages})
        chat_history.clear()
        chat_history.add_message(summary)
    return chain_input
```

This approach retains context without storing every message.
