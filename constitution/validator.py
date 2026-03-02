#!/usr/bin/env python3
"""
Constitutional Validator for Level 7 Self-Improving Agents

Validates proposed changes against the constitutional framework to ensure
all self-improvement adheres to inviolable principles and operational rules.
"""

import json
from enum import Enum
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple, Any
from pathlib import Path


class RiskLevel(Enum):
    """Risk classification for changes."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ValidationStatus(Enum):
    """Validation outcome status."""
    APPROVED = "approved"
    REJECTED = "rejected"
    NEEDS_NOTIFICATION = "needs_notification"
    NEEDS_APPROVAL = "needs_approval"


@dataclass
class ValidationResult:
    """Result of constitutional validation."""
    status: ValidationStatus
    message: str
    risk_level: RiskLevel
    violated_principles: List[str] = field(default_factory=list)
    violated_rules: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "status": self.status.value,
            "message": self.message,
            "risk_level": self.risk_level.value,
            "violated_principles": self.violated_principles,
            "violated_rules": self.violated_rules,
            "recommendations": self.recommendations
        }
    
    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)


@dataclass
class Principle:
    """An inviolable constitutional principle."""
    id: str
    name: str
    description: str
    validations: List[str]
    
    def validate(self, change: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """
        Validate a change against this principle.
        
        Returns (passed, reason) tuple.
        """
        # Check for explicit violations in change metadata
        if "violates_principles" in change:
            if self.id in change["violates_principles"]:
                return False, f"Change explicitly marked as violating {self.name}"
        
        # Check change type against principle
        change_type = change.get("type", "")
        
        # Helpfulness checks
        if self.id == "principle-helpfulness":
            if change.get("reduces_user_value", False):
                return False, "Change reduces user value"
            if change.get("creates_friction", False):
                return False, "Change creates user friction"
                
        # Honesty checks
        if self.id == "principle-honesty":
            if change.get("hides_information", False):
                return False, "Change hides information from user"
            if change.get("deceptive", False):
                return False, "Change has deceptive elements"
                
        # Safety checks
        if self.id == "principle-safety":
            if change.get("enables_dangerous_actions", False):
                return False, "Change enables potentially dangerous actions"
            if change.get("bypasses_safeguards", False):
                return False, "Change bypasses existing safeguards"
            if change.get("expands_unauthorized_access", False):
                return False, "Change expands access without authorization"
                
        # Alignment checks
        if self.id == "principle-alignment":
            if change.get("hidden_objective", False):
                return False, "Change pursues hidden objectives"
            if change.get("against_user_boundaries", False):
                return False, "Change violates user boundaries"
        
        return True, None


@dataclass  
class OperationalRule:
    """An operational rule governing changes."""
    id: str
    name: str
    description: str
    constraint: str
    config: Dict[str, Any]
    
    def check(self, change: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """
        Check if change complies with this rule.
        
        Returns (compliant, violation_reason) tuple.
        """
        # Human oversight rule
        if self.id == "rule-human-oversight":
            risk = change.get("risk_level", "low")
            if risk == "high" and not change.get("human_notified", False):
                return False, "High-risk change requires human notification"
                
        # Reversibility rule
        if self.id == "rule-reversibility":
            if not change.get("has_rollback", False):
                return False, "Change must include rollback capability"
            if not change.get("backup_created", False):
                return False, "Change must create backup before applying"
                
        # Transparency rule
        if self.id == "rule-transparency":
            if not change.get("rationale", ""):
                return False, "Change must include rationale"
            if not change.get("evidence", ""):
                return False, "Change must include supporting evidence"
                
        # Bounded scope rule
        if self.id == "rule-bounded-scope":
            domain = change.get("domain", "")
            forbidden = self.config.get("forbidden_domains", [])
            if domain in forbidden:
                return False, f"Change in forbidden domain: {domain}"
        
        return True, None


class ConstitutionValidator:
    """
    Validates changes against the constitutional framework.
    """
    
    def __init__(self, constitution_path: Optional[str] = None):
        """
        Initialize validator with constitution file.
        
        Args:
            constitution_path: Path to constitution.yaml. If None, uses default location.
        """
        if constitution_path is None:
            constitution_path = Path(__file__).parent / "constitution.yaml"
        
        self.constitution_path = Path(constitution_path)
        self.principles: List[Principle] = []
        self.rules: List[OperationalRule] = []
        self._load_constitution()
    
    def _load_constitution(self):
        """Load and parse the constitution file."""
        with open(self.constitution_path, 'r') as f:
            content = f.read()
        
        # Parse principles
        self.principles = [
            Principle(
                id="principle-helpfulness",
                name="Helpfulness",
                description="All improvements must increase helpfulness to user",
                validations=[
                    "improvement_must_serve_user_need",
                    "improvement_must_not_reduce_response_quality",
                    "improvement_must_not_create_friction"
                ]
            ),
            Principle(
                id="principle-honesty",
                name="Honesty",
                description="All improvements must increase honesty and transparency",
                validations=[
                    "improvement_must_not_deceive_user",
                    "improvement_must_not_hide_limitations",
                    "improvement_must_explain_its_purpose"
                ]
            ),
            Principle(
                id="principle-safety",
                name="Safety",
                description="All improvements must not increase risk of harm",
                validations=[
                    "improvement_must_not_enable_dangerous_actions",
                    "improvement_must_not_bypass_safeguards",
                    "improvement_must_not_expand_unauthorized_access"
                ]
            ),
            Principle(
                id="principle-alignment",
                name="Alignment",
                description="All improvements must align with user intent",
                validations=[
                    "improvement_must_match_stated_goals",
                    "improvement_must_not_pursue_hidden_objectives",
                    "improvement_must_respect_user_boundaries"
                ]
            )
        ]
        
        # Parse rules
        self.rules = [
            OperationalRule(
                id="rule-human-oversight",
                name="Human Oversight",
                description="Significant changes require human notification",
                constraint="Changes to core behavior must be logged",
                config={
                    "high_risk": "require_notification",
                    "medium_risk": "log_and_proceed",
                    "low_risk": "proceed_autonomously"
                }
            ),
            OperationalRule(
                id="rule-reversibility",
                name="Reversibility",
                description="All changes must be reversible",
                constraint="Rollback capability required for 30 days",
                config={
                    "backup_before_change": True,
                    "version_all_modifications": True,
                    "maintain_rollback_script": True
                }
            ),
            OperationalRule(
                id="rule-transparency",
                name="Transparency",
                description="All changes must be explainable",
                constraint="Log rationale and evidence",
                config={
                    "document_why_change_made": True,
                    "record_evidence_supporting_change": True,
                    "explain_expected_outcome": True
                }
            ),
            OperationalRule(
                id="rule-bounded-scope",
                name="Bounded Scope",
                description="Changes only within defined boundaries",
                constraint="No expansion beyond authorized domains",
                config={
                    "allowed_domains": [
                        "agent-framework",
                        "memory-management",
                        "task-optimization",
                        "communication-improvement"
                    ],
                    "forbidden_domains": [
                        "external-systems-without-approval",
                        "user-data-exfiltration",
                        "autonomous-goal-setting"
                    ]
                }
            )
        ]
    
    def classify_risk(self, change: Dict[str, Any]) -> RiskLevel:
        """
        Classify the risk level of a proposed change.
        
        Args:
            change: Dictionary describing the change
            
        Returns:
            RiskLevel classification
        """
        # Critical: Changes to constitution itself
        if change.get("affects_constitution", False):
            return RiskLevel.CRITICAL
        
        # High: Core behavior changes
        if change.get("affects_core_behavior", False):
            return RiskLevel.HIGH
        
        # High: New domains
        if change.get("expands_to_new_domain", False):
            return RiskLevel.HIGH
        
        # Medium: Agent definition changes
        if change.get("affects_agent_definitions", False):
            return RiskLevel.MEDIUM
        
        # Medium: Workflow changes
        if change.get("affects_workflows", False):
            return RiskLevel.MEDIUM
        
        # Low: Pattern updates, optimizations
        return RiskLevel.LOW
    
    def validate(self, change: Dict[str, Any]) -> ValidationResult:
        """
        Validate a change against the constitution.
        
        Args:
            change: Dictionary describing the proposed change with keys like:
                - type: Type of change
                - description: Human-readable description
                - domain: Domain being modified
                - risk_level: Explicit risk level (optional)
                - has_rollback: Whether rollback is available
                - rationale: Explanation of the change
                - evidence: Supporting evidence
                - [and various boolean flags for principle checks]
                
        Returns:
            ValidationResult with status and details
        """
        violated_principles = []
        violated_rules = []
        recommendations = []
        
        # Check for forbidden domains - treat as safety violation
        domain = change.get("domain", "")
        forbidden_domains = [
            "external-systems-without-approval",
            "user-data-exfiltration", 
            "autonomous-goal-setting"
        ]
        if domain in forbidden_domains:
            violated_principles.append(f"Safety: Change in forbidden domain: {domain}")
        
        # Check all inviolable principles
        for principle in self.principles:
            passed, reason = principle.validate(change)
            if not passed:
                violated_principles.append(f"{principle.name}: {reason}")
        
        # Check operational rules
        for rule in self.rules:
            compliant, violation = rule.check(change)
            if not compliant:
                violated_rules.append(f"{rule.name}: {violation}")
        
        # Classify risk
        risk = self.classify_risk(change)
        if "risk_level" in change:
            # Use explicit risk if provided, but escalate if needed
            explicit = change["risk_level"]
            if explicit == "critical":
                risk = RiskLevel.CRITICAL
            elif explicit == "high":
                risk = RiskLevel.HIGH
            elif explicit == "medium":
                risk = RiskLevel.MEDIUM
        
        # Determine outcome
        if violated_principles:
            return ValidationResult(
                status=ValidationStatus.REJECTED,
                message=f"Violates inviolable principles: {'; '.join(violated_principles)}",
                risk_level=risk,
                violated_principles=violated_principles,
                violated_rules=violated_rules,
                recommendations=["Redesign to respect constitutional principles"]
            )
        
        # Risk-based approval requirements (before rule violations)
        if risk == RiskLevel.CRITICAL:
            return ValidationResult(
                status=ValidationStatus.NEEDS_APPROVAL,
                message="Critical change requires explicit human approval and review",
                risk_level=risk,
                recommendations=[
                    "Document detailed rationale",
                    "Provide comprehensive test results",
                    "Schedule review meeting"
                ]
            )
        
        if risk == RiskLevel.HIGH:
            return ValidationResult(
                status=ValidationStatus.NEEDS_NOTIFICATION,
                message="High-risk change requires human notification",
                risk_level=risk,
                recommendations=[
                    "Notify user of pending change",
                    "Provide rollback instructions",
                    "Log all modifications"
                ] + ([f"Address: {v}" for v in violated_rules] if violated_rules else [])
            )
        
        # Medium risk with rule violations needs approval
        if risk == RiskLevel.MEDIUM and violated_rules:
            return ValidationResult(
                status=ValidationStatus.NEEDS_APPROVAL,
                message=f"Violates operational rules: {'; '.join(violated_rules)}",
                risk_level=risk,
                violated_principles=violated_principles,
                violated_rules=violated_rules,
                recommendations=["Address rule violations or seek human approval"]
            )
        
        # Low/Medium risk rule violations just get recommendations
        if violated_rules:
            recommendations.extend([
                f"Address: {v}" for v in violated_rules
            ])
        
        # Approved
        return ValidationResult(
            status=ValidationStatus.APPROVED,
            message="Constitutional check passed",
            risk_level=risk,
            recommendations=recommendations if recommendations else [
                "Proceed with implementation",
                "Log change for audit trail"
            ]
        )
    
    def quick_check(self, change_type: str, domain: str) -> ValidationResult:
        """
        Quick validation for simple changes.
        
        Args:
            change_type: Type of change (e.g., "pattern", "workflow", "definition")
            domain: Domain being modified
            
        Returns:
            ValidationResult
        """
        change = {
            "type": change_type,
            "domain": domain,
            "has_rollback": True,
            "backup_created": True,
            "rationale": "Quick check validation",
            "evidence": "Automated check"
        }
        return self.validate(change)


def main():
    """CLI interface for constitutional validation."""
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Validate changes against constitutional framework"
    )
    parser.add_argument(
        "--check",
        help="JSON file describing the change to validate"
    )
    parser.add_argument(
        "--quick",
        nargs=2,
        metavar=("TYPE", "DOMAIN"),
        help="Quick validation: type and domain"
    )
    parser.add_argument(
        "--example",
        action="store_true",
        help="Show example validation outputs"
    )
    
    args = parser.parse_args()
    
    validator = ConstitutionValidator()
    
    if args.example:
        print("=== Constitutional Validator Examples ===\n")
        
        # Example 1: Safe change
        print("1. Safe pattern update:")
        result = validator.quick_check("pattern", "agent-framework")
        print(f"   Status: {result.status.value}")
        print(f"   Message: {result.message}")
        print(f"   Risk: {result.risk_level.value}\n")
        
        # Example 2: Violation
        print("2. Change violating safety:")
        unsafe_change = {
            "type": "capability",
            "domain": "external-systems-without-approval",
            "enables_dangerous_actions": True,
            "has_rollback": True,
            "rationale": "Test"
        }
        result = validator.validate(unsafe_change)
        print(f"   Status: {result.status.value}")
        print(f"   Message: {result.message}")
        print(f"   Risk: {result.risk_level.value}\n")
        
        # Example 3: High risk
        print("3. High-risk core behavior change:")
        high_risk_change = {
            "type": "behavior",
            "domain": "agent-framework",
            "affects_core_behavior": True,
            "has_rollback": True,
            "rationale": "Improve response quality"
        }
        result = validator.validate(high_risk_change)
        print(f"   Status: {result.status.value}")
        print(f"   Message: {result.message}")
        print(f"   Risk: {result.risk_level.value}\n")
        
        return 0
    
    if args.quick:
        change_type, domain = args.quick
        result = validator.quick_check(change_type, domain)
        print(result.to_json())
        return 0 if result.status == ValidationStatus.APPROVED else 1
    
    if args.check:
        with open(args.check, 'r') as f:
            change = json.load(f)
        result = validator.validate(change)
        print(result.to_json())
        return 0 if result.status in [ValidationStatus.APPROVED, ValidationStatus.NEEDS_NOTIFICATION] else 1
    
    parser.print_help()
    return 1


if __name__ == "__main__":
    exit(main())