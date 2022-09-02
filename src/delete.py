import logging.config
import os.path
import time
from functools import cached_property

from requests import Response

from extractors.base import BaseExtractor
from gen_final import FinalListGenerator, like_generator, tweet_generator
from utils.csv import read_csv_one_col
from utils.twitter_api import session, USER_ID


class BaseDeleter:
    LOGGING_DIR = os.path.join(BaseExtractor.ROOT_DIR, 'delete-logs')

    os.makedirs(LOGGING_DIR, exist_ok=True)

    LOGGING = {
        'version': 1,
        'formatters': {
            'default': {
                'class': 'logging.Formatter',
                'format': '[%(levelname)s %(asctime)s] %(message)s',
            },
        },
        'handlers': {},
        'loggers': {},
    }

    class RetryLater(Exception):
        def __init__(self, rate_limit_reset):
            self.rate_limit_reset = rate_limit_reset

    def __init__(self, generator: FinalListGenerator):
        self.generator = generator
        self.LOGGING['handlers'][self.data_type] = {
            'class': 'logging.FileHandler',
            'filename': os.path.join(self.LOGGING_DIR, f'{self.data_type}.log'),
            'formatter': 'default',
        }
        self.LOGGING['loggers'][self.logger_name] = {
            'level': 'INFO',
            'handlers': [self.data_type],
        }

        self.success_count = 0
        self.failure_count = 0

    @property
    def data_type(self):
        return self.generator.data_type

    @cached_property
    def logger_name(self):
        return f'delete.{self.data_type}'

    @cached_property
    def logger(self):
        return logging.getLogger(self.logger_name)

    @cached_property
    def id_list(self) -> list:
        return read_csv_one_col(self.generator.final_list_file)

    def get_url(self, tweet_id) -> str:
        raise NotImplementedError

    def _delete(self, tweet_id):
        resp = session.delete(self.get_url(tweet_id))
        try:
            resp.raise_for_status()
        except Exception as e:
            self.logger.error(f'{tweet_id}: {e}, {resp.content}')
            if resp.status_code == 429:
                raise self.RetryLater(float(resp.headers['x-rate-limit-reset'])) from None
            raise
        return resp

    def _delete_retry(self, tweet_id):
        while True:
            try:
                return self._delete(tweet_id)
            except self.RetryLater as retry:
                sleep = retry.rate_limit_reset - time.time() + 1  # add 1 second just to be safe
                msg = f'Sleeping for {sleep} seconds due to rate limit...'
                print(msg)
                self.logger.info(msg)
                time.sleep(sleep)

    def check_success(self, resp: Response) -> bool:
        raise NotImplementedError

    def delete(self, tweet_id):
        resp = self._delete_retry(tweet_id)
        if self.check_success(resp):
            self.logger.info(f'{tweet_id}: {resp.content}')
            self.success_count += 1
        else:
            self.logger.warning(f'{tweet_id}: {resp.content}')
            self.failure_count += 1
        return resp

    def __call__(self):
        for tweet_id in self.id_list:
            self.delete(tweet_id)
        print(f'{self.data_type}: {self.success_count} SUCCESS, {self.failure_count} FAILURE')


class LikeDeleter(BaseDeleter):
    def get_url(self, tweet_id) -> str:
        return f'https://api.twitter.com/2/users/{USER_ID}/likes/{tweet_id}'

    def check_success(self, resp: Response) -> bool:
        return not resp.json()['data']['liked']


class TweetDeleter(BaseDeleter):
    def get_url(self, tweet_id) -> str:
        return f'https://api.twitter.com/2/tweets/{tweet_id}'

    def check_success(self, resp: Response) -> bool:
        return resp.json()['data']['deleted']


like_deleter = LikeDeleter(like_generator)
tweet_deleter = TweetDeleter(tweet_generator)

if __name__ == '__main__':
    logging.config.dictConfig(BaseDeleter.LOGGING)
    like_deleter()
    tweet_deleter()
