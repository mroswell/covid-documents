#!/usr/bin/env python3
import json

# Read the JSON file
with open('eua-tagged-files.json', 'r') as f:
    data = json.load(f)

# Counter for updated files
updated_count = 0
file_types_updated = {'XPT': 0, 'JMP': 0}

# Update documentType for all XPT and JMP files
for document in data['documents']:
    if document['fileType'] in ['XPT', 'JMP']:
        old_type = document['documentType']
        document['documentType'] = 'Dataset'
        updated_count += 1
        file_types_updated[document['fileType']] += 1
        print(f"Updated: {document['filename']} from '{old_type}' to 'Dataset'")

# Write the updated data back to the file
with open('eua-tagged-files.json', 'w') as f:
    json.dump(data, f, indent=2)

# Update statistics if they exist
if 'summary' in data and 'statistics' in data['summary']:
    stats = data['summary']['statistics']
    if 'byDocumentType' in stats:
        # Recalculate document type statistics
        doc_type_counts = {}
        for document in data['documents']:
            doc_type = document.get('documentType', 'Unknown')
            doc_type_counts[doc_type] = doc_type_counts.get(doc_type, 0) + 1
        
        stats['byDocumentType'] = doc_type_counts
        
        # Write updated statistics
        with open('eua-tagged-files.json', 'w') as f:
            json.dump(data, f, indent=2)

print(f"\nSuccessfully updated {updated_count} files to documentType: 'Dataset'")
print(f"  - XPT files: {file_types_updated['XPT']}")
print(f"  - JMP files: {file_types_updated['JMP']}")