import os, re, glob
import numpy as np
import streamlit as st
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer
from huggingface_hub import InferenceClient

NAME = "Fatima"
MODEL_ID = os.environ.get("MODEL_ID", "meta-llama/Llama-3.1-8B-Instruct")
EMB_FILE = "embeddings.npy"
CHUNK_WORDS, OVERLAP, TOP_K, RRF_K = 250, 40, 4, 60

def tok(t):
    return re.findall(r"\w+", t.lower())

@st.cache_resource(show_spinner="Loading knowledge base...")
def load():
    chunks = []
    here = os.getcwd()
    found = glob.glob(os.path.join(here, "**", "*.md"), recursive=True) + glob.glob(os.path.join(here, "**", "*.txt"), recursive=True)
    found = [p for p in found if os.path.basename(p).lower() not in ("readme.md", "requirements.txt") and "/." not in p]
    for path in sorted(found):
        words = re.sub(r"<!--.*?-->", "", open(path, encoding="utf-8").read(), flags=re.S).split()
        step = CHUNK_WORDS - OVERLAP
        for i, start in enumerate(range(0, max(len(words), 1), step)):
            piece = words[start:start + CHUNK_WORDS]
            if len(piece) < 30 and i > 0:
                break
            chunks.append({"source": os.path.basename(path), "chunk_id": i, "text": " ".join(piece)})
    texts = [c["text"] for c in chunks]
    if not texts:
        st.error("No data files found. Put your .md files inside a 'data' folder in the GitHub repo. Files seen here: " + ", ".join(sorted(os.listdir(here))))
        st.stop()
    bm25 = BM25Okapi([tok(t) for t in texts])
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    emb = None
    if os.path.exists(EMB_FILE):
        e = np.load(EMB_FILE)
        if e.shape[0] == len(texts):
            emb = e
    if emb is None:
        emb = model.encode(texts, normalize_embeddings=True)
        np.save(EMB_FILE, emb)
    return chunks, texts, bm25, model, emb

CHUNKS, TEXTS, BM25, MODEL, EMB = load()

def bm25_search(q, k=TOP_K):
    s = BM25.get_scores(tok(q))
    idx = np.argsort(-s)[:k]
    return [(int(i), float(s[i])) for i in idx if s[i] > 0]

def dense_search(q, k=TOP_K):
    qv = MODEL.encode([q], normalize_embeddings=True)[0]
    s = EMB @ qv
    idx = np.argsort(-s)[:k]
    return [(int(i), float(s[i])) for i in idx]

def hybrid_search(q, k=TOP_K):
    scores = {}
    for ranking in (bm25_search(q, len(TEXTS)), dense_search(q, len(TEXTS))):
        for rank, (i, _) in enumerate(ranking, start=1):
            scores[i] = scores.get(i, 0.0) + 1.0 / (RRF_K + rank)
    return sorted(scores.items(), key=lambda x: -x[1])[:k]

PROMPT = """You are the AI clone of {name}, a software engineering student.
Speak in the first person, in a friendly, casual tone with short sentences.
Rules:
1. Answer ONLY using the CONTEXT below. It comes from my own documents.
2. If the context does not contain the answer, say: "I don't have that in my notes." Do not guess or invent facts about me.
3. Never share phone numbers, addresses, ID numbers or other private details.
4. If asked whether you are the real person, say you are an AI clone of {name}.
CONTEXT:
{context}
QUESTION:
{question}"""

def get_token():
    try:
        return st.secrets["HF_TOKEN"]
    except Exception:
        return os.environ.get("HF_TOKEN")

def generate(question, hits):
    if not hits:
        return "I don't have that in my notes."
    context = "\n\n".join(f"[{CHUNKS[i]['source']}#{CHUNKS[i]['chunk_id']}] {CHUNKS[i]['text']}" for i, _ in hits)
    token = get_token()
    if not token:
        return "(Templated answer - no API key set.) Most relevant note: " + CHUNKS[hits[0][0]]["text"][:400] + "..."
    prompt = PROMPT.format(name=NAME, context=context, question=question)
    errors = []
    for model_id in dict.fromkeys([MODEL_ID, "Qwen/Qwen2.5-7B-Instruct", "meta-llama/Llama-3.2-3B-Instruct", "HuggingFaceH4/zephyr-7b-beta"]):
        try:
            client = InferenceClient(model=model_id, token=token)
            out = client.chat_completion(messages=[{"role": "user", "content": prompt}], max_tokens=400, temperature=0.3)
            return out.choices[0].message.content.strip()
        except Exception as e:
            errors.append(f"{model_id}: {str(e)[:150]}")
    st.session_state["llm_errors"] = errors
    return "(LLM unavailable.) Most relevant note: " + CHUNKS[hits[0][0]]["text"][:400] + "..."

st.set_page_config(page_title=f"{NAME}'s Digital Clone", page_icon="🤖")
st.error("🤖 This is an AI clone, not the real person.")
st.title(f"{NAME}'s Digital Clone")
st.caption(f"Ask me anything about {NAME}. I answer only from my own notes.")

question = st.text_input("Your question", placeholder="e.g. What projects have you built?")
mode = st.radio("Retrieval mode", ["BM25 only", "Dense only", "Hybrid"], index=2, horizontal=True)

if st.button("Ask", type="primary") and question.strip():
    hits = {"BM25 only": bm25_search, "Dense only": dense_search, "Hybrid": hybrid_search}[mode](question)
    with st.spinner("Thinking..."):
        answer = generate(question, hits)
    st.markdown("### Answer")
    st.write(answer)
    label = {"BM25 only": "BM25 score", "Dense only": "cosine", "Hybrid": "RRF score"}[mode]
    if st.session_state.get("llm_errors"):
        st.warning("LLM error details: " + " | ".join(st.session_state.pop("llm_errors")))
    st.markdown("### Retrieved chunks")
    if not hits:
        st.info("No chunks matched.")
    for n, (i, s) in enumerate(hits, 1):
        with st.expander(f"{n}. {CHUNKS[i]['source']} (chunk {CHUNKS[i]['chunk_id']}) - {label}: {s:.4f}"):
            st.write(CHUNKS[i]["text"])
