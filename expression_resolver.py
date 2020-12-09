# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    expression_resolver.py                             :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: mabouce <ma.sithis@gmail.com>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/12/01 21:41:09 by mabouce           #+#    #+#              #
#    Updated: 2020/12/09 12:45:54 by mabouce          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import re

from equation_solver import _EquationSolver
from calculator import _Calculator
from globals_vars import (
    _OPERATORS,
    _OPERATORS_PRIORITY,
    _SIGN,
    _COMMA,
    _OPEN_PARENTHESES,
    _CLOSING_PARENTHESES,
)

from utils import convert_to_tokens, parse_sign, convert_signed_number


class ExpressionResolver:

    expression = None
    _vars_set = None
    _verbose = None
    _solver = None

    def __init__(self, verbose: bool = False):
        self._verbose = verbose

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
                            assert part[-1].isdecimal()
                        elif part == comma_split[-1]:
                            assert len(part) >= 1
                            assert part[0].isdecimal()
                        else:
                            assert len(part) >= 2
                            assert part[0].isdecimal()
                            assert part[-1].isdecimal()
            except AssertionError:
                raise SyntaxError("Some numbers are not well formated (Comma error).")

        # Check allowed char.
        for c in self.expression:
            if (
                c not in "="
                and c not in _OPERATORS
                and c not in _SIGN
                and c not in _OPEN_PARENTHESES
                and c not in _CLOSING_PARENTHESES
                and not c.isalnum()
                and c not in _COMMA
            ):
                raise SyntaxError(
                    "This is not an expression or some of the operators are not reconized."
                )
            # Check multiple operators before alphanum. Check parenthesis count.
            # Checking also that a sign isn't followed by an operator
            if (
                c in _OPERATORS
                and last_operator
                and (last_operator in _OPERATORS or last_operator in _SIGN)
            ):
                raise SyntaxError(
                    "Operators must be followed by a value or a variable, not another operator."
                )
            elif c in _OPERATORS or c in _SIGN:
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

    def _add_implicit_cross_operator_when_parenthesis(self):
        """
            Checking for numbers before open or after closing parenthesis without sign and add a
            multiplicator operator.
        """
        # Checking open parenthesis
        for open_parenthese in _OPEN_PARENTHESES:
            splitted_expression = self.expression.split(open_parenthese)
            index = 1
            while index < len(splitted_expression):
                # Checking if previous part is not empty
                if len(splitted_expression[index - 1]) > 0:
                    # Getting previous part to check sign
                    if (
                        splitted_expression[index - 1][-1].isdecimal() is True
                        or splitted_expression[index - 1][-1] in _CLOSING_PARENTHESES
                    ):
                        splitted_expression[index - 1] = splitted_expression[index - 1] + "*"
                index += 1
            self.expression = open_parenthese.join(splitted_expression)

        # Checking closing parenthesis
        for closing_parenthese in _CLOSING_PARENTHESES:
            splitted_expression = self.expression.split(closing_parenthese)
            index = 0
            while index < len(splitted_expression) - 1:
                # Getting previous part to check sign
                if (
                    splitted_expression[index + 1]
                    and splitted_expression[index + 1][0].isdecimal() is True
                ):
                    splitted_expression[index + 1] = "*" + splitted_expression[index + 1]
                index += 1
            self.expression = closing_parenthese.join(splitted_expression)

    def _add_implicit_cross_operator_for_vars(self):
        # Splitting from vars
        for var in self._vars_set:
            splitted_expression = self.expression.split(var)
            index = 1
            while index < len(splitted_expression):
                # Checking if previous part is not empty
                if len(splitted_expression[index - 1]) > 0:
                    # Getting previous part to check sign
                    if (
                        splitted_expression[index - 1][-1].isdecimal() is True
                        or splitted_expression[index - 1][-1] in _CLOSING_PARENTHESES
                    ):
                        splitted_expression[index - 1] = splitted_expression[index - 1] + "*"
                # Checking implicit mult after the var
                if splitted_expression[index] and (
                    splitted_expression[index][0].isdecimal() is True
                    or splitted_expression[index][0] in _OPEN_PARENTHESES
                ):
                    splitted_expression[index] = "*" + splitted_expression[index]
                index += 1
            self.expression = var.join(splitted_expression)

    def _removing_trailing_zero_and_converting_numbers_to_float(self):
        for index, token in enumerate(self.expression):
            if token.isdecimal():
                self.expression[index] = str(float(token))

    def _get_vars(self):
        vars_list = re.findall(pattern=r"[A-Z]+", string=self.expression)
        # Removing duplicate var
        self._vars_set = list(set(vars_list))

        # Prevent var in parenthesis
        index = 0
        parenthesis_counter = 0
        is_open = False
        first_open_index = 0
        for var in self._vars_set:
            while index < len(self.expression):
                if self.expression[index] in _OPEN_PARENTHESES:
                    if not is_open:
                        is_open = True
                        first_open_index = index
                    parenthesis_counter += 1
                elif self.expression[index] in _CLOSING_PARENTHESES:
                    parenthesis_counter -= 1
                if parenthesis_counter == 0 and is_open:
                    is_open = False
                    if var in self.expression[first_open_index : index + 1]:
                        raise NotImplementedError(
                            "Var cannot be inside a parenthesis for the moment."
                        )
                index += 1

    def _parse_expression(self):
        print("Expression before parsing : ", self.expression) if self._verbose is True else None

        # Removing all spaces
        self.expression = self.expression.replace(" ", "")

        print(
            "Removing all space from the expression : ", self.expression
        ) if self._verbose is True else None

        self.expression = parse_sign(self.expression)
        print("Parsing signs : ", self.expression) if self._verbose is True else None

        # To put before convert_signed_number because it is creating parenthesis
        self._get_vars()
        print("vars = ", self._vars_set) if self._verbose is True else None

        self.expression = convert_signed_number(expression=self.expression, accept_var=True)

        print("Convert signed numbers : ", self.expression) if self._verbose is True else None

        self._add_implicit_cross_operator_when_parenthesis()
        self._add_implicit_cross_operator_for_vars()

        print(
            "Convert implicit multiplication : ", self.expression
        ) if self._verbose is True else None

        # Checking args here before converting to token
        self._check_args()

        # Transforming expression to tokens
        self.expression = convert_to_tokens(self.expression)

        print("Convert to token : ", self.expression) if self._verbose is True else None
        self._removing_trailing_zero_and_converting_numbers_to_float()
        print(
            "Removing extra zero and converting numbers to float: ", self.expression
        ) if self._verbose is True else None

    def _set_solver(self):
        """
            Setting the right class to solve the expression
        """
        # Check if it is an equation
        equal_operator = [elem for elem in self.expression if elem == "="]
        if len(equal_operator) == 0:
            self._solver = _Calculator()
        elif len(equal_operator) == 1:
            self._solver = _EquationSolver(_Calculator())
        else:
            raise NotImplementedError("More than one comparison is not supported for the moment.")

    def solve(self, expression: str):
        """
            Use the solver of the class set by set_solver to solve the expression.
        """
        self.expression = expression.upper()
        self._parse_expression()
        self._set_solver()
        return self._solver.solve(self.expression, verbose=self._verbose)
