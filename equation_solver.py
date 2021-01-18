# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    equation_solver.py                                 :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: mabouce <ma.sithis@gmail.com>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/12/01 20:27:27 by mabouce           #+#    #+#              #
#    Updated: 2021/01/18 17:52:21 by mabouce          ###   ########.fr        #
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
    my_power,
    my_sqrt,
    my_round,
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
    solution: None

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
        if len(vars_set) > 1:
            raise SyntaxError("EquationSolver cannot handle more than one var for the moment.")
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
            return 1.0
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

    def _get_polynom_dict(self, simplified_part: str) -> dict:
        polynom_dict = {}
        index = 0
        part = ""
        sign = "+"
        print("simplified_part = ", simplified_part)
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
        return my_power(b, 2.0) - 4.0 * a * c

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
            c = float(self._polynom_dict_left["c"])
        except:
            c = 0.0

        print(" a = ", a, " b = ", b, " c = ", c) if self._verbose is True else None

        discriminant = self._get_discriminant(a, b, c)
        print("discriminant = ", discriminant) if self._verbose is True else None
        if discriminant > 0:
            self.solution = []
            solution_one = (-b + my_sqrt(discriminant)) / (2 * a)
            solution_two = (-b - my_sqrt(discriminant)) / (2 * a)
            self.solution.append(str(my_round(solution_one, 6)))
            self.solution.append(str(my_round(solution_two, 6)))
        elif discriminant == 0:
            self.solution = str((-b) / (2 * a))
        else:
            self.solution = "No solution in real number."

    def _solve_polynom_degree_one(self):
        try:
            b = get_var_multiplier(self._polynom_dict_left["b"], var_name=self.var_name)
        except:
            b = 0.0
        try:
            c = float(self._polynom_dict_left["c"])
        except:
            c = 0.0

        print(" b = ", b, " c = ", c) if self._verbose is True else None
        if b != 0:
            self.solution = str(-(c / b))
        else:
            if b != c:
                self.solution = "There is no solution for this equation."
            else:
                self.solution = "X can be any real number."

    def _check_var_negative_power(self, string: str) -> bool:
        split = string.split(self.var_name + "^")
        index = 1
        while index < len(split):
            if split[index].startswith("-"):
                raise NotImplementedError(f"Some part of the polynomial var have negative power.")
            index += 1

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
        if self.var_name != "":
            self._check_var_negative_power(simplified_left)
            self._check_var_negative_power(simplified_right)
        self._polynom_dict_left = self._get_polynom_dict(simplified_left)
        self._polynom_dict_right = self._get_polynom_dict(simplified_right)
        self._push_right_to_left()

        # Below if is only for equation without var
        if self.var_name == "":
            print(
                "There is no var in the equation, considering there is an X^0(=1), checking if the statement is true"
            ) if self._verbose is True else None
            if simplified_left == simplified_right:
                self.solution = "X can be any real number."
            else:
                self.solution = "The equation is False."
        else:
            for key, value in self._polynom_dict_left.items():
                if self._reduced_form and len(self._reduced_form) > 0:
                    self._reduced_form = self._reduced_form + "+" + str(value)
                else:
                    self._reduced_form = str(value)
            self._reduced_form = parse_sign(self._reduced_form) + "=0.0"

            print("Reduced form : ", self._reduced_form) if self._verbose is True else None

            self._check_polynom_degree()

            print("Polynomial degree: ", self._polynom_degree) if self._verbose is True else None

            if self._polynom_degree > 2:
                raise NotImplementedError(
                    f"The polynomial degree is strictly greater than 2, the resolver is not implemented yet."
                )
            elif self._polynom_degree == 2:
                self._solve_polynom_degree_two()
            else:
                self._solve_polynom_degree_one()

        return self.solution
