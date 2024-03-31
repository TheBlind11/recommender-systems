import argparse

def parser():
    #Create the main parser
    parser = argparse.ArgumentParser(description='Group recommendation methods')

    #Create sub-parsers
    subparsers = parser.add_subparsers(dest='method', help='Available methods')

    add_parser_avg = subparsers.add_parser('avg', help='Average method')
    add_parser_avg.add_argument('function', choices=['pc', 'cs', 'ed', 'js'], help='Available similarity functions')
    add_parser_avg.add_argument('users', nargs='+', type=int, help='Input users')

    add_parser_lm = subparsers.add_parser('lm', help='Least misery method')
    add_parser_lm.add_argument('function', choices=['pc', 'cs', 'ed', 'js'], help='Available similarity functions')
    add_parser_lm.add_argument('users', nargs='+', type=int, help='Input users')

    add_parser_msd = subparsers.add_parser('msd', help='Mean squared deviation method')
    add_parser_msd.add_argument('function', choices=['pc', 'cs', 'ed', 'js'], help='Available similarity functions')
    add_parser_msd.add_argument('users', nargs='+', type=int, help='Input users')

    args = parser.parse_args()

    return args