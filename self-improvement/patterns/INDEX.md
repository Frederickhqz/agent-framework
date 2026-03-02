# Pattern Extraction System
## From Observations to Learned Principles

---

## Pattern Types

### Success Patterns
- High confidence + success → Reinforce approach
- Low confidence + success → Document why it worked (discovery)
- Fast completion + success → Optimize for this path

### Failure Patterns
- High confidence + failure → Investigate overconfidence
- Low confidence + failure → Improve estimation
- Repeated failures → Systematic issue

### Efficiency Patterns
- Time taken vs complexity
- QA cycles vs task type
- Tool usage effectiveness
- Context switching costs

---

## Extraction Algorithm

```python
def extract_patterns(observations, lookback_days=30):
    """
    1. Cluster similar observations by tags/task_type
    2. Identify correlation between approach and outcome
    3. Calculate confidence intervals
    4. Generate hypothesis: "If X, then Y (confidence: Z%)"
    5. Rank by: potential_impact * confidence
    """
    pass
```

---

## Pattern Template

```yaml
pattern_id: PAT-YYYY-MM-DD-###
extraction_date: YYYY-MM-DD
source_observations:
  - OBS-YYYY-MM-DD-001
  - OBS-YYYY-MM-DD-002

pattern:
  name: "Descriptive name"
  type: [success|failure|efficiency]
  description: "What the pattern describes"
  
  # The correlation found
  if_conditions:
    - "Condition 1"
    - "Condition 2"
  then_outcome: "Expected result"
  
  # Evidence
  sample_size: [N]
  confidence: 0.0-1.0
  success_rate: 0.0-1.0  # for success patterns
  avg_time_savings_minutes: [N]  # for efficiency patterns
  
  # Actionable insight
  recommendation: "What to do based on this pattern"
  applies_to: [task types this applies to]
  
status: [candidate|validated|rejected]
validated_date: [date if validated]
```

---

## Extracted Patterns

