---
name: agent-testing-framework
description: Automated testing framework for LearnFlow AI agent interactions and skill validation
triggers:
  - "test agents"
  - "validate skill"
  - "run agent tests"
  - "test ai responses"
  - "verify agent behavior"
---

# Agent Testing Framework

## When to Use
- Validating that AI agents respond correctly to student queries
- Testing that Skills produce expected outputs
- Regression testing after agent prompt changes
- Verifying end-to-end tutoring flow

## Instructions

1. Run all agent tests:
   ```bash
   python scripts/run_tests.py
   ```

2. Test a specific agent:
   ```bash
   python scripts/run_tests.py --agent concepts
   ```

3. Validate skill outputs:
   ```bash
   python scripts/validate_skills.py
   ```

4. Generate test report:
   ```bash
   python scripts/generate_report.py
   ```

## Test Categories
| Test Suite | Covers |
|-----------|--------|
| `test_triage` | Query routing accuracy |
| `test_concepts` | Explanation quality |
| `test_debug` | Error identification |
| `test_exercise` | Exercise validity |
| `test_progress` | Mastery calculation |

## Validation
- [ ] All agent tests pass (> 80% accuracy)
- [ ] Response time < 5 seconds per query
- [ ] No hallucinated Python syntax in responses
- [ ] Struggle detection triggers correctly

See [REFERENCE.md](./REFERENCE.md) for test case format and evaluation rubric.
