# Digital Clone - Hybrid RAG (BM25 + Dense + RRF)
**This is an AI clone, not the real person.**
Streamlit version. Run: `streamlit run streamlit_app.py`
Pipeline: chunk (250 words, 40 overlap) -> BM25 + MiniLM embeddings (embeddings.npy) -> Reciprocal Rank Fusion (1/(60+rank)) -> LLM answer in first person, grounded in retrieved chunks.

## One-page report
**1. Knowledge base and why:** [files + reason]

| Question | BM25 result | Dense result | Hybrid result | Best mode and why |
|---|---|---|---|---|
| Q1 (exact rare keyword) | | | | |
| Q2 (paraphrase, no shared words) | | | | |
| Q3 | | | | |
| Q4 | | | | |
| Q5 | | | | |

**3. Failure case:** [..]
**4. Improvement:** [..]
