# SentinelIQ — CoCo CLI Build Script

Run these in order inside a `cortex` session. Paste each block as-is, let CoCo finish before moving to the next.

## 0. Install & connect

```bash
curl -LsS https://ai.snowflake.com/static/cc-scripts/install.sh | sh   # macOS/Linux
# irm https://ai.snowflake.com/static/cc-scripts/install.ps1 | iex     # Windows PowerShell
cortex --version
cortex
```
Complete the connection wizard (choose AWS/US trial account), then confirm with `/status`.

## 1. Generate the synthetic dataset

```
Set up a database RISKCOPILOT_DB with schema RISK and warehouse RISKCOPILOT_WH (X-Small).

Generate and load synthetic data into three tables. All data must be entirely fictional.

Table 1: ACCOUNTS_TXN (500 rows)
Columns: txn_id, account_id, amount, timestamp, merchant_category, channel, geography, txn_type
- amounts ranging $5 to $25,000
- channels: online, POS, ATM, wire
- txn_type: purchase, refund, transfer, withdrawal
- IMPORTANT: all timestamps must fall within the last 90 days relative to CURRENT_DATE() (not a fixed historical range), so "this week"/"this month" queries always resolve to real rows regardless of when the demo runs
- include a deliberate subset (~5%) of accounts with a genuine velocity spike: 8-15 transactions clustered within a single 48-hour window in the last 14 days, clearly standing out against that account's normal baseline of 1-2 transactions/week, so the demo has something real to find

Table 2: CUSTOMER_KYC (100 rows)
Columns: account_id, customer_name (fictional names only), risk_tier (low/medium/high), onboarding_date, doc_status (verified/pending/expired)

Table 3: CASE_NOTES (80 rows)
Columns: case_id, account_id, note_text, created_date
- note_text: realistic 2-4 sentence fraud/dispute narratives (e.g. "customer reports unauthorized transaction," "merchant dispute — goods not delivered," "suspected account takeover")
- created_date must also fall within the last 90 days relative to CURRENT_DATE(), for the same reason as ACCOUNTS_TXN
- make sure some CASE_NOTES reference account_ids that also appear in the velocity-spike subset above, so combined queries return real matches

After loading, enable change tracking on CASE_NOTES.
```

Verify:
```
How many rows are in RISKCOPILOT_DB.RISK.ACCOUNTS_TXN, CUSTOMER_KYC, and CASE_NOTES?
```

## 2. Create the Cortex Search service (unstructured layer)

```
Create a Cortex Search service called CASE_NOTES_SEARCH on note_text in RISKCOPILOT_DB.RISK.CASE_NOTES
with attributes account_id, created_date using warehouse RISKCOPILOT_WH
```

## 3. Create the semantic view (structured layer)

```
Create a semantic view for the RISKCOPILOT_DB.RISK.ACCOUNTS_TXN table
```
Accept the defaults when prompted for naming/location.

## 4. Create the agent

```
Create an agent called SENTINELIQ_AGENT in RISKCOPILOT_DB.RISK that uses the CASE_NOTES_SEARCH
cortex search service and the accounts_txn semantic view. In the agent's orchestration/response
instructions, specify: "Do not narrate your reasoning steps to the user; return only the final
answer with citations." This keeps the chat UI clean for a live demo instead of exposing
intermediate planning/narration.
```

## 5. Test it

```
Chat with agent RISKCOPILOT_DB.RISK.SENTINELIQ_AGENT and ask:
Which accounts had unusual transaction velocity this week that also have case notes mentioning delivery disputes?
```
```
Ask the agent: What objections or issues came up in case notes for high-risk-tier customers?
```
```
Ask the agent the same question two different ways and confirm the numbers match:
1) "What is the total refund amount this month?"
2) "How much have we refunded customers so far this month?"
```

## 6. Scaffold the Streamlit UI

```
Build a Streamlit app called sentineliq_app that provides a chat interface to SENTINELIQ_AGENT.
Requirements:
- Show inline citations/evidence (source transaction rows or case note excerpts) under each answer
- Let the user click a flagged account to generate a compliance-style summary with citations
- Include a "suggested next action" field (escalate / request more docs / close as false positive) with a way to log the analyst's decision back to a DECISION_LOG table
- Use Snowflake-branded theming
```
CoCo will generate `streamlit_app.py` (and any supporting files) wired to your account. Compare it against the scaffold in `streamlit_app.py` in this folder — use CoCo's version for the real agent-call wiring since it introspects your actual deployed agent, and borrow structure/UX ideas from the scaffold if useful.

## 7. Deploy

```bash
snow streamlit deploy
```
The app appears in Snowsight under Projects → Streamlit with a shareable URL.

## 8. Useful follow-ups while polishing

```
/plan
```
Turns on plan mode so CoCo shows you each step before running it — useful once you're editing an existing setup instead of building from scratch, so you don't accidentally overwrite the agent or tables.

```
/rewind
```
Roll back if a prompt takes CoCo in the wrong direction.
