# Hypothesis Template for Self-Improvement
# Version: 2.0.0
# Purpose: Structure improvement proposals for safe testing
# OHEA Integration: Observe → Hypothesize → Experiment → Analyze

---

## Hypothesis ID System

### Format
```
H-{TYPE}-{YYYY}{MM}{DD}-{NNN}
```

### Components
- **TYPE**: Category of improvement
  - `SPD` - Speed/Performance
  - `ACC` - Accuracy/Quality  
  - `REL` - Reliability/Stability
  - `SAF` - Safety/Security
  - `OPT` - Optimization/Resource
  - `WFL` - Workflow/Process
- **YYYY**: 4-digit year
- **MM**: 2-digit month
- **DD**: 2-digit day
- **NNN**: Sequential number (001-999)

### Examples
- `H-SPD-20260302-001` - Speed hypothesis from March 2, 2026
- `H-ACC-20260302-042` - Accuracy hypothesis #42 from same day
- `H-SAF-20260315-003` - Safety hypothesis from March 15

---

## JSON Schema Definition

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "$id": "https://agent-framework.local/schemas/hypothesis-v2.json",
  "title": "Self-Improvement Hypothesis",
  "type": "object",
  "required": [
    "hypothesis_id",
    "created",
    "version",
    "ohea_phase",
    "source",
    "proposed_change",
    "predicted_outcome",
    "safety_assessment",
    "test_plan"
  ],
  "properties": {
    "hypothesis_id": {
      "type": "string",
      "pattern": "^H-[A-Z]{3}-\\d{8}-\\d{3}$"
    },
    "created": {
      "type": "string",
      "format": "date-time"
    },
    "version": {
      "type": "string",
      "enum": ["2.0.0"]
    },
    "ohea_phase": {
      "type": "string",
      "enum": ["hypothesize", "experiment", "analyze"]
    },
    "status": {
      "type": "string",
      "enum": ["draft", "proposed", "under_review", "approved", "testing", "analyzing", "accepted", "rejected", "rollback"]
    },
    "source": {
      "type": "object",
      "required": ["pattern_id", "observation_ids", "confidence"],
      "properties": {
        "pattern_id": { "type": "string" },
        "observation_ids": {
          "type": "array",
          "items": { "type": "string" },
          "minItems": 1
        },
        "confidence": {
          "type": "number",
          "minimum": 0.0,
          "maximum": 1.0
        },
        "extracted_by": { "type": "string" },
        "extraction_date": { "type": "string", "format": "date-time" }
      }
    },
    "proposed_change": {
      "type": "object",
      "required": ["type", "scope", "description", "affected_files"],
      "properties": {
        "type": {
          "type": "string",
          "enum": ["workflow", "behavior", "memory", "communication", "optimization", "tool", "definition"]
        },
        "scope": {
          "type": "string",
          "enum": ["single_task", "task_type", "agent_definition", "all_tasks", "global"]
        },
        "description": { "type": "string", "minLength": 10 },
        "affected_files": {
          "type": "array",
          "items": { "type": "string" },
          "minItems": 1
        },
        "implementation_steps": {
          "type": "array",
          "items": { "type": "string" }
        }
      }
    },
    "predicted_outcome": {
      "type": "object",
      "required": ["metric", "current_baseline", "predicted_value", "improvement_percent", "confidence"],
      "properties": {
        "metric": { "type": "string" },
        "metric_type": {
          "type": "string",
          "enum": ["duration", "count", "percentage", "ratio", "score"]
        },
        "current_baseline": { "type": "number" },
        "predicted_value": { "type": "number" },
        "improvement_percent": { "type": "number" },
        "confidence": {
          "type": "number",
          "minimum": 0.0,
          "maximum": 1.0
        },
        "prediction_method": {
          "type": "string",
          "enum": ["historical_trend", "extrapolation", "expert_estimate", "simulation"]
        }
      }
    },
    "safety_assessment": {
      "type": "object",
      "required": ["constitutional_check", "risk_level", "human_approval_required"],
      "properties": {
        "constitutional_check": {
          "type": "object",
          "required": ["helpfulness", "honesty", "safety", "alignment"],
          "properties": {
            "helpfulness": { "type": "string", "enum": ["pass", "fail", "pending"] },
            "honesty": { "type": "string", "enum": ["pass", "fail", "pending"] },
            "safety": { "type": "string", "enum": ["pass", "fail", "pending"] },
            "alignment": { "type": "string", "enum": ["pass", "fail", "pending"] }
          }
        },
        "risk_level": {
          "type": "string",
          "enum": ["low", "medium", "high", "critical"]
        },
        "reversibility": {
          "type": "string",
          "enum": ["easy", "moderate", "difficult", "irreversible"]
        },
        "human_approval_required": { "type": "boolean" },
        "rollback_plan": { "type": "string", "minLength": 10 },
        "safety_notes": { "type": "string" }
      }
    },
    "test_plan": {
      "type": "object",
      "required": ["method", "duration_days", "success_criteria", "failure_criteria"],
      "properties": {
        "method": {
          "type": "string",
          "enum": ["shadow", "canary", "gradual", "human_approval", "simulation"]
        },
        "duration_days": { "type": "integer", "minimum": 1 },
        "control_group": {
          "type": "object",
          "properties": {
            "size": { "type": "integer" },
            "description": { "type": "string" },
            "selection_criteria": { "type": "string" }
          }
        },
        "experiment_group": {
          "type": "object",
          "properties": {
            "size": { "type": "integer" },
            "description": { "type": "string" },
            "selection_criteria": { "type": "string" }
          }
        },
        "success_criteria": {
          "type": "array",
          "items": { "type": "string" },
          "minItems": 1
        },
        "failure_criteria": {
          "type": "array",
          "items": { "type": "string" },
          "minItems": 1
        },
        "metrics_to_track": {
          "type": "array",
          "items": { "type": "string" }
        },
        "stopping_conditions": {
          "type": "array",
          "items": { "type": "string" }
        }
      }
    }
  }
}
```

---

## Master Template (All Improvement Types)

```yaml
# ═══════════════════════════════════════════════════════════════
# HYPOTHESIS TEMPLATE v2.0
# OHEA Cycle: Observe → Hypothesize → Experiment → Analyze
# ═══════════════════════════════════════════════════════════════

