import re
from models.ast_node import ASTNode
from typing import Any, List, Union
from flask import Blueprint
import sqlite3


def parse_condition(condition: str) -> List[str]:
    """Parse a single condition string into a list of [attribute, operator, value]."""
    match = re.match(r"(\w+)\s*([<>!=]+)\s*(.+)", condition)
    if match:
        return list(match.groups())
    raise ValueError(f"Invalid condition: {condition}")


def parse_rule_to_list(rule_string: str) -> List[Union[str, int]]:
    # A simple parser that splits rules based on spaces
    tokens = rule_string.split()  # Basic example; more robust parsing may be needed
    parsed_list = []

    for token in tokens:
        if token.isdigit():  # Check if token is a number
            parsed_list.append(int(token))  # Convert to integer
        elif token in ['AND', 'OR', '>', '<', '=', '>=', '<=']:
            parsed_list.append(token)  # Keep operators as strings
        else:
            parsed_list.append(token)  # Keep variable names as strings

    return parsed_list


def create_rule(rule_string: str) -> Any:
    """Create a rule (AST) from the rule string."""
    operators = []
    conditions = re.split(r'\s+(AND|OR)\s+', rule_string)
    
    ast = [parse_condition(condition.strip()) for condition in conditions if condition.strip()]
    
    return _combine_conditions(ast, operators)


def _combine_conditions(ast: List[List[str]], operators: List[str]) -> Any:
    """Combine conditions into an AST based on logical operators."""
    if not ast:
        return None

    combined_ast = create_condition_node(ast[0])
    for operator, next_condition in zip(operators, ast[1:]):
        combined_ast = _combine_nodes(combined_ast, create_condition_node(next_condition), operator)
    return combined_ast


def create_ast_from_list(parsed_list: List[Union[str, int]]) -> ASTNode:
    def build_ast(tokens):
        if not tokens:
            return None

        # Check for logical operators first
        for op in ['AND', 'OR']:
            idx = find_operator(tokens, op)
            if idx != -1:
                left = build_ast(tokens[:idx])
                right = build_ast(tokens[idx + 1:])
                node = ASTNode(node_type='operator', value=op)
                node.left = left
                node.right = right
                return node

        # Check for relational operators next
        for op in ['>', '<', '=', '>=', '<=']:
            idx = find_operator(tokens, op)
            if idx != -1:
                left = build_ast(tokens[:idx])
                right = build_ast(tokens[idx + 1:])
                node = ASTNode(node_type='operator', value=op)
                node.left = left
                node.right = right
                return node

        # If no operators are found, assume it's an operand
        token = tokens[0]
        return ASTNode(node_type='operand', value=token)

    # Create the AST from the parsed list
    ast = build_ast(parsed_list)
    return ast


def find_operator(tokens: List[Union[str, int]], operator: str) -> int:
    """Helper function to find the operator index in tokens."""
    # Return the index of the operator if it exists in the tokens
    for i in range(len(tokens)):
        if tokens[i] == operator:
            return i
    return -1


def create_condition_node(condition: List[str]) -> ASTNode:
    """Create an AST node from a condition list."""
    if len(condition) != 3:
        raise ValueError("Condition must be a list of three elements")

    left_node = ASTNode('operand', value=condition[0])
    operator_node = ASTNode('operator', value=condition[1])
    right_node_value = convert_to_int_if_needed(condition[2])  # Convert right value
    right_node = ASTNode('operand', value=right_node_value)

    operator_node.left = left_node
    operator_node.right = right_node

    return operator_node


def _combine_nodes(combined_node: ASTNode | None, current_node: ASTNode, operator: str | None) -> ASTNode | None:
    """Combine two AST nodes with the specified operator."""
    if combined_node is None:
        return current_node
    
    if operator is None:
        raise ValueError("Operator must be set before combining nodes.")
    
    operator_node = ASTNode('operator', value=operator)
    operator_node.left = combined_node
    operator_node.right = current_node

    return operator_node


def evaluate_rule(ast: ASTNode, data: dict) -> (int | Any | str | bool):
    if ast.node_type == 'operand':
        return evaluate_operand(ast, data)
    elif ast.node_type == 'operator':
        return evaluate_operator(ast, data)
    raise ValueError("Invalid AST structure.")

def evaluate_operator(ast: ASTNode, data: dict) -> (bool | Any):
    left_value = evaluate_rule(ast.left, data)
    right_value = evaluate_rule(ast.right, data)

    # Debugging output
    print(f"Evaluating: {ast.value} with left {left_value} ({type(left_value)}) and right {right_value} ({type(right_value)})")

    return apply_operator(ast.value, left_value, right_value)

def evaluate_operand(ast: ASTNode, data: dict) -> Any:
    # Fetch value from data, treat it as literal if not found
    value = data.get(ast.value, ast.value)
    
    # Convert value to the appropriate type if it's a string representing a number
    if isinstance(value, str) and value.isdigit():
        return int(value)
    elif isinstance(value, str) and is_float(value):  # Check if it's a float
        return float(value)

    return value

def is_float(value: str) -> bool:
    try:
        float(value)
        return True
    except ValueError:
        return False


def convert_to_int_if_needed(value: Any) -> Any:
    """Convert string digits to integers."""
    if isinstance(value, str) and value.isdigit():
        return int(value)
    return value


def evaluate_single_condition(condition: str, data: dict) -> bool:
    """
    Evaluates a single condition against the data.

    Args:
        condition (str): The condition in string format (e.g. "age > 18").
        data (dict): The data to evaluate against.

    Returns:
        bool: The result of the evaluation.
    """
    parts = condition.split()

    if len(parts) == 3:
        attribute = parts[0]
        operator = parts[1]
        value = parts[2]

        data_value = data.get(attribute)

        if data_value is None:
            raise KeyError(f"Attribute '{attribute}' not found in the provided data.")

        # Ensure the value is correctly compared based on the data type
        value = convert_to_int_if_needed(value)

        # Evaluate the condition based on the operator
        if operator == '>':
            return data_value > value
        elif operator == '<':
            return data_value < value
        elif operator == '==':
            return data_value == value
        elif operator == '>=':
            return data_value >= value
        elif operator == '<=':
            return data_value <= value
        else:
            raise ValueError(f"Unsupported operator: {operator}")

    raise ValueError("Condition format is invalid.")


def apply_operator(operator: str, left_value: Any, right_value: Any) -> (bool | Any):
    """Apply the operator on the left and right values."""
    if operator == '>':
        return left_value > right_value
    elif operator == '<':
        return left_value < right_value
    elif operator == '==':
        return left_value == right_value
    elif operator == '>=':
        return left_value >= right_value
    elif operator == '<=':
        return left_value <= right_value
    elif operator == 'AND':
        return left_value and right_value
    elif operator == 'OR':
        return left_value or right_value
    else:
        raise ValueError(f"Unsupported operator: {operator}")


def create_connection() -> sqlite3.Connection:
    conn = sqlite3.connect('rules.db')
    return conn


rule_app = Blueprint('rule_app', __name__)


def combine_rules(rule1: str, rule2: str, operator: str) -> str:
    """Combine two rules with a logical operator."""
    if operator not in ['AND', 'OR']:
        raise ValueError("Operator must be 'AND' or 'OR'")
    
    return f"({rule1}) {operator} ({rule2})"
