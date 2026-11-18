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

-- KPI 5: chronic condition rates by age group
SELECT CASE WHEN age < 65 THEN 'Under 65'
            WHEN age < 75 THEN '65-74'
            WHEN age < 85 THEN '75-84'
            ELSE '85+' END AS age_group,
       COUNT(*) AS patients,
       ROUND(100.0 * AVG(has_diabetes::int), 1)      AS diabetes_pct,
       ROUND(100.0 * AVG(has_heart_failure::int), 1) AS heart_failure_pct,
       ROUND(100.0 * AVG(has_cancer::int), 1)        AS cancer_pct
FROM clean.patients
GROUP BY age_group
ORDER BY age_group;

-- KPI 6: gender split and cost per patient
SELECT p.gender,
       COUNT(DISTINCT p.patient_id) AS patients,
       ROUND(SUM(c.claim_amount), 0) AS total_cost,
       ROUND(SUM(c.claim_amount) / COUNT(DISTINCT p.patient_id), 0) AS cost_per_patient
FROM clean.patients p
LEFT JOIN clean.claims c ON c.patient_id = p.patient_id
GROUP BY p.gender;

-- KPI 7: average hospital stay (inpatient only)
SELECT ROUND(AVG(discharge_date - admission_date), 1) AS avg_stay_days,
       MAX(discharge_date - admission_date)            AS longest_stay_days
FROM clean.claims
WHERE claim_type = 'inpatient';

-- KPI 8: monthly claims and cost
SELECT DATE_TRUNC('month', claim_start_date)::date AS month,
       COUNT(*) AS claims,
       ROUND(SUM(claim_amount), 0) AS total_cost
FROM clean.claims
WHERE claim_start_date IS NOT NULL
GROUP BY month
ORDER BY month;