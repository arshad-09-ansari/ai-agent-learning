from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
)

from app.day32.config import llm

messages = [
    SystemMessage(
        content="You are a senior Java backend engineer."
    ),
    HumanMessage(
        content="Explain dependency injection in Spring Boot."
    ),
]

response = llm.invoke(messages)

print("Response type:", type(response))
print("Answer:", response.content)
print("Usage:", response.usage_metadata)