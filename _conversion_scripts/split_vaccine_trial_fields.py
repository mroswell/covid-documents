#!/usr/bin/env python3
import json
import re

def extract_vaccine_candidates(text):
    """Extract vaccine candidates from text, return as list"""
    candidates = []
    
    # Define patterns for each vaccine candidate
    patterns = {
        'BNT162b2': r'BNT162[Bb]2',
        'BNT162b1': r'BNT162[Bb]1',
        'BNT162a1': r'BNT162[Aa]1',
        'BNT162b3c': r'BNT162[Bb]3[Cc]',
        'BNT162c2': r'BNT162[Cc]2'
    }
    
    for candidate, pattern in patterns.items():
        if re.search(pattern, text, re.IGNORECASE):
            candidates.append(candidate)
    
    return candidates if candidates else None

def extract_clinical_trial(text):
    """Extract clinical trial from text"""
    # Check for clinical trials
    if 'C4591001' in text:
        return 'C4591001'
    elif 'C4591011' in text:
        return 'C4591011'
    elif re.search(r'BNT162-01|bnt162-01', text):
        return 'BNT162-01'
    
    return None

# Read the JSON file
with open('eua-tagged-files.json', 'r') as f:
    data = json.load(f)

# Statistics
vaccine_stats = {}
trial_stats = {}
multi_vaccine_count = 0

# Process each document
for document in data['documents']:
    # Combine filename, title, and tags for searching
    search_text = document['filename'] + ' ' + document.get('title', '') + ' ' + ' '.join(document.get('tags', []))
    
    # Extract vaccine candidates (can be multiple)
    vaccine_candidates = extract_vaccine_candidates(search_text)
    
    # Extract clinical trial (single value)
    clinical_trial = extract_clinical_trial(search_text)
    
    # Update document
    document['vaccineCandidate'] = vaccine_candidates
    document['clinicalTrial'] = clinical_trial
    
    # Update statistics
    if vaccine_candidates:
        if len(vaccine_candidates) > 1:
            multi_vaccine_count += 1
        for candidate in vaccine_candidates:
            vaccine_stats[candidate] = vaccine_stats.get(candidate, 0) + 1
    else:
        vaccine_stats['None'] = vaccine_stats.get('None', 0) + 1
    
    if clinical_trial:
        trial_stats[clinical_trial] = trial_stats.get(clinical_trial, 0) + 1
    else:
        trial_stats['None'] = trial_stats.get('None', 0) + 1

# Update statistics in the data
if 'statistics' not in data:
    data['statistics'] = {}

data['statistics']['byVaccineCandidate'] = vaccine_stats
data['statistics']['byClinicalTrial'] = trial_stats

# Write the updated data back to the file
with open('eua-tagged-files.json', 'w') as f:
    json.dump(data, f, indent=2)

print("Successfully split vaccine candidate and clinical trial fields")
print(f"\nVaccine Candidate distribution:")
for candidate, count in sorted(vaccine_stats.items()):
    print(f"  {candidate}: {count} documents")

print(f"\nClinical Trial distribution:")
for trial, count in sorted(trial_stats.items()):
    print(f"  {trial}: {count} documents")

print(f"\nDocuments with multiple vaccine candidates: {multi_vaccine_count}")