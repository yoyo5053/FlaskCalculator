from playwright.sync_api import Page, expect

BASE_URL = "http://127.0.0.1:5000"

def test_addition(page: Page):
    page.goto(BASE_URL)
    page.fill("#num1", "5")
    page.fill("#num2", "3")
    page.select_option("#operation", "add")
    page.click("input[type='submit']")
    result = page.locator(".result-box p")
    expect(result).to_have_text("8")

def test_subtraction(page: Page):
    page.goto(BASE_URL)
    page.fill("#num1", "10")
    page.fill("#num2", "4")
    page.select_option("#operation", "subtract")
    page.click("input[type='submit']")
    result = page.locator(".result-box p")
    expect(result).to_have_text("6")

def test_multiplication(page: Page):
    page.goto(BASE_URL)
    page.fill("#num1", "6")
    page.fill("#num2", "7")
    page.select_option("#operation", "multiply")
    page.click("input[type='submit']")
    result = page.locator(".result-box p")
    expect(result).to_have_text("42")

def test_division(page: Page):
    page.goto(BASE_URL)
    page.fill("#num1", "15")
    page.fill("#num2", "3")
    page.select_option("#operation", "divide")
    page.click("input[type='submit']")
    result = page.locator(".result-box p")
    expect(result).to_have_text("5")

def test_division_by_zero(page: Page):
    page.goto(BASE_URL)
    page.fill("#num1", "10")
    page.fill("#num2", "0")
    page.select_option("#operation", "divide")
    page.click("input[type='submit']")
    error = page.locator(".result-box p")
    expect(error).to_have_text("Division by zero is not allowed.")

def test_invalid_input(page: Page):
    page.goto(BASE_URL)
    page.fill("#num1", "")
    page.fill("#num2", "123")
    page.click("input[type='submit']")
    error = page.locator(".result-box p")
    expect(error).to_have_text("Invalid input. Please enter valid numbers.")