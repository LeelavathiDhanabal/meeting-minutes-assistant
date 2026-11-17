# Meeting Minutes Assistant

A Streamlit demo that turns meeting notes or a transcript into structured minutes, action items, decisions, pending questions, and unclear commitments. Users can also ask questions about the meeting or draft a follow-up email.

## Application flow

```text
Paste meeting notes or upload a UTF-8 .txt/.md file
                         |
                         v
          Generate Meeting Minutes (gpt-4o-mini)
                         |
                         v
       Structured minutes validated by Pydantic
                         |
            +------------+------------+
            |                         |
            v                         v
     Quick action controls      Ask a question
     - Action items             - Structured answers use
     - Decisions                  generated meeting data
     - Conflicts                - Other questions use Q&A
                                  - Email requests draft an email
```

Generated minutes and the conversation are kept in the current Streamlit session. **Clear conversation** removes only the chat history. **Clear Meeting notes** also clears the transcript, generated minutes, and chat.

## Requirements

- Windows, macOS, or Linux
- Python 3.11 recommended
- An OpenAI API key with access to `gpt-4o-mini`

## Installation (Windows PowerShell)

Run these commands from the project directory:

1. Create and activate a virtual environment:

   ```powershell
   py -3.11 -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   If PowerShell blocks activation, use the environment's Python directly in the commands below (for example, `.\.venv\Scripts\python.exe`).

2. Install the application dependencies:

   ```powershell
   python -m pip install --upgrade pip
   python -m pip install -r requirements.txt
   ```

3. Create a local environment file and add your API key:

   ```powershell
   Copy-Item .env.example .env
   notepad .env
   ```

   Replace the placeholder with your key:

   ```text
   OPENAI_API_KEY=your-real-openai-api-key
   ```

   Keep `.env` private. It is excluded from Git by `.gitignore`; never paste the real key into source code or commit it.

## Run the application

From the activated environment and project directory:

```powershell
streamlit run app.py
```

Open the local URL printed by Streamlit, usually <http://localhost:8501>.

## Demo walkthrough

1. Select **Paste text** and enter notes, or select **Upload file** and choose a UTF-8 `.txt` or `.md` transcript. The included sample is `sample_data/meeting.txt`.
2. Select **Generate Meeting Minutes** and wait for the analysis to finish.
3. Review the summary, decisions, action items, pending questions, and unclear commitments.
4. Use **Show Action Items**, **Show Decisions**, or **Show Conflicts** for quick results. Their answers appear in the conversation area.
5. Ask a free-form question using the chat input at the bottom of the app. Try a question from `meeting_transcripts/SampleQuestions.txt`.
6. Select **Clear conversation** to reset only the Q&A history, or **Clear Meeting notes** to start a new meeting.

## Optional evaluation dependency

DeepEval is not required to run the Streamlit app. Install it only when working with local evaluation tooling:

```powershell
python -m pip install -r requirements-evaluation.txt
```

## Project layout

```text
app.py                    Streamlit UI and request routing
chains/                   Meeting minutes, Q&A, and email model chains
models/                   Pydantic schema for structured meeting minutes
prompts/                  Meeting analysis instructions
sample_data/              Example transcript for a demo
meeting_transcripts/      Additional sample transcripts and questions
requirements.txt          Runtime dependencies
requirements-evaluation.txt  Optional DeepEval dependency
```
