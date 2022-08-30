from extractors.likes import LikeExtractor
from extractors.tweets import TweetExtractor


def main():
    LikeExtractor()()
    TweetExtractor()()


if __name__ == '__main__':
    main()
