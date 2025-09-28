# Calculator Application

This is a simple calculator application that evaluates mathematical expressions provided as command-line arguments.

## Features

*   Supports addition, subtraction, multiplication, and division.
*   Handles operator precedence (multiplication and division are performed before addition and subtraction).
*   Provides a formatted output of the expression and its result within a box.
*   Includes unit tests to ensure the calculator functions correctly.

## Usage

To use the calculator, run `main.py` with the expression as a command-line argument:

```bash
python main.py "3 + 5 * 2"
```

This will output:

```
┌───────────┐
│  3 + 5 * 2  │
│             │
│  =          │
│             │
│  13         │
└───────────┘
```

## Files

*   `main.py`: The main entry point of the application.
*   `pkg/calculator.py`: Defines the `Calculator` class, which evaluates the expressions.
*   `pkg/render.py`: Defines the `render` function, which formats the output.
*   `tests.py`: Contains unit tests for the `Calculator` class.

## Running Tests

To run the unit tests, execute the `tests.py` file:

```bash
python tests.py
```

## Example Usage from Python
```python
from pkg.calculator import Calculator

calculator = Calculator()
result = calculator.evaluate("3 + 7 * 2")
print(result)
```
