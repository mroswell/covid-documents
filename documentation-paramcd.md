# PARAMCD (Parameter Code) Documentation

## Overview
PARAMCD is a standardized 8-character parameter code variable used in the ADSYMPT (COVID-19 Signs and Symptoms) dataset to uniquely identify different types of clinical measurements, symptoms, and events related to COVID-19 illness.

## Variable Definition
- **Variable Name**: PARAMCD
- **Label**: Parameter Code
- **Type**: Character
- **Length**: 8
- **Dataset**: ADSYMPT

## PARAMCD Values and Definitions

### COVID-19 Symptoms
| PARAMCD | PARAM Description | Category |
|---------|-------------------|----------|
| CHILLS | Chills | Signs and Symptoms of Disease |
| DIARRHEA | Diarrhea | Signs and Symptoms of Disease |
| FEVER | Fever | Signs and Symptoms of Disease |
| NLTSTSML | New Loss of Taste or Smell | Signs and Symptoms of Disease |
| NCOUG | New or Increased Cough | Signs and Symptoms of Disease |
| NMUSPN | New or Increased Muscle Pain | Signs and Symptoms of Disease |
| NSTBRTH | New or Increased Shortness of Breath | Signs and Symptoms of Disease |
| NSRTHROT | New or Increased Sore Throat | Signs and Symptoms of Disease |
| VOMIT | Vomiting | Signs and Symptoms of Disease |
| LSTSTSML | Loss of Taste/Smell | Signs and Symptoms of Disease |
| NNSLCONG | New or Increased Nasal Congestion | Signs and Symptoms of Disease |
| NNSLDSCH | New or Increased Nasal Discharge | Signs and Symptoms of Disease |
| SPUTPROD | New or Increased Sputum Production | Signs and Symptoms of Disease |
| WHEEZ | New or Increased Wheezing | Signs and Symptoms of Disease |
| FATIGUE | Fatigue | Signs and Symptoms of Disease |
| HEADACHE | Headache | Signs and Symptoms of Disease |
| NAUSEA | Nausea | Signs and Symptoms of Disease |
| RIHNRA | Rhinorrhoea | Signs and Symptoms of Disease |

### Severe COVID-19 Clinical Events
| PARAMCD | PARAM Description | Source Domain |
|---------|-------------------|---------------|
| SARDFN | Significant Acute Renal Dysfunction | CE (Clinical Events) |
| SAHDFN | Significant Acute Hepatic Dysfunction | CE (Clinical Events) |
| SANDFN | Significant Acute Neurologic Dysfunction | CE (Clinical Events) |

### Vital Signs and Measurements
| PARAMCD | PARAM Description | Source Domain |
|---------|-------------------|---------------|
| RESP | Respiratory Rate | VS (Vital Signs) |
| HR | Heart Rate | VS (Vital Signs) |
| OXYSAT | Oxygen Saturation | VS (Vital Signs) |
| DIABP | Diastolic Blood Pressure | VS (Vital Signs) |
| SYSBP | Systolic Blood Pressure | VS (Vital Signs) |
| PO2FIO2 | PO2/FIO2 Ratio | LB (Laboratory) |

### Medical Interventions and Treatments
| PARAMCD | PARAM Description | Category |
|---------|-------------------|----------|
| VSOPRES | Vasopressor Agents | Concomitant Medications |
| INTBTION | Intubation | Respiratory Support |
| NIPPV | Non-Invasive Positive Pressure Ventilation | Respiratory Support |
| CPAP | Continuous Positive Airway Pressure | Respiratory Support |
| OXYTHRP | Oxygen Therapy | Respiratory Support |
| MCHVENT | Mechanical Ventilation | Respiratory Support |
| ECMO | Extracorporeal Membrane Oxygenation | Respiratory Support |
| HFOXTHRP | High Flow Oxygen Therapy | Respiratory Support |

### Other Clinical Parameters
| PARAMCD | PARAM Description | Source Domain |
|---------|-------------------|---------------|
| DEATH | Death | DS (Disposition) |
| HCUICU | Subject in ICU due to potential COVID-19 illness | HO (Hospitalization) |
| C19NIG | COVID-19 Nucleocapsid IgG | IS (Immunogenicity Specimen) |
| SARSCOV2 | Severe Acute Resp Syndrome Coronavirus 2 | MB (Microbiology) |
| RTCOV2NS | Cepheid RT-PCR Assay for SARS-CoV-2 | MB (Microbiology) |

## Usage Notes

1. **Parameter Assignment**: Each unique clinical measurement or event is assigned a specific PARAMCD value based on the source data and clinical meaning.

2. **Corresponding Variables**: 
   - PARAMCD is always used in conjunction with PARAM (full parameter description)
   - PARAMN provides the numeric ordering for parameters

3. **Data Sources**: Parameters are derived from multiple SDTM domains including:
   - CE (Clinical Events)
   - CM (Concomitant Medications)
   - DS (Disposition)
   - FA (Findings About)
   - HO (Hospitalization)
   - IS (Immunogenicity Specimen)
   - LB (Laboratory)
   - MB (Microbiology)
   - PR (Procedures)
   - VS (Vital Signs)

4. **Character Limit**: All PARAMCD values must be 8 characters or less due to SAS variable length restrictions.

5. **Standardization**: These codes provide a standardized way to identify parameters across different analyses and outputs.

## Related Variables
- **PARAM**: Full parameter description
- **PARAMN**: Numeric parameter code for sorting
- **PARCAT1**: Parameter Category 1
- **PARCAT2**: Parameter Category 2
- **AVAL**: Analysis Value (numeric)
- **AVALC**: Analysis Value (character)

## Version History
- Created for C4591001 COVID-19 vaccine efficacy study
- Last updated: Based on adsympt.sas program dated 17Nov2020
