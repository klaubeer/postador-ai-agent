# Postador — AI Agent for Content Creation

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-backend-green?logo=fastapi&logoColor=white)
![LangGraph](https://img.shields.io/badge/LangGraph-agent_pipeline-orange)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4.1--mini-412991?logo=openai&logoColor=white)
![Vercel](https://img.shields.io/badge/Frontend-Vercel-black?logo=vercel&logoColor=white)
![Render](https://img.shields.io/badge/Backend-Render-46E3B7?logo=render&logoColor=white)

> Conversational AI agent that generates complete social media posts — from idea to caption, hashtags, and image prompt — through a multi-node LangGraph pipeline.

**Access:** (https://postador.klauberfischer.online/)

---

## How It Works

The system operates in two layers:

**Layer 1 — Planner (conversational LLM)**
Converses with the user to collect context: post goal, platform, topic/product, and target audience. With enough context, it triggers the generation pipeline.

**Layer 2 — LangGraph Pipeline (specialized nodes)**
Stateful pipeline with multiple nodes, each responsible for one step. Nodes run in sequence, each building on the previous result.

```
User Input
        │
        ▼
┌───────────────────────────────────┐
│  Planner  (GPT-4.1-mini)          │
│  Collects: goal · platform        │
│            topic · audience       │
└──────────────┬────────────────────┘
               │ when enough context is gathered
               ▼
┌───────────────────────────────────┐
│       LangGraph Pipeline          │
│                                   │
│  [idea node]                      │
│      ↓  generates post concept    │
│  [caption node]                   │
│      ↓  writes caption + CTA      │
│  [image prompt node]              │
│      ↓  creates visual prompt     │
│  [hashtags node]                  │
│      ↓  platform-specific tags    │
│  [formatting node]                │
│      ↓  assembles final post      │
└──────────────┬────────────────────┘
               │
               ▼
       Structured Post
               │
               ▼ (optional)
     Image Generation
     (OpenAI gpt-image-1)
```

---

## Features

- Conversational context gathering before generating
- Automatic post idea generation
- Caption creation with engagement-optimized CTA
- Platform-specific hashtags (Instagram / TikTok)
- Image prompt for visual generation tools
- On-demand image generation (OpenAI gpt-image-1)
- Copy post and download image with one click
- Bilingual interface (PT 🇧🇷 / EN 🇺🇸)
- Session management with unique IDs
- RAG pipeline with FAISS vector search for contextual knowledge

---

## Tech Stack

| Layer | Technology |
|--------|-----------|
| LLM | OpenAI GPT-4.1-mini |
| Image Generation | OpenAI gpt-image-1 |
| Agent Pipeline | LangGraph |
| Embeddings / RAG | OpenAI text-embedding-3-small + FAISS |
| Backend API | FastAPI + Uvicorn |
| Frontend | Vanilla JS + HTML + CSS |


## Concepts Demonstrated

- AI agents and multi-node pipelines (LangGraph)
- Prompt Engineering
- RAG (Retrieval-Augmented Generation)
- Vector search with FAISS
- Text embeddings (OpenAI)
- REST API design with FastAPI
- Stateful session management
- Full-stack AI application deployment

---

## Author

**Klauber Fischer** — [T2K](https://t2k.site)
Joinville, Santa Catarina, Brazil
