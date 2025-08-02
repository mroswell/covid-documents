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
Of course. Here are several useful queries to generate demographic reports from that dataset, starting with simple breakdowns and moving to more detailed views.

-----

### 1\. Breakdown by Sex

This query counts the number of male and female participants.

```sql
SELECT
    SEX,
    count(*) AS number_of_subjects
FROM
    `FDA-CBER-2022-1614-3825109-3825910_125752_S3_M5_mrna-1273-p301_S_dm`
GROUP BY
    SEX;
```

-----

### 2\. Breakdown by Race

This query shows the racial composition of the trial participants.

```sql
SELECT
    RACE,
    count(*) AS number_of_subjects
FROM
    `FDA-CBER-2022-1614-3825109-3825910_125752_S3_M5_mrna-1273-p301_S_dm`
GROUP BY
    RACE
ORDER BY
    number_of_subjects DESC;
```

-----

### 3\. Breakdown by Ethnicity

This query provides a count of participants by their specified ethnicity.

```sql
SELECT
    ETHNIC,
    count(*) AS number_of_subjects
FROM
    `FDA-CBER-2022-1614-3825109-3825910_125752_S3_M5_mrna-1273-p301_S_dm`
GROUP BY
    ETHNIC
ORDER BY
    number_of_subjects DESC;
```

-----

### 4\. Age Distribution

This query groups participants into common age brackets to give a clear picture of the age distribution.

```sql
SELECT
    CASE
        WHEN AGE < 18 THEN 'Under 18'
        WHEN AGE BETWEEN 18 AND 64 THEN '18-64 years'
        WHEN AGE >= 65 THEN '65 years and over'
        ELSE 'Not Reported'
    END AS age_group,
    count(*) as number_of_subjects
FROM
    `FDA-CBER-2022-1614-3825109-3825910_125752_S3_M5_mrna-1273-p301_S_dm`
GROUP BY
    age_group
ORDER BY
    age_group;
```

-----

### 5\. Participants by Treatment Arm and Race

This is a more advanced query that cross-references the treatment arm (e.g., placebo vs. vaccine) with the race of the participants. This is useful for seeing the demographic breakdown of each experimental group.

```sql
SELECT
    ARM,
    RACE,
    count(*) as number_of_subjects
FROM
    `FDA-CBER-2022-1614-3825109-3825910_125752_S3_M5_mrna-1273-p301_S_dm`
GROUP BY
    ARM,
    RACE
ORDER BY
    ARM,
    number_of_subjects DESC;
```
