# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    calculator.py                                      :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: mabouce <ma.sithis@gmail.com>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/12/01 20:27:15 by mabouce           #+#    #+#              #
#    Updated: 2021/01/19 18:14:07 by mabouce          ###   ########.fr        #
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
    parse_sign,
    convert_signed_number,
    add_implicit_cross_operator_for_vars,
    my_power,
    my_round,
)


class _Calculator:

    _tokens = None
    _npi_list = None
    var_name = None

    def stack_last_element(self, elem: list) -> str:
        try:
            return elem[-1][0]
        except IndexError:
            return []

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
            return split[1]

    def _write_power_to_var(self, var, power):
        if float(power) != int(float(power)):
            raise NotImplementedError("irrational numbers are not accepted as exponent.")
        if float(power) == 1:
            return var
        return var + "^" + str(power)

    def _power_a_var(self, first_var: str, second_var: str):

        sign = ""
        if first_var[0] in _SIGN:
            sign = first_var[0]
        first_var_power = str(self._get_power(first_var))

        # Cutting respective power and convert signed numbers
        first_var = convert_signed_number(first_var.split("^")[0], accept_var=True)
        second_var = convert_signed_number(second_var.split("^")[0], accept_var=True)
        second_var = self.solve(convert_to_tokens(second_var), internal=True)
        if is_number(second_var) and float(second_var) != int(float(second_var)):
            raise NotImplementedError("irrational numbers are not accepted as exponent.")
        if is_number(second_var) and float(second_var) < 0:
            raise NotImplementedError(f"Some part of the polynomial var have negative power.")
        if not self._check_have_var(first_var):
            raise NotImplementedError("Cannot power a number by a var for the moment.")
        elif self._check_have_var(second_var):
            raise NotImplementedError("Cannot power a var by a var for the moment.")
        else:
            tokens = []
            tokens = convert_to_tokens(first_var_power + "*" + second_var)
            sum_power = self.solve(tokens, internal=True)
            if float(sum_power) == 0:
                return "1"
            return sign + self._write_power_to_var(var=self.var_name, power=sum_power)

    def _divide_a_var(self, first_var: str, second_var: str):

        first_var_power = str(self._get_power(first_var))
        second_var_power = str(self._get_power(second_var))

        # Cutting respective power and convert signed numbers
        first_var = convert_signed_number(first_var.split("^")[0], accept_var=True)
        second_var = convert_signed_number(second_var.split("^")[0], accept_var=True)

        if not self._check_have_var(first_var):
            raise NotImplementedError("Cannot divide a number by a var for the moment.")
        elif not self._check_have_var(second_var):
            if second_var == "0.0":
                raise ValueError(
                    "The expression lead to a division by zero : ", first_var, " / ", second_var
                )
            sum_power = first_var_power
            removed_var1_name = first_var.replace(self.var_name, "1")
            tokens = []
            # Signed numbers are already converted.
            tokens = convert_to_tokens(removed_var1_name + "/" + second_var)
            result = self.solve(tokens, internal=True)
            if float(result) != 1 and float(result) != -1:
                if float(sum_power) == 0:
                    return result
                return result + "*" + self._write_power_to_var(var=self.var_name, power=sum_power)
            else:
                if float(sum_power) == 0:
                    return "1"
                elif float(result) == -1:
                    return "-" + self._write_power_to_var(var=self.var_name, power=sum_power)
                else:
                    return self._write_power_to_var(var=self.var_name, power=sum_power)
        else:
            sum_power = str(self.solve([first_var_power, "-", second_var_power], internal=True))

            removed_var1_name = first_var.replace(self.var_name, "1")
            removed_var2_name = second_var.replace(self.var_name, "1")
            tokens = []
            tokens = convert_to_tokens(removed_var1_name + "/" + removed_var2_name)
            result = self.solve(tokens, internal=True)
            if float(sum_power) == 0:
                return result
            return result + "*" + self._write_power_to_var(var=self.var_name, power=sum_power)

    def _add_or_substract_var_to_var(self, operator: str, first_var: str, second_var: str):
        pattern = self.var_name
        # Checking if multiple var in first_var (ex : x + X ^ 2)
        if len(re.findall(pattern=pattern, string=first_var)) > 1:
            second_var_power = str(float(self._get_power(second_var)))
            if second_var_power != "1.0":
                # regex that match any sign or none, followed by any number or none
                # followed by the var name followed by the power of the var
                pattern = "[{sign}]*[.\d]*[\*]*{var_name}\^{second_var_power}".format(
                    var_name=self.var_name, second_var_power=second_var_power, sign=_SIGN
                )
            else:
                # Same for simple X, the var name shouln't be followed by a power operator
                pattern = "[{sign}]*[.\d]*[\*]*{var_name}(?!\^)".format(
                    var_name=self.var_name, second_var_power=second_var_power, sign=_SIGN
                )
            split = re.split(pattern=pattern, string=first_var)
            if len(split) > 1:
                search = re.search(pattern=pattern, string=first_var)
                if search is not None:
                    # Cutting respective power and convert signed numbers
                    first_var = add_implicit_cross_operator_for_vars(
                        vars_list=list(self.var_name),
                        expression=convert_signed_number(search.group(0), accept_var=True),
                    )
                    second_var = add_implicit_cross_operator_for_vars(
                        vars_list=list(self.var_name),
                        expression=convert_signed_number(second_var, accept_var=True),
                    )
                    tokens = convert_to_tokens(first_var + operator + second_var)
                    result = self.solve(tokens=tokens, internal=True)
                    if result == "0.0":
                        return parse_sign("".join(split))
                    else:
                        return parse_sign(result + "+" + "".join(split))

        first_var_power = str(self._get_power(first_var))
        second_var_power = str(self._get_power(second_var))

        # Different power
        if first_var_power != second_var_power:
            return first_var + operator + second_var

        # Cutting respective power and convert signed numbers
        first_var = add_implicit_cross_operator_for_vars(
            vars_list=list(self.var_name),
            expression=convert_signed_number(first_var.split("^")[0], accept_var=True),
        )
        second_var = add_implicit_cross_operator_for_vars(
            vars_list=list(self.var_name),
            expression=convert_signed_number(second_var.split("^")[0], accept_var=True),
        )

        removed_var1_name = first_var.replace(self.var_name, "1")
        removed_var2_name = second_var.replace(self.var_name, "1")

        tokens = convert_to_tokens(removed_var1_name + operator + removed_var2_name)
        result = self.solve(tokens, internal=True)
        if float(result) == 0:
            return "0.0"
        elif float(result) == 1:
            return self._write_power_to_var(var=self.var_name, power=first_var_power)
        else:
            return str(result) + self._write_power_to_var(var=self.var_name, power=first_var_power)

    def _multiply_a_var(self, first_var: str, second_var: str):

        first_var_power = str(self._get_power(first_var))
        second_var_power = str(self._get_power(second_var))

        # Cutting respective power and convert signed numbers
        first_var = convert_signed_number(first_var.split("^")[0], accept_var=True)
        second_var = convert_signed_number(second_var.split("^")[0], accept_var=True)

        if not self._check_have_var(first_var):
            if first_var == "0.0":
                return "0.0"
            else:
                sum_power = second_var_power
                remove_var_name = second_var.replace(self.var_name, "1")
                tokens = []
                tokens = convert_to_tokens(first_var + "*" + remove_var_name)
                result = self.solve(tokens, internal=True)
                if float(result) != 1 and float(result) != -1:
                    if float(sum_power) == 0:
                        return result
                    return (
                        result + "*" + self._write_power_to_var(var=self.var_name, power=sum_power)
                    )
                else:
                    if float(sum_power) == 0:
                        return "1"
                    elif float(result) == -1:
                        return "-" + self._write_power_to_var(var=self.var_name, power=sum_power)
                    else:
                        return self._write_power_to_var(var=self.var_name, power=sum_power)

        elif not self._check_have_var(second_var):
            sum_power = first_var_power

            remove_var_name = first_var.replace(self.var_name, "1")
            tokens = []
            tokens = convert_to_tokens(remove_var_name + "*" + second_var)
            result = self.solve(tokens, internal=True)
            if float(result) != 1 and float(result) != -1:
                if float(sum_power) == 0:
                    return result
                return result + "*" + self._write_power_to_var(var=self.var_name, power=sum_power)
            else:
                if float(sum_power) == 0:
                    return "1"
                elif float(result) == -1:
                    return "-" + self._write_power_to_var(var=self.var_name, power=sum_power)
                else:
                    return self._write_power_to_var(var=self.var_name, power=sum_power)
        # Both have var.
        else:
            sum_power = str(self.solve([first_var_power, "+", second_var_power], internal=True))

            removed_var1_name = first_var.replace(self.var_name, "1")
            removed_var2_name = second_var.replace(self.var_name, "1")
            tokens = []
            tokens = convert_to_tokens(removed_var1_name + "*" + removed_var2_name)

            result = self.solve(tokens, internal=True)
            if float(result) != 1 and float(result) != -1:
                if float(sum_power) == 0:
                    return result
                return result + "*" + self._write_power_to_var(var=self.var_name, power=sum_power)
            else:
                if float(sum_power) == 0:
                    return "1"
                elif float(result) == -1:
                    return "-" + self._write_power_to_var(var=self.var_name, power=sum_power)
                else:
                    return self._write_power_to_var(var=self.var_name, power=sum_power)

    def resolve_npi(self, npi_list) -> str:
        stack = []
        c = 0.0
        var_is_present = True if self.var_name else False

        for elem in npi_list:
            if is_number(elem) or (var_is_present and elem in self.var_name):
                stack.append(elem)
            else:
                last_two_in_stack = stack[-2:]
                del stack[-2:]
                if len(last_two_in_stack) < 2:
                    raise IndexError(
                        "There is a problem in the npi resolver, the npi_list isn't well formated."
                    )
                # Doing var calc if there is a var
                if var_is_present and (
                    self._check_have_var(str(last_two_in_stack[0]))
                    or self._check_have_var(str(last_two_in_stack[1]))
                ):
                    # - or + operator, adding to c
                    if elem in _SIGN:
                        if not self._check_have_var(str(last_two_in_stack[0])):
                            if elem == "-":
                                c = my_round(c + float(last_two_in_stack[0]))
                                # Inverting the sign of the var because it is the second element.
                                result = self._multiply_a_var("-1", str(last_two_in_stack[1]))
                            else:
                                c = my_round(c + float(last_two_in_stack[0]))
                                result = str(last_two_in_stack[1])

                        elif not self._check_have_var(str(last_two_in_stack[1])):
                            if elem == "-":
                                c = my_round(c - float(last_two_in_stack[1]))
                            else:
                                c = my_round(c + float(last_two_in_stack[1]))
                            result = str(last_two_in_stack[0])
                        else:
                            # Adding var to var
                            result = self._add_or_substract_var_to_var(
                                operator=elem,
                                first_var=str(last_two_in_stack[0]),
                                second_var=str(last_two_in_stack[1]),
                            )
                    elif elem == "*":
                        result = self._multiply_a_var(
                            str(last_two_in_stack[0]), str(last_two_in_stack[1])
                        )
                    elif elem == "/":
                        result = self._divide_a_var(
                            str(last_two_in_stack[0]), str(last_two_in_stack[1])
                        )
                    elif elem == "^":
                        result = self._power_a_var(
                            str(last_two_in_stack[0]), str(last_two_in_stack[1])
                        )
                    else:
                        raise NotImplementedError(
                            "This type of operation with vars is not accepted for the moment."
                        )

                # Doing usual calc
                elif elem == "^":
                    result = my_round(
                        my_power(float(last_two_in_stack[0]), float(last_two_in_stack[1]))
                    )
                elif elem == "*":
                    result = my_round(float(last_two_in_stack[0]) * float(last_two_in_stack[1]))
                elif elem == "/":
                    if float(last_two_in_stack[1]) == 0.0:
                        raise ValueError(
                            "The expression lead to a division by zero : ",
                            float(last_two_in_stack[0]),
                            " / ",
                            float(last_two_in_stack[1]),
                        )
                    result = my_round(float(last_two_in_stack[0]) / float(last_two_in_stack[1]))
                elif elem == "%":
                    if float(last_two_in_stack[1]) == 0.0:
                        raise ValueError(
                            "The expression lead to a modulo zero : ",
                            float(last_two_in_stack[0]),
                            " % ",
                            float(last_two_in_stack[1]),
                        )
                    result = my_round(float(last_two_in_stack[0]) % float(last_two_in_stack[1]))
                elif elem == "+":
                    result = my_round(float(last_two_in_stack[0]) + float(last_two_in_stack[1]))
                elif elem == "-":
                    result = my_round(float(last_two_in_stack[0]) - float(last_two_in_stack[1]), 6)
                stack.append(result)

        if len(stack) > 1:
            raise Exception(
                "Unexpected error when trying to resolve npi. Maybe your input format is not accepted?"
            )

        if var_is_present:
            if c != 0.0:
                print("ici, c = ", c)
                # Parse sign because could have duplicate sign with the add of the +
                return parse_sign(str(c) + "+" + str(stack[0]))
            else:
                return str(stack[0])
        else:
            return str(stack[0])

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
        """
        Actually checking there is one and only one var and getting the name of it.
        Also checking notImplemented operations.
        """
        vars_list = re.findall(pattern=r"[a-zA-Z]+", string="".join(self._tokens))
        # Removing duplicate var
        vars_set = list(set(vars_list))
        if len(vars_set) > 1:
            print("vars_set = ", vars_set)
            raise SyntaxError("Calculator does not accept more than 1 var.")
        self.var_name = "".join(vars_set)

    def _remove_extra_zero(self, expression: str):
        pass

    def solve(self, tokens: list, verbose: bool = False, internal: bool = False) -> str:
        """
        Resolving str calc.
        If internal is set to true, it means that the calc is from inside the class and should check
        For vars because it should be already set.
        """
        self._tokens = tokens
        self._verbose = verbose
        print("Token inside Calculator : ", tokens) if self._verbose is True else None
        if not internal:
            self._check_vars()
        npi = self.npi_converter(self._tokens, accept_var=True if self.var_name else False)
        print("Token converted to npi system : ", npi) if self._verbose is True else None
        result = parse_sign(self.resolve_npi(npi))
        return result
