import streamlit as st
from engine import run_growth_engine

st.set_page_config(
    page_title="DataVex Growth Engine",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 DataVex Growth Intelligence Engine")
st.markdown("### Autonomous Signal → Strategy → Content System")

st.divider()

# Input Section
keyword = st.text_input("🔎 Enter Keyword to Research Signal")

if st.button("🚀 Run AI Growth Engine"):

    if keyword.strip() == "":
        st.warning("⚠️ Please enter a keyword.")
    else:
        with st.spinner("🤖 Agents are thinking..."):
            result = run_growth_engine(keyword)

        st.divider()

        # -------- AGENT TRACE SECTION --------
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

        # -------- GENERATED CONTENT --------
        st.header("✍️ Generated Content")

        edited_content = st.text_area(
            "Human-in-the-loop: Edit before posting",
            value=result["content"],
            height=400
        )

        st.divider()

        # -------- APPROVE SECTION --------
        if st.button("✅ Approve & Simulate Posting"):
            st.success("🎉 Content Approved!")

            st.write("📢 Posting to LinkedIn...")
            st.write("📢 Posting to Twitter (X)...")
            st.write("📢 Publishing Blog...")

            st.success("🚀 All platforms updated successfully!")
            st.balloons()