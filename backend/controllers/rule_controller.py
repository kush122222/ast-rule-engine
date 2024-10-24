from flask import Blueprint, request, jsonify
import logging
from services.rule_service import create_rule, evaluate_rule, parse_rule_to_list, create_ast_from_list , combine_rules
import sqlite3

rule_app = Blueprint('rule_app', __name__)

def create_connection():
    conn = sqlite3.connect('rules.db')
    return conn

@rule_app.route('/create_rule', methods=['POST'])
def create_rule_endpoint():
    data = request.json
    rule_string = data.get('rule_string', '')
    print(f"Received rule string: {rule_string}")  # Debugging line

    # Parse and create AST from rule string
    ast_list = parse_rule_to_list(rule_string)
    print(f"Parsed AST List: {ast_list}")  # Debugging line

    ast = create_ast_from_list(ast_list)
    print(f"Created AST: {ast}")  # Debugging line

    if ast is None:
        return jsonify(error="AST creation failed"), 400

    # Save the rule in the database
    conn = create_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('INSERT INTO rules (rule) VALUES (?)', (rule_string,))
        conn.commit()
        print("Rule saved to database.")  # Debugging line
    except Exception as e:
        print(f"Error saving rule: {str(e)}")  # Debugging line
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

    return jsonify(ast=ast.to_dict()), 200


@rule_app.route('/combine_rules', methods=['POST'])
def combine_rules_endpoint():
    data = request.get_json()
    rule1 = data.get('rule1')
    rule2 = data.get('rule2')
    operator = data.get('operator')
    
    if not all([rule1, rule2, operator]):
        return jsonify({"error": "Missing rule1, rule2, or operator"}), 400

    conn = create_connection()

    try:
        combined_rule = combine_rules(rule1, rule2, operator)
        
        # Optionally save the combined rule to the database
        # cursor = conn.cursor()
        # cursor.execute('INSERT INTO rules (combined_rule) VALUES (?)', (combined_rule,))
        # conn.commit()

        return jsonify({"combined_rule": combined_rule}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        conn.close()



@rule_app.route('/evaluate_rule', methods=['POST'])
def evaluate_rule_endpoint():
    # Check if the request body is JSON
    if not request.json:
        return jsonify({"error": "Request body must be JSON"}), 400

    # Extract data and rule from the request
    data = request.json.get('data')
    rule = request.json.get('rule')

    # Validate inputs
    if not data or not rule:
        return jsonify({"error": "Missing 'data' or 'rule' in request body"}), 400

    try:
        # Parse the rule into a list
        ast_list = parse_rule_to_list(rule)
        print(f"Parsed AST List: {ast_list}")  # Debugging line

        # Create AST from the list
        ast = create_ast_from_list(ast_list)
        print(f"Created AST: {ast}")  # Debugging line

        if ast is None:
            return jsonify({"error": "AST creation failed"}), 400

        # Evaluate the rule with the provided data
        result = evaluate_rule(ast, data)
        print(f"Evaluation result: {result}")  # Debugging line

        return jsonify({"result": result}), 200

    except Exception as e:
        print(f"Error during evaluation: {str(e)}")  # Debugging line
        return jsonify({"error": str(e)}), 500