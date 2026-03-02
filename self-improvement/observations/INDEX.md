# Self-Improvement Observation Log
## Episodic Memory for Agent Learning

---

## Observation Template

Use this template for each significant task:

```yaml
observation_id: OBS-YYYY-MM-DD-###
timestamp: YYYY-MM-DDTHH:MM:SSZ
session_id: "agent:main:session:xxxxx"
task_type: [architect|builder|reviewer|orchestrator|other]

# What was attempted
action:
  description: "Brief description of what was done"
  plane_issue: [issue_id if applicable]
  context:
    user_request: "Original user request"
    complexity_estimate: [low|medium|high]
    confidence: 0.0-1.0
    approach: "Description of approach taken"

# What happened
outcome:
  success: [true|false]
  time_taken_minutes: [N]
  qa_cycles: [N]
  completion_percentage: [0-100]
  
# Evidence
artifacts:
  - type: [file|screenshot|test_result|log]
    path: "path/to/evidence"
    description: "What this shows"

# Reflections - what was learned
reflections:
  - "What worked well"
  - "What didn't work"
  - "Surprises encountered"
  - "What to do differently next time"

# Metrics
metrics:
  user_satisfaction: [1-5|null]
  error_count: [N]
  error_types:
    - "description of error"
  completion_rate: 0.0-1.0
  efficiency_score: 0.0-1.0

# Tags for clustering
tags:
  - "technology"
  - "task-type"
  - "outcome"
```

---

## Observations

