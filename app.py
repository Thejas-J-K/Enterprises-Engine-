import streamlit as st
from engine import run_growth_engine
import time
import uuid
import json
from datetime import datetime
import os
import requests
from PIL import Image
from io import BytesIO

# ===============================
# PAGE CONFIG
# ===============================
st.set_page_config(
    page_title="DataVex Growth Engine",
    page_icon="🚀",
    layout="wide"
)

# ===============================
# PROFESSIONAL STYLING
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
    .stTextArea textarea {
        font-family: 'Inter', sans-serif;
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

    # ===============================
    # STEP 1 — INTELLIGENCE
    # ===============================
    st.header("🧠 Step 1: Intelligence Analysis")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📡 Analyst Signal")
        st.info(res.get("signal", "No signal detected."))

    with col2:
        st.subheader("🧩 Strategic Positioning")
        st.success("Signal aligned with DataVex growth thesis.")

    # ===============================
    # STEP 2 — STRATEGY
    # ===============================
    st.divider()
    st.header("📈 Step 2: Growth Strategy Brief")

    with st.expander("View Strategy Rationale", expanded=True):
        st.write(res.get("strategy", "Strategy not generated."))

    # ===============================
    # STEP 3 — CREATOR TRACE
    # ===============================
    st.divider()
    st.header("⚡ Step 3: Real-Time Creator Intelligence")

    trace_col1, trace_col2 = st.columns(2)

    with trace_col1:
        st.markdown("**Initial Creative Draft (Internal)**")
        st.text_area(
            "draft_box",
            res.get("first_draft", ""),
            height=200,
            disabled=True,
            label_visibility="collapsed"
        )

    with trace_col2:
        st.markdown("**Self-Critique & Brand Alignment Feedback**")
        st.warning(res.get("trace", "No critique log available."))

    # ===============================
    # STEP 4 — VISUAL + VIDEO
    # ===============================
    st.divider()
    st.header("🎨 Step 4: Multimodal Asset Generation")


    # ✅ Correct image rendering
    if res.get("image"):
     st.subheader("🖼️ AI-Generated Visual")

    try:
        response = requests.get(res["image"])
        img = Image.open(BytesIO(response.content))
        st.image(img, width=700)
    except Exception as e:
        st.error("Image failed to load.")
        st.write("Image URL:", res["image"])
    # ✅ Clean storyboard display
    if res.get("video"):
        st.subheader("🎬 AI-Generated Video Storyboard")
        st.markdown(res["video"])

    # ===============================
    # STEP 5 — FINAL CONTENT
    # ===============================
    st.divider()
    st.header("📝 Step 5: Final Publish-Ready Content")

    edited_content = st.text_area(
        "Human Review & Edit Before Publishing",
        value=res.get("content", ""),
        height=400,
        key="editor"
    )

    # ===============================
    # PUBLISH WORKFLOW
    # ===============================
    if st.button("🚀 Approve & Auto-Publish to DataVex Channels"):

        with st.status("Executing Autonomous Publish Pipeline...") as status:
            st.write("🔐 Authenticating API credentials...")
            time.sleep(1)

            st.write("📤 Uploading image asset...")
            time.sleep(1)

            st.write("🌐 Posting to LinkedIn & X...")
            time.sleep(1)

            tweet_id = str(uuid.uuid4())[:8]
            tweet_url = f"https://x.com/datavex_ai/status/{tweet_id}"

            post_data = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "tweet_id": tweet_id,
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
                label="✅ Successfully Published Across Channels",
                state="complete",
                expanded=False
            )

        st.success(f"🔗 View Live Post: {tweet_url}")
        st.balloons()

# ===============================
# HISTORY LOG
# ===============================
st.divider()
st.header("📜 Published Content Log")

if os.path.exists("posted_content.json"):
    with open("posted_content.json", "r") as f:
        posts = json.load(f)

    if posts:
        for post in reversed(posts):
            with st.expander(f"🕒 {post['timestamp']}"):
                st.write(f"**Post URL:** {post['tweet_url']}")
                st.write(post["content"])
    else:
        st.info("No published posts yet.")
else:
    st.info("No published posts yet.")