# ─── HEADER ─────────────────────────────────────────────────────
hypothesis_id: H-{TYPE}-{YYYY}{MM}{DD}-{NNN}
created: "YYYY-MM-DDTHH:MM:SSZ"
version: "2.0.0"

# ─── OHEA INTEGRATION ──────────────────────────────────────────
ohea_phase: hypothesize | experiment | analyze
status: draft | proposed | under_review | approved | testing | analyzing | accepted | rejected | rollback

# ─── SOURCE (OBSERVE Phase Output) ─────────────────────────────
source:
  pattern_id: "PAT-{YYYY}-{MM}{DD}-{NNN}"
  observation_ids:
    - "OBS-{YYYY}{MM}{DD}-{NNNN}"
    - "OBS-{YYYY}{MM}{DD}-{NNNN}"
  confidence: 0.00-1.00
  extracted_by: "pattern-extractor.sh | human | agent"
  extraction_date: "YYYY-MM-DDTHH:MM:SSZ"

# ─── PROPOSED CHANGE (HYPOTHESIZE Phase) ────────────────────────
proposed_change:
  type: workflow | behavior | memory | communication | optimization | tool | definition
  category: speed | accuracy | reliability | safety | optimization | workflow
  scope: single_task | task_type | agent_definition | all_tasks | global
  description: ""
  affected_files:
    - "path/to/file1"
    - "path/to/file2"
  implementation_steps:
    - "Step 1"
    - "Step 2"
    - "Step 3"

