#!/usr/bin/env python3
"""
Update navigation menus to include Pfizer BLA Navigator in alphabetical order
"""

import os
import re

def update_navigation_menu(filepath):
    """Update the navigation dropdown menu in an HTML file"""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern to find the dropdown menu
    old_pattern1 = r'(<div class="dropdown-menu">\s*)<a href="moderna-bla-navigator.html">Moderna BLA Navigator</a>\s*<a href="pfizer-eua-navigator.html">Pfizer EUA Navigator</a>'
    
    old_pattern2 = r'(<div class="dropdown-menu">\s*)<a href="moderna-bla-navigator.html">Moderna BLA Navigator</a>\s*<a href="pfizer-bla-navigator.html">Pfizer BLA Navigator</a>\s*<a href="pfizer-eua-navigator.html">Pfizer EUA Navigator</a>'
    
    # New alphabetized menu
    new_menu = r'\1<a href="moderna-bla-navigator.html">Moderna BLA Navigator</a>\n                    <a href="pfizer-bla-navigator.html">Pfizer BLA Navigator</a>\n                    <a href="pfizer-eua-navigator.html">Pfizer EUA Navigator</a>'
    
    # Check if already has all three in correct order
    if 'Moderna BLA Navigator</a>\n                    <a href="pfizer-bla-navigator.html">Pfizer BLA Navigator</a>\n                    <a href="pfizer-eua-navigator.html">Pfizer EUA Navigator' in content:
        print(f"  {os.path.basename(filepath)}: Already updated")
        return False
    
    # Try first pattern (missing Pfizer BLA)
    updated_content = re.sub(old_pattern1, new_menu, content)
    
    if updated_content == content:
        # Try second pattern (has all three but maybe wrong order)
        updated_content = re.sub(old_pattern2, new_menu, content)
    
    if updated_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        print(f"  {os.path.basename(filepath)}: Updated")
        return True
    else:
        print(f"  {os.path.basename(filepath)}: No changes needed")
        return False

def main():
    """Update all HTML files with navigation menus"""
    
    files_to_update = [
        'index.html',
        'pfizer-eua-navigator.html',
        'pfizer-bla-navigator.html',
        'moderna-bla-navigator.html',
        'moderna-bla.html',
        'data-dictionary.html',
        'about.html',
        'metadata/index.html',
        'metadata/index-cards.html'
    ]
    
    print("Updating navigation menus...")
    updated_count = 0
    
    for filepath in files_to_update:
        if os.path.exists(filepath):
            if update_navigation_menu(filepath):
                updated_count += 1
        else:
            print(f"  {filepath}: File not found")
    
    print(f"\nTotal files updated: {updated_count}")

if __name__ == "__main__":
    main()