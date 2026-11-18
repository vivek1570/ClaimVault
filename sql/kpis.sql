-- KPI 1: patients and cost by age group
SELECT CASE WHEN age < 65 THEN 'Under 65'
            WHEN age < 75 THEN '65-74'
            WHEN age < 85 THEN '75-84'
            ELSE '85+' END AS age_group,
       COUNT(DISTINCT p.patient_id) AS patients,
       ROUND(SUM(c.claim_amount), 0) AS total_cost
FROM clean.patients p
LEFT JOIN clean.claims c ON c.patient_id = p.patient_id
GROUP BY age_group
ORDER BY age_group;

-- KPI 2: inpatient vs outpatient
SELECT claim_type,
       COUNT(*) AS claims,
       ROUND(SUM(claim_amount), 0) AS total_cost,
       ROUND(AVG(claim_amount), 0) AS avg_claim
FROM clean.claims
GROUP BY claim_type;

-- KPI 3: top 10 providers by cost, with fraud flag
SELECT c.provider_id, pr.potential_fraud,
       COUNT(*) AS claims,
       ROUND(SUM(c.claim_amount), 0) AS total_cost
FROM clean.claims c
JOIN clean.providers pr ON pr.provider_id = c.provider_id
GROUP BY c.provider_id, pr.potential_fraud
ORDER BY total_cost DESC
LIMIT 10;

-- KPI 4: share of total cost from flagged providers
SELECT ROUND(100.0 * SUM(c.claim_amount) FILTER (WHERE pr.potential_fraud)
             / SUM(c.claim_amount), 1) AS fraud_cost_pct
FROM clean.claims c
JOIN clean.providers pr ON pr.provider_id = c.provider_id;