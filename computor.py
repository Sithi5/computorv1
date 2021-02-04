# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    computor.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: mabouce <ma.sithis@gmail.com>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/12/01 20:27:45 by mabouce           #+#    #+#              #
#    Updated: 2021/02/04 11:45:28 by mabouce          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sys
import argparse, parser

from expression_resolver import ExpressionResolver
from exception import NothingToDoError


def main(argv=None):
    print()
    parser = argparse.ArgumentParser()
    parser.add_argument("expression", type=str, help="Insert expression to resolve.")
    parser.add_argument(
        "-v",
        "--verbose",
        help="Add verbose and print different resolving step.",
        action="store_true",
    )
    parser.add_argument(
        "-vv",
        "--force_calculator_verbose",
        help="Add all verbose and force the calculator verbose.",
        action="store_true",
    )
    args = parser.parse_args(argv)

    resolver = ExpressionResolver(
        verbose=args.verbose | args.force_calculator_verbose,
        force_calculator_verbose=args.force_calculator_verbose,
    )
    try:
        result = resolver.solve(args.expression)
        if isinstance(result, list):
            print("The ", len(result), " solutions are :")
            for res in result:
                print(res)
        else:
            print("result = ", result)
    except SyntaxError as e:
        print("The expression syntax is not accepted : ", e)
    except ValueError as e:
        print("One of the value in the expression is not accepted : ", e)
    except NotImplementedError as e:
        print("One of the methods needed is not implemented yet : ", e)
    except NothingToDoError as e:
        print(e)
    except Exception as e:
        print("An exception appened : ", e)


if __name__ == "__main__":
    main()
