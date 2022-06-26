from better_tokens import *
from pprint import pprint

code = 'set("hello", "world"); 5.0 + 5; do thing;'

pprint(Tokenizer(code).raw_tokens)