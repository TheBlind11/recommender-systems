import argparse

def parser():
    #Create the main parser
    parser = argparse.ArgumentParser(description='User-based Collaborative Filtering approaches')

    #Create sub-parsers
    subparsers = parser.add_subparsers(dest='function', help='Available similarity functions')

    add_parser_pc = subparsers.add_parser('pc', help='Pearson correlation function')
    add_parser_pc.add_argument('user', type=int, help='Input user')

    add_parser_cs = subparsers.add_parser('cs', help='Cosine similarity function')
    add_parser_cs.add_argument('user', type=int, help='Input user')

    add_parser_ed = subparsers.add_parser('ed', help='Euclidean distance function')
    add_parser_ed.add_argument('user', type=int, help='Input user')

    add_parser_js = subparsers.add_parser('js', help='Jaccard similarity function')
    add_parser_js.add_argument('user', type=int, help='Input user')

    args = parser.parse_args()

    return args