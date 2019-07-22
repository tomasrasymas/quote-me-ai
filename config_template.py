import os


class Config:
    DATASET_PATH = 'datasets'
    QUOTES_IMAGES_PATH = 'quotes_images'
    FONTS_PATH = 'fonts'
    DATASET_FILES_ATTRIBUTES_SEPARATOR = '||'
    CORPUS_FILE_PATH = 'corpus'
    UNSPLASH_API_KEY = ''
    IMAGE_TEXT_PLACES = ['center', 'right', 'left']
    IMAGE_TEXT_XY_PAIRS = [(10, 10), (10, 200), (300, 100), (300, 10)]
    IMAGE_TEXT_PAD_WIDTH = 10
    IMAGE_TEXT_PAD_HEIGHT = 10
    UNSPLASH_PHOTOS_TO_ANALYSE = 10
    NUMBER_OF_KEYWORDS = 2
    MAX_QUOTE_TEXT_LENGTH = 200
    IMAGE_TEXT_COLOR = (255, 255, 255)
    SIMILARITY_POS_TAGS = ['NOUN', 'PROPN', 'VERB']
    SIMILARITY_METRIC = 'cosine'
    FILES_TO_DOWNLOAD = {
        'model.zip': ''
    }
    GENERATION_TIMEOUT = 5
    LOG_PATH = 'log'
    REDDIT_SUBREDDIT = ''
    REDDIT_CLIENT_ID = ''
    REDDIT_CLIENT_SECRET = ''
    REDDIT_PASSWORD = ''
    REDDIT_USER_AGENT = ''
    REDDIT_USERNAME = ''


class DevelopmentConfig(Config):
    pass


class TestConfig(Config):
    pass


class ProductionConfig(Config):
    pass


def get_config():
    env = os.environ.get('env', None)

    if env == 'development':
        return DevelopmentConfig
    elif env == 'production':
        return ProductionConfig
    elif env == 'test':
        return TestConfig
    else:
        return DevelopmentConfig
