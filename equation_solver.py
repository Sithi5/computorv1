# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    equation_solver.py                                 :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: mabouce <ma.sithis@gmail.com>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/12/01 20:27:27 by mabouce           #+#    #+#              #
#    Updated: 2020/12/04 14:58:10 by mabouce          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import argparse, parser, re

from globals_vars import (
    _OPERATORS,
    _OPERATORS_PRIORITY,
    _SIGN,
    _COMMA,
    _OPEN_PARENTHESES,
    _CLOSING_PARENTHESES,
)

from utils import convert_to_tokens, is_number


class _EquationSolver:
    _tokens: list = None
    _left_part = []
    _right_part = []
    _reduced_form = None
    _var_name: str = None
    _calculator = None

    def __init__(self, calculator):
        self._calculator = calculator

    def _check_vars(self):
        """
        Actually checking there is one and only one var and getting the name of it.
        Also checking notImplemented operations.
        """
        vars_list = re.findall(pattern=r"[A-Z]+", string="".join(self._tokens))
        # Removing duplicate var
        vars_set = list(set(vars_list))
        if len(vars_set) != 1:
            raise SyntaxError("EquationSolver need exactly one variable.")
        self._var_name = "".join(vars_set)

    def _set_parts(self):
        left_part = True
        for token in self._tokens:
            if token != "=" and left_part is True:
                self._left_part.append(token)
            elif token != "=" and left_part is False:
                self._right_part.append(token)
            elif token == "=":
                left_part = False
        if len(self._left_part) == 0 or len(self._right_part) == 0:
            raise SyntaxError("The equation is not well formated. No left or right part.")

    def _send_to_calc(self, start_index, end_index):
        try:
            calc_result = self._calculator.solve(self._tokens[start_index:end_index])
        except NotImplementedError:
            raise NotImplementedError("Variable between parenthesis is not supported yet.")
        del self._tokens[start_index:end_index]
        self._tokens.insert(start_index, str(calc_result))

    def _solving_parenthesis(self):
        index = 0
        start_parenthesis = 0
        end_parenthesis = 0
        while index < len(self._tokens):
            if self._tokens[index] in _OPEN_PARENTHESES:
                start_parenthesis = index
                # Skip first parenthesis to avoid incrementing the counter
                index += 1
                # Check for other open parenthesis in between
                open_parenthesis_count = 1
                while open_parenthesis_count != 0:
                    if self._tokens[index] in _OPEN_PARENTHESES:
                        open_parenthesis_count += 1
                    elif self._tokens[index] in _CLOSING_PARENTHESES:
                        open_parenthesis_count -= 1
                    index += 1
                    if index >= len(self._tokens):
                        raise SyntaxError("Open parenthesis with not closing one.")
                end_parenthesis = index
                # Sending the calc to the calculator
                self._send_to_calc(start_parenthesis, end_parenthesis)
                index = start_parenthesis + 1
            else:
                index += 1

    def _check_have_var(self, var) -> bool:
        if self._var_name in var:
            return True
        return False

    def _get_power(self, var):
        """
        Returning the power of a number or a var.
        If there is multiple "^" operators, it return the first power.
        """
        split = var.split("^")
        if len(split) == 1:
            return 1
        else:
            return float(split[1])

    def _multiply_a_var(self, first_var: str, second_var: str):
        print("first_var = ", first_var, "second_var = ", second_var)

        first_var_power = str(self._get_power(first_var))
        second_var_power = str(self._get_power(second_var))
        print("first_var_power = ", first_var_power)
        print("second_var_power = ", second_var_power)

        # Cutting respective power
        first_var = first_var.split("^")[0]
        second_var = second_var.split("^")[0]

        if not self._check_have_var(first_var):
            sum_power = second_var_power
            # No number before
            if len(second_var) == len(self._var_name):
                return first_var + "*" + second_var + "^" + sum_power
            else:
                remove_var_name = second_var.replace(self._var_name, "1")
                tokens = []
                tokens.append(first_var)
                tokens.append("*")
                tokens = tokens + convert_to_tokens(remove_var_name)
                return str(self._calculator.solve(tokens)) + "*" + self._var_name + "^" + sum_power
        elif not self._check_have_var(second_var):
            sum_power = first_var_power

            if len(first_var) == len(self._var_name):
                return second_var + "*" + first_var + "^" + sum_power
            else:
                remove_var_name = first_var.replace(self._var_name, "1")
                tokens = []
                tokens.append(second_var)
                tokens.append("*")
                tokens = tokens + convert_to_tokens(remove_var_name)
                return str(self._calculator.solve(tokens)) + "*" + self._var_name + "^" + sum_power
        # Both have var.
        else:
            sum_power = str(self._calculator.solve([first_var_power, "+", second_var_power]))

            if len(first_var) == len(self._var_name) == len(second_var):
                return first_var + "^" + sum_power
            elif len(first_var) == len(self._var_name):
                return second_var + "^" + sum_power
            elif len(second_var) == len(self._var_name):
                return first_var + "^" + sum_power
            else:
                remove_var1_name = first_var.replace(self._var_name, "1")
                remove_var2_name = second_var.replace(self._var_name, "1")
                tokens = []
                tokens = tokens + convert_to_tokens(remove_var1_name)
                tokens.append("*")
                tokens = tokens + convert_to_tokens(remove_var2_name)
                return str(self._calculator.solve(tokens)) + "*" + self._var_name + "^" + sum_power

    def resolve_npi_with_var(self, npi_list):
        stack = []
        c = 0

        for elem in npi_list:
            if is_number(elem) or elem in self._var_name:
                stack.append(elem)
            else:
                last_two_in_stack = stack[-2:]
                del stack[-2:]
                if self._check_have_var(str(last_two_in_stack[0])) or self._check_have_var(
                    str(last_two_in_stack[1])
                ):
                    # Doing var calc
                    # - or + operator, adding to c
                    if elem in _SIGN:

                        if not self._check_have_var(str(last_two_in_stack[0])):
                            if elem == "-":
                                c -= float(last_two_in_stack[0])
                            else:
                                c += float(last_two_in_stack[0])
                            result = str(last_two_in_stack[1])
                        elif not self._check_have_var(str(last_two_in_stack[1])):
                            if elem == "-":
                                c -= float(last_two_in_stack[1])
                            else:
                                c += float(last_two_in_stack[1])
                            result = str(last_two_in_stack[0])
                        else:
                            result = str(last_two_in_stack[0]) + elem + str(last_two_in_stack[1])
                    # mult of var
                    elif elem == "*":
                        result = self._multiply_a_var(
                            str(last_two_in_stack[0]), str(last_two_in_stack[1])
                        )
                    else:
                        result = str(last_two_in_stack[0]) + elem + str(last_two_in_stack[1])

                # Power is not noted the same in python
                elif elem == "^":
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
        return str(c) + "+" + stack[0]

    def solve(self, tokens):
        self._tokens = tokens
        self._check_vars()
        self._solving_parenthesis()
        self._set_parts()

        npi = self._calculator.npi_converter(self._left_part, accept_var=True)
        print("npi = ", npi)
        print("resolved npi = ", self.resolve_npi_with_var(npi))
        print("end token = ", self._tokens)

        return self._tokens
