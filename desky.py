import argparse
from Token import Tokenizer, parse_tokens

parser = argparse.ArgumentParser()
parser.add_argument('-m',
                    type=str,
                    help='insert your math expression in quotes behind this param, for example -m "4 + 5 + 6"')

parser.add_argument("-v",
                    default=False,
                    action="store_true",
                    help="verbose")

args = parser.parse_args()

if __name__ == "__main__":
    # we don't need the first arguments here, that's just the file name
    tokenizer = Tokenizer(args.m)
    result = parse_tokens(tokenizer.tokens, verbose=args.v)
    print(result)
