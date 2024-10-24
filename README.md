# Rule Engine with AST

This project implements a Rule Engine using an Abstract Syntax Tree (AST) to determine user eligibility based on various attributes such as age, department, income, and spending. The application allows dynamic rule creation, combination, and evaluation through a web interface.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Folder Structure](#folder-structure)
- [Setup Instructions](#setup-instructions)
- [API Endpoints](#api-endpoints)
- [Running the Application](#running-the-application)
- [License](#license)

## Features

- Create, combine, and evaluate rules dynamically.
- Serve a user-friendly web interface for interaction.
- Utilize a backend powered by Flask for handling API requests and database interactions.
- Enable CORS for cross-origin requests.

## Technologies Used

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python, Flask
- **Database**: SQLite (or your chosen database)
- **Libraries**: Flask-CORS for handling CORS, etc.



## Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd rule-engine-with-ast

go to backen folder on terminal 

cd /Users/kushalsgowda/Desktop/rule-engine-with-ast/backend(eg)

python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

pip install -r requirements.txt

run server python app.py

Access the frontend:

Open your browser and go to http://127.0.0.1:5000.

Running the Application
Make sure your Flask server is running and access the application through your web browser at http://127.0.0.1:5000

user can check the end point or how the ast is working on post man like this 

Open Postman
If you don’t have Postman installed, you can download it from Postman’s official website.

2. Create a New Request
Click on "New" in the top left corner.
Select "Request".
Give your request a name and optionally organize it in a collection.
3. Set the Request Type and URL
Choose the appropriate HTTP method (GET, POST, etc.) from the dropdown next to the URL input field.
For example, if you want to create a rule, select POST.
Enter the URL of your API endpoint. For example, to create a rule, use:
arduino
Copy code
http://127.0.0.1:5000/api/create_rule
4. Set Up the Request Body
For POST requests, you need to send data in the request body.

Click on the "Body" tab.
Select "raw" and choose JSON from the dropdown on the right.
Enter your JSON data. For example, to create a rule:
json
Copy code
{
    "rule": "age > 30 AND department = 'Sales'"
}
5. Send the Request
Click the "Send" button to execute the request.
You should see the response from your API in the section below.
6. Check the Response
Postman will show the response status code (e.g., 200 OK) and the response body.
For the example above, you should see the AST representation returned by your API if the request was successful.
Example Requests
Here are examples of how to test each endpoint:

Create Rule
Method: POST
URL: http://127.0.0.1:5000/api/create_rule
Body:
json
Copy code
{
    "rule": "age > 30 AND department = 'Sales'"
}
Combine Rules
Method: POST
URL: http://127.0.0.1:5000/api/combine_rules
Body:
json
Copy code
{
    "rule1": "age > 30",
    "rule2": "department = 'Sales'",
    "operator": "AND"
}
Evaluate Rule
Method: POST
URL: http://127.0.0.1:5000/api/evaluate_rule
Body:
json
Copy code
{
    "ast": "<your_ast>",
    "data": {
        "age": 35,
        "department": "Sales"
    }
}

Frontend input 
create rule 
add any rule name
then enter the rule as per the placeholder 
Combine rule 
give two rule which created as the same rule format 
Evaluate rule
do as in the place holder 

u can verify the logic in endpoints also on post man as mentioned in above


