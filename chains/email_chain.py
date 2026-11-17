from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

email_prompt = ChatPromptTemplate.from_template(
"""
You are a professional project coordinator.

Create a follow-up email from the meeting details below.

Meeting Data:
{meeting_data}

Include:

1. Thank participants
2. Meeting summary
3. Decisions
4. Action items
5. Pending questions
6. Next steps

Generate a professional email.
"""
)

email_chain = email_prompt | llm