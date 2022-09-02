import os.path
from datetime import datetime
from functools import cached_property

from utils.json import pretty_dump
from .base import BaseExtractor


class TweetExtractor(BaseExtractor):
    @cached_property
    def data_type(self):
        return 'tweet'

    def _get_id(self, tweet):
        return self._get_content(tweet)['id']

    created_at_format = '%a %b %d %H:%M:%S %z %Y'

    @cached_property
    def json_sorted_file(self):
        return os.path.join(self.INTERMEDIATE_DIR, f'{self.data_type}-sorted.json')

    @cached_property
    def json_data(self):
        data: list = super().json_data
        for tweet in data:
            created_at = self._get_content(tweet)['created_at']
            created_at_datetime = datetime.strptime(created_at, self.created_at_format)
            created_at_timestamp = created_at_datetime.timestamp()
            self._get_content(tweet)['created_at_timestamp'] = created_at_timestamp
        data.sort(key=lambda t: self._get_content(t)['created_at_timestamp'])
        pretty_dump(data, self.json_sorted_file)
        return data

    def __call__(self):
        return super().__call__()


tweet_extractor = TweetExtractor()

if __name__ == '__main__':
    tweet_extractor()
