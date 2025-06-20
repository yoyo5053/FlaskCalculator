import pytest
from decimal import Decimal
from main import app, Calculator, validate_input, DivisionByZeroError, InvalidOperationError

@pytest.mark.parametrize("num1, num2, operation, expected", [
    (Decimal("1"), Decimal("1"), "add", Decimal("2")),
    (Decimal("5"), Decimal("3"), "subtract", Decimal("2")),
    (Decimal("4"), Decimal("3"), "multiply", Decimal("12")),
    (Decimal("6"), Decimal("2"), "divide", Decimal("3")),
])
def test_calculate_normaux(num1, num2, operation, expected):
    calc = Calculator(num1, num2, operation)
    assert calc.calculate() == expected

def test_big_numbers():
    big = Decimal(10**18)
    calc = Calculator(big, big, "add")
    assert calc.calculate() == big * 2

def test_floats():
    calc = Calculator(Decimal("2.5"), Decimal("4.2"), "multiply")
    assert calc.calculate() == Decimal("10.5")

def test_zero_operand():
    assert Calculator(Decimal("0"), Decimal("12345"), "multiply").calculate() == 0
    assert Calculator(Decimal("0"), Decimal("0"), "add").calculate() == 0

def test_division_par_zero():
    calc = Calculator(Decimal("5"), Decimal("0"), "divide")
    # La méthode renvoie le message d'erreur en chaîne de caractères
    result = calc.calculate()
    assert isinstance(result, str)
    assert result == "Division by zero is not allowed."

def test_invalid_operation():
    with pytest.raises(InvalidOperationError):
        Calculator(Decimal("1"), Decimal("2"), "modulo")

@pytest.mark.parametrize("input_str, expected", [
    ("123.45", Decimal("123.45")),
    ("-0.001", Decimal("-0.001")),
])
def test_validate_input_valide(input_str, expected):
    assert validate_input(input_str) == expected

@pytest.mark.parametrize("bad_input", ["abc", "", None])
def test_validate_input_invalide(bad_input):
    assert validate_input(bad_input) is None