#!/usr/bin/env python3
"""
Script to populate clinicalTrial values in pd-bla-tagged-files.json
Extracts clinical trial IDs from filenames using pattern c4591XXX
"""

import json
import re
from pathlib import Path

def extract_clinical_trial_id(filename):
    """
    Extract clinical trial ID from filename.
    Looks for pattern c4591XXX where XXX is 3 digits.
    """
    # Pattern to match c4591 followed by 3 digits
    pattern = r'c4591(\d{3})'
    match = re.search(pattern, filename, re.IGNORECASE)
    
    if match:
        # Return the full trial ID
        return f"c4591{match.group(1)}"
    
    return None

def main():
    # Path to the JSON file
    json_file = Path("pd-bla-tagged-files.json")
    
    # Read the JSON file
    print(f"Reading {json_file}...")
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Statistics
    total_docs = len(data['documents'])
    updated_count = 0
    trial_counts = {}
    
    print(f"Processing {total_docs} documents...")
    
    # Process each document
    for doc in data['documents']:
        filename = doc.get('filename', '')
        
        # Extract clinical trial ID
        trial_id = extract_clinical_trial_id(filename)
        
        if trial_id:
            doc['clinicalTrial'] = trial_id
            updated_count += 1
            
            # Track counts for statistics
            trial_counts[trial_id] = trial_counts.get(trial_id, 0) + 1
    
    # Save the updated JSON
    print(f"\nSaving updated data to {json_file}...")
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    # Print statistics
    print(f"\n✅ Update complete!")
    print(f"Total documents: {total_docs}")
    print(f"Documents updated: {updated_count}")
    print(f"Documents without trial ID: {total_docs - updated_count}")
    
    print(f"\nClinical trial distribution:")
    for trial_id, count in sorted(trial_counts.items()):
        print(f"  {trial_id}: {count} documents")

if __name__ == "__main__":
    main()