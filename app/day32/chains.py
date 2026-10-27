from langchain_core.output_parsers import StrOutputParser

from app.day32.config import llm
from app.day32.prompts import story_prompt

story_chain = story_prompt | llm | StrOutputParser()


def analyze_story(title: str, description: str) -> str:
    return story_chain.invoke({
        "title": title,
        "description": description,
    })