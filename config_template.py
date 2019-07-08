import os


class Config:
    DATASET_PATH = 'datasets'
    QUOTES_IMAGES_PATH = 'quotes_images'
    FONTS_PATH = 'fonts'
    DATASET_FILES_ATTRIBUTES_SEPARATOR = '||'
    CORPUS_FILE_PATH = 'corpus'
    UNSPLASH_API_KEY = 'YOURS'
    IMAGE_TEXT_PLACES = ['center', 'right', 'left']
    IMAGE_TEXT_XY_PAIRS = [(100, 100), (100, 500), (500, 100), (500, 500)]
    IMAGE_TEXT_PAD_WIDTH = 50
    IMAGE_TEXT_PAD_HEIGHT = 50
    UNSPLASH_PHOTOS_TO_ANALYSE = 10
    NUMBER_OF_KEYWORDS = 2
    MAX_QUOTE_TEXT_LENGTH = 150
    IMAGE_TEXT_COLOR = (255, 255, 255)
    SIMILARITY_POS_TAGS = ['NOUN', 'PROPN', 'VERB']
    SIMILARITY_METRIC = 'cosine'
    FACEBOOK_ACCESS_TOKEN = 'YOURS'
    FILES_TO_DOWNLOAD = {
        'model.zip': 'YOURS'
    }
    GENERATION_TIMEOUT = 60 * 60
    LOG_PATH = 'log'


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
