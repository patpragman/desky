from dataclasses import dataclass


@dataclass(unsafe_hash=True)
class Token:
    name: str

@dataclass(unsafe_hash=True)
class Number(Token):
    value: float

@dataclass(unsafe_hash=True)
class String(Token):
    value: str

@dataclass(unsafe_hash=True)
class Delimiter(Token):
    value: str

@dataclass(unsafe_hash=True)
class UnattachedString(Token):
    value: str

@dataclass(unsafe_hash=True)
class Function(Token):
    args: int
    def value(self, *args):
        pass

@dataclass(unsafe_hash=True)
class Statement(Token):
    value: str


# all the delimiters that define various delimiters and whitespace between end_statements
open_delimiter = Delimiter(name="open", value="(")
close_delimiter = Delimiter(name="close", value=")")
separator_delimiter = Delimiter(name="separator", value=",")
endl_delimiter = Delimiter(name="endl", value=";")
tab_delimiter = Delimiter(name="tab", value="\t")
space_delimiter = Delimiter(name="space", value=" ")
newline_delimiter = Delimiter(name="newline", value="\n")
empty_string_delimiter = Delimiter(name="empty_string", value='')
# all the various delimiters in a set for ease of access in the Tokenizer class
delimiters = {open_delimiter, close_delimiter, separator_delimiter,
              endl_delimiter, tab_delimiter, space_delimiter,
              newline_delimiter, empty_string_delimiter}
# whitespace delimiters set for similar reasons
white_space_delimiters = {tab_delimiter, space_delimiter, newline_delimiter, empty_string_delimiter}

"""
Now we will define the various statement strings


"""
set_value = Statement(name="set", value="set")
print_value = Statement(name="print", value="print")
get_value = Statement(name="get",value="get")

pat_script_statements = {set_value, print_value, get_value}

"""
now we should define the operators
"""
exponentiation = Function(name="^", args=2)
exponentiation.value = lambda x, y: x**y

multiply = Function(name="*", args=2)
multiply.value = lambda x, y: x * y

divide = Function(name="/", args=2)
divide.value = lambda x, y: x / y

add = Function(name="+", args=2)
add.value = lambda x, y: x + y

subtract = Function(name="-", args=2)
subtract.value = lambda x, y: x - y

pat_script_operators = {exponentiation, multiply, divide, add, subtract}


class Tokenizer:

    def __init__(self, parseable_string):
        del_map = {d.value: d for d in delimiters}

        """
        build out a list of strings and the first tokens (which are single characters)
        """
        self.raw_tokens = []
        working_string = [s for s in parseable_string]
        word = ""
        while working_string:
            current_char = working_string.pop(0)

            if current_char in del_map:
                self.raw_tokens.extend([word, del_map[current_char]])
                word = ""
            else:
                word = word + current_char

        # remove the left over empty strings
        for i, token in enumerate(self.raw_tokens):
            if token == "":
                self.raw_tokens.pop(i)

        # remove all the white space
        for i, token in enumerate(self.raw_tokens):
            if token in white_space_delimiters:
                self.raw_tokens.pop(i)

        # let's evaluate strings and numbers...
        for i, token in enumerate(self.raw_tokens):
            if type(token) is str:
                try:
                    value = float(token)
                    self.raw_tokens[i] = Number(name=token, value=value)

                except ValueError:
                    if token[0] == '"':
                        value = "".join([chr for chr in token[1 : -1]])
                        if token[-1] != '"':
                            raise Exception('String not closed!  Unable to parse tokens.')
                        self.raw_tokens[i] = String(name=token, value=value)
                    elif '"' not in token:
                        self.raw_tokens[i] = UnattachedString(name=token, value=token)

        # now iterate through it again, and changed unattached strings that are operators to operator objects
        operator_map = {o.name: o for o in pat_script_operators}
        for i, token in enumerate(self.raw_tokens):
            if type(token) is UnattachedString:
                if token.name in operator_map:
                    self.raw_tokens[i] = operator_map[token.name]

        # now let's do the same sort of thing to track down the statements
        statement_map = {s.value: s for s in pat_script_statements}
        for i, token in enumerate(self.raw_tokens):
            if token in statement_map:
                self.raw_tokens[i] = statement_map[token]


