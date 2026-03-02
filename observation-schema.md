# Observation Log Schema
# Version: 1.0.0
# Purpose: Track all actions, decisions, and outcomes for pattern extraction

## Schema Definition

```yaml
# observation-log-entry.yaml
observation_id: OBS-YYYY-MMDD-NNNN
timestamp: ISO8601
session_id: string
agent_mode: default | architect | builder | reviewer

# What was attempted
action:
  type: task | decision | communication | tool_use
  description: string
  task_id: string (Plane issue ID if applicable)
  
# Context at time of action
context:
  user_request: string (verbatim or summary)
  confidence: float (0.0-1.0)
  approach: string (strategy used)
  tools_available: [string]
  relevant_principles: [string] (from QMD)

# Outcome of action
outcome:
  success: boolean
  completion_time_seconds: integer
  evidence:
    - type: screenshot | test_result | code | log
      path: string
  qa_cycles: integer
  retry_count: integer
  
# Self-reflection
reflection:
  what_worked: string
  what_didnt: string
  would_do_differently: string
  pattern_hypothesis: string (optional)

# Metrics
metrics:
  user_satisfaction: float | null (if known)
  error_count: integer
  tokens_used: integer
  tools_called: [string]
  
# Constitutional check
constitutional:
  helpfulness_check: pass | fail
  honesty_check: pass | fail
  safety_check: pass | fail
  alignment_check: pass | fail
```

## Storage Location

Observations are stored in:
```
memory/observations/YYYY/MM/YYYY-MM-DD-observations.md
```

## Aggregation

Daily observations are aggregated into:
```
memory/observations/YYYY/MM/YYYY-MM-DD-summary.md
```

## Example Entry

```yaml
observation_id: OBS-2026-0302-0001
timestamp: 2026-03-02T12:30:00Z
session_id: agent:main:session:abc123
agent_mode: builder

action:
  type: task
  description: "Implemented constitutional framework for Level 7"
  task_id: "FRAME-4"
  
context:
  user_request: "Create constitutional framework"
  confidence: 0.95
  approach: "Research-then-implement with YAML schema"
  tools_available: [web_search, write, exec]
  relevant_principles: ["self-improvement", "safety-first"]

outcome:
  success: true
  completion_time_seconds: 180
  evidence:
    - type: code
      path: "agent-framework/constitution/constitution.yaml"
  qa_cycles: 0
  retry_count: 0
  
reflection:
  what_worked: "YAML format is clear and parseable"
  what_didnt: "None significant"
  would_do_differently: "Could add more examples in comments"
  pattern_hypothesis: "YAML configs work well for structured frameworks"

metrics:
  user_satisfaction: null
  error_count: 0
  tokens_used: 1500
  tools_called: [web_search, write]
  
constitutional:
  helpfulness_check: pass
  honesty_check: pass
  safety_check: pass
  alignment_check: pass
```

## Indexing for QMD

Observations are indexed in QMD collection "observations":
```bash
qmd add memory/observations/YYYY/MM/YYYY-MM-DD-observations.md --collection observations
```

## Retention Policy

- Raw observations: 90 days
- Daily summaries: Permanent
- Patterns extracted: Permanent (in principles collection)