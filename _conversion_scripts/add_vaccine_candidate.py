#!/usr/bin/env python3
import json
import re

def extract_vaccine_candidate(document):
    """Extract vaccine candidate from filename, title, or tags"""
    
    # Combine filename, title, and tags for searching
    search_text = (document.get('filename', '') + ' ' + 
                   document.get('title', '') + ' ' + 
                   ' '.join(document.get('tags', [])))
    
    # Define patterns in order of specificity
    patterns = [
        # Most specific patterns first
        (r'BNT162[Bb]2', 'BNT162b2 (Main candidate)'),
        (r'BNT162[Bb]1', 'BNT162b1 (Alternative candidate)'),
        (r'BNT162B3C', 'BNT162B3C (Variant)'),
        (r'BNT162-01', 'BNT162-01 (Early phase trial)'),
        (r'C4591011', 'C4591011 (Related study)'),
        (r'C4591001', 'C4591001 (Main clinical study)'),
        # General pattern last
        (r'BNT162(?![BbC\-])', 'BNT162 (General platform)')
    ]
    
    # Check each pattern
    for pattern, label in patterns:
        if re.search(pattern, search_text, re.IGNORECASE):
            return label
    
    # No pattern found
    return None

# Read the JSON file
with open('eua-tagged-files.json', 'r') as f:
    data = json.load(f)

# Count occurrences for reporting
candidate_counts = {}

# Add vaccineCandidate field to each document
for document in data['documents']:
    vaccine_candidate = extract_vaccine_candidate(document)
    document['vaccineCandidate'] = vaccine_candidate
    
    # Count for reporting
    if vaccine_candidate:
        candidate_counts[vaccine_candidate] = candidate_counts.get(vaccine_candidate, 0) + 1
    else:
        candidate_counts['None'] = candidate_counts.get('None', 0) + 1

# Write the updated data back to the file
with open('eua-tagged-files.json', 'w') as f:
    json.dump(data, f, indent=2)

# Report results
print("Successfully added vaccineCandidate field to all documents")
print("\nVaccine candidate distribution:")
for candidate, count in sorted(candidate_counts.items(), key=lambda x: x[1], reverse=True):
    print(f"  {candidate}: {count} documents")