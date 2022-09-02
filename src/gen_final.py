import os.path
from functools import cached_property

from extractors.base import BaseExtractor
from extractors.likes import like_extractor
from extractors.tweets import tweet_extractor
from utils.csv import read_csv_one_col, write_csv_one_col


class FinalListGenerator:
    DATA_DIR = os.path.join(BaseExtractor.ROOT_DIR, 'customize')
    OUTPUT_DIR = os.path.join(BaseExtractor.ROOT_DIR, 'to-delete')

    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    def __init__(self, extractor: BaseExtractor):
        self.extractor = extractor

    @property
    def data_type(self):
        return self.extractor.data_type

    @cached_property
    def id_list(self) -> list:
        return read_csv_one_col(self.extractor.id_list_file)

    @cached_property
    def keep_list_file(self):
        return os.path.join(self.DATA_DIR, 'keep', f'{self.data_type}.csv')

    @cached_property
    def has_keep_list(self) -> bool:
        return os.path.exists(self.keep_list_file)

    @cached_property
    def keep_list(self):
        return read_csv_one_col(self.keep_list_file)

    @cached_property
    def final_list_file(self):
        return os.path.join(self.OUTPUT_DIR, f'{self.data_type}.csv')

    @cached_property
    def final_list(self):
        final = self.id_list.copy()
        if self.has_keep_list:
            final = [
                id_
                for id_ in final
                if id_ not in self.keep_list
            ]
        write_csv_one_col(final, self.final_list_file)
        return final

    def __call__(self):
        return self.final_list


like_generator = FinalListGenerator(like_extractor)
tweet_generator = FinalListGenerator(tweet_extractor)

if __name__ == '__main__':
    like_generator()
    tweet_generator()
