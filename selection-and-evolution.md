# Selection and Evolution System
# Version: 1.0.0
# Purpose: Select improvements to keep, log evolution events

## Selection Criteria

### Metric Improvement Threshold
- Minimum improvement: 5%
- Statistical significance: p < 0.05
- Confidence interval: 95%

### Quality Gates
| Gate | Criteria | Weight |
|------|----------|--------|
| Performance | Metrics improved | 40% |
| Safety | No constitutional violations | 30% |
| User Impact | No complaints, positive feedback | 20% |
| Maintainability | Code/docs are clean | 10% |

### Decision Matrix
```
IF safety_gate FAILED:
    REJECT immediately
    
IF performance_gate FAILED:
    IF degradation > 10%:
        ROLLBACK
    ELSE:
        EXTEND_TEST
        
IF all_gates PASSED:
    IF improvement >= 5%:
        ACCEPT
    ELSE:
        NEUTRAL (keep monitoring)
```

## Evolution Log Schema

```yaml
# Evolution Event
evolution_id: E-YYYY-MMDD-NNN
hypothesis_id: H-YYYY-MMDD-NNN
decision: accepted | rejected | neutral | rollback

# Timing
created: ISO8601
test_started: ISO8601
test_completed: ISO8601
decision_made: ISO8601

# Test Results
test_results:
  method: shadow | canary | gradual | human_approval
  duration_days: float
  control_group:
    size: int
    metrics:
      metric_name: value
  experiment_group:
    size: int
    metrics:
      metric_name: value
  statistical_significance: float

# Decision Rationale
rationale:
  gates_passed: [string]
  gates_failed: [string]
  key_metrics:
    - name: string
      before: number
      after: number
      change_percent: number
  reasoning: "Explanation of decision"

# Applied Changes (if accepted)
applied_changes:
  - file: path
    change_type: create | modify | delete
    description: "What changed"
    backup_location: path

# Rollback Info
rollback:
  available: boolean
  expires: ISO8601 (30 days)
  procedure: "How to rollback"
```

## Evolution Event Template

```yaml
evolution_id: E-2026-0302-001
hypothesis_id: H-2026-0302-001
decision: accepted

created: 2026-03-02T18:00:00Z
test_started: 2026-03-02T18:05:00Z
test_completed: 2026-03-02T19:05:00Z
decision_made: 2026-03-02T19:10:00Z

test_results:
  method: canary
  duration_days: 1.0
  control_group:
    size: 5
    metrics:
      avg_qa_cycles: 2.3
      avg_time_seconds: 280
  experiment_group:
    size: 5
    metrics:
      avg_qa_cycles: 1.6
      avg_time_seconds: 240
  statistical_significance: 0.95

rationale:
  gates_passed: [performance, safety, user_impact]
  gates_failed: []
  key_metrics:
    - name: qa_cycles
      before: 2.3
      after: 1.6
      change_percent: -30.4
    - name: time_seconds
      before: 280
      after: 240
      change_percent: -14.3
  reasoning: "Token refresh checklist reduced QA cycles by 30% without any errors"

applied_changes:
  - file: agent-definitions/builder.md
    change_type: modify
    description: "Added token refresh to auth checklist"
    backup_location: backups/builder-2026-03-02-pre.md

rollback:
  available: true
  expires: 2026-04-01T19:10:00Z
  procedure: "Restore backup, remove checklist item"
```

## Storage

Evolution events are stored in:
```
memory/evolution/E-YYYY-MMDD-NNN.md
```

Daily summary in:
```
memory/evolution/YYYY/MM/YYYY-MM-DD-evolution-summary.md
```

## Audit Trail

Every evolution event creates an audit entry:

```yaml
audit_entry:
  timestamp: ISO8601
  actor: agent:main
  action: evolution_decision
  hypothesis_id: string
  decision: string
  evidence:
    - path/to/evidence1
    - path/to/evidence2
  constitutional_check: pass
  human_approval: boolean
```

Audit log location:
```
memory/audit/evolution-audit.log
```

## Rollback Management

### Rollback Window
- All changes have 30-day rollback window
- After 30 days, backup is archived
- Archived backups kept for 90 days

### Rollback Execution
```python
def execute_rollback(evolution_id, reason):
    evolution = load_evolution(evolution_id)
    
    # Restore all affected files
    for change in evolution.applied_changes:
        restore_from_backup(change.backup_location, change.file)
    
    # Update evolution status
    evolution.status = "rolled_back"
    evolution.rollback_reason = reason
    evolution.rolled_back_at = now()
    save_evolution(evolution)
    
    # Log audit
    log_audit({
        "type": "rollback",
        "evolution_id": evolution_id,
        "reason": reason
    })
    
    # Notify if significant
    if evolution.test_results.method in ["gradual", "human_approval"]:
        notify_user(f"Rolled back: {reason}")
```

## Metrics Dashboard

Track over time:
- Total evolutions: count
- Acceptance rate: accepted / total
- Average improvement: mean of change_percent
- Rollback rate: rolled_back / accepted
- Most improved metric: by change_percent
- Most tested change type: by frequency