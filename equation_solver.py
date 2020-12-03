# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    equation_solver.py                                 :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: mabouce <ma.sithis@gmail.com>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/12/01 20:27:27 by mabouce           #+#    #+#              #
#    Updated: 2020/12/03 16:57:39 by mabouce          ###   ########.fr        #
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

from calculator import _is_number


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

    def resolve_npi_with_var(self, npi_list):
        stack = []
        rest_stack = []

        last_was_var = False
        for elem in npi_list:
            print("elem = ", elem)
            print("last was var ? ", last_was_var)
            if _is_number(elem):
                if last_was_var is True:
                    rest_stack.append(elem)
                else:
                    stack.append(elem)
            elif elem in self._var_name:
                rest_stack.append(elem)
                last_was_var = True
            else:
                if last_was_var is True and _OPERATORS_PRIORITY[elem] > 1:
                    rest_stack.append(elem)
                    if len(stack) > 0:
                        rest_stack.append(stack.pop())
                else:
                    print("Operator ? ")
                    if last_was_var is True:
                        stack.append(rest_stack.pop())
                        rest_stack.append(elem)
                        last_was_var = False
                        continue
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
            print("end loop stack = ", stack)
            print("end loop rest = ", rest_stack)

        print("end stack = ", stack)
        print("end rest = ", rest_stack)
        return rest_stack + stack

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
