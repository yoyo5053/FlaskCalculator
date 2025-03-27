from flask import Flask, render_template, request

app = Flask(__name__)

class Calculator:
    def __init__(self, num1, num2, operation):
        self.num1 = num1
        self.num2 = num2
        self.operation = operation

    def calculate(self):
        if self.operation == "add":
            return self.num1 + self.num2
        elif self.operation == "subtract":
            return self.num1 - self.num2
        elif self.operation == "multiply":
            return self.num1 * self.num2
        elif self.operation == "divide":
            if self.num2 == 0:
                return "Division by zero is not allowed."
            else:
                return self.num1 / self.num2
        else:
            return "Invalid operation."

@app.route("/", methods=["GET", "POST"])
def calculator():
    result = None
    error = None

    if request.method == "POST":
        num1 = request.form.get("num1")
        num2 = request.form.get("num2")
        operation = request.form.get("operation")

        # Validate input
        try:
            num1 = float(num1)
            num2 = float(num2)
        except (TypeError, ValueError):
            error = "Invalid input. Please enter valid numbers."
        else:
            calc = Calculator(num1, num2, operation)
            result = calc.calculate()

    return render_template("calculator.html", result=result, error=error)

if __name__ == "__main__":
    app.run(debug=True)