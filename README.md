# agentic_bgw

This repo is currently testing a simple LangChain RAG workflow.

Current setup:

- `src/main.py` builds a tiny in-memory vector store from local text files in `docs/`
- the agent uses `gpt-4.1-nano`
- a retrieval tool is used to answer a question from the dummy notes

Run from `src/` with:

```bash
python main.py
```
