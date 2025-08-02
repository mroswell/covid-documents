For participant mRNA-1273-P301-US377-2086, show study ID, participant ID, and which treatment group they were in
``` sql
SELECT
    STUDYID,
    USUBJID,
    COALESCE(ACTARM, 'Null') AS treatment_arm_assignment
FROM
    `FDA-CBER-2022-1614-3825109-3825910_125752_S3_M5_mrna-1273-p301_S_dm`
WHERE
    USUBJID = 'mRNA-1273-P301-US377-2086';
```
