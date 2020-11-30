import argparse, parser, re


_OPERATORS = "/*%^="
_OPERATORS_PRIORITY = {"/": 2, "*": 2, "%": 2, "^": 3, "+": 1, "-": 1}
_SIGN = "+-"
_COMMA = ".,"
_OPEN_PARENTHESES = "("
_CLOSING_PARENTHESES = ")"


def _is_number(n: str) -> bool:
    try:
        float(n)
        return True
    except ValueError:
        return False


class _EquationSolver:
    _equation = None
    reduced_form = None
    _vars_set = None

    def _check_vars(self):
        vars_list = re.findall(pattern=r"[A-Z]+", string=self._equation)
        # Removing duplicate var
        self._vars_set = list(set(vars_list))
        if len(self._vars_set) > 2:
            raise SyntaxError("EquationSolver does not support more than two variables.")

    def _reduce_form(self):
        pass

    def solve(self, equation):
        self._equation = equation
        self._check_vars()
        self._reduce_form()
        return self._equation


class _Calculator:
    _calc = None
    _execution_pile = []

    def _check_vars(self):
        vars_list = re.findall(pattern=r"[A-Z]+", string=self._calc)
        # Removing duplicate var
        vars_set = list(set(vars_list))
        if len(vars_set) > 0:
            raise SyntaxError("Calculator does not support variables.")

    def stack_last_element(self, elem: list) -> str:
        try:
            return elem[-1][0]
        except IndexError:
            return []

    def _resolve_npi(self, npi_list: list):
        stack = []

        for elem in npi_list:
            if _is_number(elem):
                stack.append(elem)
            else:
                last_two_in_stack = stack[-2:]
                del stack[-2:]
                # Power is not noted the same in python
                if elem == "^":
                    result = float(last_two_in_stack[0]) ** float(last_two_in_stack[1])
                elif elem == "*":
                    result = float(last_two_in_stack[0]) * float(last_two_in_stack[1])
                elif elem == "/":
                    result = float(last_two_in_stack[0]) / float(last_two_in_stack[1])
                elif elem == "%":
                    result = float(last_two_in_stack[0]) % float(last_two_in_stack[1])
                elif elem == "+":
                    result = float(last_two_in_stack[0]) + float(last_two_in_stack[1])
                elif elem == "-":
                    result = float(last_two_in_stack[0]) - float(last_two_in_stack[1])

                stack.append(result)

        if len(stack) > 1:
            raise Exception(
                "Unexpected error when trying to resolve npi. Maybe your input format is not accepted?"
            )
        return stack[0]

    def convert_to_tokens(self) -> list:
        tokens = []
        current_char = 0
        last_char = 0
        while current_char < len(self._calc):
            if self._calc[current_char].isnumeric():
                while current_char < len(self._calc) and (
                    self._calc[current_char].isnumeric() or self._calc[current_char] in _COMMA
                ):
                    current_char += 1
            else:
                current_char += 1
            tokens.append(self._calc[last_char:current_char])
            last_char = current_char
        return tokens

    def npi_converter(self, tokens: list) -> list:
        """
        Convert an expression to npi.
        """

        res = []
        stack = []
        for token in tokens:
            print(token)
            if token in _OPERATORS or token in _SIGN:
                # This loop will unpill elem from stack to res if operators on the pile have bigger priority.
                while (
                    stack
                    and not self.stack_last_element(stack) in _OPEN_PARENTHESES
                    and _OPERATORS_PRIORITY[self.stack_last_element(stack)]
                    >= _OPERATORS_PRIORITY[token]
                ):
                    res.append(stack.pop())
                stack.append(token)
            elif token in _OPEN_PARENTHESES:
                stack.append(token)
            elif token in _CLOSING_PARENTHESES:
                while not self.stack_last_element(stack) in _OPEN_PARENTHESES:
                    res.append(stack.pop())
                if self.stack_last_element(stack) in _OPEN_PARENTHESES:
                    stack.pop()
            else:
                if not _is_number(token):
                    raise SyntaxError("Some numbers are not well formated (Comma error).")
                res.append(token)

        return res + stack[::-1]

    def solve(self, calc: str) -> int:
        self._calc = calc
        self._check_vars()
        npi_list = self.npi_converter(self.convert_to_tokens())
        result = self._resolve_npi(npi_list=npi_list)
        return result


