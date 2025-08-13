#!/usr/bin/env python3
"""
Script to populate vaccineCandidate values and update clinical trials in pd-bla-tagged-files.json
- Extracts vaccine candidates (BNT162b2, BNT162b1, etc.) from tags, titles, and filenames
- Adds BNT162-01 clinical trial identifier to appropriate documents
- Maps COMIRNATY to BNT162b2 since it's the brand name
- Stores multiple candidates as array when present
"""

import json
import re
from pathlib import Path

def extract_vaccine_candidates(doc):
    """
    Extract vaccine candidates from document tags, title, and filename.
    Returns a single string if one candidate, array if multiple, or None if none.
    """
    candidates = set()
    
    # Define the vaccine candidates we're looking for
    # Order matters for b3 vs b3c - check b3c first!
    vaccine_patterns = [
        ('BNT162b3c', r'bnt162b3c'),
        ('BNT162b3', r'bnt162b3(?!c)'),  # b3 NOT followed by c
        ('BNT162b2', r'(?:bnt162b2|comirnaty)'),
        ('BNT162b1', r'bnt162b1'),
        ('BNT162a1', r'bnt162a1'),
        ('BNT162c2', r'bnt162c2'),
    ]
    
    # Check tags
    tags = doc.get('tags', [])
    for tag in tags:
        tag_lower = tag.lower()
        for vaccine, pattern in vaccine_patterns:
            if re.search(pattern, tag_lower):
                candidates.add(vaccine)
    
    # Check title
    title = doc.get('title', '')
    if title:
        title_lower = title.lower()
        for vaccine, pattern in vaccine_patterns:
            if re.search(pattern, title_lower):
                candidates.add(vaccine)
    
    # Check filename
    filename = doc.get('filename', '')
    if filename:
        filename_lower = filename.lower()
        # Be careful not to confuse BNT162-01 trial with vaccine candidates
        # Only look for vaccine variants (letter + number combinations)
        for vaccine, pattern in vaccine_patterns:
            # Skip if it's part of BNT162-01 trial name
            if vaccine == 'BNT162b1' and re.search(r'bnt162-01', filename_lower):
                continue
            if re.search(pattern, filename_lower):
                candidates.add(vaccine)
    
    # Return results
    if not candidates:
        return None
    elif len(candidates) == 1:
        return list(candidates)[0]
    else:
        # Return as sorted array for consistency
        return sorted(list(candidates))

def update_clinical_trial_bnt162_01(doc):
    """
    Update clinical trial field to include BNT162-01 if present in filename.
    Returns True if updated.
    """
    filename = doc.get('filename', '')
    
    # Check for BNT162-01 trial identifier
    if re.search(r'bnt162-01', filename, re.IGNORECASE):
        # Don't overwrite existing clinical trial, just update if it's null
        if doc.get('clinicalTrial') is None:
            doc['clinicalTrial'] = 'BNT162-01'
            return True
    
    return False

def main():
    # Path to the JSON file
    json_file = Path("pd-bla-tagged-files.json")
    
    # Read the JSON file
    print(f"Reading {json_file}...")
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Statistics
    total_docs = len(data['documents'])
    vaccine_updated_count = 0
    trial_updated_count = 0
    vaccine_counts = {}
    multi_vaccine_count = 0
    
    print(f"Processing {total_docs} documents...")
    
    # Process each document
    for doc in data['documents']:
        # Update vaccine candidate(s)
        vaccines = extract_vaccine_candidates(doc)
        if vaccines:
            doc['vaccineCandidate'] = vaccines
            vaccine_updated_count += 1
            
            # Track statistics
            if isinstance(vaccines, list):
                multi_vaccine_count += 1
                for v in vaccines:
                    vaccine_counts[v] = vaccine_counts.get(v, 0) + 1
            else:
                vaccine_counts[vaccines] = vaccine_counts.get(vaccines, 0) + 1
        
        # Update clinical trial for BNT162-01
        if update_clinical_trial_bnt162_01(doc):
            trial_updated_count += 1
    
    # Save the updated JSON
    print(f"\nSaving updated data to {json_file}...")
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    # Print statistics
    print(f"\n✅ Update complete!")
    print(f"\nVaccine Candidates:")
    print(f"  Total documents: {total_docs}")
    print(f"  Documents with vaccine candidate(s): {vaccine_updated_count}")
    print(f"  Documents with multiple candidates: {multi_vaccine_count}")
    print(f"  Documents without vaccine candidate: {total_docs - vaccine_updated_count}")
    
    print(f"\n  Vaccine distribution:")
    for vaccine, count in sorted(vaccine_counts.items(), key=lambda x: -x[1]):
        print(f"    {vaccine}: {count} documents")
    
    print(f"\nClinical Trials:")
    print(f"  BNT162-01 trial documents added: {trial_updated_count}")

if __name__ == "__main__":
    main()