# calculator/pkg/calculator.py

class Calculator:
    def __init__(self):
        self.operators = {
            "+": lambda a, b: a + b,
            "-": lambda a, b: a - b,
            "*": lambda a, b: a * b,
            "/": lambda a, b: a / b,
        }
        self.precedence = {
            "+": 1,
            "-": 1,
            "*": 2,
            "/": 2,
        }

    def evaluate(self, expression):
        if not expression or expression.isspace():
            return None
        tokens = expression.strip().split()
        return self._evaluate_infix(tokens)

    def _evaluate_infix(self, tokens):
        values = []
        operators = []

        for token in tokens:
            if token in self.operators:
                while (
                    operators
                    and operators[-1] in self.operators
                    and self.precedence[operators[-1]] >= self.precedence[token]
                ):
                    self._apply_operator(operators, values)
                operators.append(token)
            elif token.isdigit() or (token[0] == '-' and token[1:].isdigit()):
                values.append(int(token))
            elif token == "(":
                operators.append(token)
            elif token == ")":
                while operators and operators[-1] != "(":
                    self._apply_operator(operators, values)
                if operators and operators[-1] == "(":
                    operators.pop()  # Pop "("
                else:
                    raise ValueError("Mismatched parentheses")
            else:
                raise ValueError(f"Unknown token: {token}")

        while operators:
            self._apply_operator(operators, values)

        if len(values) != 1:
            raise ValueError("Invalid expression")
        return values[0]

    def _apply_operator(self, operators, values):
        operator = operators.pop()
        right = values.pop()
        left = values.pop()
        values.append(self.operators[operator](left, right))
