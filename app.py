import streamlit as st
from agent.research_agent import research

st.set_page_config(
    page_title="Secure Enterprise AI Research Agent",
    page_icon="🔐",
    layout="wide"
)

st.title("🔐 Secure Enterprise AI Research Agent")
st.caption("Authorization-aware enterprise research assistant")

st.sidebar.header("User")

user_id = st.sidebar.selectbox(
    "Select user",
    ["U102", "U205", "U301"]
)

st.sidebar.info(
    "Only documents authorized for the selected user "
    "are provided to the research workflow."
)

st.header("Ask a question")

query = st.text_input(
    "Enter your question",
    placeholder="What is the Q4 revenue forecast?"
)

if st.button("Search"):
    if not query.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Researching authorized information..."):
            result = research(user_id, query)

        if result["status"] == "no_accessible_evidence":
            st.warning(result["answer"])

            st.error("🔒 Authorization: DENIED")
            st.write("LLM evidence: None")
            st.write("Restricted content was not provided to the LLM.")

        else:
            st.success("Answer found")

            st.subheader("Answer")
            st.write(result["answer"])

            st.subheader("Sources")

            for source in result["sources"]:
                st.write(
                    f"**{source['document_id']}** — "
                    f"{source['title']} "
                    f"(v{source['version']}, "
                    f"{source['effective_date']})"
                )

            st.subheader("Security")
            st.success("✅ Authorization: ALLOWED")

            evidence_ids = [
                source["document_id"]
                for source in result["sources"]
            ]

            st.write(
                f"LLM evidence: {', '.join(evidence_ids)}"
            )

            st.caption(
                "Only authorized evidence is supplied to the AI workflow."
            )