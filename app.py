import os, re, glob
import numpy as np
import gradio as gr
from rank_bm25 import BM25Okapi
from sentence_transformers import SentenceTransformer
from huggingface_hub import InferenceClient

NAME = "Fatima"
MODEL_ID = os.environ.get("MODEL_ID", "meta-llama/Llama-3.1-8B-Instruct")
EMB_FILE = "embeddings.npy"
CHUNK_WORDS, OVERLAP, TOP_K, RRF_K = 250, 40, 4, 60

# ---------- 1. Load + chunk ----------
def load_chunks():
    chunks = []
    for path in sorted(glob.glob("data/*.md") + glob.glob("data/*.txt")):
        words = re.sub(r"<!--.*?-->", "", open(path, encoding="utf-8").read(), flags=re.S).split()
        step = CHUNK_WORDS - OVERLAP
        for i, start in enumerate(range(0, max(len(words), 1), step)):
            piece = words[start:start + CHUNK_WORDS]
            if len(piece) < 30 and i > 0:
                break
            chunks.append({"source": os.path.basename(path), "chunk_id": i, "text": " ".join(piece)})
    return chunks

CHUNKS = load_chunks()
TEXTS = [c["text"] for c in CHUNKS]

# ---------- 2. Index twice ----------
def tok(t):
    return re.findall(r"\w+", t.lower())

BM25 = BM25Okapi([tok(t) for t in TEXTS])
EMB_MODEL = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def get_embeddings():
    if os.path.exists(EMB_FILE):
        e = np.load(EMB_FILE)
        if e.shape[0] == len(TEXTS):
            return e
    e = EMB_MODEL.encode(TEXTS, normalize_embeddings=True)
    np.save(EMB_FILE, e)
    return e

EMB = get_embeddings()

# ---------- 3. Retrieve ----------
def bm25_search(q, k=TOP_K):
    s = BM25.get_scores(tok(q))
    idx = np.argsort(-s)[:k]
    return [(int(i), float(s[i])) for i in idx if s[i] > 0]

def dense_search(q, k=TOP_K):
    qv = EMB_MODEL.encode([q], normalize_embeddings=True)[0]
    s = EMB @ qv  # cosine (vectors are normalized)
    idx = np.argsort(-s)[:k]
    return [(int(i), float(s[i])) for i in idx]

# ---------- 4. Fuse (Reciprocal Rank Fusion) ----------
def hybrid_search(q, k=TOP_K):
    b = bm25_search(q, len(TEXTS))
    d = dense_search(q, len(TEXTS))
    scores = {}
    for ranking in (b, d):
        for rank, (i, _) in enumerate(ranking, start=1):
            scores[i] = scores.get(i, 0.0) + 1.0 / (RRF_K + rank)
    top = sorted(scores.items(), key=lambda x: -x[1])[:k]
    return [(i, s) for i, s in top]

# ---------- 5. Generate ----------
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

def generate(question, hits):
    if not hits:
        return "I don't have that in my notes."
    context = "\n\n".join(f"[{CHUNKS[i]['source']}#{CHUNKS[i]['chunk_id']}] {CHUNKS[i]['text']}" for i, _ in hits)
    token = os.environ.get("HF_TOKEN")
    if not token:
        return "(Templated answer - no API key set.) Most relevant note: " + CHUNKS[hits[0][0]]["text"][:400] + "..."
    try:
        client = InferenceClient(model=MODEL_ID, token=token)
        out = client.chat_completion(
            messages=[{"role": "user", "content": PROMPT.format(name=NAME, context=context, question=question)}],
            max_tokens=400, temperature=0.3)
        return out.choices[0].message.content.strip()
    except Exception as e:
        return f"(LLM unavailable: {type(e).__name__}.) Most relevant note: " + CHUNKS[hits[0][0]]["text"][:400] + "..."

# ---------- 6. UI ----------
def ask(question, mode):
    if not question.strip():
        return "Please type a question.", ""
    hits = {"BM25 only": bm25_search, "Dense only": dense_search, "Hybrid": hybrid_search}[mode](question)
    answer = generate(question, hits)
    label = {"BM25 only": "BM25 score", "Dense only": "cosine", "Hybrid": "RRF score"}[mode]
    md = "\n\n".join(
        f"**{n}. {CHUNKS[i]['source']} (chunk {CHUNKS[i]['chunk_id']})** - {label}: `{s:.4f}`\n\n> {CHUNKS[i]['text'][:500]}..."
        for n, (i, s) in enumerate(hits, 1)) or "_No chunks matched._"
    return answer, md

with gr.Blocks(title=f"{NAME}'s Digital Clone") as demo:
    gr.Markdown("# 🤖 This is an AI clone, not the real person.")
    gr.Markdown(f"Ask me anything about {NAME}. I answer only from my own notes.")
    q = gr.Textbox(label="Your question", placeholder="e.g. What projects have you built?")
    mode = gr.Radio(["BM25 only", "Dense only", "Hybrid"], value="Hybrid", label="Retrieval mode")
    btn = gr.Button("Ask", variant="primary")
    ans = gr.Markdown(label="Answer")
    gr.Markdown("### Retrieved chunks")
    chunks_out = gr.Markdown()
    btn.click(ask, [q, mode], [ans, chunks_out])
    q.submit(ask, [q, mode], [ans, chunks_out])

if __name__ == "__main__":
    demo.launch()
