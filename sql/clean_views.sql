CREATE SCHEMA IF NOT EXISTS clean;

CREATE OR REPLACE VIEW clean.claims AS
SELECT "ClaimID"                                   AS claim_id,
       "BeneID"                                    AS patient_id,
       "Provider"                                  AS provider_id,
       'inpatient'                                 AS claim_type,
       NULLIF("ClaimStartDt",'')::date             AS claim_start_date,
       NULLIF("ClaimEndDt",'')::date               AS claim_end_date,
       NULLIF("AdmissionDt",'')::date              AS admission_date,
       NULLIF("DischargeDt",'')::date              AS discharge_date,
       NULLIF("InscClaimAmtReimbursed",'')::numeric(12,2) AS claim_amount
FROM bronze.raw_inpatient
UNION ALL
SELECT "ClaimID", "BeneID", "Provider", 'outpatient',
       NULLIF("ClaimStartDt",'')::date,
       NULLIF("ClaimEndDt",'')::date,
       NULL::date, NULL::date,
       NULLIF("InscClaimAmtReimbursed",'')::numeric(12,2)
FROM bronze.raw_outpatient;

CREATE OR REPLACE VIEW clean.patients AS
SELECT "BeneID"                                    AS patient_id,
       NULLIF("DOB",'')::date                      AS date_of_birth,
       NULLIF("DOD",'')::date                      AS date_of_death,
       DATE_PART('year', AGE(DATE '2009-12-31', NULLIF("DOB",'')::date))::int AS age,
       CASE "Gender" WHEN '1' THEN 'Male' WHEN '2' THEN 'Female' END AS gender,
       "State"                                     AS state,
       "County"                                    AS county,
       ("ChronicCond_Diabetes"  = '1')             AS has_diabetes,
       ("ChronicCond_Heartfailure" = '1')          AS has_heart_failure,
       ("ChronicCond_Cancer" = '1')                AS has_cancer
FROM bronze.raw_beneficiaries;

CREATE OR REPLACE VIEW clean.providers AS
SELECT "Provider" AS provider_id,
       ("PotentialFraud" = 'Yes') AS potential_fraud
FROM bronze.raw_providers;