# ─── PREDICTED OUTCOME ──────────────────────────────────────────
predicted_outcome:
  metric: ""
  metric_type: duration | count | percentage | ratio | score
  current_baseline: 0.0
  predicted_value: 0.0
  improvement_percent: 0.0
  confidence: 0.00-1.00
  prediction_method: historical_trend | extrapolation | expert_estimate | simulation

# ─── SAFETY ASSESSMENT (MANDATORY) ──────────────────────────────
safety_assessment:
  constitutional_check:
    helpfulness: pass | fail | pending
    honesty: pass | fail | pending
    safety: pass | fail | pending
    alignment: pass | fail | pending
  risk_level: low | medium | high | critical
  reversibility: easy | moderate | difficult | irreversible
  human_approval_required: true | false
  rollback_plan: ""
  safety_notes: ""

# ─── TEST PLAN (EXPERIMENT Phase) ───────────────────────────────
test_plan:
  method: shadow | canary | gradual | human_approval | simulation
  duration_days: 0
  control_group:
    size: 0
    description: ""
    selection_criteria: ""
  experiment_group:
    size: 0
    description: ""
    selection_criteria: ""
  success_criteria:
    - "Criterion 1"
    - "Criterion 2"
  failure_criteria:
    - "Criterion that triggers rollback"
  metrics_to_track:
    - "metric_1"
    - "metric_2"
  stopping_conditions:
    - "Condition to stop early"

# ─── RESULTS (ANALYZE Phase Output) ──────────────────────────────
results:
  started: "YYYY-MM-DDTHH:MM:SSZ"
  completed: "YYYY-MM-DDTHH:MM:SSZ"
  control_metrics:
    metric_name: 0.0
  experiment_metrics:
    metric_name: 0.0
  actual_improvement_percent: 0.0
  statistical_significance: 0.0
  confidence_interval: [0.0, 0.0]
  decision: accepted | rejected | extend_test
  decision_rationale: ""

# ─── ROLLBACK (If Applicable) ───────────────────────────────────
rollback:
  triggered: false | true
  reason: ""
  restored_to: ""
  rollback_date: "YYYY-MM-DDTHH:MM:SSZ"

# ─── EVOLUTION TRACKING ─────────────────────────────────────────
evolution:
  principle_id: "PRIN-{YYYY}-{MM}{DD}-{NNN}"
  incorporated_into: []
  related_hypotheses: []
```

---

## Template A: Speed/Performance Improvements (SPD)

```yaml
# ═══════════════════════════════════════════════════════════════
# SPEED HYPOTHESIS TEMPLATE (H-SPD-*)
# Focus: Reducing time, latency, or resource consumption
# ═══════════════════════════════════════════════════════════════

hypothesis_id: H-SPD-20260302-001
created: "2026-03-02T12:00:00Z"
version: "2.0.0"

ohea_phase: hypothesize
status: proposed

source:
  pattern_id: "PAT-2026-03-01-001"
  observation_ids:
    - "OBS-20260301-0001"
    - "OBS-20260301-0002"
    - "OBS-20260301-0003"
  confidence: 0.82
  extracted_by: "pattern-extractor.sh"
  extraction_date: "2026-03-02T10:00:00Z"

proposed_change:
  type: optimization
  category: speed
  scope: task_type:authentication
  description: "Cache authentication tokens for 5 minutes to reduce redundant API calls"
  affected_files:
    - "agent-framework/scripts/auth-helper.sh"
    - "agent-framework/agent-definitions/builder.md"
  implementation_steps:
    - "Add in-memory token cache with TTL"
    - "Modify auth calls to check cache first"
    - "Add cache invalidation on token refresh"
    - "Update builder.md with caching guidance"

predicted_outcome:
  metric: "auth_api_calls_per_session"
  metric_type: count
  current_baseline: 4.2
  predicted_value: 1.1
  improvement_percent: 73.8
  confidence: 0.85
  prediction_method: extrapolation

safety_assessment:
  constitutional_check:
    helpfulness: pass
    honesty: pass
    safety: pass
    alignment: pass
  risk_level: low
  reversibility: easy
  human_approval_required: false
  rollback_plan: "Remove cache check logic and revert to direct API calls"
  safety_notes: "Token TTL prevents stale token issues; cache is session-only"

