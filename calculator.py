# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    calculator.py                                      :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: mabouce <ma.sithis@gmail.com>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/12/01 20:27:15 by mabouce           #+#    #+#              #
#    Updated: 2020/12/04 16:33:03 by mabouce          ###   ########.fr        #
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

from utils import convert_to_tokens, is_number, parse_sign, convert_signed_number


class _Calculator:

    _tokens = None
    _npi_list = None
    _var_name = None

    def stack_last_element(self, elem: list) -> str:
        try:
            return elem[-1][0]
        except IndexError:
            return []

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

    def _write_power_to_var(self, var, power):
        if int(power) == 1:
            return var
        return var + "^" + str(power)

    def _multiply_a_var(self, first_var: str, second_var: str):

        first_var_power = str(self._get_power(first_var))
        second_var_power = str(self._get_power(second_var))

        # Cutting respective power and convert signed numbers
        first_var = convert_signed_number(first_var.split("^")[0])
        second_var = convert_signed_number(second_var.split("^")[0])

        if not self._check_have_var(first_var):
            sum_power = second_var_power
            # No number before
            if len(second_var) == len(self._var_name):
                return first_var + "*" + self._write_power_to_var(var=second_var, power=sum_power)
            else:
                remove_var_name = second_var.replace(self._var_name, "1")
                tokens = []
                tokens.append(first_var)
                tokens.append("*")
                tokens = tokens + convert_to_tokens(remove_var_name)
                return (
                    str(self.solve(tokens))
                    + "*"
                    + self._write_power_to_var(var=self._var_name, power=sum_power)
                )
        elif not self._check_have_var(second_var):
            sum_power = first_var_power

            if len(first_var) == len(self._var_name):
                return second_var + "*" + self._write_power_to_var(var=first_var, power=sum_power)
            else:
                remove_var_name = first_var.replace(self._var_name, "1")
                tokens = []
                tokens.append(second_var)
                tokens.append("*")
                tokens = tokens + convert_to_tokens(remove_var_name)
                return (
                    str(self.solve(tokens))
                    + "*"
                    + self._write_power_to_var(var=self._var_name, power=sum_power)
                )
        # Both have var.
        else:
            sum_power = str(self.solve([first_var_power, "+", second_var_power]))

            if len(first_var) == len(self._var_name) == len(second_var):
                return self._write_power_to_var(var=first_var, power=sum_power)
            elif len(first_var) == len(self._var_name):
                return self._write_power_to_var(var=second_var, power=sum_power)
            elif len(second_var) == len(self._var_name):
                return self._write_power_to_var(var=first_var, power=sum_power)
            else:
                remove_var1_name = first_var.replace(self._var_name, "1")
                remove_var2_name = second_var.replace(self._var_name, "1")
                tokens = []
                tokens = tokens + convert_to_tokens(remove_var1_name)
                tokens.append("*")
                tokens = tokens + convert_to_tokens(remove_var2_name)
                return (
                    str(self.solve(tokens))
                    + "*"
                    + self._write_power_to_var(var=self._var_name, power=sum_power)
                )

    def resolve_npi(self, npi_list):
        stack = []
        c = 0
        var_is_present = True if self._var_name else False

        for elem in npi_list:
            if is_number(elem) or (var_is_present and elem in self._var_name):
                stack.append(elem)
            else:
                last_two_in_stack = stack[-2:]
                del stack[-2:]
                # Doing var calc if there is a var
                if var_is_present and (
                    self._check_have_var(str(last_two_in_stack[0]))
                    or self._check_have_var(str(last_two_in_stack[1]))
                ):
                    # - or + operator, adding to c
                    if elem in _SIGN:

                        if not self._check_have_var(str(last_two_in_stack[0])):
                            if elem == "-":
                                c += float(last_two_in_stack[0])
                            else:
                                c += float(last_two_in_stack[0])
                            print("la doing the truc bizarre")
                            print("var = ", str(last_two_in_stack[1]))
                            result = self._multiply_a_var("-1", str(last_two_in_stack[1]))
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

                # Doing usual calc
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
            print("stack at end = ", stack)
            print()

        if len(stack) > 1:
            raise Exception(
                "Unexpected error when trying to resolve npi. Maybe your input format is not accepted?"
            )
        if var_is_present:
            if c != 0:
                # Parse sign because could have duplicate sign with the add of the +
                return parse_sign(str(c) + "+" + str(stack[0]))
            else:
                return str(stack[0])
        else:
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
        nb_of_var = 0
        for token in self._tokens:
            if (
                not token in _OPEN_PARENTHESES + _CLOSING_PARENTHESES + _OPERATORS + _SIGN
                and not is_number(token)
            ):
                if token.isalpha():
                    nb_of_var += 1
                    if nb_of_var > 1:
                        raise NotImplementedError(
                            "Calculator does not support more than one variables."
                        )
                    else:
                        self._var_name = token
                else:
                    raise SyntaxError(f"An error occured with the following syntax : {token}")

    def solve(self, tokens: list) -> int:
        self._tokens = tokens
        self._check_vars()
        print("token in calc = ", tokens)
        npi = self.npi_converter(self._tokens, accept_var=True if self._var_name else False)
        print("npi in calc = ", npi)
        result = self.resolve_npi(npi)
        print("result of calc = ", result)
        return result
