#!/usr/bin/env python3
"""
Script to extract JSON arrays from markdown files and create separate .json files.
Removes the JSON arrays from the original markdown files.
"""

import os
import json
import re
from pathlib import Path

def process_markdown_file(filepath):
    """Process a single markdown file, extracting JSON and cleaning the markdown."""
    print(f"Processing: {filepath}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the JSON array at the end of the file
    # Look for pattern: optional whitespace, then [ ... ] at the end
    json_pattern = r'\n\s*(\[.*\])\s*$'
    match = re.search(json_pattern, content, re.DOTALL)
    
    if not match:
        print(f"  No JSON array found in {filepath}")
        return False
    
    json_content = match.group(1)
    
    # Validate JSON
    try:
        parsed_json = json.loads(json_content)
    except json.JSONDecodeError as e:
        print(f"  Invalid JSON in {filepath}: {e}")
        return False
    
    # Create .json file with same name
    json_filepath = filepath.with_suffix('.json')
    
    # Write pretty-printed JSON to separate file
    with open(json_filepath, 'w', encoding='utf-8') as f:
        json.dump(parsed_json, f, indent=2, ensure_ascii=False)
    
    # Remove JSON from markdown and clean up trailing whitespace
    markdown_content = content[:match.start()].rstrip() + '\n'
    
    # Write cleaned markdown back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    
    print(f"  ✓ Created {json_filepath}")
    print(f"  ✓ Cleaned {filepath}")
    return True

def main():
    """Main function to process all markdown files in _reviewers directory."""
    reviewers_dir = Path("_reviewers")
    
    if not reviewers_dir.exists():
        print(f"Error: {reviewers_dir} directory not found")
        return
    
    # Get all .md files in _reviewers directory
    md_files = list(reviewers_dir.glob("*.md"))
    
    if not md_files:
        print("No .md files found in _reviewers directory")
        return
    
    print(f"Found {len(md_files)} markdown files to process")
    
    processed_count = 0
    
    for md_file in md_files:
        if process_markdown_file(md_file):
            processed_count += 1
    
    print(f"\nSummary:")
    print(f"Total files: {len(md_files)}")
    print(f"Successfully processed: {processed_count}")
    print(f"Files with no JSON: {len(md_files) - processed_count}")

if __name__ == "__main__":
    main()