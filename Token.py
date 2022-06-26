from math import sin, cos, tan, degrees, radians
from operator import add, sub, mul, truediv, floordiv, pow



def print_with_return(x):
    print(x)
    return 0

class Token:

    whitespace = {"\t", " ", "\n"}

    delimiters = {"(": lambda l :parse_tokens(l),
                  ")": lambda r: r}
    operators = {"^": pow,
                 "*": mul,
                 "/": truediv,
                 "+": add,
                 "-": sub,
                 "_": floordiv}

    functions = {"abs": abs,
                 "sin": sin,
                 "cos": cos,
                 "tan": tan,
                 "rad": radians,
                 "degrees": degrees,
                 "print": lambda x: print_with_return(x)}


    n_functions = {}

    order_of_operations = ["^", "*", "/", "_", "+", "-"]


class Tokenizer:

    def __init__(self, parseable_string):
        self.raw_tokens = []

        working_string = [s for s in parseable_string]
        word = ""
        while working_string:
            current_char = working_string.pop(0)
            if current_char in Token.operators:
                self.raw_tokens.extend([word, current_char])
                word = ""
            elif current_char in Token.delimiters:
                self.raw_tokens.extend([word, current_char])
                word = ""
            elif current_char in Token.whitespace:
                self.raw_tokens.extend([word])
                word = ""
            else:
                word = word + current_char

        self.raw_tokens.append(word)

        # remove all whitespace and none tokens
        self.raw_tokens = [t for t in self.raw_tokens
                           if t not in Token.whitespace]
        self.raw_tokens = [t for t in self.raw_tokens if
                           t != ""]

        # try to clean the raw tokens
        working_list = []
        for token in self.raw_tokens:
            try:
                working_list.append(float(token))
            except:
                working_list.append(token)


        for index, token in enumerate(working_list):
            # find negative numbers
            if working_list[index] == "-":
                if type(working_list[index - 1]) is str:
                    working_list[index + 1] = -working_list[index + 1]
                    working_list.pop(index)

        self.tokens = working_list


def find_sublists(token_list) -> list:

    new_list = []

    while token_list:
        token = token_list.pop(0)

        if token == ")":
            return new_list
        elif token == "(":
            new_list.append(find_sublists(token_list))
        else:
            new_list.append(token)

    return new_list

def parse_tokens(token_list, verbose=False) -> list:
    token_list = find_sublists(token_list)
    if verbose:
        print("Sub-problem:", token_list)

    functions = Token.functions
    n_functions = Token.n_functions

    operators = Token.operators
    order_of_operations = Token.order_of_operations

    # go through and parse the perens out...
    previous_list = token_list.copy()
    index = 0


    for func in functions:
        for i, token in enumerate(previous_list):
            if token == func:
                f = functions[func]

                if previous_list[i + 1] is list:
                    previous_list[i + 1] = previous_list[i + 1].pop(0)
                    print("here", previous_list[i + 1])
                previous_list[i] = f(parse_tokens(previous_list.pop(i + 1))[0])

    for op in order_of_operations:
        index = 0
        while index < len(previous_list):

            if previous_list[index] == op:
                left = previous_list.pop(index - 1)
                f = operators[previous_list.pop(index - 1)]
                right = previous_list.pop(index - 1)

                # deal with sublists returned as lists
                if type(left) is list:
                    left = left[0]

                if type(right) is list:
                    right = right[0]

                new = f(left, right)
                previous_list.insert(index - 1, new)

            index += 1

    if len(previous_list) > 1:
        return parse_tokens(previous_list, verbose=verbose)
    else:
        return previous_list
