#!/usr/bin/env python3
"""
Add Moderna BLA Navigator to the dropdown menu on all pages
"""
import os
import re

# Files to update
files = [
    '../index.html',
    '../pfizer-eua-navigator.html',
    '../moderna-bla-navigator.html',
    '../data-dictionary.html',
    '../about.html',
    '../metadata/index.html'
]

def update_navigation(file_path):
    """Add Moderna BLA Navigator to dropdown menu"""
    
    # Read the file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if Moderna BLA Navigator is already in the dropdown
    if 'moderna-bla-navigator.html' in content:
        print(f"  {file_path} already has Moderna BLA Navigator")
        return
    
    # Pattern to find the dropdown menu with Pfizer EUA Navigator
    pattern = r'(<a href="[./]*pfizer-eua-navigator\.html">Pfizer EUA Navigator</a>)'
    
    # Determine the correct path prefix based on file location
    if 'metadata/' in file_path:
        moderna_path = '../moderna-bla-navigator.html'
    else:
        moderna_path = 'moderna-bla-navigator.html'
    
    # Replace with both navigators
    replacement = r'\1\n                    <a href="' + moderna_path + '">Moderna BLA Navigator</a>'
    
    # Apply the replacement
    new_content = re.sub(pattern, replacement, content)
    
    if new_content != content:
        # Write the updated content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"  ✓ Updated {file_path}")
    else:
        print(f"  ⚠️  Could not update {file_path} - pattern not found")

# Main execution
print("Adding Moderna BLA Navigator to dropdown menus...")
for file_path in files:
    if os.path.exists(file_path):
        update_navigation(file_path)
    else:
        print(f"  File not found: {file_path}")

print("\nDone!")