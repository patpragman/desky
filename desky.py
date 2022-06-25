import argparse
from Token import Tokenizer, parse_tokens, show_memory

parser = argparse.ArgumentParser()
parser.add_argument('-m',
                    type=str,
                    help='insert your math expression in quotes behind this param, for example -m "4 + 5 + 6"')

parser.add_argument('-f',
                    type=str,
                    help='file path to a script')


parser.add_argument("-v",
                    default=False,
                    action="store_true",
                    help="verbose")

args = parser.parse_args()

if __name__ == "__main__":
    # we don't need the first arguments here, that's just the file name
    if args.m:
        tokenizer = Tokenizer(args.m)
        result = parse_tokens(tokenizer.tokens, verbose=args.v)
        show_memory()
    elif args.f:
        with open(args.f, "r") as file:
            for line in file.readlines():
                tokenizer = Tokenizer(line)
                result = parse_tokens(tokenizer.tokens, verbose=args.v)
                show_memory()