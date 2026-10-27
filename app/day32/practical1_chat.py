from langchain_core.messages import SystemMessage, HumanMessage

from app.day32.config import llm


messages = [
    SystemMessage(
        content="You are a senior Java backend engineer. "
                "Explain concepts in simple English."
    ),
    HumanMessage(
        content="Explain dependency injection in Spring Boot."
    ),
]

response = llm.invoke(messages)

print("Response class:", type(response).__name__)
print("\nAI response:")
print(response.content)

print("\nToken usage:")
print(response.usage_metadata)