# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    equation_solver.py                                 :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: mabouce <ma.sithis@gmail.com>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/12/01 20:27:27 by mabouce           #+#    #+#              #
#    Updated: 2020/12/09 19:08:33 by mabouce          ###   ########.fr        #
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

from utils import (
    convert_to_tokens,
    is_number,
    convert_signed_number,
    parse_sign,
    get_var_multiplier,
)


class _EquationSolver:
    _tokens: list = None
    _left_part: list = []
    _right_part: list = []
    _reduced_form: str = None
    _polynom_dict_right: dict = None
    _polynom_dict_left: dict = None
    _polynom_degree = float
    var_name: str = None
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
        self.var_name = "".join(vars_set)

    def _check_have_var(self, var) -> bool:
        if self.var_name in var:
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

    def _get_polynom_dict(self, simplified_part: str):
        polynom_dict = {}
        index = 0
        part = ""
        sign = "+"
        while index < len(simplified_part):
            if simplified_part[index] in _SIGN and len(part) > 0:
                if self._check_have_var(part):
                    power = self._get_power(part)
                    if power == 1:
                        polynom_dict["b"] = "-" + part if sign == "-" else part
                    elif power == 2:
                        polynom_dict["a"] = "-" + part if sign == "-" else part
                    else:
                        polynom_dict[str(power)] = "-" + part if sign == "-" else part
                else:
                    polynom_dict["c"] = "-" + part if sign == "-" else part
                part = ""

            if simplified_part[index] in _SIGN:
                sign = simplified_part[index]
            else:
                part = part + simplified_part[index]
            index += 1
        if self._check_have_var(part):
            power = self._get_power(part)
            if power == 1:
                polynom_dict["b"] = "-" + part if sign == "-" else part
            elif power == 2:
                polynom_dict["a"] = "-" + part if sign == "-" else part
            else:
                polynom_dict[str(power)] = "-" + part if sign == "-" else part
        else:
            polynom_dict["c"] = "-" + part if sign == "-" else part
        return polynom_dict

    def _push_right_to_left(self):
        for key, right_value in self._polynom_dict_right.items():
            try:
                left_value = self._polynom_dict_left[key]
            except:
                left_value = 0
            tokens = []
            tokens = convert_to_tokens(
                convert_signed_number(
                    parse_sign(str(left_value) + "-" + str(right_value)), accept_var=True
                )
            )
            self._polynom_dict_left[key] = self._calculator.solve(tokens, verbose=False)

    def _check_polynom_degree(self):
        polynom_max_degree = 0.0
        for key, value in self._polynom_dict_left.items():
            if key == "a":
                if self.var_name in value and polynom_max_degree < 2:
                    polynom_max_degree = float(2)
                else:
                    continue
            elif key == "b":
                if self.var_name in value and polynom_max_degree < 1:
                    polynom_max_degree = float(1)
                else:
                    continue
            elif key == "c":
                continue
            elif float(key) > 2 and self.var_name in value and polynom_max_degree < float(key):
                polynom_max_degree = float(key)
        self._polynom_degree = polynom_max_degree

    def _get_discriminant(self, a: float, b: float, c: float) -> float:
        return b ** 2.0 - 4.0 * a * c

    def _solve_polynom_degree_two(self):
        try:
            a = get_var_multiplier(self._polynom_dict_left["a"], var_name=self.var_name)
        except:
            a = 0.0
        try:
            b = get_var_multiplier(self._polynom_dict_left["b"], var_name=self.var_name)
        except:
            b = 0.0
        try:
            c = get_var_multiplier(self._polynom_dict_left["c"], var_name=self.var_name)
        except:
            c = 0.0

        discriminant = self._get_discriminant(a, b, c)
        if discriminant > 0:
            solution_one = (-b + (b ** 2 - 4 * a * c)) / (2 * a)
            solution_two = (-b - (b ** 2 - 4 * a * c)) / (2 * a)
            print("solution_one = ", solution_one)
            print("solution_two = ", solution_two)

    def solve(self, tokens: list, verbose: bool = False):
        self._verbose = verbose
        self._tokens = tokens
        self._left_part.clear()
        self._right_part.clear()
        self._check_vars()
        self._set_parts()

        simplified_left = self._calculator.solve(self._left_part)
        simplified_right = self._calculator.solve(self._right_part)
        print("Simplified left part : ", simplified_left) if self._verbose is True else None
        print("Simplified right part : ", simplified_right) if self._verbose is True else None
        self._polynom_dict_left = self._get_polynom_dict(simplified_left)
        self._polynom_dict_right = self._get_polynom_dict(simplified_right)
        self._push_right_to_left()

        for key, value in self._polynom_dict_left.items():
            if self._reduced_form and len(self._reduced_form) > 0:
                self._reduced_form = self._reduced_form + "+" + str(value)
            else:
                self._reduced_form = value
        self._reduced_form = parse_sign(self._reduced_form) + "=0.0"

        print("Reduced form : ", self._reduced_form) if self._verbose is True else None

        self._check_polynom_degree()

        print("Polynomial degree: ", self._polynom_degree) if self._verbose is True else None

        if self._polynom_degree > 2:
            raise NotImplementedError(
                f"The polynomial degree is strictly greater than 2, the resolver is not implemented yet."
            )
        if self._polynom_degree == 2:
            self._solve_polynom_degree_two()

        return self._polynom_dict_left
