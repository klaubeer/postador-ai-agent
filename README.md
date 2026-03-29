# Postador — Agente de IA para Criação de Conteúdo

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-backend-green?logo=fastapi&logoColor=white)
![LangGraph](https://img.shields.io/badge/LangGraph-pipeline_de_agentes-orange)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4.1--mini-412991?logo=openai&logoColor=white)
![Vercel](https://img.shields.io/badge/Frontend-Vercel-black?logo=vercel&logoColor=white)
![Render](https://img.shields.io/badge/Backend-Render-46E3B7?logo=render&logoColor=white)

> Agente de IA conversacional que gera posts completos para redes sociais — da ideia à legenda, hashtags e prompt de imagem — por meio de um pipeline multi-nó com LangGraph.

**Demo ao vivo:** [postador-ai-agent.vercel.app](https://postador-ai-agent.vercel.app)

---

## Como funciona

O sistema opera em duas camadas:

**Camada 1 — Planner (LLM conversacional)**
Conversa com o usuário para coletar contexto: objetivo do post, plataforma, tema/produto e público-alvo. Com contexto suficiente, aciona o pipeline de geração.

**Camada 2 — Pipeline LangGraph (nós especializados)**
Pipeline stateful com múltiplos nós, cada um responsável por uma etapa. Os nós rodam em sequência, cada um construindo sobre o resultado anterior.

```
Entrada do Usuário
        │
        ▼
┌───────────────────────────────────┐
│  Planner  (GPT-4.1-mini)          │
│  Coleta: objetivo · plataforma    │
│          tema · público           │
└──────────────┬────────────────────┘
               │ quando há contexto suficiente
               ▼
┌───────────────────────────────────┐
│       Pipeline LangGraph          │
│                                   │
│  [nó ideia]                       │
│      ↓  gera o conceito do post   │
│  [nó legenda]                     │
│      ↓  escreve legenda + CTA     │
│  [nó prompt de imagem]            │
│      ↓  cria prompt visual        │
│  [nó hashtags]                    │
│      ↓  hashtags por plataforma   │
│  [nó formatação]                  │
│      ↓  monta o post final        │
└──────────────┬────────────────────┘
               │
               ▼
       Post Estruturado
               │
               ▼ (opcional)
     Geração de Imagem
     (OpenAI gpt-image-1)
```

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


## Conceitos Demonstrados

- Agentes de IA e pipelines multi-nó (LangGraph)
- Engenharia de Prompts
- RAG (Retrieval-Augmented Generation)
- Busca vetorial com FAISS
- Embeddings de texto (OpenAI)
- Design de API REST com FastAPI
- Gerenciamento de sessão stateful
- Deploy de aplicação full-stack com IA

---

## Autor

**Klauber Fischer** — [T2K](https://t2k.site)
Joinville, Santa Catarina, Brasil
