# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    equation_solver.py                                 :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: mabouce <ma.sithis@gmail.com>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/12/01 20:27:27 by mabouce           #+#    #+#              #
#    Updated: 2020/12/01 22:01:16 by mabouce          ###   ########.fr        #
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


class _EquationSolver:
    _equation = None
    reduced_form = None
    _vars_set = None
    _calculator = None

    def __init__(self, calculator):
        self._calculator = calculator

    def _check_vars(self):
        vars_list = re.findall(pattern=r"[A-Z]+", string=self._equation)
        # Removing duplicate var
        self._vars_set = list(set(vars_list))
        if len(self._vars_set) > 1:
            raise SyntaxError("EquationSolver does not support more than one variables.")

    def _reduce_form(self):
        pass

    def solve(self, equation):
        self._equation = equation
        return self._equation
        self._check_vars()
        self._reduce_form()
        print("equation in equation solver = ", self._equation)
