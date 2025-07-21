First effort to review newly-released EUA documents (Source: search for `eua` at https://phmpt.org) 
These cover:
- BNT162b2: A Multi-site, Phase I/II, 2-Part, Dose-Escalation Trial Investigating the Safety and Immunogenicity of Four Prophylactic SARS-CoV-2 RNA Vaccines Against COVID-19 Using Different Dosing Regimens in Healthy Adults
- C4591001: A Phase 1/2/3 Study to Evaluate the Safety, Tolerability, Immunogenicity, and Efficacy of RNA Vaccine Candidates Against COVID-19 in Healthy Adults


### Applications
[Data Dictionary](data-dictionary.html) | [Tag Visualization](index.html)

### Documents 
[Domains](domains.txt) | [FOIA Exemptions](FOIA-exemptions.md) | [Inclusions/Exclusions](documentation/inclusion-exclusion.txt) | [Modules](modules.md) | [Parameter Codes](documentation-paramcd.md)

#### Python Programs
[process_define_xml_to_single_csv.py](process_define_xml_to_single_csv.py) | [xpt2csv.py](xpt2csv.py)

# Data

### Data Visualization of Tags (and file picker)
1. Download the CSV from this repository
2. Visit https://mroswell.github.io/eua-review
3. Upload the csv file that has used AI to tag the first 7 pages of each document
4. Click on a tag name or bar to access the files that were given those tags.

### Steps I've taken to explore this release
1. Download and unzip the two 'eua' zipfiles at https://phmpt.org/multiple-file-downloads/
2. Upload all the files to Google Drive
4. Write Python code to create tagged_eua_files.csv
5. Create web visialization of the tags. This serves as an index.
6. Write and run xpt2csv.py to export thr SAS export files to CSVs
7. Use sql-utils to convert the files to Sqllite
8. Create a Google Compute Engine virtual machine with a virtual environment to view all 158 tables in Datasette
9. Build a data dictionary, using the XML files and SAS code and internet research to inform the field descriptions and (developing) code values
10. Use a trial version of JMP to export JMP fiors to csv

### Data Dictionary

https://mroswell.github.io/eua-review/data-dictionary.html

### Related Documentation that can provide insight into data variables
- Study Data Tabulation Model: https://www.cdisc.org/system/files/members/standard/foundational/SDTM_v2.0.pdf
- Analysis Data Reviewer Guide - BLA Analysis for Participants ≥16 Years of Age BioNTech SE and PFIZER INC.
Study C4591001: https://phmpt.org/wp-content/uploads/2022/03/125742_S1_M5_c4591001-A-adrg.pdf
- Analysis Data Reviewer’s Guide - ModernaTX, Inc. Study mRNA-1273-P201 Part A: https://phmpt.org/wp-content/uploads/2025/05/125752_S3_M5_mrna-1273-p201-add1_A_D_adrg.pdf
- https://phmpt.org/wp-content/uploads/2022/05/125742_S1_M5_bnt162-01-A-adrg.pdf
- https://rpodcast.quarto.pub/pilot4-webassembly-adrg/
- Create addv dataset (SAS) https://phmpt.org/wp-content/uploads/2023/09/125742-45_S211_M5_c4591001-A_1mth-P-addv-sas.pdf
- Create adsl dataset (SAS): https://phmpt.org/wp-content/uploads/2022/03/FDA-CBER-2021-5683-0022867-to-0023006_125742_S1_M5_c4591001-A-P-adsl-sas.txt
- Create adc19ef-ve-cov-7pd2-wo-sg-eval (SAS): https://phmpt.org/wp-content/uploads/2022/03/FDA-CBER-2021-5683-0022041-to-0022053_125742_S1_M5_c4591001-A-P-adc19ef-ve-cov-7pd2-wo-sg-eval-sas.txt
- https://phmpt.org/wp-content/uploads/2022/03/FDA-CBER-2021-5683-0022041-to-0022053_125742_S1_M5_c4591001-A-P-adc19ef-ve-cov-7pd2-wo-sg-eval-sas.txt
- create admh dataset (SAS) https://icandecide.org/wp-content/uploads/2022/03/FDA-CBER-2021-5683-0022601-to-0022617_125742_S1_M5_c4591001-A-P-admh-sas.txt
- SDTM Variables You Might Forget About: https://pharmasug.org/proceedings/2023/DS/PharmaSUG-2023-DS-054.pdf
- Practical Guide to Creating ADaM Datasets for Cross-over Studies: https://www.lexjansen.com/pharmasug/2019/DS/PharmaSUG-2019-DS-196.pdf
- CDISC Standards RDF REference Guide Final https://www.cdisc.org/system/files/members/standard/foundational/rdf/CDISC%20Standards%20RDF%20Reference%20Guide%201.0%20Final%202015-06-18.pdf
- Analysis of Adverse EVEnts: https://leg.colorado.gov/sites/default/files/html-attachments/h_bus_2022a_03032022_013716_pm_committee_summary/Attachment%20C.pdf
- https://dctd.cancer.gov/research/ctep-trials/trial-development
- SAP - https://cdn.clinicaltrials.gov/large-docs/28/NCT04368728/SAP_001.pdf
- https://rdrr.io/cran/pharmaversesdtm/man/suppae.html



