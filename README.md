# Postador — AI Social Media Content Agent

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-backend-green?logo=fastapi&logoColor=white)
![LangGraph](https://img.shields.io/badge/LangGraph-agent_pipeline-orange)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4.1--mini-412991?logo=openai&logoColor=white)
![Vercel](https://img.shields.io/badge/Frontend-Vercel-black?logo=vercel&logoColor=white)
![Render](https://img.shields.io/badge/Backend-Render-46E3B7?logo=render&logoColor=white)

> Conversational AI agent that generates complete social media posts — from idea to caption, hashtags, and AI image prompt — through a LangGraph-powered multi-node pipeline.

**Live demo:** [postador-ai-agent.vercel.app](https://postador-ai-agent.vercel.app)

---

## How It Works

The system runs in two layers:

**Layer 1 — Planner (conversational LLM)**
Engages the user in a short conversation to collect context: post objective, platform, topic/product, and target audience. Once enough context is gathered, it triggers the generation pipeline.

**Layer 2 — LangGraph Pipeline (specialized agent nodes)**
A stateful multi-node pipeline where each node is responsible for one task. Nodes run sequentially, each building on the previous output.

```
User Input
    │
    ▼
┌───────────────────────────────────┐
│  Planner  (GPT-4.1-mini)          │
│  Collects: objetivo · plataforma  │
│            tema · público         │
└──────────────┬────────────────────┘
               │ when context is ready
               ▼
┌───────────────────────────────────┐
│         LangGraph Pipeline        │
│                                   │
│  [idea node]                      │
│      ↓  generates post concept    │
│  [caption node]                   │
│      ↓  writes caption + CTA      │
│  [image_prompt node]              │
│      ↓  creates AI image prompt   │
│  [hashtags node]                  │
│      ↓  platform-aware hashtags   │
│  [format node]                    │
│      ↓  assembles final output    │
└──────────────┬────────────────────┘
               │
               ▼
    Structured Post Output
               │
               ▼ (optional)
    Image Generation
    (OpenAI gpt-image-1)
```

---

## Features

- Conversational context collection before generation
- Automated post idea generation
- Caption writing optimized for engagement, with CTA
- Platform-aware hashtag generation (Instagram / TikTok)
- AI image prompt generation for creative direction
- On-demand image generation (OpenAI gpt-image-1)
- One-click post copy and image download
- Bilingual interface (PT 🇧🇷 / EN 🇺🇸)
- Session management with unique session IDs
- RAG pipeline with FAISS vector search for contextual knowledge

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| LLM | OpenAI GPT-4.1-mini |
| Image Generation | OpenAI gpt-image-1 |
| Agent Pipeline | LangGraph |
| Embeddings / RAG | OpenAI text-embedding-3-small + FAISS |
| Backend API | FastAPI + Uvicorn |
| Frontend | Vanilla JS + HTML + CSS |
| Backend Hosting | Render |
| Frontend Hosting | Vercel |

---

## Project Structure

```
postador-ai-agent/
├── backend/
│   ├── main.py           # FastAPI app — /chat and /gerar-imagem endpoints
│   ├── agent_graph.py    # LangGraph pipeline definition
│   ├── nodes.py          # Pipeline nodes: idea, caption, image_prompt, hashtags, format
│   ├── planner.py        # Conversational planner — collects context before triggering pipeline
│   ├── state.py          # AgentState TypedDict
│   ├── llm.py            # OpenAI LLM wrapper with session token tracking
│   ├── image_gen.py      # OpenAI image generation (gpt-image-1)
│   └── rag/
│       ├── dados.txt     # Knowledge base source
│       ├── ingest.py     # Embeddings ingestion script
│       └── retriever.py  # FAISS vector search
├── frontend/
│   ├── index.html        # Chat UI (bilingual PT/EN)
│   ├── style.css         # Responsive styles
│   └── app.js            # Client logic + API integration
├── Dockerfile
├── requirements.txt
└── .env.example
```

---

## Setup

### Prerequisites

- Python 3.11+
- OpenAI API key

### Install

```bash
git clone https://github.com/your-username/postador-ai-agent.git
cd postador-ai-agent

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

### Environment Variables

```bash
cp .env.example .env
# Add your OPENAI_API_KEY to .env
```

### Run Locally

```bash
# Backend
uvicorn backend.main:app --reload

# Frontend
# Open frontend/index.html in your browser
# or serve it with any static server
```

---

## Deployment

**Backend → Render**

- Build command: `pip install -r requirements.txt`
- Start command: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
- Environment variable: `OPENAI_API_KEY`

**Frontend → Vercel**

- Root directory: `frontend/`
- No build step required (static files)
- The `API_URL` in `app.js` automatically switches between localhost and the Render URL

---

## Concepts Demonstrated

- AI Agents & multi-node pipelines (LangGraph)
- Prompt Engineering
- RAG (Retrieval-Augmented Generation)
- Vector search with FAISS
- Text embeddings (OpenAI)
- FastAPI REST API design
- Stateful session management
- Full-stack AI application deployment

---

## Author

**Klauber Fischer** — [T2K](https://t2k.site)
Joinville, Santa Catarina, Brasil

---

---

# 🇧🇷 Postador — Agente de IA para Criação de Conteúdo

> Agente de IA conversacional que gera posts completos para redes sociais — da ideia à legenda, hashtags e prompt de imagem — por meio de um pipeline multi-nó com LangGraph.

**Demo ao vivo:** [postador-ai-agent.vercel.app](https://postador-ai-agent.vercel.app)

---

## Como funciona

O sistema opera em duas camadas:

**Camada 1 — Planner (LLM conversacional)**
Conversa com o usuário para coletar contexto: objetivo do post, plataforma, tema/produto e público-alvo. Com contexto suficiente, aciona o pipeline de geração.

**Camada 2 — Pipeline LangGraph (nós especializados)**
Pipeline stateful com múltiplos nós, cada um responsável por uma etapa. Os nós rodam em sequência, cada um construindo sobre o resultado anterior.

---

## Funcionalidades

- Coleta conversacional de contexto antes de gerar
- Geração automática de ideias de post
- Criação de legenda com CTA otimizado para engajamento
- Hashtags por plataforma (Instagram / TikTok)
- Prompt de imagem para ferramentas de geração visual
- Geração de imagem sob demanda (OpenAI gpt-image-1)
- Copiar post e baixar imagem com um clique
- Interface bilíngue (PT 🇧🇷 / EN 🇺🇸)
- Gerenciamento de sessão com IDs únicos
- Pipeline RAG com busca vetorial FAISS para conhecimento contextual

---

## Stack Tecnológica

| Camada | Tecnologia |
|--------|-----------|
| LLM | OpenAI GPT-4.1-mini |
| Geração de Imagem | OpenAI gpt-image-1 |
| Pipeline de Agentes | LangGraph |
| Embeddings / RAG | OpenAI text-embedding-3-small + FAISS |
| API Backend | FastAPI + Uvicorn |
| Frontend | Vanilla JS + HTML + CSS |
| Hospedagem Backend | Render |
| Hospedagem Frontend | Vercel |

---

## Autor

**Klauber Fischer** — [T2K](https://t2k.site)
Joinville, Santa Catarina, Brasil
