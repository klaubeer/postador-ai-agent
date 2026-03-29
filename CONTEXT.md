# CONTEXT.md

## STATUS GERAL DO PROJETO

- **Fase atual:** DESENVOLVIMENTO
- **Milestone atual:** Redesign v2 completo — código pronto, falta testar e deployar
- **Última decisão relevante:** Toda refatoração de backend + frontend concluída em 2026-03-29
- **Próximo passo:** Testar localmente (uvicorn backend + abrir frontend), depois deploy na VPS

---

## FEATURES

| Status | Feature | Observações |
|--------|---------|-------------|
| ✅ DONE | state.py — schema simplificado | Campo "detalhes" adicionado, removidos campos mortos |
| ✅ DONE | llm.py — token tracking por sessão | Bug global corrigido, llm_chat com histórico, json_mode |
| ✅ DONE | planner.py — conversa natural | JSON mode nativo OpenAI, histórico completo, extração implícita |
| ✅ DONE | nodes.py — pipeline 2 nós | generate_content (legenda+hashtags) e generate_image_prompt |
| ✅ DONE | image_gen.py — Pollinations.ai | Grátis, sem API key, retorna URL direto |
| ✅ DONE | agent_graph.py — graph 2 nós | content → image_prompt → END |
| ✅ DONE | main.py — endpoints refatorados | /api/chat, /api/gerar-imagem, /api/reset. Histórico por sessão. Imagem automática |
| ✅ DONE | index.html — dark theme | Header com logo, sem toggle idioma, SVG icons |
| ✅ DONE | style.css — dark profissional | Fundo #0a0a0a, accent violeta #8b5cf6, post-card, typing indicator, responsive |
| ✅ DONE | app.js — refatorado | Loading states, typing dots, post card com imagem, toast notifications, copiar separado (legenda/hashtags), download imagem |
| ✅ DONE | nginx.conf | HTTPS + reverse proxy /api/ → uvicorn :8000 |
| ✅ DONE | requirements.txt | Versões mínimas fixadas, httpx adicionado, python-dotenv |
| ✅ DONE | Dockerfile | Simplificado para VPS |
| ✅ DONE | Limpeza | Removido image-prompt.py (legado) |
| 🔄 IN PROGRESS | Teste local | Rodando backend na porta 8010 para não conflitar |
| 📋 PLANNED | Deploy VPS | Configurar nginx, certbot, uvicorn na VPS |
| 📋 PLANNED | Ativar RAG | Integrar retriever.py no pipeline (próxima iteração) |

---

## DECISÕES ATIVAS — NÃO ALTERAR SEM DISCUSSÃO

- **Imagem:** Pollinations.ai (FLUX model), grátis, 1 imagem por post sem refinamento — decidido em 2026-03-29
- **Deploy:** VPS própria com Nginx, URL postador.klauberfischer.online — decidido em 2026-03-29
- **Idioma frontend:** Apenas português, sem toggle PT/EN — decidido em 2026-03-29
- **Pipeline:** 2 nós LangGraph (content + image_prompt), imagem gerada automaticamente no /api/chat — decidido em 2026-03-29
- **LLM:** OpenAI gpt-4.1-mini, JSON mode para planner — decidido em 2026-03-29
- **Stack:** FastAPI + LangGraph + OpenAI + vanilla JS (mantido do v1) — decidido em 2026-03-29
- **Portas:** Usar portas altas (8010+) para dev local e VPS — máquinas têm outros serviços rodando — decidido em 2026-03-29
