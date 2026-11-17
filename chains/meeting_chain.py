from dotenv import load_dotenv
load_dotenv()
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from prompts.meeting_prompt import SYSTEM_PROMPT
from models.meeting_schema import MeetingMinutes

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

structured_llm = llm.with_structured_output(
    MeetingMinutes
)

prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("human", "{meeting_notes}")
])

chain = prompt | structured_llm