class ExpressionResolver:

    expression = None
    _solver = None

    def _check_args(self):
        # Var to check operator is followed by alphanum.
        last_operator = None
        # Var to check good parentheses use.
        parentheses_count = 0
        # Checking comma is followed and preceded by a digit.
        # This is not checking the use of more than one comma in same number !
        for comma in _COMMA:
            comma_split = self.expression.split(comma)
            try:
                if len(comma_split) > 1:
                    for part in comma_split:
                        if part == comma_split[0]:
                            assert len(part) >= 1
                            assert part[-1].isdigit()
                        elif part == comma_split[-1]:
                            assert len(part) >= 1
                            assert part[0].isdigit()
                        else:
                            assert len(part) >= 2
                            assert part[0].isdigit()
                            assert part[-1].isdigit()
            except AssertionError:
                raise SyntaxError("Some numbers are not well formated (Comma error).")

        for c in self.expression:
            # Check allowed char.
            if (
                c not in _OPERATORS
                and c not in _SIGN
                and c not in _OPEN_PARENTHESES
                and c not in _CLOSING_PARENTHESES
                and not c.isalnum()
                and c not in _COMMA
            ):
                raise SyntaxError(
                    "This is not an expression or some of the operators are not reconized."
                )
            # Check multiple _operators before alphanum. Check parenthesis count.
            if c in _OPERATORS and last_operator and last_operator in _OPERATORS:
                raise SyntaxError(
                    "Operators must be followed by a value or a variable, not another operator."
                )
            elif c in _OPERATORS:
                last_operator = c
            elif c.isalnum():
                last_operator = None
            elif c in _OPEN_PARENTHESES:
                parentheses_count += 1
            elif c in _CLOSING_PARENTHESES:
                parentheses_count -= 1

            if parentheses_count < 0:
                raise SyntaxError("Closing parenthesis with no opened one.")

        if (
            self.expression[-1] in _OPERATORS
            or self.expression[-1] in _SIGN
            or (last_operator and last_operator in _OPERATORS)
        ):
            raise SyntaxError("Operators or sign must be followed by a value or a variable.")
        if parentheses_count != 0:
            raise SyntaxError("Problem with parenthesis.")

    def _parse__sign(self):
        """
            Removing extra _sign
        """
        while (
            "--" in self.expression
            or "++" in self.expression
            or "-+" in self.expression
            or "+-" in self.expression
        ):
            self.expression = (
                self.expression.replace("--", "+")
                .replace("++", "+")
                .replace("+-", "-")
                .replace("-+", "-")
            )

    def _convert_signed_number(self):
        """
        This method convert signed number to a sentence readable for npi process.
        Exemple :
            5 * -5 is converted to 5 * (0 - 5)
            10 / +5 is converted to 10 / (0 + 5)
        """

        pass

    def _add_cross_operator_when_parenthesis(self):
        """
            Checking for numbers before open or after closing parenthesis without signe and add a
            multiplicator operator.
        """
        splitted_expression = self.expression.split("(")
        index = 1
        while index < len(splitted_expression):
            # Getting previous part to check sign
            if splitted_expression[index - 1][-1].isdecimal() is True:
                splitted_expression[index - 1] = splitted_expression[index - 1] + "*"
            index += 1
        self.expression = "(".join(splitted_expression)
        splitted_expression = self.expression.split(")")
        index = 0
        while index < len(splitted_expression) - 1:
            # Getting previous part to check sign
            if (
                splitted_expression[index + 1]
                and splitted_expression[index + 1][0].isdecimal() is True
            ):
                splitted_expression[index + 1] = "*" + splitted_expression[index + 1]
            index += 1
        self.expression = ")".join(splitted_expression)

    def _parse_expression(self):
        # Removing all spaces
        print("Before parsing = ", self.expression)
        self.expression = self.expression.replace(" ", "")
        self._parse__sign()
        self._add_cross_operator_when_parenthesis()
        self._convert_signed_number()
        print("After parsing = ", self.expression)
        self._check_args()

    def _set_solver(self):
        """
            Setting the right class to solve the expression
        """
        # Check if it is an equation
        expression_parts = len(self.expression.split("="))
        if expression_parts == 1:
            self._solver = _Calculator()
        elif expression_parts == 2:
            self._solver = _EquationSolver()
        else:
            raise NotImplementedError("More than one comparison is not supported for the moment.")

    def solve(self, expression: str):
        """
            Use the solver of the class set by set_solver to solve the expression.
        """
        self.expression = expression.upper()
        self._parse_expression()
        self._set_solver()
        return self._solver.solve(self.expression)


def main(argv=None):
    print()
    parser = argparse.ArgumentParser()
    parser.add_argument("expression", help="Insert expression to resolve")
    args = parser.parse_args(argv)

    resolver = ExpressionResolver()
    print("args = ", resolver.solve(args.expression))


if __name__ == "__main__":
    main()
