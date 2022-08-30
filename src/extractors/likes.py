from functools import cached_property

from .base import BaseExtractor


class LikeExtractor(BaseExtractor):
    @cached_property
    def data_type(self):
        return 'like'

    def _get_id(self, tweet):
        return tweet[self.data_type]['tweetId']


if __name__ == '__main__':
    LikeExtractor()()
