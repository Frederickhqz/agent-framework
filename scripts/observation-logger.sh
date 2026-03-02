#!/bin/bash
# Level 7 Self-Improvement Observation Logger
# Records task outcomes for pattern extraction

WORKSPACE="/data/.openclaw/workspace/agent-framework"
OBS_DIR="$WORKSPACE/self-improvement/observations"
PLANE_API="http://168.231.69.92:54617/api/v1"
API_KEY="${PLANE_API_KEY:-plane_api_a671d43b3a7248108f522e8c6703aa85}"

# Generate observation ID
generate_id() {
    local date_str=$(date +%Y-%m-%d)
    local count=$(ls -1 "$OBS_DIR"/obs-*.md 2>/dev/null | wc -l)
    printf "OBS-%s-%03d" "$date_str" $((count + 1))
}

# Log observation
log_observation() {
    local task_type="$1"
    local description="$2"
    local outcome="$3"
    local time_taken="$4"
    local qa_cycles="$5"
    local plane_issue="${6:-}"
    
    local obs_id=$(generate_id)
    local timestamp=$(date -Iseconds)
    local session_id="${OPENCLAW_SESSION_ID:-unknown}"
    
    cat > "$OBS_DIR/${obs_id}.md" << EOF
---
observation_id: $obs_id
timestamp: $timestamp
session_id: "$session_id"
task_type: $task_type
plane_issue: "$plane_issue"

action:
  description: "$description"
  context:
    complexity_estimate: 
    confidence: 
    approach: ""

outcome:
  success: $outcome
  time_taken_minutes: $time_taken
  qa_cycles: $qa_cycles
  completion_percentage: 100

artifacts: []

reflections:
  - "To be filled during end-of-session reflection"

metrics:
  user_satisfaction: 
  error_count: 0
  error_types: []
  completion_rate: $(if [ "$outcome" = "true" ]; then echo "1.0"; else echo "0.0"; fi)
  efficiency_score: 

tags:
  - "$task_type"
  - "$(if [ "$outcome" = "true" ]; then echo "success"; else echo "failure"; fi)"
---

# Observation: $obs_id

## Task
$description

## Outcome
- **Success**: $outcome
- **Time**: ${time_taken}min
- **QA Cycles**: $qa_cycles

## Reflection
*To be completed during end-of-session review*

- What worked well:
- What didn't work:
- What to do differently:

EOF

    echo "Logged observation: $obs_id"
    
    # Update Plane issue if provided
    if [ -n "$plane_issue" ]; then
        curl -s -X POST "$PLANE_API/workspaces/agents/issues/$plane_issue/comments" \
            -H "x-api-key: $API_KEY" \
            -H "Content-Type: application/json" \
            -d "{\"body_html\": \"<p>Observation logged: <code>$obs_id</code></p><ul><li>Outcome: $outcome</li><li>Time: ${time_taken}min</li><li>QA cycles: $qa_cycles</li></ul>\"}" \
            > /dev/null 2>&1
    fi
}

# Main
if [ "$1" = "log" ]; then
    shift
    log_observation "$@"
else
    echo "Usage: $0 log <task_type> <description> <true|false> <time_min> <qa_cycles> [plane_issue]"
    exit 1
fi
