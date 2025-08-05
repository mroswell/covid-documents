#!/usr/bin/env python3
"""
Convert moderna_tagged_files.csv to match the structure of eua_tagged_files.csv
and generate moderna-tagged-files.json for the file navigator
"""
import csv
import json
import re
import os

def extract_module_from_text(filename, tags):
    """Extract module (M1, M2, etc.) from filename or tags"""
    # Check filename for module pattern
    module_match = re.search(r'[_\s]M(\d+)[_\s]', filename, re.IGNORECASE)
    if module_match:
        return f"M{module_match.group(1)}"
    
    # Check tags for module mentions
    if tags:
        tag_list = tags.split(',')
        for tag in tag_list:
            if re.match(r'^\s*M\d+\s*$', tag.strip()):
                return tag.strip()
    
    # Default to M5 for clinical data
    return "M5"

def convert_file_extension(ext):
    """Convert file extension to file type format"""
    if ext.startswith('.'):
        ext = ext[1:]
    return ext.upper()

def convert_processed_flag(flag):
    """Convert 0/1 to True/False"""
    return str(flag) == "1"

def clean_tags(tags):
    """Clean and standardize tags"""
    if not tags:
        return ""
    # Split by comma, clean each tag, and rejoin
    tag_list = [tag.strip() for tag in tags.split(',') if tag.strip()]
    return ", ".join(tag_list)

def parse_people_mentioned(people_str):
    """Parse people mentioned string into list"""
    if not people_str or people_str.strip() == "":
        return []
    # Split by common delimiters
    people = re.split(r'[,;]', people_str)
    return [person.strip() for person in people if person.strip()]

def convert_moderna_csv():
    """Main conversion function"""
    input_file = "../moderna_tagged_files.csv"
    output_csv = "../moderna-tagged-files.csv"
    output_json = "../moderna-tagged-files.json"
    
    # Read the input CSV
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    # Convert each row to match eua_tagged_files structure
    converted_rows = []
    json_documents = []
    
    for row in rows:
        # Create converted row for CSV
        converted_row = {
            'filename': row['filename'],
            'title': row['title'],
            'date': row['date'],
            'google_drive_link': row['google_drive_link'],
            'folder': row['folder'],
            'file_type': convert_file_extension(row['file_extension']),
            'page_count': row['page_count'],
            'module': extract_module_from_text(row['filename'], row.get('tags', '')),
            'document_type': row['document_type'],
            'people_mentioned': row['people_mentioned'],
            'tags': clean_tags(row['tags']),
            'has_exemption': 'False',  # Default value
            'has_exclusion': 'False',  # Default value
            'password_protected': row['password_protected'],
            'processed': str(convert_processed_flag(row.get('claude_parse_flag', 0)))
        }
        converted_rows.append(converted_row)
        
        # Create JSON document
        json_doc = {
            'filename': row['filename'],
            'title': row['title'],
            'date': row['date'],
            'googleDriveLink': row['google_drive_link'],
            'folder': row['folder'],
            'fileType': convert_file_extension(row['file_extension']),
            'pageCount': int(row['page_count']) if row['page_count'] else 0,
            'module': extract_module_from_text(row['filename'], row.get('tags', '')),
            'documentType': row['document_type'],
            'peopleMentioned': parse_people_mentioned(row['people_mentioned']),
            'tags': [tag.strip() for tag in row['tags'].split(',') if tag.strip()] if row['tags'] else [],
            'hasExemption': False,
            'hasExclusion': False,
            'passwordProtected': row['password_protected'].lower() == 'true',
            'processed': convert_processed_flag(row.get('claude_parse_flag', 0)),
            'vaccineCandidate': 'mRNA-1273',
            'clinicalTrial': 'COVE'  # Primary Moderna trial name
        }
        json_documents.append(json_doc)
    
    # Write the converted CSV
    with open(output_csv, 'w', newline='', encoding='utf-8') as f:
        fieldnames = [
            'filename', 'title', 'date', 'google_drive_link', 'folder',
            'file_type', 'page_count', 'module', 'document_type',
            'people_mentioned', 'tags', 'has_exemption', 'has_exclusion',
            'password_protected', 'processed'
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(converted_rows)
    
    # Write the JSON file
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump({'documents': json_documents}, f, indent=2)
    
    print(f"Conversion complete!")
    print(f"Created: {output_csv}")
    print(f"Created: {output_json}")
    print(f"Total documents converted: {len(converted_rows)}")

if __name__ == "__main__":
    # Change to scripts directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    convert_moderna_csv()