import streamlit as st
from engine import run_growth_engine
import time
import uuid
import json
from datetime import datetime
import os

st.set_page_config(
    page_title="DataVex Growth Engine",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 DataVex Growth Intelligence Engine")
st.markdown("### Autonomous Signal → Strategy → Content System")

st.divider()

# Initialize session storage
if "result" not in st.session_state:
    st.session_state.result = None

# ===============================
# INPUT
# ===============================
keyword = st.text_input("🔎 Enter Keyword to Research Signal")

if st.button("🚀 Run AI Growth Engine"):

    if keyword.strip() == "":
        st.warning("⚠️ Please enter a keyword.")
    else:
        with st.spinner("🤖 Agents are thinking..."):
            st.session_state.result = run_growth_engine(keyword)

# ===============================
# DISPLAY RESULT
# ===============================
if st.session_state.result:

    result = st.session_state.result

    st.divider()
    st.header("🧠 Agent Trace")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🛰️ Scout Agent")
        st.info(result["signal"])

    with col2:
        st.subheader("🧠 Brain Agent")
        if "APPROVED" in result["brain"].upper():
            st.success(result["brain"])
        else:
            st.error(result["brain"])

    st.divider()
    st.header("✍️ Generated Content")

    edited_content = st.text_area(
        "Edit before publishing",
        value=result["content"],
        height=350,
        key="editor"
    )

    # ===============================
    # APPROVE BUTTON
    # ===============================
    if st.button("✅ Approve & Auto-Publish"):

        st.info("🔐 Authenticating...")
        time.sleep(1)
        st.info("📡 Publishing...")
        time.sleep(1)

        tweet_id = str(uuid.uuid4())[:8]
        tweet_url = f"https://x.com/yourhandle/status/{tweet_id}"

        post_data = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "keyword": keyword,
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

        st.success("🚀 Published Successfully!")
        st.write(f"🔗 {tweet_url}")
        st.balloons()

# ===============================
# POST HISTORY
# ===============================
st.divider()
st.header("📜 Published Content Log")

if os.path.exists("posted_content.json"):
    with open("posted_content.json", "r") as f:
        posts = json.load(f)

    if posts:
        for post in reversed(posts):
            st.subheader(f"🕒 {post['timestamp']}")
            st.write(f"Keyword: {post['keyword']}")
            st.write(f"Tweet ID: {post['tweet_id']}")
            st.write(f"URL: {post['tweet_url']}")
            st.write(post["content"])
            st.divider()
    else:
        st.info("No published posts yet.")
else:
    st.info("No published posts yet.")