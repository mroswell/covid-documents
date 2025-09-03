#!/usr/bin/env python3
import os
import re

# CSS for dropdown menu
dropdown_css = '''        
        /* Dropdown styles */
        .nav-menu .dropdown {
            position: relative;
        }
        
        .nav-menu .dropdown-toggle {
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 5px;
        }
        
        .nav-menu .dropdown-toggle::after {
            content: '▼';
            font-size: 0.8em;
        }
        
        .nav-menu .dropdown-menu {
            position: absolute;
            top: 100%;
            left: 0;
            background: white;
            border: 1px solid #e9ecef;
            border-radius: 4px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            min-width: 200px;
            display: none;
            z-index: 1000;
            margin-top: 5px;
        }
        
        .nav-menu .dropdown:hover .dropdown-menu {
            display: block;
        }
        
        .nav-menu .dropdown-menu a {
            display: block;
            padding: 10px 15px;
            color: #495057;
            text-decoration: none;
            border-bottom: none !important;
        }
        
        .nav-menu .dropdown-menu a:hover {
            background: #f8f9fa;
            color: #0066cc;
        }
'''

# Files to update
files = [
    'index.html',
    'pfizer-eua-navigator.html', 
    'data-dictionary.html',
    'about.html',
    'metadata/index.html'
]

for file_path in files:
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        continue
        
    print(f"Updating {file_path}...")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Add dropdown CSS before closing style tag
    if '.nav-menu .dropdown' not in content:
        # Find the last closing style tag before the nav menu
        style_pattern = r'(</style>\s*</head>)'
        content = re.sub(style_pattern, dropdown_css + r'\1', content)
    
    # Update navigation menu - handle both relative and absolute paths
    if 'metadata/index.html' in file_path:
        # For metadata/index.html, use ../ paths
        old_nav = r'<li><a href="../index.html">Home</a></li>'
        new_nav = '''<li><a href="../index.html">Home</a></li>
            <li class="dropdown">
                <a href="#" class="dropdown-toggle">File Navigator</a>
                <div class="dropdown-menu">
                    <a href="../pfizer-eua-navigator.html">Pfizer EUA Navigator</a>
                </div>
            </li>'''
    else:
        # For root level files
        old_nav = r'<li><a href="index.html"[^>]*>Home</a></li>'
        new_nav = '''<li><a href="index.html">Home</a></li>
            <li class="dropdown">
                <a href="#" class="dropdown-toggle">File Navigator</a>
                <div class="dropdown-menu">
                    <a href="pfizer-eua-navigator.html">Pfizer EUA Navigator</a>
                </div>
            </li>'''
    
    # Replace navigation
    content = re.sub(old_nav, new_nav, content)
    
    # Special handling for index.html to mark it as active
    if file_path == 'index.html':
        content = content.replace('<li><a href="index.html">Home</a></li>', '<li><a href="index.html" class="active">Home</a></li>')
    
    # Write updated content
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"  ✓ Updated {file_path}")

print("\nAll files updated successfully!")