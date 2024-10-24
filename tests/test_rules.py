# tests/test_rules.py
import unittest
from backend.services.rule_service import create_rule, evaluate_rule


class TestRuleEngine(unittest.TestCase):

    def test_create_rule(self):
        rule = "age > 30 AND department = 'Sales'"
        ast = create_rule(rule)
        self.assertIsNotNone(ast)

    def test_evaluate_rule(self):
        rule = "age > 30 AND department = 'Sales'"
        ast = create_rule(rule)
        data = {"age": 35, "department": "Sales", "salary": 60000, "experience": 3}
        result = evaluate_rule(ast, data)
        self.assertTrue(result)

    def test_invalid_rule(self):
        with self.assertRaises(ValueError):
            create_rule("invalid_rule")

if __name__ == '__main__':
    unittest.main()
