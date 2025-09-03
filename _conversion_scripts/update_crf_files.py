#!/usr/bin/env python3
"""
Update CRF files in JSON documents to use Electronic Case Report Form (eCRF) format
with proper site and subject extraction
"""

import json
import re
import sys

def extract_moderna_info(filename):
    """Extract site and subject from Moderna CRF filename"""
    # Pattern: 125752_SXX_M5_CRF_mrna-1273-p301-usXXXXXXX.pdf
    match = re.search(r'CRF_mrna-(\d+)-p\d+-us(\d+)\.pdf', filename)
    if match:
        site = match.group(1)  # Always "1273" for mrna-1273
        subject = match.group(2)
        return site, subject
    return None, None

def extract_pfizer_info(filename):
    """Extract site and subject from Pfizer CRF filename"""
    # Pattern: PREFIX_CRF_c4591001-SITE-SITESUBJECT.pdf
    match = re.search(r'CRF_c4591001-(\d{4})-(\d{4})(\d+)\.pdf', filename)
    if match:
        site = match.group(1)
        # The subject is the combination after the site
        subject = match.group(2) + match.group(3)
        return site, subject
    return None, None

def extract_special_site(filename):
    """Extract site from special CRF filenames like CRFs-for-site-XXXX.pdf"""
    match = re.search(r'CRFs-for-site-(\d+)\.pdf', filename)
    if match:
        return match.group(1)
    return None

def update_crf_document(doc):
    """Update a single document if it contains CRF in filename"""
    filename = doc.get('filename', '')
    
    # Skip annotated CRF files (acrf)
    if 'acrf' in filename.lower():
        return doc
    
    # Check if this is a CRF file
    if 'CRF' in filename:
        # Update documentType
        doc['documentType'] = 'Electronic Case Report Form (eCRF)'
        
        # Check for special case files
        special_site = extract_special_site(filename)
        if special_site:
            doc['title'] = f'Electronic Case Report Forms (Site: {special_site})'
        else:
            # Try to extract site and subject based on pattern
            site = None
            subject = None
            
            # Check if it's a Moderna file
            if 'mrna-1273' in filename:
                site, subject = extract_moderna_info(filename)
            # Check if it's a Pfizer file
            elif 'c4591001' in filename:
                site, subject = extract_pfizer_info(filename)
            
            # Update title if we found site and subject
            if site and subject:
                doc['title'] = f'Electronic Case Report Form (Site: {site}; Subject: {subject})'
            elif 'CRF' in filename:
                # Generic update for CRF files without clear pattern
                doc['title'] = 'Electronic Case Report Form (eCRF)'
        
        # Update tags
        if 'tags' in doc:
            updated_tags = []
            for tag in doc['tags']:
                if tag == 'CRF':
                    updated_tags.append('Case Report Form (CRF)')
                elif tag == 'eCRF':
                    updated_tags.append('Electronic Case Report Form (eCRF)')
                elif tag == 'eCRF Audit Trail':
                    updated_tags.append('Electronic Case Report Form (eCRF) Audit Trail')
                else:
                    updated_tags.append(tag)
            doc['tags'] = updated_tags
    
    # Also update tags even if CRF is not in filename
    elif 'tags' in doc:
        updated_tags = []
        for tag in doc['tags']:
            if tag == 'CRF' or tag == 'crf':
                updated_tags.append('Case Report Form (CRF)')
            elif tag == 'eCRF':
                updated_tags.append('Electronic Case Report Form (eCRF)')
            else:
                updated_tags.append(tag)
        doc['tags'] = updated_tags
    
    return doc

def update_json_file(filepath):
    """Update all CRF documents in a JSON file"""
    print(f"Processing {filepath}...")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Track statistics
        updated_count = 0
        total_count = len(data['documents'])
        
        # Update each document
        for i, doc in enumerate(data['documents']):
            original_title = doc.get('title', '')
            updated_doc = update_crf_document(doc)
            if updated_doc.get('title', '') != original_title or \
               updated_doc.get('documentType', '') == 'Electronic Case Report Form (eCRF)':
                updated_count += 1
                # Show a few examples
                if updated_count <= 3:
                    print(f"  Example: {doc.get('filename', '')}")
                    print(f"    New title: {updated_doc.get('title', '')}")
        
        # Write back to file
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"  Updated {updated_count} of {total_count} documents")
        return updated_count
        
    except Exception as e:
        print(f"  Error: {e}")
        return 0

def main():
    """Main function to update all JSON files"""
    files_to_update = [
        'moderna-tagged-files.json',
        'pfizer-eua-tagged-files.json',
        'pd-bla-tagged-files.json'
    ]
    
    total_updated = 0
    
    for filepath in files_to_update:
        updated = update_json_file(filepath)
        total_updated += updated
    
    print(f"\nTotal documents updated: {total_updated}")

if __name__ == "__main__":
    main()