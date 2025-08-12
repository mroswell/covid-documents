# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview
This repository analyzes COVID-19 vaccine clinical trial documents released under Emergency Use Authorization (EUA). It processes data from BNT162b2 (Pfizer-BioNTech) and C4591001 trials, converting clinical data formats into accessible CSV/SQLite formats with web-based visualization.

## Key Commands

### Data Processing
```bash
# Convert SAS XPT files to CSV (processes subdirectories)
python xpt2csv.py

# Convert CDISC Define-XML metadata to CSV
python definexml2csv.py
```

### Web Interfaces
- Open `index.html` for the interactive document tag browser (D3.js visualization)
- Open `data-dictionary.html` for the data dictionary viewer

## Architecture & Code Structure

### Core Scripts
- **xpt2csv.py**: Converts SAS transport files (.xpt) to CSV format
  - Uses pandas to read XPT files
  - Processes files in subdirectories
  - Handles large clinical trial datasets

- **definexml2csv.py**: Parses CDISC Define-XML metadata
  - Extracts dataset and variable definitions
  - Creates structured CSV output from XML metadata

### Data Standards
The project works with CDISC-compliant clinical trial data:
- **SDTM** (Study Data Tabulation Model): Raw clinical data
- **ADaM** (Analysis Data Model): Analysis-ready datasets
- **Define-XML**: Metadata describing datasets and variables

### Web Components
- **index.html**: Uses D3.js to create an interactive visualization of tagged documents from `pfizer-eua-tagged-files.csv`
- **data-dictionary.html**: Displays field definitions from `fda_field_dictionary.csv`

### Key Data Files
- `pfizer-eua-tagged-files.csv`: AI-generated tags for document navigation
- `fda_field_dictionary.csv`: Field definitions for understanding clinical data
- `CDISC-Domain-definitions.csv`: Standard domain definitions
- `variables_report.csv`: Analysis of variables across datasets

## Development Notes

### Dependencies
- Python: pandas, lxml, tqdm
- JavaScript: D3.js, PapaParse (included via CDN in HTML files)

### Data Processing Workflow
1. Clinical trial data arrives in XPT format (SAS transport files)
2. `xpt2csv.py` converts these to CSV for easier analysis
3. Define-XML files provide metadata about the datasets
4. `definexml2csv.py` extracts this metadata into searchable format
5. Web interfaces provide interactive exploration of the processed data

### Working with Clinical Data
- XPT files contain the actual clinical trial observations
- Define-XML files describe what each variable means
- Domain files follow CDISC standards (e.g., AE for Adverse Events, DM for Demographics)
- Variable names follow standard conventions (e.g., USUBJID for unique subject identifier)