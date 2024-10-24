import os
from flask import Flask, jsonify, render_template, request
from controllers.rule_controller import rule_app
from database.db_setup import setup_database
from flask_cors import CORS

# Initialize the Flask app with specified template and static folders
app = Flask(__name__, static_folder='../frontend/static', template_folder='../frontend/templates')

# Enable CORS
CORS(app)

# Initialize the database
setup_database()

@app.route('/')
def home():
    # Print the path to index.html for debugging
    index_path = os.path.join(app.template_folder, 'index.html')
    print(f"Looking for template at: {index_path}")  # Debugging statement
    return render_template('index.html')

# Register the blueprint for rule endpoints
app.register_blueprint(rule_app, url_prefix='/api')

@app.route('/api/create_rule', methods=['POST'])
def create_rule():
    data = request.get_json()
    rule_string = data.get('rule_string')
    parameters = data.get('parameters')
    # Implement your rule creation logic here and return a response
    return jsonify({"status": "success", "rule_string": rule_string, "parameters": parameters})

@app.route('/api/combine_rule', methods=['POST'])
def combine_rule():
    data = request.get_json()
    rule1 = data.get('rule1')
    rule2 = data.get('rule2')
    operator = data.get('operator')
    # Implement your combination logic here
    return jsonify({"status": "success", "combined_rule": f"{rule1} {operator} {rule2}"})

@app.route('/api/evaluate_rule', methods=['POST'])
def evaluate_rule():
    data = request.json
    
    # Validate the request
    if 'data' not in data or 'rule' not in data:
        return jsonify({'error': "Missing 'data' or 'rule' in request body"}), 400
    
    rule = data['rule']
    attributes = data['data']

    # Debugging output
    print(f"Received rule: {rule} and attributes: {attributes}")

    # Extracting the values
    try:
        attribute1 = float(attributes['attribute1'])  # Convert to float
        attribute2 = float(attributes['attribute2'])  # Convert to float
    except (ValueError, KeyError):
        return jsonify({'error': 'Invalid input data'}), 400

    # Debugging output
    print(f"Evaluating: {rule} with attribute1: {attribute1}, attribute2: {attribute2}")

    # Evaluate the rule (simple example)
    try:
        # Replace attributes in the rule with actual values
        eval_rule = rule.replace('attribute1', str(attribute1)).replace('attribute2', str(attribute2))
        result = eval(eval_rule)  # Evaluate the rule
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    return jsonify({'result': result})


@app.route('/submit', methods=['POST'])
def submit():
    input_value = request.form.get('inputField')
    return f"You entered: {input_value}"

# Custom error handling for common HTTP errors
@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(debug=True)  # Change to debug=False in production
