#!/usr/bin/env python3
"""Verify that AGENTS.md was generated correctly."""
import sys
from pathlib import Path


def verify():
    root = Path.cwd()
    agents_md = root / 'AGENTS.md'
    errors = []
    warnings = []

    # Check file exists
    if not agents_md.exists():
        errors.append("AGENTS.md not found at repository root")
        print('\n'.join(errors))
        sys.exit(1)

    content = agents_md.read_text()
    lines = content.splitlines()

    # Required sections
    required_sections = [
        '## Overview',
        '## Tech Stack',
        '## Development Commands',
        '## Coding Conventions',
    ]

    for section in required_sections:
        if section not in content:
            errors.append(f"Missing section: {section}")

    # Check line count (should be substantive but not bloated)
    if len(lines) < 30:
        warnings.append(f"AGENTS.md seems too short ({len(lines)} lines) — may be incomplete")
    if len(lines) > 300:
        warnings.append(f"AGENTS.md is very long ({len(lines)} lines) — consider trimming for token efficiency")

    # Check for placeholder text
    placeholders = ['[PROJECT NAME]', '[TODO]', '[FIXME]', 'placeholder']
    for ph in placeholders:
        if ph.lower() in content.lower():
            warnings.append(f"Found placeholder text: {ph}")

    if warnings:
        for w in warnings:
            print(f"⚠  {w}")

    if errors:
        for e in errors:
            print(f"✗ {e}")
        sys.exit(1)

    print(f"✓ AGENTS.md exists ({len(lines)} lines)")
    print(f"✓ All required sections present")
    print(f"✓ AGENTS.md is ready for AI agent consumption")
    sys.exit(0)


if __name__ == '__main__':
    verify()
