# HiResume

Generates an ATS-friendly resume tailored to a specific job description,
using a candidate's stored career history — via RAG + a Groq-hosted LLM,
orchestrated with LangGraph.

## Core guarantees

1. **Profile info is always included.** Name, college, branch, LinkedIn,
   GitHub, and other links are stored as a *static profile* and merged
   into every resume regardless of what the JD asks for or what RAG
   retrieves.
2. **Never a blank/incomplete resume.** If the JD asks for something the
   candidate has no direct experience in, a gap-analysis step identifies
   the closest transferable skill/project in their background and the
   generation step honestly reframes it — instead of leaving the section
   empty or fabricating experience.

## Architecture

```
Upload career history --> chunk --> embed --> Chroma vector store (per user)
                                                        │
Job description ──────────────────────────────────────►│
                                                        ▼
                              ┌── LangGraph pipeline ──────────────┐
                              │ retrieve → classify → gap_analysis │
                              │   → generate_sections → assemble   │
                              └─────────────────────────────────────┘
                                                        │
                                     Static profile ────┘ (always merged in)
                                                        ▼
                                  Final resume (PDF / Markdown / on-screen)
```

- **Retrieval**: top-k relevant chunks from the user's own career-history
  vector store are pulled using the JD as the query.
- **Classification**: an LLM sorts raw retrieved facts into resume
  categories (experience, projects, skills, certifications, achievements)
  without inventing anything.
- **Gap analysis**: compares JD requirements against the candidate's
  available facts and marks each as covered / partially covered (with the
  closest transferable evidence) / not covered.
- **Generation**: writes ATS-optimized, quantified bullet points per
  section, using the gap analysis to reframe transferable experience
  honestly rather than fabricate or omit.
- **Assembly**: merges the static profile with the generated sections and
  computes a deterministic keyword-overlap ATS score.

## Project structure

```
ai_resume_generator/
├── app.py                     # Streamlit UI entry point
├── .env.example                # copy to .env and fill in your Groq key
├── requirements.txt
├── config/
│   └── settings.py             # loads and validates all env vars
├── core/                       # low-level, reusable building blocks
│   ├── schemas.py               # Pydantic models (StaticProfile, FinalResume, ...)
│   ├── document_loader.py       # pdf/docx/txt -> plain text
│   ├── chunking.py              # text splitting for embeddings
│   ├── embeddings.py            # local HuggingFace embedding model
│   ├── vector_store.py          # Chroma wrapper (per-user collections)
│   ├── llm_client.py            # Groq LLM wrapper
│   └── json_utils.py            # robust JSON parsing for LLM output
├── graph/                       # LangGraph orchestration
│   ├── state.py                  # shared pipeline state
│   ├── nodes.py                  # one function per graph node
│   └── workflow.py               # builds & runs the compiled graph
├── services/                    # business logic used by graph nodes / UI
│   ├── prompts.py                 # all LLM prompt templates
│   ├── classifier.py              # RAG chunks -> resume sections
│   ├── gap_analyzer.py            # JD requirements vs candidate facts
│   ├── section_generator.py       # writes tailored, ATS-friendly bullets
│   ├── resume_assembler.py        # merges profile + generated content
│   ├── ats_optimizer.py           # keyword-overlap ATS scoring
│   ├── markdown_exporter.py       # resume -> markdown
│   ├── pdf_exporter.py            # resume -> ATS-friendly PDF
│   ├── ingestion.py               # upload/paste -> chunk -> index
│   └── profile_store.py           # persists the static profile as JSON
├── ui/
│   ├── styles.py                  # custom CSS (design system)
│   └── components.py              # Streamlit components (form, meter, preview)
├── data/
│   ├── vector_db/                 # persisted Chroma DB (gitignored contents)
│   └── profiles/                  # one JSON file per user profile
├── outputs/                      # nothing written here by default (downloads are in-browser)
└── tests/
    └── test_workflow.py          # tests for the non-LLM deterministic logic
```

## Setup

```bash
cd ai_resume_generator
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
# then edit .env and paste your GROQ_API_KEY (https://console.groq.com/keys)

streamlit run app.py
```

The first run will download the local embedding model
(`sentence-transformers/all-MiniLM-L6-v2`, ~80MB) — this needs internet
access once, after which embedding runs fully offline/locally. Only the
generation/classification/gap-analysis steps call the Groq API.

## Using it

1. In the sidebar, enter a **Profile ID** (any unique string — lets
   multiple people use the same deployment without mixing data).
2. Fill in and save your **static profile** (name, contact, college,
   branch, LinkedIn, GitHub, etc.) — this always appears on the resume.
3. Upload or paste your **career history** (past roles, project
   descriptions, skills, achievements) and click **Index my background**.
4. Paste a **job description** and click **Generate tailored resume**.
5. Review the preview, check the **ATS Match** tab for keyword coverage,
   and download as PDF or Markdown.

## Notes on model choice

- `GROQ_MODEL` defaults to `llama-3.3-70b-versatile`. Swap it in `.env`
  for any other Groq-hosted chat model (see
  https://console.groq.com/docs/models for the current list).
- Embeddings run locally via `sentence-transformers` so no second API
  key is required — Groq is chat/completion only.

## Running tests

```bash
pytest tests/
```

Tests cover only the deterministic logic (chunking, JSON parsing, ATS
scoring, resume assembly) so they run without a Groq API key.
