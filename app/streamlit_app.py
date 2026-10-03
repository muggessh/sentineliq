"""
SentinelIQ — Risk, Fraud & Regulatory Intelligence Copilot
Streamlit UI scaffold (for Streamlit in Snowflake)

This is a STRUCTURAL starting point, not a finished integration.
Have CoCo CLI generate the real agent-call wiring (see step 6 in
SentinelIQ_CoCo_Prompts.md) — it introspects your actual deployed
SENTINELIQ_AGENT and will produce correct, current API calls.
Use this file for the UX layout, session state, and demo flow, and
drop CoCo's agent-calling code into `call_sentineliq_agent()` below.

All data referenced here is synthetic (see SentinelIQ_CoCo_Prompts.md,
step 1). Nothing in this app should be wired to real institution data.
"""

import streamlit as st
from snowflake.snowpark.context import get_active_session

st.set_page_config(page_title="SentinelIQ", page_icon="🛡️", layout="wide")
session = get_active_session()

AGENT_FQN = "RISKCOPILOT_DB.RISK.SENTINELIQ_AGENT"
DECISION_LOG_TABLE = "RISKCOPILOT_DB.RISK.DECISION_LOG"

# ---------------------------------------------------------------------------
# Session state
# ---------------------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []  # list of {role, content, citations}
if "flagged_account" not in st.session_state:
    st.session_state.flagged_account = None


# ---------------------------------------------------------------------------
# Agent call — REPLACE with CoCo-generated integration
# ---------------------------------------------------------------------------
def call_sentineliq_agent(question: str) -> dict:
    """
    Call SENTINELIQ_AGENT and return a dict like:
        {
            "answer": "...",
            "citations": [
                {"source": "ACCOUNTS_TXN", "detail": "txn_id=..., amount=..."},
                {"source": "CASE_NOTES", "detail": "case_id=..., excerpt=..."},
            ],
        }

    TODO: Replace this stub with the real call CoCo generates for your
    deployed agent (typically via the Cortex Agents REST API, called
    through Streamlit-in-Snowflake's built-in request helper, or via
    a SQL wrapper CoCo creates around the agent). Ask CoCo:

        "Show me the exact code this app should use to call
         RISKCOPILOT_DB.RISK.SENTINELIQ_AGENT from Streamlit in Snowflake"

    and paste the result in here.
    """
    raise NotImplementedError(
        "Wire this up to SENTINELIQ_AGENT — see the docstring above."
    )


def log_decision(account_id: str, action: str, analyst_note: str) -> None:
    """Append an analyst decision to the audit log table."""
    session.sql(
        f"""
        INSERT INTO {DECISION_LOG_TABLE}
            (account_id, action, analyst_note, decided_at)
        SELECT ?, ?, ?, CURRENT_TIMESTAMP()
        """,
        params=[account_id, action, analyst_note],
    ).collect()


# ---------------------------------------------------------------------------
# Sidebar — flagged account drill-down
# ---------------------------------------------------------------------------
with st.sidebar:
    st.header("🛡️ SentinelIQ")
    st.caption("Risk, Fraud & Regulatory Intelligence Copilot")
    st.divider()

    st.subheader("Flag an account for review")
    account_id = st.text_input("Account ID")
    if st.button("Generate compliance summary", disabled=not account_id):
        with st.spinner("Drafting summary..."):
            result = call_sentineliq_agent(
                f"Generate a compliance-style summary for account {account_id}, "
                f"citing the exact transactions and case notes involved."
            )
        st.session_state.flagged_account = {"id": account_id, "result": result}

    flagged = st.session_state.flagged_account
    if flagged:
        st.markdown(f"**Account:** {flagged['id']}")
        st.markdown(flagged["result"]["answer"])
        st.markdown("**Evidence:**")
        for c in flagged["result"]["citations"]:
            st.markdown(f"- `{c['source']}` — {c['detail']}")

        st.markdown("**Suggested next action**")
        action = st.selectbox(
            "Action",
            ["Escalate", "Request more documentation", "Close as false positive"],
            label_visibility="collapsed",
        )
        note = st.text_area("Analyst note", height=80)
        if st.button("Log decision"):
            log_decision(flagged["id"], action, note)
            st.success("Decision logged to audit trail.")


# ---------------------------------------------------------------------------
# Main chat panel
# ---------------------------------------------------------------------------
st.title("Ask SentinelIQ")
st.caption(
    "Ask about transaction patterns, case notes, or combined risk signals. "
    "All data is synthetic."
)

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("citations"):
            with st.expander("Evidence / citations"):
                for c in msg["citations"]:
                    st.markdown(f"- `{c['source']}` — {c['detail']}")

if question := st.chat_input(
    "e.g. Which accounts had unusual transaction velocity this week that "
    "also have case notes mentioning delivery disputes?"
):
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                result = call_sentineliq_agent(question)
                st.markdown(result["answer"])
                if result.get("citations"):
                    with st.expander("Evidence / citations"):
                        for c in result["citations"]:
                            st.markdown(f"- `{c['source']}` — {c['detail']}")
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": result["answer"],
                        "citations": result.get("citations", []),
                    }
                )
            except NotImplementedError as e:
                st.warning(str(e))
