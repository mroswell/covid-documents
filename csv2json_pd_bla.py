#!/usr/bin/env python3
"""
Convert pd_bla_tagged_files CSV to JSON format matching the structure of moderna-tagged-files.json
and eua-tagged-files.json
"""

import csv
import json
from datetime import datetime
import sys

def parse_people_mentioned(people_str):
    """Parse people_mentioned field into a list"""
    if not people_str or people_str.strip() == '':
        return []
    # Split by comma and clean up whitespace
    return [p.strip() for p in people_str.split(',') if p.strip()]

def parse_tags(tags_str):
    """Parse tags field into a list"""
    if not tags_str or tags_str.strip() == '':
        return []
    # Tags appear to be comma-separated
    return [tag.strip() for tag in tags_str.split(',') if tag.strip()]

def parse_boolean(value):
    """Parse boolean string values"""
    if value is None or value == '':
        return False
    return value.lower() in ['true', 'yes', '1']

def extract_year_from_date(date_str):
    """Extract year from various date formats"""
    if not date_str or date_str == 'undated':
        return None
    
    # Try to extract just the year if it's in YYYY-MM-DD or YYYY-MM format
    if len(date_str) >= 4:
        year = date_str[:4]
        if year.isdigit():
            return year
    
    return date_str  # Return as-is if we can't parse it

def convert_csv_to_json(csv_file, json_file):
    """Convert CSV file to JSON format"""
    documents = []
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            # Extract file type from extension
            file_extension = row.get('file_extension', '').upper()
            if not file_extension and '.' in row['filename']:
                file_extension = row['filename'].split('.')[-1].upper()
            
            # Build document object matching the JSON structure
            doc = {
                'filename': row['filename'],
                'title': row.get('title', ''),
                'date': extract_year_from_date(row.get('date', '')),
                'googleDriveLink': row.get('google_drive_link', ''),
                'folder': row.get('folder', ''),
                'fileType': file_extension,
                'pageCount': int(row.get('page_count', 0)) if row.get('page_count', '').isdigit() else 0,
                'module': row.get('modules', '') if row.get('modules', '') else None,
                'documentType': row.get('document_type', '').replace('-', ' ').title() if row.get('document_type') else None,
                'peopleMentioned': parse_people_mentioned(row.get('people_mentioned', '')),
                'tags': parse_tags(row.get('tags', '')),
                'hasExemption': parse_boolean(row.get('has_exemption')),
                'hasExclusion': parse_boolean(row.get('has_exclusion')),
                'passwordProtected': parse_boolean(row.get('password_protected')),
                'processed': parse_boolean(row.get('processed', 'true')),  # Default to true if not specified
                'vaccineCandidate': None,  # Not in CSV, set to null like in other JSONs
                'clinicalTrial': None  # Not in CSV, set to null like in other JSONs
            }
            
            # Add CRF and Protocol fields if they exist
            if 'has_crf' in row:
                doc['hasCRF'] = parse_boolean(row['has_crf'])
            if 'has_protocol' in row:
                doc['hasProtocol'] = parse_boolean(row['has_protocol'])
            
            documents.append(doc)
    
    # Create the final JSON structure
    output = {
        'documents': documents
    }
    
    # Write to JSON file
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"Conversion complete. {len(documents)} documents converted.")
    print(f"Output saved to: {json_file}")

if __name__ == "__main__":
    csv_file = "pd_bla_tagged_files_20250812_011628.csv"
    json_file = "pd-bla-tagged-files.json"
    
    try:
        convert_csv_to_json(csv_file, json_file)
    except Exception as e:
        print(f"Error during conversion: {e}")
        sys.exit(1)