# Safe Testing Environment
# Version: 1.0.0
# Purpose: Test improvements safely with rollback capability

## Testing Hierarchy

### Level 1: Shadow Testing (Zero Risk)
Run hypothesis in parallel with normal operation without affecting actual work.

```yaml
shadow_test:
  description: "Run new approach alongside current approach"
  risk: zero
  duration: 24-72 hours
  procedure:
    - Execute both old and new approaches
    - Compare results
    - No user-facing changes
  success_criteria:
    - New approach performs as well or better
    - No errors in new approach
  rollback: automatic (no changes made)
```

### Level 2: Canary Testing (Low Risk)
Apply change to single task type, monitor closely.

```yaml
canary_test:
  description: "Apply to one task type, monitor"
  risk: low
  duration: 3-7 days
  procedure:
    - Select single task type
    - Apply change only to that type
    - Monitor metrics continuously
  sample_size: 5-10 tasks
  success_criteria:
    - No degradation in quality
    - Metrics improve or stay same
  failure_criteria:
    - Quality degradation > 10%
    - Any error or user complaint
  rollback: automatic on failure
```

### Level 3: Gradual Rollout (Medium Risk)
Roll out to subset of task types, compare against baseline.

```yaml
gradual_test:
  description: "Expand to multiple task types"
  risk: medium
  duration: 7-14 days
  procedure:
    - Select 2-3 task types
    - Apply change to subset
    - Compare with control group
  sample_size: 10-20 tasks
  success_criteria:
    - Statistically significant improvement
    - No quality regression
  failure_criteria:
    - Statistical regression
    - Any safety concern
  rollback: manual but quick
```

### Level 4: Human Approval (High Risk)
Requires explicit human approval before any testing.

```yaml
human_approval_test:
  description: "Major changes require human sign-off"
  risk: high
  triggers:
    - Changes to constitutional rules
    - Changes to core behavior
    - Expansion to new domains
    - Any safety mechanism modification
  procedure:
    - Document change thoroughly
    - Explain rationale and evidence
    - Request human approval
    - Wait for explicit approval
  rollback: documented, tested procedure
```

## Risk Classification

| Change Type | Risk Level | Testing Required |
|-------------|------------|------------------|
| Memory update | Low | Shadow |
| Pattern addition | Low | Shadow |
| Workflow tweak | Low | Canary |
| New tool usage | Medium | Canary |
| Confidence adjustment | Medium | Gradual |
| Agent definition change | Medium | Gradual |
| Constitutional amendment | High | Human Approval |
| New domain expansion | High | Human Approval |

## Monitoring

### Metrics to Track
- Task completion time
- QA cycles required
- Error rate
- User satisfaction (if available)
- Constitutional compliance rate

### Monitoring Interval
- Shadow: Every 6 hours
- Canary: Every 1 hour
- Gradual: Every 2 hours
- Human Approval: Continuous

## Automatic Rollback

### Triggers
- Quality degradation > 10%
- Error rate > baseline + 5%
- Constitutional violation detected
- User complaint received

### Rollback Procedure
```python
def rollback(hypothesis_id, reason):
    # Load backup
    backup = load_backup(hypothesis_id.backup_id)
    
    # Restore previous state
    for file in hypothesis_id.affected_files:
        restore_file(file, backup[file])
    
    # Log rollback
    log_event({
        "type": "rollback",
        "hypothesis": hypothesis_id,
        "reason": reason,
        "timestamp": now()
    })
    
    # Notify if high risk
    if hypothesis_id.risk_level in ["high", "critical"]:
        notify_user(f"Rollback executed: {reason}")
```

## Test Execution Flow

```
1. Receive hypothesis
2. Classify risk level
3. Select test tier
4. If high risk → Request human approval
5. Create backup
6. Execute test
7. Monitor metrics
8. Evaluate results
9. Decision: Accept / Reject / Extend
10. If accept → Commit change
11. If reject → Rollback
12. Log outcome
```

## Evidence Requirements

Each test must produce:
- Screenshots or logs of execution
- Metric comparisons (before/after)
- Statistical significance calculation
- Constitutional compliance check

Evidence is stored in:
```
memory/evidence/H-YYYY-MMDD-NNN/
```