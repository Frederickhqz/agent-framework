# Full OHEA Loop Implementation
# Version: 1.0.0
# Purpose: Activate complete Observe-Hypothesize-Experiment-Analyze cycle

## OHEA Cycle Overview

```
     ┌─────────────────────────────────────────────────────────────┐
     │                      OHEA CYCLE                            │
     │                                                            │
     │   ┌──────────┐    ┌──────────────┐    ┌──────────────┐    │
     │   │ OBSERVE  │───▶│ HYPOTHESIZE  │───▶│  EXPERIMENT  │    │
     │   └──────────┘    └──────────────┘    └──────────────┘    │
     │        ▲                                     │            │
     │        │              ┌──────────────┐       │            │
     │        └──────────────│   ANALYZE    │◀──────┘            │
     │                       └──────────────┘                    │
     │                                                            │
     └─────────────────────────────────────────────────────────────┘
```

## Daily Cycle

### Observe (Continuous)
During every session:
- Log all actions with context
- Record outcomes and reflections
- Track metrics automatically
- Store in episodic memory

### Hypothesize (Nightly - 2 AM)
During idle time:
- Load observations from past 7 days
- Cluster similar observations
- Calculate pattern metrics
- Generate hypotheses for patterns meeting criteria
- Rank by potential impact

### Experiment (During Sessions)
When hypothesis ready:
- Select appropriate test tier
- Create backup
- Execute test
- Monitor metrics
- Collect evidence

### Analyze (Nightly - 3 AM)
After tests complete:
- Compare control vs experiment
- Calculate statistical significance
- Make decision (Accept/Reject/Extend)
- Log evolution event
- Update principles if accepted

## Scheduling

### Heartbeat Integration
```yaml
# HEARTBEAT.md additions
ohea_cycle:
  observe:
    frequency: continuous
    action: log_observations
    
  hypothesize:
    frequency: nightly
    time: 02:00 EST
    condition: idle > 30 minutes
    action: run_pattern_extraction
    
  experiment:
    frequency: during_sessions
    trigger: hypothesis_ready
    action: execute_test
    
  analyze:
    frequency: nightly
    time: 03:00 EST
    condition: tests_completed
    action: evaluate_results
```

### Cron Jobs
```json
{
  "jobs": [
    {
      "name": "ohea-hypothesize",
      "schedule": "0 2 * * *",
      "tz": "America/New_York",
      "payload": {
        "kind": "agentTurn",
        "message": "Run pattern extraction and hypothesis generation. Check observations from past 7 days. Generate hypotheses for patterns with sample ≥5 and confidence ≥70%. Store in memory/hypotheses/."
      }
    },
    {
      "name": "ohea-analyze",
      "schedule": "0 3 * * *",
      "tz": "America/New_York",
      "payload": {
        "kind": "agentTurn",
        "message": "Analyze completed experiments from past 24 hours. Calculate statistical significance. Make accept/reject decisions. Log evolution events. Update principles collection if accepted."
      }
    }
  ]
}
```

## State Management

### Current State File
```yaml
# memory/ohea-state.yaml
current_phase: observe | hypothesize | experiment | analyze
last_observation: ISO8601
last_hypothesis: ISO8601
last_experiment: ISO8601
last_analysis: ISO8601

active_hypotheses:
  - id: H-YYYY-MMDD-NNN
    status: testing
    started: ISO8601
    expected_completion: ISO8601

pending_observations: int
pending_hypotheses: int
pending_experiments: int

metrics_7day:
  observations_logged: int
  patterns_extracted: int
  hypotheses_generated: int
  tests_executed: int
  improvements_accepted: int
  rollbacks: int
```

## Response Rules for Heartbeat

```yaml
# During heartbeat, check OHEA state:

if current_time in ["02:00-03:00"] and idle:
  phase: HYPOTHESIZE
  action: run_pattern_extraction()
  
elif current_time in ["03:00-04:00"] and idle:
  phase: ANALYZE
  action: evaluate_experiments()
  
elif active_hypotheses and not testing:
  phase: EXPERIMENT
  action: execute_next_test()
  
else:
  phase: OBSERVE
  action: continue_logging()
```

## Integration Points

### QMD
- Observations indexed for semantic search
- Principles queryable for context
- Patterns stored with embeddings

### Plane
- Hypotheses tracked as issues
- Evolution events logged as comments
- Metrics tracked in project dashboard

### Memory
- Observations: memory/observations/
- Principles: memory/principles/
- Hypotheses: memory/hypotheses/
- Evolution: memory/evolution/
- Audit: memory/audit/

## Success Metrics

| Metric | Baseline | Week 4 | Week 8 | Week 12 |
|--------|----------|--------|--------|---------|
| Observations/day | 5 | 15 | 25 | 30 |
| Patterns extracted/week | 0 | 2 | 5 | 10 |
| Hypotheses tested/month | 0 | 3 | 8 | 15 |
| Improvements accepted | 0 | 2 | 5 | 10 |
| QA cycles avg | 2.3 | 2.0 | 1.7 | 1.5 |
| Error rate | baseline | -10% | -25% | -40% |

## Startup Sequence

On agent startup:
1. Load OHEA state from memory/ohea-state.yaml
2. Check for active hypotheses that need testing
3. Check for experiments that need analysis
4. Resume from last phase
5. Log startup observation

## Shutdown Sequence

On agent shutdown:
1. Complete current observation
2. Save OHEA state
3. Log shutdown observation
4. Ensure all backups are persisted