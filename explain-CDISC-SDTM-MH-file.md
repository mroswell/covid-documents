## FDA-CBER-2021-5683-1209276_27034_S1_M5_bnt162-01-S-mh.csv

**FDA-CBER-2021-5683**: 
- **FDA**: Food and Drug Administration
- **CBER**: Center for Biologics Evaluation and Research (handles vaccines)
- **2021-5683**: Likely a FOIA (Freedom of Information Act) request number or submission tracking number from 2021

**1209276_27034**: 
- These appear to be document or page range numbers, possibly indicating this file is from pages 1,209,276 to some later page in a massive submission

**S1**: 
- Likely "Supplement 1" or "Submission 1"

**M5**: 
- Module 5 in the CTD (Common Technical Document) format
- Module 5 specifically contains Clinical Study Reports

**bnt162-01**: 
- **BNT162**: Pfizer-BioNTech's COVID-19 vaccine development program code
- **01**: Likely refers to the first variant tested (they tested multiple candidates like BNT162b1, BNT162b2, etc.)
- Note: BNT162b2 became the approved vaccine (Comirnaty)

**S**: 
- Likely stands for "SDTM" (Study Data Tabulation Model) format

**mh**: 
- Medical History domain

So this file contains medical history data from an early Pfizer-BioNTech COVID-19 vaccine trial, formatted according to regulatory standards, and was part of a large FDA submission that was later released (probably through FOIA).

This grep output shows the header row from a medical history (MH) dataset file. Let me break down what each column represents:

## File Information:
- **FDA-CBER-2021-5683-1209276_27034_S1_M5_bnt162-01-S-mh.csv**: This appears to be a different file from your earlier examples - note it's "bnt162-01" (likely an earlier phase study) rather than "C4591001"

## Column Definitions:

**Basic Identifiers:**
- **STUDYID**: Study identifier
- **DOMAIN**: Domain (MH = Medical History)
- **USUBJID**: Unique Subject Identifier
- **MHSEQ**: Medical History Sequence Number

**MedDRA Coding Hierarchy (from most specific to most general):**
- **MHTERM**: Verbatim term - exactly what was reported/recorded
- **MHMODIFY**: Modified term (if the verbatim was adjusted)
- **MHLLT**: Lowest Level Term
- **MHLLTCD**: LLT Code
- **MHDECOD**: Preferred Term (PT) - the standard MedDRA term
- **MHPTCD**: PT Code
- **MHHLT**: High Level Term
- **MHHLTCD**: HLT Code
- **MHHLGT**: High Level Group Term
- **MHHLGTCD**: HLGT Code
- **MHBODSYS**: Body System (deprecated term for SOC)
- **MHBDSYCD**: Body System Code
- **MHSOC**: System Organ Class - the highest level
- **MHSOCCD**: SOC Code

**Timing Variables:**
- **MHSTDTC**: Start Date/Time (Character format)
- **MHENDTC**: End Date/Time (Character format)
- **MHENRTPT**: End Relative to Reference Time Point
- **MHENTPT**: End Reference Time Point

## MedDRA Hierarchy Example:
If someone reported "severe headache", it might be coded as:
- MHTERM: "severe headache" (verbatim)
- MHDECOD: "Headache" (Preferred Term)
- MHHLT: "Headaches NEC" (High Level Term)
- MHHLGT: "Neurological signs and symptoms" (High Level Group Term)
- MHSOC: "Nervous system disorders" (System Organ Class)

This structure follows CDISC SDTM (Study Data Tabulation Model) standards for clinical trial data submission to regulatory authorities.

```
% wc -l FDA-CBER-2021-5683-1209276_27034_S1_M5_bnt162-01-S-mh.csv
      48 FDA-CBER-2021-5683-1209276_27034_S1_M5_bnt162-01-S-mh.csv
```
