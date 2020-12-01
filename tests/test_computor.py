# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    test_computor.py                                   :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: mabouce <ma.sithis@gmail.com>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/12/01 20:27:33 by mabouce           #+#    #+#              #
#    Updated: 2020/12/01 22:32:38 by mabouce          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import pytest

from expression_resolver import ExpressionResolver


def test_expression_parser():
    resolver = ExpressionResolver(verbose=True)

    # Test sign before
    ret = resolver.solve(expression="+X = 10")

    # Test sign before
    ret = resolver.solve(expression="-X = 10")

    # Test addition with sign before var
    ret = resolver.solve(expression="X -5 = -X")

    # lot of sign
    ret = resolver.solve(expression="4-+-2 ------+-----++++++ X^0 = 0")

    # lot of sign
    ret = resolver.solve(expression="4-+-2 ------+-----++++++ X^+-+++-0 = 0")

    # Extra zero
    ret = resolver.solve(expression="04578 + 000450")
    assert ret == 5028

    # Test method _replace_zero_power_by_one
    ret = resolver.solve(expression="04578 + 15000 ^0")
    assert ret == 4579

    # Test method _replace_zero_power_by_one, the following one shouln't proc because it use a parenthesis
    ret = resolver.solve(expression="04578 + (15000 * 450)^0")
    assert ret == 4579


def test_wrong_args():
    resolver = ExpressionResolver(verbose=True)

    # Wrong args
    with pytest.raises(SyntaxError) as e:
        resolver.solve(expression="6&7-2=5")
    assert str(e.value) == "This is not an expression or some of the operators are not reconized."

    # Sign without value after
    with pytest.raises(SyntaxError) as e:
        resolver.solve(expression="4^0-")
    assert str(e.value) == "Operators or sign must be followed by a value or a variable."

    # Operator wrong syntax
    with pytest.raises(SyntaxError) as e:
        resolver.solve(expression="42//5")
    assert (
        str(e.value) == "Operators must be followed by a value or a variable, not another operator."
    )

    # Tests var in calculator
    with pytest.raises(SyntaxError) as e:
        resolver.solve(expression="X+18+ 5")
    assert str(e.value) == "Calculator does not support variables."

    # More than one = in the expression
    with pytest.raises(NotImplementedError) as e:
        resolver.solve(expression="42 * X = 42 * Y = 42 * Z")
        out, err = capsys.readouterr()
    assert str(e.value) == "More than one comparison is not supported for the moment."

    # lot of sign and operator between
    with pytest.raises(SyntaxError) as e:
        ret = resolver.solve(expression="4X^+-+^++-0 = 0")
    assert (
        str(e.value) == "Operators must be followed by a value or a variable, not another operator."
    )

    # multiple comma in one number
    with pytest.raises(SyntaxError) as e:
        ret = resolver.solve(expression="450.25.45 + 12")
    assert str(e.value) == "An error occured with the following syntax : 450.25.45"

    # wrong use of comma
    with pytest.raises(SyntaxError) as e:
        ret = resolver.solve(expression="450. + 12")
    assert str(e.value) == "Some numbers are not well formated (Comma error)."

    # wrong use of comma
    with pytest.raises(SyntaxError) as e:
        ret = resolver.solve(expression=".45 + 12")
    assert str(e.value) == "Some numbers are not well formated (Comma error)."

    # Sign before operator
    with pytest.raises(SyntaxError) as e:
        ret = resolver.solve(expression="45 + * 12")
    assert (
        str(e.value) == "Operators must be followed by a value or a variable, not another operator."
    )

    # Test sign before closing parenthesis
    with pytest.raises(SyntaxError) as e:
        ret = resolver.solve(expression="5 * (5 +)10")
    assert (
        str(e.value) == "Operators must be followed by a value or a variable, not another operator."
    )

    # Test operator before closing parenthesis
    with pytest.raises(SyntaxError) as e:
        ret = resolver.solve(expression="5 * (5 *)10")
    assert (
        str(e.value) == "Operators must be followed by a value or a variable, not another operator."
    )
