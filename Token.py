import operator
from operator import add, sub, mul, truediv, floordiv, pow


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

    order_of_operations = ["^", "*", "/", "+", "-", "_"]




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


    operators = Token.operators
    order_of_operations = Token.order_of_operations

    # go through and parse the perens out...
    previous_list = token_list.copy()
    index = 0
    while index < len(previous_list):
        if type(previous_list[index]) is list:
            previous_list[index] = parse_tokens(previous_list[index],  verbose=verbose)
        index += 1

    output = []
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
