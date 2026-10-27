from langchain_core.prompts import ChatPromptTemplate

story_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        You are an experienced Agile Scrum Master.
        Analyze user stories clearly.
        Do not invent missing requirements.
        """
    ),
    (
        "human",
        """
        Analyze this user story:

        Title: {title}
        Description: {description}

        Explain:
        1. Business goal
        2. Missing requirements
        3. Implementation approach
        4. Estimated story points
        """
    )
])