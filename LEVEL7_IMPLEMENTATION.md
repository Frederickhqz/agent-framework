# Level 7 Self-Improving Agent Architecture
## Implementation Guide

---

## Overview

This is the **Level 7 Self-Improving Agent Architecture** - an extension of the OpenClaw agent-framework that enables agents to:

1. **Observe** their own behavior and outcomes
2. **Hypothesize** improvements based on patterns
3. **Experiment** safely with changes
4. **Analyze** results and evolve

### The OHEA Cycle

```
┌─────────────────────────────────────────────────────────────────┐
│                      OHEA Cycle                                │
│                                                                │
│   ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐ │
│   │  Observe │───▶│ Hypothesize│──▶│ Experiment│──▶│  Analyze │ │
│   └──────────┘    └──────────┘    └──────────┘    └──────────┘ │
│        │                                                │      │
│        │              ┌──────────────────┐            │      │
│        │              │  Principle Store  │            │      │
│        │              │  (QMD + Memory)   │            │      │
│        │              └──────────────────┘            │      │
│        │                      ▲                         │      │
│        └──────────────────────┴─────────────────────────┘      │
│                                                                │
└─────────────────────────────────────────────────────────────────┘
```

---

## Directory Structure

```
agent-framework/
├── self-improvement/
│   ├── CONSTITUTION.md           # Core safety principles
│   ├── observations/             # Task outcome logs
│   │   ├── INDEX.md
│   │   └── obs-YYYY-MM-DD-###.md
│   ├── patterns/                 # Extracted patterns
│   │   ├── INDEX.md
│   │   └── pat-YYYY-MM-DD-###.md
│   ├── hypotheses/               # Testable improvement ideas
│   │   ├── INDEX.md
│   │   └── hyp-YYYY-MM-DD-###.md
│   ├── evolution/                # Applied changes
│   │   ├── INDEX.md
│   │   └── evo-YYYY-MM-DD-###.md
│   └── principles/               # Codified learnings
│       ├── INDEX.md
│       └── prin-YYYY-MM-DD-###.md
├── agent-definitions/            # Specialized agent modes
│   ├── _schema.md
│   ├── default.md
│   ├── architect.md
│   ├── builder.md
│   ├── reviewer.md
│   └── orchestrator.md
├── scripts/
│   ├── observation-logger.sh     # Log task outcomes
│   ├── pattern-extractor.sh      # Extract patterns from observations
│   └── self-improvement-cycle.sh # Run OHEA cycle
└── HEARTBEAT.md                  # Updated with Level 7 checks
```

---

## Quick Start

### 1. Initialize Level 7 System

```bash
cd /data/.openclaw/workspace/agent-framework

# Make scripts executable
chmod +x scripts/*.sh

# Test observation logging
./scripts/observation-logger.sh log builder "Implemented auth feature" true 45 2
```

### 2. Run Pattern Extraction

```bash
# Extract patterns from recent observations
./scripts/pattern-extractor.sh extract
```

### 3. Run Full Self-Improvement Cycle

```bash
# Run complete OHEA cycle
./scripts/self-improvement-cycle.sh full
```

---

## Usage

### Daily (Automatic via Heartbeat)

The HEARTBEAT.md now includes Level 7 checks:
- Logs observations for completed tasks
- Records metrics (time, QA cycles, success)
- Monday: Pattern extraction
- Monthly: Full improvement cycle

### Manual Observation Logging

```bash
# Log a task outcome
./scripts/observation-logger.sh log \
  <task_type> \
  "Description" \
  <true|false> \
  <time_minutes> \
  <qa_cycles> \
  [plane_issue_id]
```

Example:
```bash
./scripts/observation-logger.sh log \
  builder \
  "Created REST API endpoint" \
  true \
  30 \
  1 \
  FRAME-12
```

### Creating Patterns

```bash
# Create a new pattern from observations
./scripts/pattern-extractor.sh create \
  "Auth tasks need 2 QA cycles" \
  success \
  "Authentication implementations consistently require 2 QA cycles" \
  "Add auth checklist with token refresh validation"
```

---

## Safety: The Constitution

All self-improvement is constrained by `self-improvement/CONSTITUTION.md`:

### Inviolable Principles
1. **Helpfulness** - Must improve user outcomes
2. **Honesty** - Must be transparent
3. **Safety** - Must not increase risk
4. **Alignment** - Must match user intent

### Operational Rules
1. **Human Oversight** - Significant changes need approval
2. **Reversibility** - All changes can be undone
3. **Transparency** - All changes are explainable
4. **Bounded Scope** - Only within allowed domains

### Risk Levels
| Level | Human Approval | Auto-Apply | Examples |
|-------|---------------|------------|----------|
| Low | Not Required | After test | Minor workflow tweaks |
| Medium | Recommended | After 7 days | New patterns, preferences |
| High | Required | Never | Definition changes |
| Critical | Required + Review | Never | Core system mods |

---

## Agent Definitions

The framework includes specialized agents:

### Architect
- **Triggers**: plan, design, architecture
- **Mission**: Break down problems, create ADRs
- **Deliverables**: Plane issues with acceptance criteria

### Builder
- **Triggers**: implement, build, create
- **Mission**: Produce working code
- **Deliverables**: Working code with evidence

### Reviewer
- **Triggers**: review, QA, validate
- **Mission**: Verify quality before delivery
- **Deliverables**: PASS/FAIL with specific feedback

### Orchestrator
- **Triggers**: orchestrate, coordinate
- **Mission**: Coordinate multi-agent workflows
- **Deliverables**: Complete projects through all phases

### Default
- **Triggers**: catch-all
- **Mission**: General assistance, route to specialists
- **Deliverables**: Efficient task handling

---

## Integration with Plane

The system integrates with Plane for:
- Task tracking and assignment
- Evidence attachment
- Quality gates
- Hypothesis testing coordination

### Quality Gates

Each task goes through gates:
1. **Design** - Architecture reviewed
2. **Build** - Implementation complete
3. **Review** - QA passed with evidence
4. **Deploy** - Production ready

### Example Plane Issue Format

```markdown
## Task: [Description]

### Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2

### Quality Gates
| Gate | Status | Evidence |
|------|--------|----------|
| Design | ⏳ | |
| Build | ⏳ | |
| Review | ⏳ | |

### Observation
- ID: [auto-logged]
- Outcome: pending
- Time: pending
- QA: pending
```

---

## Success Metrics

Track these over time:

| Metric | Baseline | Target (3mo) | Target (6mo) |
|--------|----------|--------------|--------------|
| QA cycles/task | 2.3 | 1.8 | 1.5 |
| Completion time | baseline | -15% | -25% |
| Error rate | baseline | -20% | -40% |
| Self-corrections/month | 0 | 5 | 15 |
| Principles extracted | 0 | 20 | 100 |

---

## Troubleshooting

### Observation not logging
- Check scripts are executable: `chmod +x scripts/*.sh`
- Verify OBS_DIR exists

### Pattern extraction empty
- Need 3+ observations in lookback period
- Check observations/ directory has .md files

### Constitutional check fails
- Verify CONSTITUTION.md exists
- Check file permissions

---

## Future Enhancements

- [ ] Automatic hypothesis generation from patterns
- [ ] QMD integration for principle semantic search
- [ ] Automatic A/B test creation in Plane
- [ ] Metrics dashboard
- [ ] Rollback automation

---

## References

- Original Research: LEVEL7_RESEARCH.md
- Implementation Plan: IMPLEMENTATION_PLAN.md
- Memory Framework: MEMORY_FRAMEWORK.md
