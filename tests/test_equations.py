# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    test_equations.py                                  :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: mabouce <ma.sithis@gmail.com>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/12/01 20:27:30 by mabouce           #+#    #+#              #
#    Updated: 2020/12/02 18:44:29 by mabouce          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import pytest

from expression_resolver import ExpressionResolver


def test_equations_degree_one():
    resolver = ExpressionResolver(verbose=False)

    # Polynomial degree 1 with parenthesis to calc, no solution
    ret = resolver.solve(
        expression="2 + (42 * (10 + 5) )(58*2) + 2 * X^0 + 5(25 * -2) + X2 = (42 * 10) * X^0"
    )

    # 73 082 + 2 X^0 + -248

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
