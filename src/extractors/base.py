import os
from functools import cached_property

from utils.csv import write_csv
from utils.json import js_to_json, pretty_dump


class BaseExtractor:
    ROOT_DIR = '/data'
    SOURCE_DIR = os.path.join(ROOT_DIR, 'backup-data')
    INTERMEDIATE_DIR = os.path.join(ROOT_DIR, 'extract-tmp')
    OUTPUT_DIR = os.path.join(ROOT_DIR, 'extracted')

    os.makedirs(INTERMEDIATE_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    @property
    def data_type(self):
        raise NotImplementedError

    @cached_property
    def source_file(self):
        return os.path.join(self.SOURCE_DIR, f'{self.data_type}.js')

    @cached_property
    def json_file(self):
        return os.path.join(self.INTERMEDIATE_DIR, f'{self.data_type}.json')

    @cached_property
    def json_data(self):
        data = js_to_json(self.source_file)
        pretty_dump(data, self.json_file)
        return data

    def _get_id(self, tweet):
        raise NotImplementedError

    @cached_property
    def id_list_file(self):
        return os.path.join(self.OUTPUT_DIR, f'{self.data_type}.csv')

    @cached_property
    def id_list(self):
        data = [self._get_id(tweet) for tweet in self.json_data]
        csv_data = [[tweet_id] for tweet_id in data]
        write_csv(csv_data, self.id_list_file)
        return data

    def __call__(self):
        return self.id_list
