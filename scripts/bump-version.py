#!/usr/bin/env python3
"""Version bump script for the project."""

import re
import sys
from pathlib import Path
from typing import Tuple

def get_current_version(pyproject_path: Path) -> str:
    """Get the current version from pyproject.toml."""
    content = pyproject_path.read_text()
    match = re.search(r'^version = "(\d+\.\d+\.\d+)"', content, re.MULTILINE)
    if not match:
        raise ValueError("Could not find version in pyproject.toml")
    return match.group(1)

def parse_version(version: str) -> Tuple[int, int, int]:
    """Parse version string into tuple of integers."""
    parts = version.split('.')
    if len(parts) != 3:
        raise ValueError(f"Invalid version format: {version}")
    return tuple(map(int, parts))

def bump_version(version: str, bump_type: str) -> str:
    """Bump the version based on the bump type."""
    major, minor, patch = parse_version(version)
    
    if bump_type == 'major':
        return f"{major + 1}.0.0"
    elif bump_type == 'minor':
        return f"{major}.{minor + 1}.0"
    elif bump_type == 'patch':
        return f"{major}.{minor}.{patch + 1}"
    else:
        raise ValueError(f"Invalid bump type: {bump_type}")

def update_version_in_file(file_path: Path, old_version: str, new_version: str) -> bool:
    """Update version in a file."""
    if not file_path.exists():
        return False
    
    content = file_path.read_text()
    new_content = content.replace(old_version, new_version)
    
    if new_content != content:
        file_path.write_text(new_content)
        return True
    return False

def main():
    if len(sys.argv) != 2 or sys.argv[1] not in ['major', 'minor', 'patch']:
        print("Usage: python bump-version.py [major|minor|patch]")
        sys.exit(1)
    
    bump_type = sys.argv[1]
    project_root = Path(__file__).parent.parent
    pyproject_path = project_root / "pyproject.toml"
    
    # Get current version
    current_version = get_current_version(pyproject_path)
    print(f"Current version: {current_version}")
    
    # Calculate new version
    new_version = bump_version(current_version, bump_type)
    print(f"New version: {new_version}")
    
    # Update version in files
    files_to_update = [
        pyproject_path,
        project_root / "src" / "pluggedin_random_number_generator_mcp" / "__init__.py",
        project_root / "src" / "pluggedin_random_number_generator_mcp" / "server.py",
    ]
    
    updated_files = []
    for file_path in files_to_update:
        if update_version_in_file(file_path, current_version, new_version):
            updated_files.append(file_path.name)
    
    if updated_files:
        print(f"Updated version in: {', '.join(updated_files)}")
        print(f"\n✓ Version bumped from {current_version} to {new_version}")
        print("\nNext steps:")
        print("1. Review the changes")
        print("2. Commit: git commit -am 'Bump version to " + new_version + "'")
        print("3. Tag: git tag v" + new_version)
        print("4. Push: git push && git push --tags")
        print("5. Publish: ./scripts/publish.sh")
    else:
        print("No files were updated")

if __name__ == "__main__":
    main()