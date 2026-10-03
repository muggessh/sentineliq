# SentinelIQ — Risk, Fraud & Regulatory Intelligence Copilot

Built for the **Snowflake CoCo CLI Hackathon 2026 — GCC Edition**
Problem statement: *Risk, Fraud and Regulatory Intelligence Copilot*

All data, account names, and case narratives referenced in this project are entirely
synthetic/fictional and were generated specifically for this hackathon. Nothing here
is modeled on, or derived from, any real institution's data.

## What it does

SentinelIQ is a conversational risk & compliance copilot built on Snowflake Cortex AI.
A risk analyst asks plain-English questions ("show accounts with unusual transaction
velocity this week that also have case notes mentioning delivery disputes") and gets
back an evidence-backed answer — citing the exact transaction rows and case-note
excerpts behind it — plus a generated compliance-style summary and a logged next
action. Every answer is traceable to its source data, which is the core differentiator
versus a generic "chat with your data" demo.

## Architecture

```
Streamlit Chat UI (Streamlit in Snowflake)
        |
   Cortex Agent (SENTINELIQ_AGENT)
     /              \
Cortex Search    Cortex Analyst
(case notes)     (semantic view over transactions)
        |              |
   Snowflake tables: ACCOUNTS_TXN, CUSTOMER_KYC, CASE_NOTES
```

Full architecture, data model, and demo script: [`docs/SentinelIQ_Project_Plan.md`](docs/SentinelIQ_Project_Plan.md)

## How it was built

The entire backend — database, synthetic data generation, Cortex Search service,
semantic view, and the Cortex Agent itself — was built conversationally using
**Snowflake CoCo CLI**. The exact sequence of prompts used is documented step by
step in [`docs/SentinelIQ_CoCo_Prompts.md`](docs/SentinelIQ_CoCo_Prompts.md),
covering:

1. Synthetic dataset generation (transactions, KYC, case notes)
2. Cortex Search service over unstructured case notes
3. Semantic view over structured transaction data
4. Cortex Agent combining both tools
5. Testing and validation
6. Streamlit UI scaffolding
7. Deployment via `snow streamlit deploy`

## App

[`app/streamlit_app.py`](app/streamlit_app.py) — the Streamlit-in-Snowflake front end:
chat interface to the Cortex Agent, evidence/citation display, account drill-down,
compliance-summary generation, and a decision-logging audit trail.

## Deployed prototype

See submission form / shared app link.

## Tech stack

- Snowflake Cortex AI (Cortex Search, Cortex Analyst, Cortex Agents)
- Snowflake CoCo CLI
- Streamlit in Snowflake (warehouse runtime)
- Synthetic data generated via CoCo CLI
