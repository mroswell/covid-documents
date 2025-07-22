# TODO List for COVID Documents Project

## Completed Tasks ✅

### Data Structure Conversion
- [x] Extract fieldDefinitions from data-dictionary.html to JSON with preserved comments
- [x] Create a JSON structure that includes comment fields (sections and inline comments)
- [x] Create conversion script for field-definitions.json to flat structure
- [x] Create conversion script for eua_tagged_files.csv to JSON
- [x] Update data-dictionary.html to load JSON dynamically
- [x] Update data-dictionary.html to use flat structure
- [x] Test that frontend works exactly the same
- [x] Organize conversion scripts into conversion_scripts/ directory

## In Progress Tasks 🔄

## Pending Tasks 📋

### Field Definitions Enhancement
- [ ] Add mandatory field information to field-definitions-flat.json
- [ ] Add codeList associations for fields that have controlled vocabularies
- [ ] Add dataType information (string, integer, date, etc.) for each field
- [ ] Add domain information for each field
- [ ] Add origin information (CRF, derived, etc.) for each field

### Data Dictionary Improvements
- [ ] Update data-dictionary.html to display additional metadata when available
- [ ] Add filtering capabilities by section, domain, or data type
- [ ] Add search highlighting in the data dictionary
- [ ] Add export functionality (export filtered results to CSV/JSON)

### EUA Tagged Files Enhancements
- [x] Update index.html to load from eua-tagged-files.json instead of CSV
- [x] Add filtering by file type and domain (extracted from filename)
- [x] Add filtering by folder, module, and date with button groups
- [x] Implement "AND" logic for all filters (must meet all selected criteria)
- [ ] Add sorting capabilities
- [ ] Implement tag-based search functionality

### Documentation
- [ ] Update CLAUDE.md with information about the new JSON files
- [ ] Document the data structure changes
- [ ] Create API documentation for the JSON structures
- [ ] Add examples of how to query the JSON data

### Data Quality
- [ ] Validate all field definitions have proper sections
- [ ] Check for duplicate field names across domains
- [ ] Verify all tags in eua-tagged-files.json are consistent
- [ ] Create a data validation script

### Future Enhancements
- [ ] Create a unified search interface across both field definitions and documents
- [ ] Add version control for field definitions (track changes over time)
- [ ] Build an API endpoint to serve the JSON data
- [ ] Create a field relationship map (which fields reference other fields)
- [ ] Add field usage statistics (which fields appear in which datasets)

## Notes

- The field-definitions-flat.json structure is designed to be extensible
- Consider creating a schema definition for both JSON files
- The conversion scripts are preserved in conversion_scripts/ for future use
- All boolean fields in eua-tagged-files.json are properly typed (not strings)