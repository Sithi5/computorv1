# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    test_equations.py                                  :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: mabouce <ma.sithis@gmail.com>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/12/01 20:27:30 by mabouce           #+#    #+#              #
#    Updated: 2020/12/11 16:42:06 by mabouce          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import pytest

import math

from expression_resolver import ExpressionResolver


def test_equation_subject():
    resolver = ExpressionResolver(verbose=False)

    ret = resolver.solve(expression="5 * X^0 + 4 * X^1 - 9.3 * X^2 = 1 * X^0")
    assert ret == [-0.475131, 0.905239]

    # ret = resolver.solve(expression="5 * X^0 + 4 * X^1 = 4 * X^0")

    # with pytest.raises(NotImplementedError) as e:
    #     ret = resolver.solve(expression="8 * X^0 - 6 * X^1 + 0 * X^2 - 5.6 * X^3 = 3 * X^0")
    # assert (
    #     str(e.value)
    #     == "The polynomial degree is strictly greater than 2, the resolver is not implemented yet."
    # )

    # ret = resolver.solve(expression="5 + 4 * X + X^2= X^2")


def test_equations_degree_one():
    resolver = ExpressionResolver(verbose=False)

    # Polynomial degree 1 with parenthesis to calc, no solution
    # ret = resolver.solve(
    #     expression="2 + (42 * (10 + 5) )(58*2) + 2 * X^0 + 5(25 * -2)- 2 = (42 * 10) * X^0"
    # )
    # 72 830 + 2 X ^0

    # Polynomial degree 1 with parenthesis to calc, no solution
    # ret = resolver.solve(expression="52 + 2 * X^0 * 4 -1 + 6 *  2 x  - 5 * 2= (42 * 10) * X^0")

    # # Multiplying var
    # ret = resolver.solve(expression="52 + 2 * X^5 * 4X -1 + 6 *  2 * x = 0")

    # # Polynomial degree 1 with parenthesis to calc
    # ret = resolver.solve(expression="-42 + (10 + 5)(58*2) + X^0 = (42 * 10) * X^0")

    # def test_equations_degree_two():
    #     resolver = ExpressionResolver()

    #     # Polynomial degree 2
    #     ret = resolver.solve(expression="5 * X^0 + 4 * X^1 - 9.3 * X^2 = 1 * X^0")

    # def test_wrong_equation():
    #     resolver = ExpressionResolver()

    #     # Polynomial degree 3, not implemented
    #     ret = resolver.solve(expression="8 * X^0 - 6 * X^1 + 0 * X^2 - 5.6 * X^3 = 3 * X^0")

    # # Polynomial degree 1, with a var in parenthesis
    # with pytest.raises(NotImplementedError) as e:
    #     ret = resolver.solve(expression="(42 * (10 + 5) )(58*2x) + X^0 = (42 * 10) * X^0")
    # assert str(e.value) == "Variable between parenthesis is not supported yet."


# def test_equations_degree_two():
#     resolver = ExpressionResolver(verbose=False)

#     # Positive equation
#     ret = resolver.solve(expression="2x^2 + -x - 6 = 0")
#     assert ret == [2.0, -1.5]

#     ret = resolver.solve(expression=" 6x^2 + 11x - 35 = 0")
#     assert ret == [5 / 3, -7 / 2]

#     ret = resolver.solve(expression="2x^2-4x-2=0")
#     assert ret == [2.414213562373095, -0.4142135623730949]

#     # Zero equation

#     # Negative equation
#     ret = resolver.solve(expression="   x^2 + 3x + 10 = 0")
#     assert ret == "No solution in real number."
