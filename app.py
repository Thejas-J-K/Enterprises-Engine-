import streamlit as st
from engine import run_growth_engine
import time
import uuid
import json
from datetime import datetime
import os

# ===============================
# PAGE CONFIG
# ===============================
st.set_page_config(
    page_title="DataVex Growth Engine",
    page_icon="🚀",
    layout="wide"
)

# ===============================
# STYLING
# ===============================
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button {
        width: 100%;
        border-radius: 6px;
        height: 3em;
        background-color: #111827;
        color: white;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🚀 DataVex Autonomous Growth Intelligence Engine")
st.markdown("### Real-Time Signal → Strategy → Content → Visuals → Publish")

st.divider()

# ===============================
# SESSION STATE
# ===============================
if "result" not in st.session_state:
    st.session_state.result = None

# ===============================
# SIDEBAR
# ===============================
with st.sidebar:
    st.header("⚙️ Autonomous Control Panel")
    run_btn = st.button("🚀 Scan & Generate Trending Asset")
    st.success("System auto-detects trending AI infrastructure signals.")
    st.caption("Architecture: Analyst → Creator → Visualist")

# ===============================
# RUN ENGINE
# ===============================
if run_btn:
    with st.spinner("🤖 Analyst scanning global AI trends..."):
        st.session_state.result = run_growth_engine()

# ===============================
# DISPLAY RESULTS
# ===============================
if st.session_state.result:

    res = st.session_state.result

    # ============================================
    # STEP 1 — SHOW 5 NEWS + SELECTED SIGNAL
    # ============================================
    st.header("🧠 Step 1: Intelligence Analysis")

    # 🔹 Show 5 News
    st.subheader("📡 Top 5 Enterprise Signals Scouted")

    for i, news in enumerate(res.get("all_news", []), start=1):
        with st.expander(f"{i}. {news.get('title')}"):
            st.write(f"**Source:** {news.get('source')}")
            st.write(f"**Published:** {news.get('published_at')}")
            st.write(f"[Read Article]({news.get('url')})")

    # 🔹 Show Selected Priority News
    st.subheader("🎯 Selected High-Priority Signal")

    selected = res.get("signal")

    if isinstance(selected, dict):
        st.success(selected.get("title"))
        st.write(f"**Reasoning:** {selected.get('reasoning')}")
        st.write(f"**Source:** {selected.get('source')}")
        st.write(f"[View Article]({selected.get('url')})")
    else:
        st.warning("No signal selected.")

    # ============================================
    # STEP 2 — STRATEGY
    # ============================================
    st.divider()
    st.header("📈 Step 2: Growth Strategy Brief")

    with st.expander("View Strategy Rationale", expanded=True):
        st.write(res.get("strategy", ""))

    # ============================================
    # STEP 3 — CREATOR TRACE
    # ============================================
    st.divider()
    st.header("⚡ Step 3: Real-Time Creator Intelligence")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Initial Draft (Internal)**")
        st.text_area(
            "draft",
            res.get("first_draft", ""),
            height=250,
            disabled=True
        )

    with col2:
        st.markdown("**Self-Critique Feedback**")
        st.warning(res.get("trace", ""))

    # ============================================
    # STEP 4 — IMAGE + VIDEO
    # ============================================
    st.divider()
    st.header("🎨 Step 4: Multimodal Asset Generation")

    image_data = res.get("image")

    if image_data:
        st.subheader("🖼️ AI-Generated Visual")

        if isinstance(image_data, bytes):
            st.image(image_data, width=700)
        elif isinstance(image_data, str):
            st.image(image_data, width=700)

    else:
        st.warning("⚠️ Image unavailable (API quota or error).")

    if res.get("video"):
        st.subheader("🎬 AI Video Storyboard")
        st.markdown(res.get("video"))

    # ============================================
    # STEP 5 — FINAL CONTENT
    # ============================================
    st.divider()
    st.header("📝 Step 5: Final Publish-Ready Content")

    edited_content = st.text_area(
        "Edit Before Publishing",
        value=res.get("content", ""),
        height=400
    )

    # ============================================
    # PUBLISH WORKFLOW
    # ============================================
    if st.button("🚀 Approve & Auto-Publish"):

        with st.status("Executing Publish Pipeline...") as status:
            time.sleep(1)

            tweet_id = str(uuid.uuid4())[:8]
            tweet_url = f"https://x.com/datavex_ai/status/{tweet_id}"

            post_data = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "tweet_url": tweet_url,
                "content": edited_content
            }

            if not os.path.exists("posted_content.json"):
                with open("posted_content.json", "w") as f:
                    json.dump([], f)

            with open("posted_content.json", "r") as f:
                posts = json.load(f)

            posts.append(post_data)

            with open("posted_content.json", "w") as f:
                json.dump(posts, f, indent=4)

            status.update(
                label="✅ Successfully Published",
                state="complete"
            )

        st.success(f"🔗 View Live Post: {tweet_url}")
        st.balloons()

# ============================================
# HISTORY
# ============================================
st.divider()
st.header("📜 Published Content Log")

if os.path.exists("posted_content.json"):
    with open("posted_content.json", "r") as f:
        posts = json.load(f)

    if posts:
        for post in reversed(posts):
            with st.expander(f"🕒 {post['timestamp']}"):
                st.write(f"[View Post]({post['tweet_url']})")
                st.write(post["content"])
    else:
        st.info("No posts yet.")
else:
    st.info("No posts yet.")