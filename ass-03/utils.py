import argparse

def parser():
    #Create the main parser
    parser = argparse.ArgumentParser(description='Sequential group recommendation methods')

    #Create sub-parsers
    subparsers = parser.add_subparsers(dest='method', help='Available methods')

    add_parser_seq = subparsers.add_parser('seq', help='Sequential standard method')
    add_parser_seq.add_argument('function', choices=['pc', 'cs', 'ed', 'js'], help='Available similarity functions')
    add_parser_seq.add_argument('users', nargs='+', type=int, help='Input users')

    args = parser.parse_args()

    return args