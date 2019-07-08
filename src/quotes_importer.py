import os
from config import get_config
import csv
import json
from tqdm import tqdm


config = get_config()


class QuotesImporter:
    def __init__(self, quotes):
        self.quotes = quotes
        self.idx = 0

    def __iter__(self):
        return self

    def __next__(self):
        try:
            quote = self.quotes[self.idx]
        except IndexError:
            raise StopIteration

        self.idx += 1

        return quote

    def __len__(self):
        return len(self.quotes)

    def to_file(self, file_path=config.CORPUS_FILE_PATH, start_prefix='', end_prefix=''):
        with open(file_path, 'w') as f:
            for quote in self.quotes:
                f.write('%s%s%s%s' % (start_prefix, quote, end_prefix, os.linesep))

    @staticmethod
    def read_file(file_path, type, separator, position):
        data = []

        if separator == 'TAB':
            separator = '\t'

        if type == 'CSV':
            with open(file_path, 'r') as f:
                buffer = csv.reader(f, delimiter=separator)
                for row in tqdm(buffer):
                    data.append(row[int(position)])
        elif type == 'JSON':
            if separator == 'ARRAY':
                with open(file_path, 'r') as f:
                    buffer = json.load(f)
                    for obj in tqdm(buffer):
                        data.append(obj[position])

        return data

    @classmethod
    def load_from_file_path(cls, files_path=config.DATASET_PATH):
        buffer = []

        for file in os.listdir(files_path):
            attributes = file.split(config.DATASET_FILES_ATTRIBUTES_SEPARATOR)
            f_type, f_separator, f_position = attributes[1:4]

            buffer += QuotesImporter.read_file(os.path.join(files_path, file), f_type, f_separator, f_position)

        return cls(list(set(buffer)))