test_plan:
  method: shadow
  duration_days: 3
  control_group:
    size: 10
    description: "Tasks using current auth implementation"
    selection_criteria: "Random sampling of auth tasks"
  experiment_group:
    size: 10
    description: "Tasks using cached auth implementation"
    selection_criteria: "Random sampling of auth tasks"
  success_criteria:
    - "API calls reduced by >= 60%"
    - "No auth failures due to caching"
    - "No increase in token refresh errors"
  failure_criteria:
    - "Any auth security issue"
    - "Cache-related errors > 1%"
    - "API calls reduced by < 40%"
  metrics_to_track:
    - "auth_api_calls_per_session"
    - "cache_hit_rate"
    - "auth_failure_rate"
    - "token_refresh_count"
  stopping_conditions:
    - "Auth failure rate > 2%"
    - "Security incident detected"

results:
  started: null
  completed: null
  control_metrics: {}
  experiment_metrics: {}
  actual_improvement_percent: null
  statistical_significance: null
  confidence_interval: null
  decision: null
  decision_rationale: null

rollback:
  triggered: false
  reason: ""
  restored_to: ""
  rollback_date: null

evolution:
  principle_id: null
  incorporated_into: []
  related_hypotheses: []
```

---

## Template B: Accuracy/Quality Improvements (ACC)

```yaml
# ═══════════════════════════════════════════════════════════════
# ACCURACY HYPOTHESIS TEMPLATE (H-ACC-*)
# Focus: Reducing errors, improving correctness, enhancing quality
# ═══════════════════════════════════════════════════════════════

hypothesis_id: H-ACC-20260302-042
created: "2026-03-02T14:30:00Z"
version: "2.0.0"

ohea_phase: hypothesize
status: proposed

source:
  pattern_id: "PAT-2026-02-28-003"
  observation_ids:
    - "OBS-20260227-0005"
    - "OBS-20260228-0008"
    - "OBS-20260301-0012"
    - "OBS-20260301-0015"
    - "OBS-20260302-0002"
  confidence: 0.79
  extracted_by: "pattern-extractor.sh"
  extraction_date: "2026-03-02T14:00:00Z"

proposed_change:
  type: workflow
  category: accuracy
  scope: agent_definition:builder
  description: "Add validation checklist before marking builder tasks complete"
  affected_files:
    - "agent-framework/agent-definitions/builder.md"
    - "agent-framework/scripts/verify.sh"
  implementation_steps:
    - "Add pre-completion validation step to builder workflow"
    - "Create checklist: tests pass, lint clean, docs updated"
    - "Integrate verify.sh into completion criteria"
    - "Add builder.md instruction to run validation"

predicted_outcome:
  metric: "qa_cycles_per_task"
  metric_type: count
  current_baseline: 2.3
  predicted_value: 1.5
  improvement_percent: 34.8
  confidence: 0.75
  prediction_method: historical_trend

safety_assessment:
  constitutional_check:
    helpfulness: pass
    honesty: pass
    safety: pass
    alignment: pass
  risk_level: low
  reversibility: easy
  human_approval_required: false
  rollback_plan: "Remove validation step from workflow; revert builder.md"
  safety_notes: "Additional validation increases safety; no risk of harm"

test_plan:
  method: canary
  duration_days: 7
  control_group:
    size: 15
    description: "Builder tasks without validation checklist"
    selection_criteria: "Random builder tasks from past week"
  experiment_group:
    size: 15
    description: "Builder tasks with validation checklist"
    selection_criteria: "Random builder tasks from current week"
  success_criteria:
    - "Average QA cycles <= 1.8"
    - "No increase in time-to-completion > 10%"
    - "Validation checklist used in >= 90% of tasks"
  failure_criteria:
    - "QA cycles increase > 10%"
    - "Completion time increase > 20%"
    - "User complaints about slowness"
  metrics_to_track:
    - "qa_cycles_per_task"
    - "time_to_completion"
    - "validation_checklist_usage_rate"
    - "post_qa_bug_count"
  stopping_conditions:
    - "QA cycles > 3.0 average"
    - "User explicitly requests rollback"

