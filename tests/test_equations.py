# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    test_equations.py                                  :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: mabouce <ma.sithis@gmail.com>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/12/01 20:27:30 by mabouce           #+#    #+#              #
#    Updated: 2020/12/02 12:19:02 by mabouce          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import pytest

from expression_resolver import ExpressionResolver


def test_equations_degree_one():
    resolver = ExpressionResolver(verbose=True)

    # # Polynomial degree 1
    # ret = resolver.solve(expression="5 * X^0 + 4 * X^1 = 4 * X^0")

    # Polynomial degree 1, result should be N
    ret = resolver.solve(expression="42 * -X^0 = 42 * X^0")

    # # Polynomial degree 1, test implicit mult for var
    # ret = resolver.solve(expression="42 * Xy42 = 42 * Xy^0")

    # # Polynomial degree 1, test implicit mult for var
    # ret = resolver.solve(expression="42 * 42Xy^0 = 42 * Xy^0")

    # # Test big name var
    # ret = resolver.solve(expression="Hello world*10+1245 = Hello world")


# def test_equations_degree_two():
#     resolver = ExpressionResolver()

#     # Polynomial degree 2
#     ret = resolver.solve(expression="5 * X^0 + 4 * X^1 - 9.3 * X^2 = 1 * X^0")


# def test_wrong_equation():
#     resolver = ExpressionResolver()

#     # Polynomial degree 3, not implemented
#     ret = resolver.solve(expression="8 * X^0 - 6 * X^1 + 0 * X^2 - 5.6 * X^3 = 3 * X^0")
