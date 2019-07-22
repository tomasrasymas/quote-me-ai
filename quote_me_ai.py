from src import quotes_generator
from src.similarity import Similarity
from src.unsplash import Unsplash
from src.image import Image
from config import get_config
from src.reddit_post import RedditPost
from src.logger_mixin import LoggerMixin
import numpy as np
import traceback
import time


config = get_config()


class QuoteMeAI(LoggerMixin):
    def __init__(self, max_quote_length):
        super().__init__()

        quotes_generator.load_model('model')
        self.similarity = Similarity()
        self.unsplash = Unsplash(api_key=config.UNSPLASH_API_KEY)
        self.max_quote_length = max_quote_length
        self.reddit = RedditPost(
            subreddit=config.REDDIT_SUBREDDIT,
            client_id=config.REDDIT_CLIENT_ID,
            client_secret=config.REDDIT_CLIENT_SECRET,
            password=config.REDDIT_PASSWORD,
            user_agent=config.REDDIT_USER_AGENT,
            username=config.REDDIT_USERNAME)

    def get_best_photo(self, photos, quote_vector):
        photos_vectors = [self.similarity.get_vector(p[2]) for p in photos]
        photos_vectors = list(filter(lambda v: v is not None, photos_vectors))

        photos_scores = self.similarity.similarity(quote_vector,
                                                   np.array(photos_vectors))

        photo_id = np.argmin(photos_scores)
        Unsplash.trigger_download(photos[photo_id][0])
        return photos[photo_id]

    def clean_quote(self, quote):
        quote = quote.replace('<|startoftext|>', '').replace('<|endoftext|>', '')
        return quote

    def run(self):
        while True:
            try:
                quote = quotes_generator.generate()[0]

                quote = self.clean_quote(quote)

                self.logger.info('Quote: %s' % quote)

                if len(quote) > self.max_quote_length:
                    self.logger.warning('Quote too long!')
                    continue

                quote_vector = self.similarity.get_vector(text=quote)
                keywords = self.similarity.get_keywords(text=quote,
                                                        num=config.NUMBER_OF_KEYWORDS)
                self.logger.info('Keywords: %s' % ','.join(keywords))

                photos = self.unsplash.get_photos(query=','.join(keywords),
                                                  num=config.UNSPLASH_PHOTOS_TO_ANALYSE)
                self.logger.info('Unsplash found photos: %s' % len(photos))

                if not photos:
                    self.logger.warning('No Unsplash photos found!')
                    continue

                photo = self.get_best_photo(photos=photos,
                                            quote_vector=quote_vector)
                self.logger.info(photo)

                image = Image(url=photo[1])
                image.draw_text(text=quote)
                image_file_path = image.save(file_path=config.QUOTES_IMAGES_PATH)

                self.reddit.post(text=photo[3],
                                 image_path=image_file_path)

                self.logger.info('Posted to reddit!')

                time.sleep(config.GENERATION_TIMEOUT)
            except KeyboardInterrupt:
                self.logger.info('Stoping!')
                break
            except:
                self.logger.exception(traceback.format_exc())
                time.sleep(60)


if __name__ == '__main__':
    q = QuoteMeAI(max_quote_length=config.MAX_QUOTE_TEXT_LENGTH)
    q.run()