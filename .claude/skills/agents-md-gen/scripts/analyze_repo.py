#!/usr/bin/env python3
"""Analyze repository structure and extract key information for AGENTS.md generation."""
import os
import json
import subprocess
from pathlib import Path


def get_dir_tree(root: Path, max_depth: int = 3, ignore: set = None) -> dict:
    """Build a directory tree representation."""
    if ignore is None:
        ignore = {'.git', 'node_modules', '__pycache__', '.next', 'venv', '.venv', 'dist', 'build'}

    result = {}
    try:
        for item in sorted(root.iterdir()):
            if item.name in ignore or item.name.startswith('.'):
                continue
            if item.is_dir() and max_depth > 0:
                result[item.name + '/'] = get_dir_tree(item, max_depth - 1, ignore)
            elif item.is_file():
                result[item.name] = None
    except PermissionError:
        pass
    return result


def detect_tech_stack(root: Path) -> dict:
    """Detect technologies used in the project."""
    stack = {}

    # Python detection
    if (root / 'pyproject.toml').exists() or list(root.rglob('requirements.txt')):
        stack['backend'] = 'Python/FastAPI'

    # Node.js detection
    if (root / 'package.json').exists() or list(root.rglob('package.json')):
        pkg_file = root / 'learnflow-frontend' / 'package.json'
        if not pkg_file.exists():
            pkg_files = list(root.rglob('package.json'))
            pkg_file = pkg_files[0] if pkg_files else None
        if pkg_file and pkg_file.exists():
            with open(pkg_file) as f:
                pkg = json.load(f)
            deps = list(pkg.get('dependencies', {}).keys())
            if 'next' in deps:
                stack['frontend'] = 'Next.js/TypeScript'
            elif 'react' in deps:
                stack['frontend'] = 'React/TypeScript'

    # Kubernetes detection
    if list(root.rglob('*.yaml')) or list(root.rglob('*.yml')):
        stack['orchestration'] = 'Kubernetes + Helm'

    # Dapr detection
    if list(root.rglob('dapr-components')) or list(root.rglob('dapr*.yaml')):
        stack['service_mesh'] = 'Dapr'

    # Kafka detection
    if list(root.rglob('kafka*.yaml')):
        stack['messaging'] = 'Apache Kafka'

    # Docker detection
    if list(root.rglob('Dockerfile')):
        stack['containerization'] = 'Docker'

    return stack


def find_services(root: Path) -> list:
    """Find all microservices."""
    services = []
    services_dir = root / 'learnflow-app' / 'services'
    if services_dir.exists():
        for svc_dir in sorted(services_dir.iterdir()):
            if svc_dir.is_dir() and not svc_dir.name.startswith('.'):
                main_py = svc_dir / 'main.py'
                if main_py.exists():
                    services.append({
                        'name': svc_dir.name,
                        'path': str(svc_dir.relative_to(root)),
                        'has_dockerfile': (svc_dir / 'Dockerfile').exists(),
                        'has_requirements': (svc_dir / 'requirements.txt').exists(),
                    })
    return services


def find_skills(root: Path) -> list:
    """Find all available skills."""
    skills = []
    skills_dir = root / '.claude' / 'skills'
    if skills_dir.exists():
        for skill_dir in sorted(skills_dir.iterdir()):
            if skill_dir.is_dir():
                skill_md = skill_dir / 'SKILL.md'
                if skill_md.exists():
                    skills.append(skill_dir.name)
    return skills


def main():
    root = Path.cwd()
    print("Analyzing repository structure...")

    analysis = {
        'root': str(root),
        'tree': get_dir_tree(root),
        'tech_stack': detect_tech_stack(root),
        'services': find_services(root),
        'skills': find_skills(root),
    }

    output_path = root / '.repo-analysis.json'
    with open(output_path, 'w') as f:
        json.dump(analysis, f, indent=2)

    print(f"Analysis saved to {output_path}")
    print(f"Found {len(analysis['services'])} services")
    print(f"Found {len(analysis['skills'])} skills")
    print(f"Tech stack: {', '.join(analysis['tech_stack'].values())}")


if __name__ == '__main__':
    main()