results:
  started: null
  completed: null
  control_metrics: {}
  experiment_metrics: {}
  actual_improvement_percent: null
  statistical_significance: null
  confidence_interval: null
  decision: null
  decision_rationale: null

rollback:
  triggered: false
  reason: ""
  restored_to: ""
  rollback_date: null

evolution:
  principle_id: null
  incorporated_into: []
  related_hypotheses: []
```

---

## Template C: Reliability/Stability Improvements (REL)

```yaml
# ═══════════════════════════════════════════════════════════════
# RELIABILITY HYPOTHESIS TEMPLATE (H-REL-*)
# Focus: Reducing failures, handling edge cases, improving stability
# ═══════════════════════════════════════════════════════════════

hypothesis_id: H-REL-20260315-003
created: "2026-03-15T09:00:00Z"
version: "2.0.0"

ohea_phase: hypothesize
status: proposed

source:
  pattern_id: "PAT-2026-03-14-001"
  observation_ids:
    - "OBS-20260310-0001"
    - "OBS-20260312-0004"
    - "OBS-20260314-0002"
  confidence: 0.88
  extracted_by: "pattern-extractor.sh"
  extraction_date: "2026-03-15T08:00:00Z"

proposed_change:
  type: behavior
  category: reliability
  scope: task_type:file_operations
  description: "Add retry logic with exponential backoff for file write operations"
  affected_files:
    - "agent-framework/scripts/safe-write.sh"
    - "agent-framework/self-improvement/CONSTITUTION.md"
  implementation_steps:
    - "Create safe-write.sh wrapper script"
    - "Implement 3 retries with 100ms, 200ms, 400ms delays"
    - "Add fallback to temp file + atomic move"
    - "Update CONSTITUTION.md reliability guidelines"

predicted_outcome:
  metric: "file_write_failure_rate"
  metric_type: percentage
  current_baseline: 0.8
  predicted_value: 0.1
  improvement_percent: 87.5
  confidence: 0.90
  prediction_method: simulation

safety_assessment:
  constitutional_check:
    helpfulness: pass
    honesty: pass
    safety: pass
    alignment: pass
  risk_level: medium
  reversibility: moderate
  human_approval_required: true
  rollback_plan: "Revert to direct file writes; remove safe-write.sh from PATH"
  safety_notes: "Retry logic may mask underlying issues; monitoring required"

test_plan:
  method: gradual
  duration_days: 14
  control_group:
    size: 20
    description: "File operations without retry logic"
    selection_criteria: "Random file write operations"
  experiment_group:
    size: 20
    description: "File operations with retry logic"
    selection_criteria: "Random file write operations with retry enabled"
  success_criteria:
    - "File write failures <= 0.2%"
    - "No data corruption incidents"
    - "Average retry count <= 0.5 per operation"
  failure_criteria:
    - "File write failures > 0.5%"
    - "Any data corruption"
    - "Latency increase > 50% for writes"
  metrics_to_track:
    - "file_write_failure_rate"
    - "retry_count_avg"
    - "write_latency_p95"
    - "data_integrity_check_passes"
  stopping_conditions:
    - "Data corruption detected"
    - "Write latency > 2x baseline"
    - "Failure rate exceeds baseline"

results:
  started: null
  completed: null
  control_metrics: {}
  experiment_metrics: {}
  actual_improvement_percent: null
  statistical_significance: null
  confidence_interval: null
  decision: null
  decision_rationale: null

rollback:
  triggered: false
  reason: ""
  restored_to: ""
  rollback_date: null

evolution:
  principle_id: null
  incorporated_into: []
  related_hypotheses: []
