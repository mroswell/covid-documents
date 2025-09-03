#!/usr/bin/env python3
import json

def proper_case(text):
    """Convert text to proper case (capitalize first letter of each word)"""
    if not text:
        return text
    return ' '.join(word.capitalize() for word in text.split())

# Read the JSON file
with open('eua-tagged-files.json', 'r') as f:
    data = json.load(f)

# Update all documentType values to proper case
for document in data['documents']:
    if 'documentType' in document and document['documentType']:
        document['documentType'] = proper_case(document['documentType'])

# Write the updated data back to the file
with open('eua-tagged-files.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Successfully updated all documentType values to proper case")