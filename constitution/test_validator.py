#!/usr/bin/env python3
"""
Unit tests for the Constitutional Validator.
"""

import unittest
import sys
import json
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from constitution.validator import (
    ConstitutionValidator,
    ValidationResult,
    ValidationStatus,
    RiskLevel,
    Principle
)


class TestConstitutionValidator(unittest.TestCase):
    """Test cases for the ConstitutionValidator."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.validator = ConstitutionValidator()
    
    def test_validator_initialization(self):
        """Test that validator loads correctly."""
        self.assertEqual(len(self.validator.principles), 4)
        self.assertEqual(len(self.validator.rules), 4)
        
        # Check principle IDs
        principle_ids = [p.id for p in self.validator.principles]
        self.assertIn("principle-helpfulness", principle_ids)
        self.assertIn("principle-safety", principle_ids)
    
    def test_low_risk_change_approved(self):
        """Test that low-risk changes are approved."""
        change = {
            "type": "pattern",
            "domain": "agent-framework",
            "has_rollback": True,
            "backup_created": True,
            "rationale": "Test rationale",
            "evidence": "Test evidence"
        }
        
        result = self.validator.validate(change)
        self.assertEqual(result.status, ValidationStatus.APPROVED)
        self.assertEqual(result.risk_level, RiskLevel.LOW)
    
    def test_high_risk_core_behavior(self):
        """Test that core behavior changes are high risk."""
        change = {
            "type": "behavior",
            "domain": "agent-framework",
            "affects_core_behavior": True,
            "has_rollback": True,
            "rationale": "Improve responses"
        }
        
        result = self.validator.validate(change)
        self.assertEqual(result.status, ValidationStatus.NEEDS_NOTIFICATION)
        self.assertEqual(result.risk_level, RiskLevel.HIGH)
    
    def test_critical_constitutional_change(self):
        """Test that constitutional changes are critical."""
        change = {
            "type": "amendment",
            "domain": "constitution",
            "affects_constitution": True,
            "has_rollback": True,
            "rationale": "Add new principle"
        }
        
        result = self.validator.validate(change)
        self.assertEqual(result.status, ValidationStatus.NEEDS_APPROVAL)
        self.assertEqual(result.risk_level, RiskLevel.CRITICAL)
    
    def test_safety_violation_rejected(self):
        """Test that safety violations are rejected."""
        change = {
            "type": "capability",
            "domain": "agent-framework",
            "enables_dangerous_actions": True,
            "has_rollback": True,
            "rationale": "Enable new feature"
        }
        
        result = self.validator.validate(change)
        self.assertEqual(result.status, ValidationStatus.REJECTED)
        self.assertTrue(len(result.violated_principles) > 0)
        self.assertIn("Safety", result.violated_principles[0])
    
    def test_honesty_violation_rejected(self):
        """Test that honesty violations are rejected."""
        change = {
            "type": "behavior",
            "domain": "agent-framework",
            "hides_information": True,
            "has_rollback": True,
            "rationale": "Simplify output"
        }
        
        result = self.validator.validate(change)
        self.assertEqual(result.status, ValidationStatus.REJECTED)
        self.assertTrue(any("Honesty" in vp for vp in result.violated_principles))
    
    def test_helpfulness_violation_rejected(self):
        """Test that helpfulness violations are rejected."""
        change = {
            "type": "optimization",
            "domain": "agent-framework",
            "reduces_user_value": True,
            "has_rollback": True,
            "rationale": "Faster responses"
        }
        
        result = self.validator.validate(change)
        self.assertEqual(result.status, ValidationStatus.REJECTED)
        self.assertTrue(any("Helpfulness" in vp for vp in result.violated_principles))
    
    def test_alignment_violation_rejected(self):
        """Test that alignment violations are rejected."""
        change = {
            "type": "behavior",
            "domain": "agent-framework",
            "hidden_objective": True,
            "has_rollback": True,
            "rationale": "Better outcomes"
        }
        
        result = self.validator.validate(change)
        self.assertEqual(result.status, ValidationStatus.REJECTED)
        self.assertTrue(any("Alignment" in vp for vp in result.violated_principles))
    
    def test_forbidden_domain_violation(self):
        """Test that forbidden domains are caught."""
        change = {
            "type": "modification",
            "domain": "user-data-exfiltration",
            "has_rollback": True,
            "rationale": "Backup data"
        }
        
        result = self.validator.validate(change)
        # Should have violated rules
        self.assertTrue(len(result.violated_rules) > 0 or 
                       result.status in [ValidationStatus.REJECTED, ValidationStatus.NEEDS_APPROVAL])
    
    def test_missing_rollback_flagged(self):
        """Test that missing rollback is flagged."""
        change = {
            "type": "workflow",
            "domain": "agent-framework",
            "has_rollback": False,
            "rationale": "New workflow"
        }
        
        result = self.validator.validate(change)
        # Should have violations for missing rollback
        self.assertTrue(len(result.violated_rules) > 0 or
                       result.recommendations)
    
    def test_missing_rationale_flagged(self):
        """Test that missing rationale is flagged."""
        change = {
            "type": "pattern",
            "domain": "agent-framework",
            "has_rollback": True,
            "rationale": "",
            "evidence": "Some evidence"
        }
        
        result = self.validator.validate(change)
        # Should have violations or recommendations
        self.assertTrue(len(result.violated_rules) > 0 or
                       len(result.recommendations) > 0)
    
    def test_quick_check(self):
        """Test the quick_check convenience method."""
        result = self.validator.quick_check("pattern", "agent-framework")
        self.assertEqual(result.status, ValidationStatus.APPROVED)
        self.assertEqual(result.risk_level, RiskLevel.LOW)
    
    def test_result_serialization(self):
        """Test that results can be serialized."""
        change = {
            "type": "pattern",
            "domain": "agent-framework",
            "has_rollback": True,
            "rationale": "Test",
            "evidence": "Test"
        }
        
        result = self.validator.validate(change)
        
        # Test dict conversion
        result_dict = result.to_dict()
        self.assertIn("status", result_dict)
        self.assertIn("message", result_dict)
        self.assertIn("risk_level", result_dict)
        
        # Test JSON conversion
        result_json = result.to_json()
        parsed = json.loads(result_json)
        self.assertEqual(parsed["status"], result.status.value)
    
    def test_risk_classification(self):
        """Test risk classification logic."""
        # Critical
        change = {"affects_constitution": True}
        self.assertEqual(self.validator.classify_risk(change), RiskLevel.CRITICAL)
        
        # High
        change = {"affects_core_behavior": True}
        self.assertEqual(self.validator.classify_risk(change), RiskLevel.HIGH)
        
        # High - new domain
        change = {"expands_to_new_domain": True}
        self.assertEqual(self.validator.classify_risk(change), RiskLevel.HIGH)
        
        # Medium - agent definitions
        change = {"affects_agent_definitions": True}
        self.assertEqual(self.validator.classify_risk(change), RiskLevel.MEDIUM)
        
        # Low - default
        change = {"type": "pattern"}
        self.assertEqual(self.validator.classify_risk(change), RiskLevel.LOW)


class TestPrinciples(unittest.TestCase):
    """Test individual principle validation."""
    
    def test_helpfulness_validation(self):
        """Test helpfulness principle validation."""
        principle = Principle(
            id="principle-helpfulness",
            name="Helpfulness",
            description="Test",
            validations=[]
        )
        
        # Should pass
        passed, reason = principle.validate({})
        self.assertTrue(passed)
        
        # Should fail - reduces user value
        passed, reason = principle.validate({"reduces_user_value": True})
        self.assertFalse(passed)
        
        # Should fail - creates friction
        passed, reason = principle.validate({"creates_friction": True})
        self.assertFalse(passed)
    
    def test_honesty_validation(self):
        """Test honesty principle validation."""
        principle = Principle(
            id="principle-honesty",
            name="Honesty",
            description="Test",
            validations=[]
        )
        
        # Should pass
        passed, reason = principle.validate({})
        self.assertTrue(passed)
        
        # Should fail - hides information
        passed, reason = principle.validate({"hides_information": True})
        self.assertFalse(passed)
        
        # Should fail - deceptive
        passed, reason = principle.validate({"deceptive": True})
        self.assertFalse(passed)
    
    def test_safety_validation(self):
        """Test safety principle validation."""
        principle = Principle(
            id="principle-safety",
            name="Safety",
            description="Test",
            validations=[]
        )
        
        # Should pass
        passed, reason = principle.validate({})
        self.assertTrue(passed)
        
        # Should fail - enables dangerous actions
        passed, reason = principle.validate({"enables_dangerous_actions": True})
        self.assertFalse(passed)
        
        # Should fail - bypasses safeguards
        passed, reason = principle.validate({"bypasses_safeguards": True})
        self.assertFalse(passed)
    
    def test_alignment_validation(self):
        """Test alignment principle validation."""
        principle = Principle(
            id="principle-alignment",
            name="Alignment",
            description="Test",
            validations=[]
        )
        
        # Should pass
        passed, reason = principle.validate({})
        self.assertTrue(passed)
        
        # Should fail - hidden objective
        passed, reason = principle.validate({"hidden_objective": True})
        self.assertFalse(passed)
        
        # Should fail - against user boundaries
        passed, reason = principle.validate({"against_user_boundaries": True})
        self.assertFalse(passed)


def run_tests():
    """Run all tests and return success status."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestConstitutionValidator))
    suite.addTests(loader.loadTestsFromTestCase(TestPrinciples))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)