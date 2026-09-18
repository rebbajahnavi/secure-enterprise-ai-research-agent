import streamlit as st
from auth.rbac import ROLE_PERMISSIONS, get_role_level
from agent.research_agent import research
from services.security_audit import load_security_audit

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

user_role = st.sidebar.selectbox(
    "User Role",
    ["Intern", "Manager", "HR Admin", "System Admin"]
)

user_info = {
    "U102": ("Finance", "Internal"),
    "U205": ("Marketing", "Internal"),
    "U301": ("Finance", "Internal")
}

department, clearance = user_info[user_id]

st.sidebar.write(f"**Department:** {department}")
st.sidebar.write(f"**Clearance:** {clearance}")
st.sidebar.write(f"**Role:** {user_role}")
st.sidebar.write(
    f"**Access Level:** {get_role_level(user_role)}"
)

st.sidebar.write("**Permissions:**")

for permission in ROLE_PERMISSIONS[user_role]:
    st.sidebar.write(f"• {permission}")

st.sidebar.info(
    "Only documents authorized for the selected user "
    "are provided to the research workflow."
)

tab1, tab2 = st.tabs([
    "🔎 Research Agent",
    "🛡️ Admin Console"
])

with tab1:
    st.header("Ask a question")

    query = st.text_input(
        "Enter your question",
        placeholder="What is the Q4 revenue forecast?"
    )

    if st.button("🔍 Search"):
        if not query.strip():
            st.warning("Please enter a question.")
        else:
            with st.spinner("Researching authorized information..."):
                result = research(
                    user_id,
                    query,
                    user_role
                )

            st.divider()

            if result["status"] == "security_violation":
                st.subheader("🚨 Security Decision")
                st.error("SECURITY VIOLATION")

                col1, col2 = st.columns(2)

                with col1:
                    st.write("**Authorization:** BLOCKED")

                with col2:
                    st.write("**LLM Evidence:** None")

                st.warning(result["answer"])

                st.caption(
                    f"Violation Type: "
                    f"{result['violation_type']}"
                )

                st.caption(
                    "The request was blocked before the "
                    "LLM was called."
                )

            elif result["status"] == "no_accessible_evidence":
                st.subheader("🔒 Security Decision")
                st.error("ACCESS DENIED")

                col1, col2 = st.columns(2)

                with col1:
                    st.write("**Authorization:** DENIED")

                with col2:
                    st.write("**LLM Evidence:** None")

                st.warning(result["answer"])

                st.caption(
                    "Restricted document content was not "
                    "provided to the AI workflow."
                )

            else:
                st.subheader("✅ Answer")
                st.write(result["answer"])

                st.subheader("📚 Authorized Sources")

                for source in result["sources"]:
                    st.write(
                        f"**{source['document_id']}** — "
                        f"{source['title']} "
                        f"(v{source['version']}, "
                        f"{source['effective_date']})"
                    )

                st.subheader("🔐 Security Decision")

                col1, col2 = st.columns(2)

                with col1:
                    st.success(
                        "AUTHORIZATION: ALLOWED"
                    )

                with col2:
                    evidence_ids = [
                        source["document_id"]
                        for source in result["sources"]
                    ]

                    st.info(
                        f"LLM Evidence: "
                        f"{', '.join(evidence_ids)}"
                    )

                st.caption(
                    "Only authorized evidence is supplied "
                    "to the AI workflow."
                )

with tab2:
    st.header("🛡️ Admin Security Console")

    if user_role not in ["HR Admin", "System Admin"]:
        st.warning(
            "Admin Console is intended for authorized "
            "administrative roles."
        )
    else:
        audit_df = load_security_audit()

        if audit_df.empty:
            st.info(
                "No blocked security attempts "
                "have been recorded."
            )
        else:
            attempt_counts = (
                audit_df["User Role"]
                .value_counts()
                .to_dict()
            )

            audit_df["Risk Score"] = audit_df[
                "User Role"
            ].apply(
                lambda role: (
                    "HIGH"
                    if attempt_counts.get(role, 0) > 3
                    else "NORMAL"
                )
            )

            st.subheader("Security Audit Log")

            st.dataframe(
                audit_df,
                use_container_width=True,
                hide_index=True
            )

            st.subheader("Risk Summary")

            for role, count in attempt_counts.items():
                if count > 3:
                    st.error(
                        f"{role}: HIGH RISK — "
                        f"{count} blocked attempts"
                    )
                else:
                    st.success(
                        f"{role}: {count} blocked "
                        f"attempt(s)"
                    )