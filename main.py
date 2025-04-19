from flask import Flask, render_template, request
from flask_restx import Api, Resource, fields
from decimal import Decimal, InvalidOperation
from loguru import logger
import sys

# Initialize Flask application
app = Flask(__name__)

# Initialize Flask-RESTx API
api = Api(app,
          version='1.0',
          title='Calculator API',
          description='A simple calculator API with basic arithmetic operations',
          prefix='/api',
          doc='/api/'
          )

# Configure Loguru for logging
logger.add("file_{time}.log", rotation="1 day", retention="7 days", level="INFO")
logger.add(sys.stdout, level="INFO")

class Calculator:
    """
    A class for performing basic arithmetic calculations.
    """
    OPERATIONS = {
        "add": lambda x, y: x + y,
        "subtract": lambda x, y: x - y,
        "multiply": lambda x, y: x * y,
        "divide": lambda x, y: x / y if y != 0 else "Division by zero is not allowed.",
    }

    def __init__(self, num1, num2, operation):
        """
        Initializes the Calculator instance with two numbers and an operation.

        Args:
            num1 (Decimal): The first number for the calculation.
            num2 (Decimal): The second number for the calculation.
            operation (str): The operation to perform (add, subtract, multiply, divide).
        """
        self.num1 = num1
        self.num2 = num2
        self.operation = operation

    def calculate(self):
        """
        Performs the calculation based on the provided operation.

        Returns:
            Union[Decimal, str]: The result of the calculation or an error message.
        """
        operation_func = self.OPERATIONS.get(self.operation)
        if operation_func:
            try:
                result = operation_func(self.num1, self.num2)
                logger.info(f"Calculation performed: {self.num1} {self.operation} {self.num2} = {result}")
                return result
            except Exception as e:
                logger.error(f"Error during calculation: {e}")
                return "An error occurred during calculation."
        return "Invalid operation."

def validate_input(num1, num2):
    """
    Validates if the input strings can be converted to Decimal numbers.

    Args:
        num1 (str): The first input number as a string.
        num2 (str): The second input number as a string.

    Returns:
        Tuple[Optional[Decimal], Optional[Decimal]]: A tuple containing the validated Decimal numbers,
                                                    or None for either if validation fails.
    """
    try:
        return Decimal(num1), Decimal(num2)
    except (InvalidOperation, TypeError, ValueError):
        return None, None

# Define the namespace for the calculator API
ns = api.namespace('calculate', description='Basic arithmetic operations')

# Define the data transfer object (DTO) for the calculator input
calculator_model = api.model('CalculatorInput', {
    'num1': fields.String(required=True, description='First number'),
    'num2': fields.String(required=True, description='Second number'),
    'operation': fields.String(required=True, description='Operation (add, subtract, multiply, divide)')
})

# Define the data transfer object (DTO) for the calculation result
result_model = api.model('Result', {
    'result': fields.String(description='Calculation result')
})

@ns.route('/')
class Calculation(Resource):
    """
    Resource representing the calculation endpoint.
    """
    @ns.expect(calculator_model)
    @ns.marshal_with(result_model)
    def post(self):
        """
        Performs a calculation based on the provided input.
        """
        data = api.payload
        num1_str = data.get('num1')
        num2_str = data.get('num2')
        operation = data.get('operation')

        validated_num1, validated_num2 = validate_input(num1_str, num2_str)

        if validated_num1 is None or validated_num2 is None:
            return {'result': "Invalid input. Please enter valid numbers."}, 400
        else:
            calc = Calculator(validated_num1, validated_num2, operation)
            result = calc.calculate()
            return {'result': str(result)}

@app.route("/", methods=["GET", "POST"])
def calculator_ui():
    """
    Route for the calculator web user interface.
    Handles both GET requests for displaying the form and POST requests for performing calculations.
    """
    result = None
    error = None

    if request.method == "POST":
        num1 = request.form.get("num1")
        num2 = request.form.get("num2")
        operation = request.form.get("operation")

        validated_num1, validated_num2 = validate_input(num1, num2)

        if validated_num1 is None or validated_num2 is None:
            error = "Invalid input. Please enter valid numbers."
        else:
            calc = Calculator(validated_num1, validated_num2, operation)
            result = calc.calculate()

    return render_template("calculator.html", result=result, error=error)

if __name__ == "__main__":
    app.run(debug=True)