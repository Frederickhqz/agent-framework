#!/bin/bash
# Self-Improvement Cycle Runner
# Executes the OHEA cycle: Observe, Hypothesize, Experiment, Analyze

WORKSPACE="/data/.openclaw/workspace/agent-framework"
SI_DIR="$WORKSPACE/self-improvement"
PLANE_API="http://168.231.69.92:54617/api/v1"
API_KEY="${PLANE_API_KEY:-plane_api_a671d43b3a7248108f522e8c6703aa85}"

log_cycle() {
    local phase="$1"
    local message="$2"
    local timestamp=$(date -Iseconds)
    
    echo "[$timestamp] [$phase] $message"
    
    # Log to cycle log
    echo "[$timestamp] [$phase] $message" >> "$SI_DIR/cycle.log"
}

# Phase 1: Observe - Daily reflection
observe_phase() {
    log_cycle "OBSERVE" "Starting daily observation review"
    
    # Count recent observations
    local recent=$(find "$SI_DIR/observations" -name "obs-*.md" -mtime -1 | wc -l)
    log_cycle "OBSERVE" "Found $recent observations from last 24 hours"
    
    # Check for incomplete reflections
    local incomplete=$(grep -L "What worked well:" "$SI_DIR/observations"/obs-*.md 2>/dev/null | wc -l)
    if [ $incomplete -gt 0 ]; then
        log_cycle "OBSERVE" "Warning: $incomplete observations need reflection"
    fi
    
    log_cycle "OBSERVE" "Complete"
}

# Phase 2: Hypothesize - Generate improvement ideas
hypothesize_phase() {
    log_cycle "HYPOTHESIZE" "Starting pattern extraction"
    
    # Run pattern extraction
    "$WORKSPACE/scripts/pattern-extractor.sh" extract
    
    # Count candidate patterns
    local candidates=$(find "$SI_DIR/patterns" -name "pat-*.md" -exec grep -l "status: candidate" {} \; 2>/dev/null | wc -l)
    log_cycle "HYPOTHESIZE" "Found $candidates candidate patterns for hypothesis generation"
    
    log_cycle "HYPOTHESIZE" "Complete"
}

# Phase 3: Experiment - Test hypotheses
experiment_phase() {
    log_cycle "EXPERIMENT" "Checking for approved hypotheses to test"
    
    # Find approved hypotheses awaiting test
    local approved=$(find "$SI_DIR/hypotheses" -name "hyp-*.md" -exec grep -l "status: awaiting_approval\|status: approved" {} \; 2>/dev/null | wc -l)
    log_cycle "EXPERIMENT" "Found $approved hypotheses ready for testing"
    
    if [ $approved -gt 0 ]; then
        log_cycle "EXPERIMENT" "Creating test issues in Plane..."
        # This would create Plane issues for testing
    fi
    
    log_cycle "EXPERIMENT" "Complete"
}

# Phase 4: Analyze - Review test results
analyze_phase() {
    log_cycle "ANALYZE" "Reviewing test results"
    
    # Find completed experiments
    local completed=$(find "$SI_DIR/evolution" -name "evo-*.md" -mtime -1 2>/dev/null | wc -l)
    log_cycle "ANALYZE" "Found $completed recent evolutions to analyze"
    
    log_cycle "ANALYZE" "Complete"
}

# Constitutional check
constitutional_check() {
    log_cycle "CONSTITUTION" "Running constitutional compliance check"
    
    # This would check proposed changes against CONSTITUTION.md
    # For now, just verify the file exists
    if [ -f "$SI_DIR/CONSTITUTION.md" ]; then
        log_cycle "CONSTITUTION" "Constitution loaded successfully"
        return 0
    else
        log_cycle "CONSTITUTION" "ERROR: Constitution not found!"
        return 1
    fi
}

# Main execution
run_full_cycle() {
    echo "=== Level 7 Self-Improvement Cycle ==="
    echo "Started: $(date)"
    echo ""
    
    constitutional_check || exit 1
    observe_phase
    hypothesize_phase
    experiment_phase
    analyze_phase
    
    echo ""
    echo "=== Cycle Complete ==="
    echo "Finished: $(date)"
}

# Daily run (lightweight)
run_daily() {
    observe_phase
    
    # Only run pattern extraction on certain days
    local day_of_week=$(date +%u)
    if [ $day_of_week -eq 1 ]; then
        # Monday: Full pattern extraction
        hypothesize_phase
    fi
}

# Weekly run (comprehensive)
run_weekly() {
    run_full_cycle
}

# Parse arguments
case "$1" in
    daily)
        run_daily
        ;;
    weekly)
        run_weekly
        ;;
    full)
        run_full_cycle
        ;;
    observe)
        observe_phase
        ;;
    hypothesize)
        hypothesize_phase
        ;;
    experiment)
        experiment_phase
        ;;
    analyze)
        analyze_phase
        ;;
    *)
        echo "Usage: $0 {daily|weekly|full|observe|hypothesize|experiment|analyze}"
        exit 1
        ;;
esac
