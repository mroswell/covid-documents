#!/usr/bin/env python3
import json

with open('eua-tagged-files.json', 'r') as f:
    data = json.load(f)

xpt_files = []
jmp_files = []

for doc in data['documents']:
    if doc['fileType'] == 'XPT':
        xpt_files.append({
            'filename': doc['filename'], 
            'documentType': doc['documentType'],
            'module': doc['module']
        })
    elif doc['fileType'] == 'JMP':
        jmp_files.append({
            'filename': doc['filename'], 
            'documentType': doc['documentType'],
            'module': doc['module']
        })

# Count XPT files by documentType
xpt_types = {}
for file in xpt_files:
    doc_type = file['documentType']
    if doc_type not in xpt_types:
        xpt_types[doc_type] = []
    xpt_types[doc_type].append(file)

print(f'Total XPT files: {len(xpt_files)}')
print(f'\nXPT files by documentType:')
for doc_type, files in sorted(xpt_types.items()):
    print(f'  {doc_type}: {len(files)} files')

print(f'\nXPT files NOT tagged as Data:')
for doc_type, files in sorted(xpt_types.items()):
    if doc_type != 'Data':
        print(f'\n{doc_type} ({len(files)} files):')
        for file in files[:5]:  # Show first 5 examples
            print(f'  - {file["filename"]} (Module: {file["module"]})')
        if len(files) > 5:
            print(f'  ... and {len(files) - 5} more')

print(f'\n\nTotal JMP files: {len(jmp_files)}')
print(f'JMP files:')
for file in jmp_files:
    print(f'  - {file["filename"]} -> documentType: {file["documentType"]}')