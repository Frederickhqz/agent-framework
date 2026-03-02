#!/bin/bash
# Pattern Extraction from Observations
# Run daily to identify patterns

WORKSPACE="/data/.openclaw/workspace/agent-framework"
OBS_DIR="$WORKSPACE/self-improvement/observations"
PAT_DIR="$WORKSPACE/self-improvement/patterns"
LOOKBACK_DAYS=7

extract_patterns() {
    echo "=== Pattern Extraction ==="
    echo "Looking back $LOOKBACK_DAYS days..."
    
    # Find recent observations
    local recent_obs=$(find "$OBS_DIR" -name "obs-*.md" -mtime -$LOOKBACK_DAYS | sort)
    local count=$(echo "$recent_obs" | wc -l)
    
    echo "Found $count recent observations"
    
    if [ $count -lt 3 ]; then
        echo "Not enough observations for pattern extraction (need >= 3)"
        return
    fi
    
    # Analyze by task type
    echo ""
    echo "=== Task Type Analysis ==="
    
    for task_type in architect builder reviewer orchestrator other; do
        local type_count=$(grep -l "task_type: $task_type" $recent_obs 2>/dev/null | wc -l)
        local success_count=$(grep -l "task_type: $task_type" $recent_obs 2>/dev/null | xargs grep -l "success: true" 2>/dev/null | wc -l)
        
        if [ $type_count -gt 0 ]; then
            local rate=$(echo "scale=2; $success_count / $type_count * 100" | bc 2>/dev/null || echo "N/A")
            echo "  $task_type: $success_count/$type_count success ($rate%)"
        fi
    done
    
    # Identify common issues
    echo ""
    echo "=== Common Issues ==="
    grep -h "error_types:" $recent_obs 2>/dev/null | sort | uniq -c | sort -rn | head -5 || echo "  No errors logged"
    
    # Extract candidate patterns
    echo ""
    echo "=== Candidate Patterns ==="
    
    # Look for high-success approaches
    local high_success=$(grep -l "success: true" $recent_obs 2>/dev/null | xargs grep -l "confidence: 0.[8-9]" 2>/dev/null | wc -l)
    if [ $high_success -gt 2 ]; then
        echo "  Pattern candidate: High confidence + High success rate"
        echo "    Evidence: $high_success instances"
        echo "    Recommendation: Trust high-confidence estimates"
    fi
    
    # Look for time patterns
    local fast_complete=$(grep -l "time_taken_minutes: [0-9]\{1,2\}$" $recent_obs 2>/dev/null | wc -l)
    if [ $fast_complete -gt 2 ]; then
        echo "  Pattern candidate: Fast completion tasks"
        echo "    Evidence: $fast_complete instances under 100 minutes"
        echo "    Recommendation: Identify commonalities in fast tasks"
    fi
    
    echo ""
    echo "Extraction complete. Review patterns/INDEX.md to formalize."
}

# Generate pattern file
generate_pattern() {
    local name="$1"
    local type="$2"
    local description="$3"
    local recommendation="$4"
    
    local date_str=$(date +%Y-%m-%d)
    local count=$(ls -1 "$PAT_DIR"/pat-*.md 2>/dev/null | wc -l)
    local pat_id=$(printf "PAT-%s-%03d" "$date_str" $((count + 1)))
    
    cat > "$PAT_DIR/${pat_id}.md" << EOF
---
pattern_id: $pat_id
extraction_date: $date_str
source_observations: []

pattern:
  name: "$name"
  type: $type
  description: "$description"
  
  if_conditions: []
  then_outcome: ""
  
  sample_size: 0
  confidence: 0.0
  success_rate: 0.0
  avg_time_savings_minutes: 0
  
  recommendation: "$recommendation"
  applies_to: []
  
status: candidate
validated_date:
---

# Pattern: $name

$description

## Recommendation
$recommendation

EOF

    echo "Created pattern: $pat_id"
}

# Main
if [ "$1" = "extract" ]; then
    extract_patterns
elif [ "$1" = "create" ]; then
    shift
    generate_pattern "$@"
else
    echo "Usage: $0 extract|create <name> <type> <description> <recommendation>"
    exit 1
fi
