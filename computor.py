# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    computor.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: mabouce <ma.sithis@gmail.com>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/12/01 20:27:45 by mabouce           #+#    #+#              #
#    Updated: 2020/12/11 16:05:07 by mabouce          ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import argparse, parser

from expression_resolver import ExpressionResolver


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
    args = parser.parse_args(argv)

    resolver = ExpressionResolver(verbose=args.verbose)
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
    except NotImplementedError as e:
        print("One of the methods needed is not implemented yet : ", e)
    except Exception as e:
        print("An exception appened : ", e)


if __name__ == "__main__":
    main()
