# Hypothesis System
## Testable Improvement Proposals

This directory contains structured hypotheses for self-improvement experiments following the OHEA cycle (Observe → Hypothesize → Experiment → Analyze).

---

## Quick Links

- [Master Template](../../hypothesis-template.md) - Complete template with all fields
- [Speed Template](../../hypothesis-template.md#template-a-speedperformance-improvements-spd) - For performance improvements
- [Accuracy Template](../../hypothesis-template.md#template-b-accuracyquality-improvements-acc) - For quality improvements  
- [Reliability Template](../../hypothesis-template.md#template-c-reliabilitystability-improvements-rel) - For stability improvements

---

## Hypothesis ID Format

```
H-{TYPE}-{YYYY}{MM}{DD}-{NNN}
```

### Type Codes
| Code | Category | Description |
|------|----------|-------------|
| SPD | Speed | Performance, latency, efficiency improvements |
| ACC | Accuracy | Quality, correctness, error reduction |
| REL | Reliability | Stability, failure reduction, robustness |
| SAF | Safety | Security hardening, safety checks |
| OPT | Optimization | Resource usage, efficiency gains |
| WFL | Workflow | Process changes, automation, tooling |

### Examples
- `H-SPD-20260302-001` - Speed hypothesis #1 from March 2, 2026
- `H-ACC-20260302-042` - Accuracy hypothesis #42 from same day

---

## Active Hypotheses

### Proposed (Awaiting Approval)
| ID | Category | Description | Risk | Status |
|----|----------|-------------|------|--------|
| [H-SPD-20260302-001](H-SPD-20260302-001.md) | Speed | Cache authentication tokens | Low | Proposed |
| [H-ACC-20260302-001](H-ACC-20260302-001.md) | Accuracy | Validation checklist for builders | Low | Proposed |
| [H-REL-20260302-001](H-REL-20260302-001.md) | Reliability | Retry logic for file writes | Medium | Proposed |

### Testing
| ID | Category | Start Date | Method | Duration |
|----|----------|------------|--------|----------|
| None currently | - | - | - | - |

### Analyzing
| ID | Category | End Date | Decision Pending |
|----|----------|----------|------------------|
| None currently | - | - | - |

### Accepted
| ID | Category | Accepted Date | Principle ID |
|----|----------|---------------|--------------|
| None currently | - | - | - |

### Rejected/Rollback
| ID | Category | Reason | Date |
|----|----------|--------|------|
| None currently | - | - | - |

---

## Required Fields Checklist

All hypotheses MUST include:

- [ ] **Unique ID** - Following `H-TYPE-YYYYMMDD-NNN` format
- [ ] **Source** - Pattern ID and observation IDs
- [ ] **Proposed Change** - Type, scope, description, affected files
- [ ] **Predicted Outcome** - Metric, baseline, prediction, confidence
- [ ] **Safety Assessment** - Constitutional check (MANDATORY)
- [ ] **Test Plan** - Method, duration, success/failure criteria

---

## Workflow

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│ OBSERVE  │───▶│ HYPOTHESIZE│───▶│ EXPERIMENT│───▶│ ANALYZE  │
└──────────┘    └──────────┘    └──────────┘    └──────────┘
     │                                          │
     └──────────────────────────────────────────┘
                    (Evolution Loop)
```

### Creating a Hypothesis

1. **Extract Pattern** from observations using `./scripts/pattern-extractor.sh`
2. **Generate Hypothesis** using the appropriate template
3. **Validate** schema compliance
4. **Submit** for review (auto-approved for low risk)
5. **Execute Test** according to test plan
6. **Analyze Results** and make decision

### Commands

```bash
# Create from pattern
./scripts/pattern-extractor.sh create \
  "Pattern description" \
  "speed|accuracy|reliability" \
  "Pattern summary" \
  "Proposed change"

# Validate hypothesis file
python3 -c "
import yaml
with open('H-SPD-20260302-001.md') as f:
    content = f.read()
    # Extract YAML from markdown code block
    yaml_content = content.split('```yaml')[1].split('```')[0]
    data = yaml.safe_load(yaml_content)
    print(f'ID: {data[\"hypothesis_id\"]}')
    print(f'Status: {data[\"status\"]}')
    print(f'Risk: {data[\"safety_assessment\"][\"risk_level\"]}')
"

# Run experiment
./scripts/self-improvement-cycle.sh test H-SPD-20260302-001

# Analyze results
./scripts/self-improvement-cycle.sh analyze H-SPD-20260302-001
```

---

## Safety Levels

| Level | Human Approval | Auto-Apply | Examples |
|-------|---------------|------------|----------|
| Low | Not Required | After test | Caching, validation, logging |
| Medium | Recommended | After 7 days | Retry logic, workflow changes |
| High | Required | Never | Definition updates, core changes |
| Critical | Required + Review | Never | Security, constitutional changes |

---

## Integration with OHEA Cycle

### Status Mapping

| OHEA Phase | Hypothesis Status | Actions |
|------------|-------------------|---------|
| Hypothesize | draft, proposed | Pattern extraction, validation |
| Experiment | approved, testing | Execute test plan |
| Analyze | analyzing | Calculate significance |
| Evolve | accepted | Apply changes, update principles |
| Rollback | rollback, rejected | Revert, document |

### Timing

- **Daily (Heartbeat)**: Check for hypotheses ready to test
- **Weekly**: Review all pending hypotheses
- **Post-Experiment**: Automatically transition to analyze phase

---

## Statistics

| Metric | Count |
|--------|-------|
| Total Hypotheses | 3 |
| Proposed | 3 |
| Testing | 0 |
| Accepted | 0 |
| Rejected | 0 |

### By Category
| Category | Count |
|----------|-------|
| Speed (SPD) | 1 |
| Accuracy (ACC) | 1 |
| Reliability (REL) | 1 |

---

## Templates

See [../../hypothesis-template.md](../../hypothesis-template.md) for:
- JSON Schema definition
- Master template with all fields
- Type-specific templates (SPD, ACC, REL, etc.)
- OHEA cycle integration details
- Validation checklist
