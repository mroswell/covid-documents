# TODO List for Data Dictionary

## Completed Tasks ✅

### Data Structure Conversion
- [x] Extract fieldDefinitions from data-dictionary.html to JSON with preserved comments
- [x] Create a JSON structure that includes comment fields (sections and inline comments)
- [x] Create conversion script for field-definitions.json to flat structure
- [x] Update data-dictionary.html to load JSON dynamically
- [x] Update data-dictionary.html to use flat structure
- [x] Test that frontend works exactly the same
- [x] Add navigation menu to data-dictionary.html

## In Progress Tasks 🔄

## Pending Tasks 📋

### Field Definitions Enhancement
- [ ] Add mandatory field information to field-definitions-flat.json
- [ ] Add codeList associations for fields that have controlled vocabularies
- [ ] Add dataType information (string, integer, date, etc.) for each field
- [ ] Add domain information for each field
- [ ] Add origin information (CRF, derived, etc.) for each field

### Data Dictionary UI Improvements
- [ ] Update data-dictionary.html to display additional metadata when available
- [ ] Add filtering capabilities by section, domain, or data type
- [ ] Add search highlighting in the data dictionary
- [ ] Add export functionality (export filtered results to CSV/JSON)
- [ ] Add column sorting functionality
- [ ] Add tooltips for technical terms

### Data Quality
- [ ] Validate all field definitions have proper sections
- [ ] Check for duplicate field names across domains
- [ ] Create a data validation script for field definitions
- [ ] Add data quality indicators to the UI

### Future Enhancements
- [ ] Add version control for field definitions (track changes over time)
- [ ] Create a field relationship map (which fields reference other fields)
- [ ] Add field usage statistics (which fields appear in which datasets)
- [ ] Add comparison view between different CDISC versions
- [ ] Create a field dependency visualization

## Notes

- The field-definitions-flat.json structure is designed to be extensible
- Consider creating a JSON Schema definition for validation
- Field definitions follow CDISC standards (SDTM and ADaM)