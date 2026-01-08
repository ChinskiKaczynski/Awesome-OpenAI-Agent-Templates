#!/usr/bin/env python3
"""
Generate README.md Template Registry table from registry.yml

Usage:
    python scripts/generate-readme.py

This script reads registry.yml and generates a markdown table 
that can be inserted into README.md.
"""

import yaml
from pathlib import Path
from datetime import datetime

REPO_ROOT = Path(__file__).parent.parent
REGISTRY_FILE = REPO_ROOT / "registry.yml"
README_FILE = REPO_ROOT / "README.md"

# Markers in README.md for table insertion
TABLE_START = "<!-- REGISTRY_TABLE_START -->"
TABLE_END = "<!-- REGISTRY_TABLE_END -->"


def load_registry():
    """Load and parse registry.yml"""
    with open(REGISTRY_FILE, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def generate_table(registry: dict) -> str:
    """Generate markdown table from registry data"""
    lines = []
    
    # Header
    lines.append("| Template | Category | Languages | Difficulty | Status | Description |")
    lines.append("|----------|----------|-----------|------------|--------|-------------|")
    
    # Group templates by category
    categories = {c['id']: c['name'] for c in registry.get('categories', [])}
    
    for template in registry.get('templates', []):
        name = template['name']
        path = template.get('path', '')
        category = categories.get(template['category'], template['category'])
        languages = ', '.join(template.get('languages', []))
        difficulty = template.get('difficulty', 'beginner').capitalize()
        status = "✅" if template.get('status') == 'verified' else "🔄"
        description = template.get('description', '')
        
        # Create link if path exists
        if path:
            name_col = f"📁 [{name}]({path}/)"
        else:
            name_col = f"📁 {name}"
        
        lines.append(f"| {name_col} | {category} | {languages} | {difficulty} | {status} | {description} |")
    
    # Add external resources
    lines.append("")
    lines.append("### External Resources")
    lines.append("")
    lines.append("| Resource | Category | Description |")
    lines.append("|----------|----------|-------------|")
    
    for resource in registry.get('external_resources', []):
        name = resource['name']
        url = resource['url']
        category = categories.get(resource['category'], resource['category'])
        description = resource.get('description', '')
        
        lines.append(f"| 🔗 [{name}]({url}) | {category} | {description} |")
    
    return '\n'.join(lines)


def generate_deprecations_section(registry: dict) -> str:
    """Generate deprecation warnings section"""
    lines = [
        "",
        "## ⚠️ Deprecation Timeline",
        "",
        "| API | Shutdown Date | Replacement | Migration Guide |",
        "|-----|---------------|-------------|-----------------|",
    ]
    
    for dep in registry.get('deprecations', []):
        api = dep['api']
        date = dep['shutdown_date']
        replacement = dep['replacement']
        guide = dep.get('migration_guide', '')
        
        if guide:
            guide_link = f"[Guide]({guide})"
        else:
            guide_link = "-"
        
        lines.append(f"| {api} | **{date}** | {replacement} | {guide_link} |")
    
    return '\n'.join(lines)


def update_readme(table: str, deprecations: str):
    """Update README.md with generated content"""
    with open(README_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find and replace the table section
    if TABLE_START in content and TABLE_END in content:
        start_idx = content.index(TABLE_START) + len(TABLE_START)
        end_idx = content.index(TABLE_END)
        
        new_content = (
            content[:start_idx] + 
            "\n\n" + table + "\n\n" + 
            content[end_idx:]
        )
        
        with open(README_FILE, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"✅ Updated {README_FILE}")
    else:
        print(f"⚠️  Could not find table markers in {README_FILE}")
        print(f"   Add {TABLE_START} and {TABLE_END} where you want the table.")
        print("\n--- Generated Table ---\n")
        print(table)
        print("\n--- Deprecations Section ---\n")
        print(deprecations)


def main():
    print(f"📖 Loading {REGISTRY_FILE}...")
    registry = load_registry()
    
    print(f"📝 Generating table for {len(registry.get('templates', []))} templates...")
    table = generate_table(registry)
    
    print(f"⚠️  Generating deprecations for {len(registry.get('deprecations', []))} items...")
    deprecations = generate_deprecations_section(registry)
    
    update_readme(table, deprecations)
    
    print("\n📊 Registry Summary:")
    print(f"   Templates: {len(registry.get('templates', []))}")
    print(f"   External Resources: {len(registry.get('external_resources', []))}")
    print(f"   Categories: {len(registry.get('categories', []))}")
    print(f"   Last Updated: {registry.get('last_updated', 'unknown')}")


if __name__ == "__main__":
    main()