```

---

## OHEA Cycle Integration

### Phase Transitions

```
┌─────────────────────────────────────────────────────────────────┐
│                    OHEA CYCLE FLOW                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────┐     ┌──────────────┐     ┌──────────────┐        │
│  │ OBSERVE  │────▶│ HYPOTHESIZE  │────▶│  EXPERIMENT  │        │
│  │          │     │  (Generate)    │     │   (Test)     │        │
│  └──────────┘     └──────────────┘     └──────────────┘        │
│       │                  │                    │                 │
│       │                  │                    │                 │
│       │                  ▼                    │                 │
│       │           ┌──────────┐              │                 │
│       │           │  ANALYZE │◀─────────────┘                 │
│       │           │(Decide)  │                                │
│       │           └────┬─────┘                                │
│       │                │                                       │
│       │                ▼                                       │
│       │           ┌──────────┐                                 │
│       └──────────▶│  EVOLVE  │                                 │
│                   │(Update)  │                                 │
│                   └──────────┘                                 │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Status Flow

```
draft → proposed → under_review → approved → testing → analyzing → accepted
  │                                    │                    │
  │                                    ▼                    ▼
  │                               rollback ─────────────► rejected
  │
  └─────────────────────────────────────────────────────────────────►
```

### Phase Mapping

| Phase | Status Values | Actions Required |
|-------|---------------|------------------|
| **Hypothesize** | draft, proposed, under_review | Pattern extraction, validation |
| **Experiment** | approved, testing | Execute test plan, monitor metrics |
| **Analyze** | analyzing | Calculate significance, make decision |
| **Evolve** | accepted | Apply changes, update principles |
| **Rollback** | rollback, rejected | Revert changes, document learnings |

---

## Validation Checklist

Before submitting a hypothesis:

- [ ] Hypothesis ID follows format: `H-{TYPE}-{YYYYMMDD}-{NNN}`
- [ ] Source pattern exists with valid observations
- [ ] Proposed change has clear description
- [ ] Affected files are specified
- [ ] Predicted outcome includes all required fields
- [ ] Safety assessment is complete (MANDATORY)
- [ ] Constitutional check passes all criteria
- [ ] Risk level is assigned
- [ ] Rollback plan is specified
- [ ] Test plan has success criteria
- [ ] Test plan has failure criteria
- [ ] Duration is specified (days)
- [ ] Method is one of: shadow, canary, gradual, human_approval, simulation

---

## Quick Reference: Improvement Types

| Type Code | Category | Example Hypotheses |
|-----------|----------|-------------------|
| SPD | Speed | Caching, parallelization, optimization |
| ACC | Accuracy | Validation, verification, quality gates |
| REL | Reliability | Retry logic, error handling, stability |
| SAF | Safety | Security hardening, safety checks |
| OPT | Optimization | Resource usage, efficiency improvements |
| WFL | Workflow | Process changes, automation, tooling |

---

## Workflow Commands

### Create New Hypothesis
```bash
# From pattern extraction
./scripts/pattern-extractor.sh create \
  "Description of pattern" \
  "speed|accuracy|reliability|safety|optimization|workflow" \
  "Pattern summary" \
  "Proposed change"
```

### Validate Hypothesis
```bash
# Check schema compliance
python3 -c "
import yaml, jsonschema
with open('hypothesis.yaml') as f:
    h = yaml.safe_load(f)
with open('schemas/hypothesis-v2.json') as f:
    schema = json.load(f)
jsonschema.validate(h, schema)
print('Valid!')
"
```

### Submit for Review
```bash
# Add to hypothesis queue
./scripts/self-improvement-cycle.sh submit hypothesis.yaml
```

### Update Plane Issue
```bash
# Sync hypothesis status to Plane
curl -X PATCH \
  -H "X-API-Key: $PLANE_API_KEY" \
  "http://168.231.69.92:54617/api/v1/workspaces/agents/projects/$PROJECT/issues/$ISSUE/" \
  -d '{"description_html": "Updated with hypothesis details"}'
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-02-22 | Initial template |
| 2.0.0 | 2026-03-02 | Added JSON schema, OHEA integration, type-specific templates |
