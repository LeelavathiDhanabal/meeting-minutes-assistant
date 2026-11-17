from dotenv import load_dotenv
load_dotenv()
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

qa_prompt = ChatPromptTemplate.from_template(
"""
You are a meeting assistant.

Use ONLY the provided meeting data.

If the answer is not available,
respond exactly:

Information not found in meeting notes.

Meeting Data:
{meeting_data}

Question:
{question}
"""
)

qa_chain = qa_prompt | llm