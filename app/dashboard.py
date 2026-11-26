import os
import sys

import pandas as pd
import plotly.express as px
import streamlit as st

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from db import get_engine  # noqa: E402

st.set_page_config(page_title="ClaimVault", layout="wide")


@st.cache_data(ttl=600)
def q(sql: str) -> pd.DataFrame:
    with get_engine().connect() as conn:
        return pd.read_sql(sql, conn)


st.title("ClaimVault: Health Insurance Claims")
st.caption(
    "Medicare claims, Nov 2008 to Dec 2009. "
    "Provider fraud is a label in the dataset (potential fraud), not a proven finding."
)

# ---------- KPI cards ----------
kpi = q("""
SELECT COUNT(*)                          AS claims,
       SUM(c.claim_amount)               AS total_cost,
       AVG(c.claim_amount)               AS avg_claim,
       100.0 * SUM(c.claim_amount) FILTER (WHERE pr.potential_fraud)
             / SUM(c.claim_amount)       AS fraud_pct
FROM clean.claims c
JOIN clean.providers pr ON pr.provider_id = c.provider_id
""").iloc[0]

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total claims", f"{int(kpi.claims):,}")
c2.metric("Total reimbursed", f"${kpi.total_cost / 1e6:,.1f}M")
c3.metric("Average claim", f"${kpi.avg_claim:,.0f}")
c4.metric("Cost from flagged providers", f"{kpi.fraud_pct:.1f}%")

st.divider()

# ---------- Row 1: age and claim type ----------
left, right = st.columns(2)

age = q("""
SELECT CASE WHEN p.age < 65 THEN 'Under 65'
            WHEN p.age < 75 THEN '65-74'
            WHEN p.age < 85 THEN '75-84'
            ELSE '85+' END AS age_group,
       COUNT(DISTINCT p.patient_id) AS patients,
       SUM(c.claim_amount)          AS total_cost
FROM clean.patients p
LEFT JOIN clean.claims c ON c.patient_id = p.patient_id
GROUP BY 1
""")
age["cost_per_patient"] = age.total_cost / age.patients
order = ["Under 65", "65-74", "75-84", "85+"]
with left:
    st.subheader("Cost per patient by age group")
    fig = px.bar(age, x="age_group", y="cost_per_patient",
                 category_orders={"age_group": order},
                 labels={"age_group": "Age group", "cost_per_patient": "Cost per patient ($)"})
    st.plotly_chart(fig, width='stretch')

ctype = q("""
SELECT claim_type, COUNT(*) AS claims, SUM(claim_amount) AS total_cost
FROM clean.claims GROUP BY claim_type
""")
with right:
    st.subheader("Inpatient vs outpatient: share of claims and cost")
    ctype["claims_pct"] = 100 * ctype.claims / ctype.claims.sum()
    ctype["cost_pct"] = 100 * ctype.total_cost / ctype.total_cost.sum()
    long = ctype.melt(id_vars="claim_type", value_vars=["claims_pct", "cost_pct"],
                      var_name="measure", value_name="percent")
    long["measure"] = long.measure.map({"claims_pct": "% of claims", "cost_pct": "% of cost"})
    fig = px.bar(long, x="measure", y="percent", color="claim_type", barmode="stack",
                 labels={"percent": "Percent", "measure": ""})
    st.plotly_chart(fig, width='stretch')

# ---------- Row 2: states and monthly trend ----------
left, right = st.columns(2)

states = q("""
SELECT state_name, COUNT(*) AS patients
FROM clean.patients_by_state
GROUP BY state_name ORDER BY patients DESC LIMIT 10
""")
with left:
    st.subheader("Top 10 states by patients")
    fig = px.bar(states.sort_values("patients"), x="patients", y="state_name",
                 orientation="h", labels={"state_name": "", "patients": "Patients"})
    st.plotly_chart(fig, width='stretch')

monthly = q("""
SELECT DATE_TRUNC('month', claim_start_date)::date AS month,
       SUM(claim_amount) AS total_cost
FROM clean.claims
WHERE claim_start_date >= DATE '2009-01-01' AND claim_start_date < DATE '2009-12-01'
GROUP BY 1 ORDER BY 1
""")
with right:
    st.subheader("Monthly cost, Jan to Nov 2009")
    fig = px.line(monthly, x="month", y="total_cost", markers=True,
                  labels={"month": "Month", "total_cost": "Cost ($)"})
    st.plotly_chart(fig, width='stretch')
    st.caption("Nov 2008 and Dec 2009 are left out: the data window starts and ends mid-stream.")

# ---------- Top providers ----------
st.subheader("Top 10 providers by cost")
prov = q("""
SELECT c.provider_id AS provider,
       CASE WHEN pr.potential_fraud THEN 'Flagged' ELSE 'Not flagged' END AS fraud_label,
       COUNT(*) AS claims,
       ROUND(SUM(c.claim_amount), 0) AS total_cost
FROM clean.claims c
JOIN clean.providers pr ON pr.provider_id = c.provider_id
GROUP BY c.provider_id, pr.potential_fraud
ORDER BY total_cost DESC LIMIT 10
""")
st.dataframe(prov, width='stretch', hide_index=True)