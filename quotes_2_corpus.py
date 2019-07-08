import argparse
from src.quotes_importer import QuotesImporter
from config import get_config


config = get_config()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate corpus out of dataset files',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-o', '--output', dest='output', type=str, required=False, metavar='',
                        help='Corpus file path', default=config.CORPUS_FILE_PATH)
    parser.add_argument('-sp', '--start_prefix', dest='start_prefix', type=str, required=False, metavar='',
                        help='Quote start prefix', default='<|startoftext|>')
    parser.add_argument('-ep', '--end_prefix', dest='end_prefix', type=str, required=False, metavar='',
                        help='Quote end prefix', default='<|endoftext|>')

    args = parser.parse_args()

    print('*' * 50)
    for i in vars(args):
        print(str(i) + ' - ' + str(getattr(args, i)))

    print('*' * 50)

    print('Loading quotes files!')

    quotes = QuotesImporter.load_from_file_path()
    quotes.to_file(file_path=args.output,
                   start_prefix=args.start_prefix,
                   end_prefix=args.end_prefix)

    print('Done!')