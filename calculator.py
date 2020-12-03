# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    calculator.py                                      :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: mabouce <ma.sithis@gmail.com>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/12/01 20:27:15 by mabouce           #+#    #+#              #
#    Updated: 2020/12/03 18:10:58 by mabouce          ###   ########.fr        #
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

from utils import is_number


class _Calculator:

    _tokens = None
    _npi_list = None

    def stack_last_element(self, elem: list) -> str:
        try:
            return elem[-1][0]
        except IndexError:
            return []

    def resolve_npi(self, npi_list):
        stack = []

        for elem in npi_list:
            if is_number(elem):
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

    def npi_converter(self, tokens, accept_var=False):
        """
        Convert an expression to npi.
        """

        res = []
        stack = []
        for token in tokens:
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
                if not is_number(token):
                    # Checking if it's alpha, then adding it as a var
                    if (accept_var is True and not token.isalpha()) or accept_var is False:
                        raise SyntaxError(f"Some numbers are not well formated : {token}")
                res.append(token)

        return res + stack[::-1]

    def _check_vars(self):
        for token in self._tokens:
            if (
                not token in _OPEN_PARENTHESES + _CLOSING_PARENTHESES + _OPERATORS + _SIGN
                and not is_number(token)
            ):
                if token.isalpha():
                    raise NotImplementedError("Calculator does not support variables.")
                else:
                    raise SyntaxError(f"An error occured with the following syntax : {token}")

    def solve(self, tokens: list) -> int:
        self._tokens = tokens
        print("token in calculator = ", tokens)
        self._check_vars()
        result = self.resolve_npi(self.npi_converter(self._tokens))
        return result
