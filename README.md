# AI Quiz Taker System

A Streamlit app that turns a PDF into a topic-based quiz, collects student answers, and evaluates them with a mix of retrieval, embeddings, and LLM feedback.

## What It Does

- Upload a PDF and extract its text.
- Build a local Chroma vector store from the document.
- Generate quiz questions for a topic you choose.
- Support configurable counts for:
  - Multiple-choice questions
  - Short-answer questions
  - Long-answer questions
- Evaluate answers:
  - MCQs are graded by exact option match.
  - Short and long answers are graded with embedding similarity plus LLM-generated feedback.

## How It Works

1. The uploaded PDF is split into chunks with `PyPDFLoader` and `RecursiveCharacterTextSplitter`.
2. Chunks are embedded with `sentence-transformers/all-MiniLM-L6-v2`.
3. A Chroma vector store is created in `vector_store/current`.
4. When you enter a topic, the app retrieves relevant document context.
5. Groq (`llama-3.1-8b-instant`) generates quiz questions and model answers in JSON.
6. Student answers are evaluated and shown with scores, model answers, and feedback.

## Tech Stack

- `Streamlit` for the UI
- `LangChain` for orchestration
- `Groq` for question generation and feedback
- `HuggingFace sentence-transformers` for embeddings
- `Chroma` for local vector storage

## Project Structure

```text
.
|-- app.py
|-- agents/
|   |-- pdf_agent.py
|   |-- question_agent.py
|   `-- evaluation_agent.py
|-- utils/
|   |-- pdf_utils.py
|   |-- rag_utils.py
|   `-- compare_utils.py
|-- requirements.txt
`-- vector_store/
```

## Setup

### 1. Create and activate a virtual environment

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```powershell
pip install -r requirements.txt
```

### 3. Add environment variables

Create a `.env` file in the project root with your Groq API key:

```env
GROQ_API_KEY=your_groq_api_key_here
```

## Run the App

```powershell
streamlit run app.py
```

Then open the local Streamlit URL shown in the terminal.

## Usage

1. Upload a PDF document.
2. Enter a topic covered by the document.
3. Choose how many MCQ, short, and long questions to generate.
4. Generate the quiz.
5. Submit answers.
6. Review scores and feedback.

## Notes

- The app currently overwrites the vector database for each new uploaded PDF.
- Retrieved context is based on similarity search over the uploaded document.
- Question quality and feedback quality depend on the PDF content and LLM output.
- The repo includes a checked-in `venv/` and generated vector store data; these usually do not need to be versioned in long-term project maintenance.

## Troubleshooting

- If question generation fails, confirm `GROQ_API_KEY` is set correctly.
- If PDF processing fails, make sure the file contains extractable text and is not image-only.
- If the first run is slow, local embedding/model setup may still be warming up or downloading dependencies.

## Future Improvements

- Persist multiple PDFs instead of replacing the current one
- Add authentication and quiz history
- Export quiz results
- Add stronger answer rubrics and per-topic analytics

