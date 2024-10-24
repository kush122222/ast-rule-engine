document.addEventListener('DOMContentLoaded', () => {
    // --- Create Rule Section ---

    // Add parameter functionality for Create Rule
    document.getElementById('addParam').addEventListener('click', () => {
        const paramContainer = document.getElementById('parametersContainer');
        const newParam = document.createElement('div');
        newParam.classList.add('parameter');
        newParam.innerHTML = `
            <input type="text" class="paramKey" placeholder="Key (e.g. age)" required>
            <input type="text" class="paramValue" placeholder="Value (e.g. 18)" required>
            <button type="button" class="removeParam">Remove</button>`;
        paramContainer.appendChild(newParam);

        // Remove parameter functionality
        newParam.querySelector('.removeParam').addEventListener('click', () => {
            paramContainer.removeChild(newParam);
        });
    });

    // Create Rule API call with parameters
    document.getElementById('createRuleForm').addEventListener('submit', async (event) => {
        event.preventDefault(); // Prevent normal form submission
        const ruleString = document.getElementById('ruleString').value;

        const params = [];
        document.querySelectorAll('.parameter').forEach(param => {
            const key = param.querySelector('.paramKey').value;
            const value = param.querySelector('.paramValue').value;
            params.push({ key, value });
        });

        try {
            const response = await fetch('/api/create_rule', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ rule_string: ruleString, parameters: params }),
            });
            if (!response.ok) throw new Error(`Error: ${response.status}`);
            const result = await response.json();
            document.getElementById('createRuleResult').textContent = JSON.stringify(result, null, 2);
        } catch (error) {
            document.getElementById('createRuleResult').textContent = `Failed to create rule: ${error.message}`;
        }
    });

    // --- Combine Rules Section ---

    // Combine Rule API call
    document.getElementById('combineRuleForm').addEventListener('submit', async (event) => {
        event.preventDefault();
        const rule1 = document.getElementById('rule1').value;
        const rule2 = document.getElementById('rule2').value;
        const operator = document.getElementById('combineOperator').value;

        try {
            const response = await fetch('/api/combine_rule', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ rule1, rule2, operator }),
            });
            if (!response.ok) throw new Error(`Error: ${response.status}`);
            const result = await response.json();
            document.getElementById('combineRuleResult').textContent = JSON.stringify(result, null, 2);
        } catch (error) {
            document.getElementById('combineRuleResult').textContent = `Failed to combine rules: ${error.message}`;
        }
    });

    // --- Evaluate Rule Section ---

    // Add data parameter functionality for Evaluate Rule
    document.getElementById('addDataParam').addEventListener('click', () => {
        const dataContainer = document.getElementById('parametersContainerEvaluate');
        const newDataParam = document.createElement('div');
        newDataParam.classList.add('data-parameter');
        newDataParam.innerHTML = `
            <input type="text" class="dataKey" placeholder="Key (e.g. age)" required>
            <input type="text" class="dataValue" placeholder="Value (e.g. 25)" required>
            <button type="button" class="removeDataParam">Remove</button>`;
        dataContainer.appendChild(newDataParam);

        // Remove data parameter functionality
        newDataParam.querySelector('.removeDataParam').addEventListener('click', () => {
            dataContainer.removeChild(newDataParam);
        });
    });

    // Evaluate Rule API call with data parameters
    // Evaluate Rule API call with data parameters
    document.getElementById('evaluateRuleForm').addEventListener('submit', async (event) => {
        event.preventDefault();  // Prevent form from submitting normally
        
        const ruleString = document.getElementById('evaluateRuleString').value;  // Get the rule string
        const dataParams = {}; // Initialize an empty object for parameters

        // Collect parameters from the form inputs
        document.querySelectorAll('.data-parameter').forEach(param => {
            const key = param.querySelector('.dataKey').value;   // Key input
            const value = param.querySelector('.dataValue').value;  // Value input
            dataParams[key] = parseFloat(value);  // Add key-value pair to dataParams and convert value to a number
        });

        console.log('Rule String:', ruleString); // Log rule string
        console.log('Data Parameters:', dataParams); // Log data parameters

        try {
            const response = await fetch('/api/evaluate_rule', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    data: dataParams, // Nesting data parameters in a 'data' object
                    rule: ruleString, // Including the rule string
                }),
            });

            const result = await response.json();

            if (!response.ok) throw new Error(result.error || 'Evaluation failed');

            // Display the result without resetting the form
            document.getElementById('evaluateRuleResult').textContent = `Result: ${result.result}`;

        } catch (error) {
            // Display error message without resetting the form
            document.getElementById('evaluateRuleResult').textContent = `Failed to evaluate rule: ${error.message}`;
        }
    });
});