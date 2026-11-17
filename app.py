import streamlit as st

from chains.meeting_chain import chain
from chains.qa_chain import qa_chain
from chains.email_chain import email_chain


st.set_page_config(
    page_title="Meeting Minutes Assistant",
    layout="wide"
)

st.title("📋 Meeting Minutes & Action Item Assistant")


st.session_state.setdefault("meeting_data", None)
st.session_state.setdefault("chat_history", [])
st.session_state.setdefault("meeting_upload_version", 0)
st.session_state.setdefault("meeting_input_mode", "Paste text")


def add_chat_entry(question, answer, answer_type):
    st.session_state.chat_history.append(
        {
            "question": question,
            "answer": answer,
            "type": answer_type,
        }
    )


def get_structured_answer(question, meeting_data):
    """Return local, schema-backed answers for common meeting questions."""
    question_lower = question.lower()

    if "action item" in question_lower:
        return [
            {
                "Owner": item.owner,
                "Task": item.task,
                "Deadline": item.due_date,
            }
            for item in meeting_data.action_items
        ], "table"

    if "decision" in question_lower:
        return meeting_data.decisions, "list"

    if "conflict" in question_lower or "unclear" in question_lower:
        conflicts = meeting_data.unclear_commitments or [
            "No conflicting statements or unclear commitments identified."
        ]
        return conflicts, "list"

    return None


def add_quick_answer(question):
    answer = get_structured_answer(question, st.session_state.meeting_data)
    if answer is not None:
        response, response_type = answer
        add_chat_entry(question, response, response_type)


def clear_conversation():
    st.session_state.chat_history = []


if st.button("Clear Meeting notes"):
    st.session_state.meeting_notes = ""
    st.session_state.meeting_data = None
    st.session_state.chat_history = []
    st.session_state.meeting_input_mode = "Paste text"
    st.session_state.meeting_upload_version += 1


# Meeting transcript input
input_mode = st.segmented_control(
    "Transcript source",
    ["Paste text", "Upload file"],
    key="meeting_input_mode"
)

meeting_notes = ""

if input_mode == "Paste text":
    meeting_notes = st.text_area(
        "Paste Meeting Notes or Transcript",
        height=300,
        key="meeting_notes"
    )
elif input_mode == "Upload file":
    uploaded_file = st.file_uploader(
        "Upload a meeting transcript",
        type=["txt", "md"],
        key=f"meeting_transcript_{st.session_state.meeting_upload_version}"
    )

    if uploaded_file is not None:
        try:
            meeting_notes = uploaded_file.getvalue().decode("utf-8-sig")
        except UnicodeDecodeError:
            st.error("The uploaded file must be a UTF-8 encoded text file.")


# Generate Minutes
if st.button("Generate Meeting Minutes"):

    if not meeting_notes.strip():
        st.warning("Paste a transcript or upload a non-empty text file first.")
    else:
        with st.spinner("Analyzing meeting..."):

            result = chain.invoke(
                {
                    "meeting_notes": meeting_notes
                }
            )

            st.session_state.meeting_data = result

        st.success("Meeting Minutes Generated")


# Display Meeting Minutes
if st.session_state.meeting_data:

    st.subheader("📌 Summary")

    for item in st.session_state.meeting_data.summary:
        st.write(f"• {item}")

    st.subheader("✅ Decisions")

    for decision in st.session_state.meeting_data.decisions:
        st.write(f"• {decision}")

    st.subheader("📝 Action Items")

    action_table = []

    for item in st.session_state.meeting_data.action_items:
        action_table.append(
            {
                "Owner": item.owner,
                "Task": item.task,
                "Due Date": item.due_date,
                "Flag": item.flag
            }
        )

    st.table(action_table)

    st.subheader("❓ Pending Questions")

    if st.session_state.meeting_data.pending_questions:

        for question in st.session_state.meeting_data.pending_questions:
            st.write(f"• {question}")

    else:
        st.success("No pending questions found.")

    st.subheader("⚠️ Unclear Commitments")

    if st.session_state.meeting_data.unclear_commitments:

        for item in st.session_state.meeting_data.unclear_commitments:
            st.write(f"• {item}")

    else:
        st.success("No unclear commitments found.")

    st.divider()

    st.subheader("Ask Questions")

    # Quick Action Buttons
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("📋 Show Action Items"):
            add_quick_answer("Show Action Items")
            st.rerun()

    with col2:
        if st.button("✅ Show Decisions"):
            add_quick_answer("Show Decisions")
            st.rerun()

    with col3:
        if st.button("⚠️ Show Conflicts"):
            add_quick_answer("Show Conflicts")
            st.rerun()

    with col4:
        st.button(
            "Clear conversation",
            icon=":material/delete:",
            key="clear_conversation",
            width="content",
            on_click=clear_conversation
        )

    # Keep responses next to the quick actions that produced them.
    if st.session_state.chat_history:
        st.subheader("Conversation")

        for chat in reversed(st.session_state.chat_history):
            st.info(f"🙋 {chat['question']}")

            if chat["type"] == "table":
                st.table(chat["answer"])
            elif chat["type"] == "list":
                for item in chat["answer"]:
                    st.write(f"• {item}")
            else:
                st.write(chat["answer"])

            st.divider()

    st.markdown("### 💡 Suggested Questions")

    suggested_questions = [
        "Summarize the meeting in five bullet points",
        "Extract all decisions",
        "Create a table of action items, owners and deadlines",
        "Identify conflicting statements or unclear commitments",
        "Draft a follow-up email for the participants"
    ]

    for item in suggested_questions:
        st.write(f"• {item}")

    question = st.chat_input(
        "Ask a question about the meeting...",
        width="stretch"
    )

    if question:
        structured_answer = get_structured_answer(
            question,
            st.session_state.meeting_data,
        )

        if structured_answer is not None:
            answer, answer_type = structured_answer
            add_chat_entry(question, answer, answer_type)
        elif "email" in question.lower() or "follow-up" in question.lower():
            email_response = email_chain.invoke(
                {
                    "meeting_data":
                    st.session_state.meeting_data.model_dump_json()
                }
            )

            add_chat_entry(question, email_response.content, "text")
        else:
            answer = qa_chain.invoke(
                {
                    "meeting_data":
                    st.session_state.meeting_data.model_dump_json(),

                    "question":
                    question
                }
            )

            add_chat_entry(question, answer.content, "text")

        st.rerun()