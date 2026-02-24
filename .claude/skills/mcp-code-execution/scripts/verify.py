#!/usr/bin/env python3
"""Verify MCP Code Execution pattern compliance for all skills."""
import sys
from pathlib import Path


def check_skill(skill_dir: Path) -> dict:
    """Check a skill for MCP code execution pattern compliance."""
    results = {'name': skill_dir.name, 'issues': [], 'passes': []}

    skill_md = skill_dir / 'SKILL.md'
    if not skill_md.exists():
        results['issues'].append('Missing SKILL.md')
        return results

    # Check token budget
    content = skill_md.read_text()
    token_estimate = len(content.split()) * 1.3
    if token_estimate < 300:
        results['passes'].append(f'SKILL.md token-efficient (~{int(token_estimate)} tokens)')
    else:
        results['issues'].append(f'SKILL.md too large (~{int(token_estimate)} tokens, target <200)')

    # Check for scripts directory
    scripts_dir = skill_dir / 'scripts'
    if scripts_dir.exists():
        scripts = list(scripts_dir.glob('*.py')) + list(scripts_dir.glob('*.sh'))
        if scripts:
            results['passes'].append(f'Has {len(scripts)} executable script(s)')
            # Check scripts have minimal output
            for script in scripts:
                if script.suffix == '.py':
                    script_content = script.read_text()
                    if 'print(' in script_content and ('sys.exit' in script_content or 'exit(0)' in script_content):
                        results['passes'].append(f'{script.name} has proper exit codes')
                    else:
                        results['issues'].append(f'{script.name} missing sys.exit() pattern')
        else:
            results['issues'].append('scripts/ directory empty - add executable scripts')
    else:
        results['issues'].append('Missing scripts/ directory - required for code execution pattern')

    # Check for REFERENCE.md (deep docs loaded on-demand)
    if (skill_dir / 'REFERENCE.md').exists():
        results['passes'].append('REFERENCE.md exists (deep docs on-demand)')

    return results


def main():
    root = Path.cwd()
    skills_dir = root / '.claude' / 'skills'

    if not skills_dir.exists():
        print('✗ .claude/skills/ directory not found')
        sys.exit(1)

    print('Checking MCP Code Execution pattern compliance...\n')

    hackathon_skills = [
        'agents-md-gen', 'kafka-k8s-setup', 'postgres-k8s-setup',
        'fastapi-dapr-agent', 'mcp-code-execution',
        'nextjs-k8s-deploy', 'docusaurus-deploy'
    ]

    all_pass = True
    for skill_name in hackathon_skills:
        skill_dir = skills_dir / skill_name
        if not skill_dir.exists():
            print(f'✗ {skill_name}: NOT FOUND')
            all_pass = False
            continue

        result = check_skill(skill_dir)
        if result['issues']:
            all_pass = False
            print(f'⚠ {skill_name}:')
            for issue in result['issues']:
                print(f'    ✗ {issue}')
        else:
            print(f'✓ {skill_name}: compliant ({len(result["passes"])} checks passed)')

    print()
    if all_pass:
        print('✓ All hackathon skills follow MCP Code Execution pattern')
        sys.exit(0)
    else:
        print('✗ Some skills need fixes for pattern compliance')
        sys.exit(1)


if __name__ == '__main__':
    main()
