import streamlit as st
from engine import run_growth_engine

st.set_page_config(page_title="DataVex Growth Engine", layout="wide")

st.title("🚀 DataVex Growth Intelligence Engine")
st.markdown("Autonomous Signal → Strategy → Content System")

# User Input
keyword = st.text_input("🔎 Enter Keyword to Research Signal:")

if st.button("Run AI Growth Engine"):

    if keyword.strip() == "":
        st.warning("Please enter a keyword.")
    else:
        with st.spinner("Agents are working..."):

            result = run_growth_engine(keyword)

        # ---- SHOW AGENT TRACE ----
        st.subheader("🧠 Agent Trace")

        st.write("### 🛰️ Scout Agent Output")
        st.info(result["signal"])

        st.write("### 🧠 Brain Agent Decision")
        st.success(result["brain"])

        # ---- GENERATED CONTENT ----
        st.subheader("✍️ Generated Content")

        edited_content = st.text_area(
            "You can edit before posting:",
            value=result["content"],
            height=400
        )

        # ---- APPROVE BUTTON ----
        if st.button("✅ Approve & Post"):
            st.success("🎉 Content Approved and Posted Successfully!")
            st.balloons()