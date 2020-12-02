# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    equation_solver.py                                 :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: mabouce <ma.sithis@gmail.com>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/12/01 20:27:27 by mabouce           #+#    #+#              #
#    Updated: 2020/12/02 11:52:07 by mabouce          ###   ########.fr        #
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
    _tokens: list = None
    _left_part = []
    _right_part = []
    _reduced_form = None
    _vars_name: str = None
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
        # Check if there is any parenthesis

    def _reduce_form(self):
        pass

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

    def _pushing_to_left(self):
        pass

    def solve(self, tokens):
        self._tokens = tokens
        self._check_vars()
        print("equation in equation solver = ", self._tokens)
        self._set_parts()
        print("different parts =\nleft = ", self._left_part, "\nright = ", self._right_part)
        self._pushing_to_left()
        return self._tokens
        self._reduce_form()
