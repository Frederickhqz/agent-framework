# Pattern Extraction Engine
# Version: 1.0.0
# Purpose: Extract improvement patterns from observations

## Overview

The Pattern Extraction Engine analyzes observations to identify patterns that can become improvement hypotheses.

## Extraction Process

### 1. Load Observations
```python
def load_observations(days=30):
    """Load observations from the past N days."""
    observations = []
    for date in date_range(today - days, today):
        file = f"memory/observations/{date.year}/{date.month:02d}/{date}-observations.md"
        observations.extend(parse_observations(file))
    return observations
```

### 2. Cluster Similar Observations
```python
def cluster_observations(observations):
    """Group observations by similarity."""
    clusters = []
    
    # Group by action type
    by_type = group_by(observations, lambda o: o.action.type)
    
    # Within each type, find similar contexts
    for action_type, obs_list in by_type.items():
        sub_clusters = semantic_cluster(obs_list, key=lambda o: o.context.approach)
        clusters.extend(sub_clusters)
    
    return clusters
```

### 3. Calculate Pattern Metrics
```python
def calculate_pattern_metrics(cluster):
    """Calculate confidence and impact for a cluster."""
    success_rate = sum(1 for o in cluster if o.outcome.success) / len(cluster)
    
    # Confidence based on consistency
    confidence = success_rate if success_rate > 0.5 else (1 - success_rate)
    
    # Impact based on time saved or quality improved
    avg_time = mean([o.outcome.completion_time_seconds for o in cluster])
    avg_qa = mean([o.outcome.qa_cycles for o in cluster])
    
    impact = "high" if avg_qa > 2 or avg_time > 300 else "medium" if avg_qa > 1 else "low"
    
    return {
        "sample_size": len(cluster),
        "success_rate": success_rate,
        "confidence": confidence,
        "avg_time": avg_time,
        "avg_qa": avg_qa,
        "impact": impact
    }
```

### 4. Extract Pattern
```python
def extract_pattern(cluster, metrics):
    """Convert a cluster into a pattern definition."""
    # Find common elements
    common_approach = find_common(cluster, lambda o: o.context.approach)
    common_tools = intersection([o.metrics.tools_called for o in cluster])
    
    # Identify what worked and what didn't
    successes = [o for o in cluster if o.outcome.success]
    failures = [o for o in cluster if not o.outcome.success]
    
    pattern = {
        "id": generate_pattern_id(),
        "action_type": cluster[0].action.type,
        "approach": common_approach,
        "tools_used": common_tools,
        "metrics": metrics,
        "success_indicators": extract_common_reflections(successes, "what_worked"),
        "failure_indicators": extract_common_reflections(failures, "what_didnt") if failures else [],
        "hypothesis": generate_hypothesis(cluster, metrics)
    }
    
    return pattern
```

## Pattern Types

### Success Pattern
- High confidence + success outcome
- Reinforces current approach
- Becomes "best practice" candidate

### Failure Pattern
- Any confidence + failure outcome
- Identifies what to avoid
- Triggers investigation

### Efficiency Pattern
- Correlation between approach and time/cycles
- Identifies optimization opportunities
- May become hypothesis for testing

### Calibration Pattern
- Mismatch between confidence and outcome
- Indicates overconfidence or underconfidence
- Triggers confidence adjustment

## Extraction Thresholds

| Metric | Threshold | Action |
|--------|-----------|--------|
| Sample size | ≥ 5 | Extract pattern |
| Confidence | ≥ 70% | Create principle |
| Confidence | 50-70% | Monitor for more data |
| Confidence | < 50% | Discard as noise |
| Impact | High | Prioritize for testing |

## Output Format

Extracted patterns are saved as:
```
memory/patterns/PATTERN-XXX-description.md
```

Pattern ID format: `PATTERN-NNN-category-description`

## Integration with Hypothesis Generation

When a pattern meets criteria:
1. Create hypothesis using template
2. Link pattern to hypothesis
3. Begin test cycle
4. Track results

## Scheduling

Pattern extraction runs:
- **Nightly**: 2 AM EST (during low-activity period)
- **Weekly**: Sunday 3 AM EST (deep analysis)
- **On-demand**: When 10+ new observations available

## Example Output

```yaml
pattern_id: PATTERN-001-success-auth-checklist
extracted: 2026-03-02T18:30:00Z
source_observations:
  - OBS-2026-0227-0003
  - OBS-2026-0228-0001
  - OBS-2026-0301-0002
  - OBS-2026-0301-0005
  - OBS-2026-0302-0001

action_type: task
approach: "Checklist-driven implementation"
tools_used: [write, exec]

metrics:
  sample_size: 5
  success_rate: 1.0
  confidence: 1.0
  avg_time: 180
  avg_qa: 0.8
  impact: medium

success_indicators:
  - "Clear structure prevents missed steps"
  - "Checklist items create natural test cases"
  
hypothesis: H-2026-0302-001
```