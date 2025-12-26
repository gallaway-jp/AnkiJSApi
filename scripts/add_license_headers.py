#!/usr/bin/env python3
"""
Add SPDX license identifiers to all Python source files.

This script adds MIT license headers to Python files that don't already have them.
"""

from pathlib import Path
from typing import List


SPDX_HEADER = """# SPDX-License-Identifier: MIT
# Copyright (c) 2025 AnkiDroid JS API Desktop Contributors

"""


def has_license_header(content: str) -> bool:
    """Check if file already has a license header."""
    return "SPDX-License-Identifier" in content or "Copyright (c)" in content


def add_license_header(file_path: Path) -> bool:
    """Add license header to a Python file if it doesn't have one."""
    try:
        content = file_path.read_text(encoding="utf-8")
        
        # Skip if already has a license header
        if has_license_header(content):
            print(f"  ⏭️  Skipped (already has header): {file_path}")
            return False
        
        # Handle shebang lines
        if content.startswith("#!"):
            lines = content.split("\n", 1)
            if len(lines) == 2:
                new_content = f"{lines[0]}\n{SPDX_HEADER}{lines[1]}"
            else:
                new_content = f"{lines[0]}\n{SPDX_HEADER}"
        else:
            new_content = SPDX_HEADER + content
        
        # Write back
        file_path.write_text(new_content, encoding="utf-8")
        print(f"  ✅ Added header: {file_path}")
        return True
        
    except Exception as e:
        print(f"  ❌ Error processing {file_path}: {e}")
        return False


def find_python_files(directory: Path) -> List[Path]:
    """Find all Python files in directory, excluding common directories."""
    exclude_dirs = {"__pycache__", ".git", ".venv", "venv", "build", "dist", ".pytest_cache"}
    
    python_files = []
    for file_path in directory.rglob("*.py"):
        # Skip files in excluded directories
        if any(excluded in file_path.parts for excluded in exclude_dirs):
            continue
        python_files.append(file_path)
    
    return sorted(python_files)


def main():
    """Main function."""
    print("=" * 70)
    print("Adding SPDX License Identifiers to Python Files")
    print("=" * 70)
    print()
    
    # Get project root (script is in scripts/ subdirectory)
    project_root = Path(__file__).parent.parent
    
    # Find source files
    src_dir = project_root / "src" / "ankidroid_js_api"
    if not src_dir.exists():
        print(f"❌ Source directory not found: {src_dir}")
        return
    
    print(f"📁 Scanning: {src_dir}")
    python_files = find_python_files(src_dir)
    print(f"📄 Found {len(python_files)} Python files")
    print()
    
    # Process each file
    added_count = 0
    for file_path in python_files:
        if add_license_header(file_path):
            added_count += 1
    
    print()
    print("=" * 70)
    print(f"✅ Complete! Added headers to {added_count}/{len(python_files)} files")
    print("=" * 70)


if __name__ == "__main__":
    main()
