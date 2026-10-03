# SentinelIQ — Risk, Fraud & Regulatory Intelligence Copilot

**Hackathon:** Snowflake CoCo CLI Hackathon 2026 — GCC Edition
**Problem statement:** Risk, Fraud and Regulatory Intelligence Copilot

All entities, customers, and data below are entirely fictional/synthetic and not modeled on any real institution.

## 1. The problem

A generic bank/NBFC's risk and compliance team investigates fraud and files regulatory reports by manually stitching together transaction logs, KYC records, and free-text case notes across spreadsheets and SQL. It's slow, inconsistent, and hard to audit.

## 2. The solution

A conversational copilot that:
- Answers risk questions in plain English by combining structured transaction data with unstructured case notes
- Drafts audit-ready compliance summaries with citations back to source rows/documents
- Recommends a next action (escalate / request more docs / close as false positive) and logs the decision trail

## 3. Architecture

```
┌─────────────────────────┐
│   Streamlit Chat UI      │  ← analyst-facing front end
└────────────┬─────────────┘
             │
┌────────────▼─────────────┐
│   Cortex Agent            │  ← orchestrates the two tools below
│   (SENTINELIQ_AGENT)      │
└──────┬─────────────┬──────┘
       │             │
┌──────▼──────┐ ┌────▼─────────────┐
│ Cortex       │ │ Cortex Analyst    │
│ Search       │ │ (Semantic View)   │
│ (case notes) │ │ (transactions)    │
└──────┬──────┘ └────┬─────────────┘
       │             │
┌──────▼─────────────▼──────┐
│  Snowflake tables           │
│  ACCOUNTS_TXN, CUSTOMER_KYC,│
│  CASE_NOTES                 │
└──────────────────────────────┘
```

## 4. Data model (synthetic)

| Table | Purpose | Key columns |
|---|---|---|
| `ACCOUNTS_TXN` | Transaction ledger | txn_id, account_id, amount, timestamp, merchant_category, channel, geography, txn_type |
| `CUSTOMER_KYC` | Onboarding/profile data | account_id, customer_name (fictional), risk_tier, onboarding_date, doc_status |
| `CASE_NOTES` | Free-text dispute/fraud narratives | case_id, account_id, note_text, created_date |

## 5. Demo script (Grand Finale)

1. **Combined query:** "Show accounts with unusual transaction velocity this week that also have case notes mentioning delivery disputes." → agent routes across both tools, returns ranked list with evidence.
2. **Drill-down:** click one account → copilot drafts a compliance-style summary citing exact transaction rows and note excerpts.
3. **Action:** copilot suggests next action (escalate/request docs/close) and logs the decision.
4. **Trust proof:** ask the same underlying question a second way, phrased differently — show the answer and citations are consistent.

## 6. Differentiator

Most teams will build a generic "chat with your data" demo. SentinelIQ's edge is the **audit trail**: every answer shows exactly which transaction rows and case-note excerpts produced it — which is what real risk/compliance workflows actually require, not just a nice chatbot.

## 7. Build order

1. Snowflake trial account (AWS, US region, Enterprise edition)
2. Install & connect CoCo CLI
3. Generate synthetic dataset (CoCo prompt)
4. Create Cortex Search service over `CASE_NOTES`
5. Create semantic view over `ACCOUNTS_TXN`
6. Create `SENTINELIQ_AGENT` combining both
7. Test agent from the CLI
8. Scaffold Streamlit chat UI (CoCo-generated)
9. Deploy via `snow streamlit deploy`
10. Record demo video + write up submission

See `SentinelIQ_CoCo_Prompts.md` for the exact prompts for steps 3–9, and `streamlit_app.py` for the UI starting point.

## 8. Submission checklist

- [ ] Public repo with CoCo prompts / any custom code documented
- [ ] Short demo video walking through the script in section 5
- [ ] Written summary tying back to the problem statement and the audit-trail differentiator
- [ ] Confirm exact submission requirements once the GCC edition's prototype submission portal opens (Sept 13–Oct 4, 2026 window)
