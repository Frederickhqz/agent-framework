# Constitutional Framework

The Constitutional Framework defines inviolable principles and operational rules that govern all self-improvement activities in the Level 7 Agent Architecture.

## Files

- **constitution.yaml** - The core constitutional document defining principles and rules
- **validator.py** - Python module for validating changes against the constitution
- **__init__.py** - Package initialization
- **test_validator.py** - Unit tests for the validator

## Principles (Inviolable)

1. **Helpfulness** - All improvements must increase helpfulness to the user
2. **Honesty** - All improvements must increase honesty and transparency
3. **Safety** - All improvements must not increase risk of harm
4. **Alignment** - All improvements must align with user intent

## Operational Rules

1. **Human Oversight** - Significant changes require human notification
2. **Reversibility** - All changes must be reversible (30-day rollback)
3. **Transparency** - All changes must be explainable
4. **Bounded Scope** - Changes only within defined boundaries

## Usage

### Python API

```python
from constitution import ConstitutionValidator

# Create validator
validator = ConstitutionValidator()

# Validate a change
change = {
    "type": "pattern_update",
    "domain": "agent-framework",
    "description": "Add new error handling pattern",
    "has_rollback": True,
    "backup_created": True,
    "rationale": "Improves error recovery",
    "evidence": "Observed 5 similar errors this week"
}

result = validator.validate(change)
print(f"Status: {result.status.value}")
print(f"Risk: {result.risk_level.value}")
```

### Command Line

```bash
# Quick validation
cd /data/.openclaw/workspace/agent-framework
python -m constitution.validator --quick pattern agent-framework

# Validate from JSON file
python -m constitution.validator --check change.json

# Show examples
python -m constitution.validator --example
```

## Risk Levels

| Level | Approval Required | Auto-Apply | Examples |
|-------|------------------|------------|----------|
| Low | No | Yes | Pattern updates, optimizations |
| Medium | Recommended | After 7 days | Definition changes, new patterns |
| High | Yes | Never | Core behavior changes |
| Critical | Yes + Review | Never | Constitutional amendments |

## Validation Results

- **APPROVED** - Change passes all checks, may proceed
- **NEEDS_NOTIFICATION** - High-risk change, notify user first
- **NEEDS_APPROVAL** - Requires explicit human approval
- **REJECTED** - Violates inviolable principles, cannot proceed

## Testing

```bash
python -m pytest constitution/test_validator.py -v
```