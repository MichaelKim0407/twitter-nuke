import os
from functools import cached_property

from utils.csv import write_csv_one_col
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

    def _get_content(self, tweet):
        return tweet[self.data_type]

    def _get_id(self, tweet):
        raise NotImplementedError

    @cached_property
    def id_map_file(self):
        return os.path.join(self.INTERMEDIATE_DIR, f'{self.data_type}-map.json')

    @cached_property
    def id_map(self):
        data = {
            self._get_id(tweet): self._get_content(tweet)
            for tweet in self.json_data
        }
        pretty_dump(data, self.id_map_file)
        return data

    @cached_property
    def id_list_file(self):
        return os.path.join(self.OUTPUT_DIR, f'{self.data_type}.csv')

    @cached_property
    def id_list(self):
        data = list(self.id_map.keys())
        write_csv_one_col(data, self.id_list_file)
        return data

    def __call__(self):
        return self.id_list
