import streamlit as st
import time
import os
from dotenv import load_dotenv
from agents.orchestrator import HospitalityOrchestrator

load_dotenv()

# ── CONFIG ─────────────────────────────────────────────
st.set_page_config(page_title="Multi-Agent Hospitality System", layout="wide")

# ── CSS ────────────────────────────────────────────────
st.markdown("""
<style>
body { background: #0d1117; color: #e6edf3; }

.title {
    text-align:center;
    font-size:2.6rem;
    font-weight:600;
    background: linear-gradient(135deg,#38bdf8,#818cf8);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
}

.stTextInput input {
    background:#161b22;
    border:1px solid #30363d;
    color:#fff;
    border-radius:10px;
    height:45px;
}

.stButton>button {
    background: linear-gradient(135deg,#38bdf8,#818cf8);
    border:none;
    color:white;
    border-radius:10px;
    height:45px;
}

.card {
    background:#161b22;
    padding:18px;
    border-radius:12px;
    border:1px solid #21262d;
    margin-bottom:15px;
}
</style>
""", unsafe_allow_html=True)

# ── HEADER ─────────────────────────────────────────────
st.markdown("<div class='title'>Multi-Agent Hospitality System</div>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#8b949e'>Plan your travel with AI agents</p>", unsafe_allow_html=True)

# ── INPUT ROW ──────────────────────────────────────────
c1, c2, c3, c4 = st.columns([3,3,2,2])

with c1:
    from_location = st.text_input("From", placeholder="Delhi")

with c2:
    destination = st.text_input("To", placeholder="Goa")

with c3:
    days = st.selectbox("Days", [1,2,3,4,5,6,7,10,14])

with c4:
    st.markdown("<br>", unsafe_allow_html=True)
    generate = st.button("✦ Generate", use_container_width=True)

# ── FILTERS ────────────────────────────────────────────
f1, f2, f3 = st.columns(3)

with f1:
    transport = st.multiselect("🚀 Transport",
        ["Flight","Train","Bus","Car Rental","Cruise","Ferry"],
        default=["Flight"]
    )

with f2:
    budget = st.radio("💰 Budget", ["Low","Mid","Luxury"], horizontal=True)

with f3:
    traveler = st.selectbox("🧳 Traveler",
        ["Tourist","Business","Solo Backpacker","Family","Couple","Senior","Adventure"]
    )

# ── AGENT PIPELINE ─────────────────────────────────────
st.markdown("### 🧠 Agent Pipeline")

p1, p2 = st.columns(2)

research_box = p1.empty()
writer_box = p2.empty()

def show_research(status):
    if status == "waiting":
        txt = "⏳ Waiting..."
    elif status == "working":
        txt = "🔄 Processing..."
    else:
        txt = "✅ Complete"

    research_box.markdown(f"""
    <div class='card'>
    <b>🔍 Researcher Agent</b><br>
    <small>Collecting travel data</small><br><br>
    {txt}
    </div>
    """, unsafe_allow_html=True)

def show_writer(status):
    if status == "waiting":
        txt = "⏳ Waiting..."
    elif status == "working":
        txt = "🔄 Processing..."
    else:
        txt = "✅ Complete"

    writer_box.markdown(f"""
    <div class='card'>
    <b>✍️ Writer Agent</b><br>
    <small>Generating itinerary</small><br><br>
    {txt}
    </div>
    """, unsafe_allow_html=True)

# initial state
show_research("waiting")
show_writer("waiting")

# ── OUTPUT ─────────────────────────────────────────────
st.markdown("### 📊 Generated Output")
output = st.empty()

# ── RUN ────────────────────────────────────────────────
if generate and destination and from_location:
    progress = st.progress(0)

    try:
        api_key = os.getenv("MISTRAL_API_KEY")
        if not api_key:
            raise RuntimeError("MISTRAL_API_KEY not set")

        orchestrator = HospitalityOrchestrator(api_key=api_key)

        # 🔍 Research START
        show_research("working")
        show_writer("waiting")

        progress.progress(30)
        time.sleep(0.5)

        result = orchestrator.run(
            destination=destination,
            origin=from_location,
            duration=days,
            travelers=1,
            hotel_tier=budget,
            transport_modes=transport,
            interests=["general"],
            budget=budget
        )

        # 🔍 Research DONE → Writer START
        show_research("done")
        show_writer("working")

        progress.progress(80)
        time.sleep(0.5)

        # ✍️ Writer DONE
        show_writer("done")
        progress.progress(100)

        # ── OUTPUT ───────────────────────────
        st.markdown(f"""
        <div class='card'>
        <h3>📍 {result.get("destination")}</h3>
        📅 {result.get("duration")} Days<br>
        💰 Budget: {result.get("budget")}<br>
        ✈️ From: {from_location}
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### 📅 Itinerary")
        st.markdown(f"<div class='card'>{result.get('itinerary')}</div>", unsafe_allow_html=True)

        st.markdown("### 🏨 Hotels")
        for h in result.get("hotels", []):
            st.markdown(f"""
            <div class='card'>
            <b>{h.get('name')}</b><br>
            ⭐ {h.get('rating')}<br>
            💰 {h.get('price_per_night')}<br>
            📍 {h.get('location')}
            </div>
            """, unsafe_allow_html=True)

        with st.expander("📄 Raw Data"):
            st.json(result)

    except Exception as e:
        st.error(f"Error: {e}")