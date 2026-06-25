import pandas as pd
import streamlit as st

from components.esg_display import render_classified_items_table, render_dimension_chart, render_financial_health, render_score_header
from components.theme import page_setup
from mock import mock_passport
from mock.seed_smes import SEED_SME_PASSPORTS
from services import client

page_setup(title="Lender View — GreenLedger")

st.title("Lender View")
st.caption("Compare SMEs side by side, then open a Financing Passport to record your decision.")

company_names = st.session_state.get("company_names", {})


def _display_name(passport: dict) -> str:
    return company_names.get(passport["passport_id"], passport["company_name"])


# Roster = demo seed SMEs (frontend/mock/seed_smes.py) + the real pipeline company, if
# one has been created in this session via the SME flow: see frontend/PLAN.md / session notes
# for why this is session-scoped rather than a backend "list passports" endpoint.
roster = list(SEED_SME_PASSPORTS)
real_passport = st.session_state.get("passport")
if real_passport:
    roster = [real_passport] + roster

st.subheader("Compare SMEs")
rows = []
for p in roster:
    profile = p["esg_profile"]
    quality = profile.get("data_quality") or {}
    rows.append(
        {
            "Company": _display_name(p),
            "Sector": (profile.get("sector_benchmark") or {}).get("sector", "—"),
            "Green Credit Score": profile["green_credit_score"],
            "Data quality": f"{quality.get('tier', '—')} ({quality.get('confidence_pct', 0):.0f}%)" if quality else "—",
            "Requested (€)": p.get("requested_amount_eur"),
            "_passport_id": p["passport_id"],
        }
    )

table_df = pd.DataFrame(rows).sort_values("Green Credit Score", ascending=False)
st.dataframe(
    table_df.drop(columns=["_passport_id"]),
    width="stretch",
    hide_index=True,
    column_config={
        "Green Credit Score": st.column_config.NumberColumn(format="%.0f / 100"),
        "Requested (€)": st.column_config.NumberColumn(format="€%.0f"),
    },
)

OTHER_OPTION = "Other: open by Passport ID…"
roster_by_id = {p["passport_id"]: p for p in roster}
option_labels = [
    f"{r['Company']}, {r['Sector']}, {r['Green Credit Score']:.0f}/100" for r in rows
]
label_to_id = {label: r["_passport_id"] for label, r in zip(option_labels, rows)}

st.subheader("Open a Financing Passport")
choice = st.selectbox("Select an SME to review", option_labels + [OTHER_OPTION])

if choice == OTHER_OPTION:
    passport_id = st.text_input("Financing Passport ID", placeholder="e.g. GP-A1B2-C3D4")
    if not passport_id:
        st.info("Enter a Passport ID shared by an SME to review their profile.")
        st.stop()

    if st.session_state.get("lender_passport_id") != passport_id:
        try:
            fetched = client.get_passport(passport_id)
        except client.BackendUnavailable:
            st.warning(
                "Could not reach the GreenLedger backend. Showing demo passport data instead. "
                "Start the backend with `uvicorn backend.app.main:app --reload` to look up real passports."
            )
            fetched = mock_passport()
        else:
            if fetched is None:
                st.error(f"No Financing Passport found for ID '{passport_id}'.")
                st.stop()

        st.session_state["lender_passport_id"] = passport_id
        st.session_state["lender_passport"] = fetched

    passport = st.session_state["lender_passport"]
else:
    passport = roster_by_id[label_to_id[choice]]

display_name = _display_name(passport)

st.divider()
st.subheader(display_name)
st.caption(f"Passport ID: `{passport['passport_id']}`  ·  created {passport['created_at']}")

requested_amount_eur = passport.get("requested_amount_eur")
if requested_amount_eur is not None:
    st.metric("Requested financing amount", f"€{requested_amount_eur:,.2f}")

render_score_header(passport["esg_profile"])

st.subheader("Financial health")
render_financial_health(passport["financial_health"])

st.subheader("Sustainability dimensions")
render_dimension_chart(passport["esg_profile"]["dimension_scores"])

st.subheader("Classified line items")
render_classified_items_table(passport["esg_profile"]["classified_line_items"])

st.divider()
st.subheader("Lending decision")

decision_result = st.session_state.get("decision_result", {}).get(passport["passport_id"])
if decision_result:
    amount = decision_result.get("approved_amount_eur")
    amount_text = f" of €{amount:,.2f}" if amount else ""
    st.success(f"Decision recorded: **{decision_result['decision'].upper()}**{amount_text}")
else:
    with st.form("decision_form"):
        decision = st.radio("Decision", ["approve", "decline"], horizontal=True)
        approved_amount = st.number_input(
            "Approved amount (€)",
            min_value=0.0,
            value=requested_amount_eur or 0.0,
            step=1_000.0,
            help="Defaults to the SME's requested amount. Adjust if approving a different amount.",
        )
        indicative_rate = st.number_input("Indicative rate (%)", min_value=0.0, max_value=100.0, value=5.0, step=0.1)
        notes = st.text_area("Notes (optional)")
        submitted = st.form_submit_button("Submit decision", type="primary")

    if submitted:
        result = client.record_decision(
            passport["passport_id"],
            decision,
            indicative_rate=indicative_rate,
            approved_amount_eur=approved_amount if decision == "approve" else None,
            notes=notes or None,
        )
        if result is None:
            st.error("Could not record the decision. The GreenLedger backend is unreachable. Please try again once it's running.")
        else:
            st.session_state.setdefault("decision_result", {})[passport["passport_id"]] = result
            st.rerun()
