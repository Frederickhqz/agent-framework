# Contributing to OpenClaw Agent Framework

Thank you for your interest in contributing! This framework is designed to be extended and customized.

## Ways to Contribute

### 1. Report Issues

- Bug reports
- Feature requests
- Documentation improvements
- Performance issues

**How to report:**
1. Check existing issues first
2. Open a new issue with:
   - Clear title
   - Steps to reproduce (for bugs)
   - Expected vs actual behavior
   - Environment details

### 2. Improve Documentation

- Fix typos
- Add examples
- Clarify confusing sections
- Translate (if applicable)

**Documentation files:**
- `README.md` - Main overview
- `MEMORY_FRAMEWORK.md` - Framework details
- `INSTALL.md` - Setup guide
- `CHANGELOG.md` - Version history

### 3. Add Scripts

New automation scripts go in `scripts/`:

```bash
# Template for new scripts
#!/bin/bash
set -euo pipefail

# 1. Configuration
MEMORY_DIR="${MEMORY_DIR:-/data/.openclaw/workspace/memory}"

# 2. Functions
main() {
    # Your logic here
}

# 3. Run
main "$@"
```

**Guidelines:**
- Use `set -euo pipefail` for safety
- Log to stderr for errors
- Document with comments
- Handle missing directories gracefully

### 4. Add Memory Tiers

To add a new memory tier:

1. Create directory: `memory/new-tier/`
2. Add retention rules to `RETENTION_POLICY.md`
3. Update janitor scripts if needed
4. Document in `MEMORY_FRAMEWORK.md`

### 5. Improve Skills

Skills go in `skills/`:

```
skills/
└── your-skill/
    └── SKILL.md
```

**SKILL.md template:**

```yaml
---
name: your-skill
description: What it does
homepage: https://example.com
metadata:
  openclaw:
    emoji: "🔧"
    requires:
      bins: ["command"]
      env: ["ENV_VAR"]
---

# Your Skill

Usage instructions here.
```

## Development Setup

```bash
# 1. Fork and clone
git clone https://github.com/YOUR_USERNAME/agent-framework.git
cd agent-framework

# 2. Create branch
git checkout -b feature/your-feature

# 3. Make changes
# ... edit files ...

# 4. Test
./scripts/verify.sh

# 5. Commit
git add .
git commit -m "Add: description of changes"

# 6. Push
git push origin feature/your-feature

# 7. Open Pull Request
```

## Code Style

### Bash Scripts

- Use `#!/bin/bash`
- `set -euo pipefail` at top
- Quote variables: `"$VAR"`
- Use `[[ ]]` for conditionals
- Functions: `lowercase_with_underscores`

### Markdown

- 80 character line wrap
- Headers with sentence case
- Code blocks with language tag
- Links as reference style

### Git Commits

Format: `TYPE: description`

Types:
- `Add:` New feature
- `Fix:` Bug fix
- `Docs:` Documentation
- `Refactor:` Code change
- `Test:` Adding tests
- `Chore:` Maintenance

Examples:
```
Add: voice message cleanup script
Fix: QMD collection not initializing
Docs: clarify retention policy
Refactor: simplify janitor logic
```

## Testing

Before submitting:

1. **Syntax check:**
   ```bash
   bash -n scripts/your-script.sh
   ```

2. **Run tests:**
   ```bash
   ./scripts/verify.sh
   ```

3. **Test manually:**
   ```bash
   # Test in isolated environment
   cp -r /tmp/test-workspace
   cd /tmp/test-workspace
   # Run your changes
   ```

## Documentation Updates

When adding features, update:

1. `README.md` - If user-facing
2. `MEMORY_FRAMEWORK.md` - If framework changes
3. `INSTALL.md` - If setup changes
4. `CHANGELOG.md` - Always

## Questions?

- Open an issue with label `question`
- Start a discussion
- Email: socials@enchantiarealms.com

## License

By contributing, you agree that your contributions will be licensed under the same license as this project.

---

**Thank you for contributing! 🎉**
