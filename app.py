import streamlit as st
from rag import ask_question

# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="DocMind · RAG Chatbot",
    page_icon="📄",
    layout="centered"
)

# ─── Custom CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

/* ── Root Variables ── */
:root {
    --bg:        #0d0f14;
    --surface:   #151820;
    --border:    #1e2330;
    --accent:    #4f8cff;
    --accent2:   #a78bfa;
    --text:      #e8eaf0;
    --muted:     #6b7280;
    --user-bg:   #1a1f2e;
    --bot-bg:    #111420;
    --radius:    14px;
}

/* ── Global Reset ── */
html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--bg) !important;
    font-family: 'DM Sans', sans-serif;
    color: var(--text);
}

[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stToolbar"] { display: none; }
#MainMenu, footer { visibility: hidden; }

/* ── Main container ── */
.block-container {
    max-width: 780px !important;
    padding: 2rem 1.5rem 4rem !important;
}

/* ── Header ── */
.docmind-header {
    text-align: center;
    padding: 2.5rem 0 1.5rem;
    margin-bottom: 2rem;
}
.docmind-logo {
    display: inline-flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 0.5rem;
}
.docmind-logo .icon {
    width: 42px; height: 42px;
    background: linear-gradient(135deg, var(--accent), var(--accent2));
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 20px;
}
.docmind-title {
    font-family: 'Syne', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    background: linear-gradient(90deg, var(--accent), var(--accent2));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -0.5px;
}
.docmind-sub {
    font-size: 0.9rem;
    color: var(--muted);
    font-weight: 300;
    letter-spacing: 0.3px;
}

/* ── Input area ── */
[data-testid="stTextInput"] > div > div {
    background: var(--surface) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: var(--radius) !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.95rem !important;
    padding: 0.6rem 1rem !important;
    transition: border-color 0.2s;
}
[data-testid="stTextInput"] > div > div:focus-within {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(79,140,255,0.15) !important;
}
[data-testid="stTextInput"] input {
    color: var(--text) !important;
    background: transparent !important;
}
[data-testid="stTextInput"] label {
    color: var(--muted) !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.5px !important;
    text-transform: uppercase !important;
}

/* ── Button ── */
[data-testid="stButton"] > button {
    background: linear-gradient(135deg, var(--accent), var(--accent2)) !important;
    color: #fff !important;
    border: none !important;
    border-radius: var(--radius) !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.92rem !important;
    letter-spacing: 0.5px !important;
    padding: 0.55rem 2rem !important;
    transition: opacity 0.2s, transform 0.15s !important;
    width: 100%;
}
[data-testid="stButton"] > button:hover {
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
}
[data-testid="stButton"] > button:active {
    transform: translateY(0px) !important;
}

/* ── Chat bubbles ── */
.chat-wrapper {
    display: flex;
    flex-direction: column;
    gap: 1.2rem;
    margin-top: 2rem;
}
.chat-bubble {
    padding: 1rem 1.25rem;
    border-radius: var(--radius);
    line-height: 1.65;
    font-size: 0.93rem;
    position: relative;
    animation: fadeSlide 0.3s ease forwards;
}
@keyframes fadeSlide {
    from { opacity: 0; transform: translateY(8px); }
    to   { opacity: 1; transform: translateY(0); }
}
.bubble-user {
    background: var(--user-bg);
    border: 1px solid var(--border);
    border-left: 3px solid var(--accent);
    margin-left: 2rem;
}
.bubble-bot {
    background: var(--bot-bg);
    border: 1px solid var(--border);
    border-left: 3px solid var(--accent2);
    margin-right: 2rem;
}
.bubble-label {
    font-family: 'Syne', sans-serif;
    font-size: 0.7rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 0.4rem;
}
.label-user  { color: var(--accent); }
.label-bot   { color: var(--accent2); }
.bubble-text { color: var(--text); white-space: pre-wrap; }

/* ── Divider ── */
.chat-divider {
    border: none;
    border-top: 1px solid var(--border);
    margin: 0.5rem 0;
}

/* ── Empty state ── */
.empty-state {
    text-align: center;
    padding: 3rem 1rem;
    color: var(--muted);
}
.empty-state .big-icon { font-size: 2.5rem; margin-bottom: 0.75rem; }
.empty-state p { font-size: 0.88rem; font-weight: 300; line-height: 1.6; }

/* ── Warning ── */
[data-testid="stAlert"] {
    background: rgba(79,140,255,0.08) !important;
    border: 1px solid rgba(79,140,255,0.25) !important;
    border-radius: var(--radius) !important;
    color: var(--text) !important;
}

/* ── Spinner ── */
[data-testid="stSpinner"] { color: var(--accent) !important; }

/* ── Clear button ── */
.clear-btn-row { display: flex; justify-content: flex-end; margin-bottom: 0.5rem; }
</style>
""", unsafe_allow_html=True)

# ─── Header ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="docmind-header">
    <div class="docmind-logo">
        <div class="icon">📄</div>
        <span class="docmind-title">DocMind</span>
    </div>
    <p class="docmind-sub">Ask anything about your PDF — powered by RAG</p>
</div>
""", unsafe_allow_html=True)

# ─── Session State ───────────────────────────────────────────────────────────
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ─── Input ───────────────────────────────────────────────────────────────────
query = st.text_input("Your Question", placeholder="e.g. What is the main topic of chapter 2?")

col1, col2 = st.columns([3, 1])
with col1:
    ask_btn = st.button("✦ Ask DocMind", use_container_width=True)
with col2:
    clear_btn = st.button("Clear Chat", use_container_width=True)

# ─── Clear History ────────────────────────────────────────────────────────────
if clear_btn:
    st.session_state.chat_history = []
    st.rerun()

# ─── Handle Ask ──────────────────────────────────────────────────────────────
if ask_btn:
    if query.strip():
        with st.spinner("Reading through your document..."):
            response = ask_question(query)
        st.session_state.chat_history.append({
            "question": query,
            "answer": response
        })
        st.rerun()
    else:
        st.warning("Please enter a question before asking.")

# ─── Chat Display ─────────────────────────────────────────────────────────────
if st.session_state.chat_history:
    st.markdown('<div class="chat-wrapper">', unsafe_allow_html=True)

    for i, chat in enumerate(reversed(st.session_state.chat_history)):
        q = chat["question"].replace("<", "&lt;").replace(">", "&gt;")
        a = chat["answer"].replace("<", "&lt;").replace(">", "&gt;")

        st.markdown(f"""
        <div class="chat-bubble bubble-user">
            <div class="bubble-label label-user">You</div>
            <div class="bubble-text">{q}</div>
        </div>
        <div class="chat-bubble bubble-bot">
            <div class="bubble-label label-bot">DocMind</div>
            <div class="bubble-text">{a}</div>
        </div>
        """, unsafe_allow_html=True)

        if i < len(st.session_state.chat_history) - 1:
            st.markdown('<hr class="chat-divider">', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

else:
    st.markdown("""
    <div class="empty-state">
        <div class="big-icon">🔍</div>
        <p>No questions yet.<br>Type something above and hit <strong>Ask DocMind</strong> to get started.</p>
    </div>
    """, unsafe_allow_html=True)