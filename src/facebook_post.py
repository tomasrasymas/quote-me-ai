import facebook
from config import get_config


config = get_config()


class FacebookPost:
    def __init__(self, access_token):
        self.access_token = access_token
        self.graph = facebook.GraphAPI(access_token=self.access_token, version='3.2')

    def post(self, text, image_path):
        with open(image_path, 'rb') as image:
            self.graph.put_photo(image=image, message=text)


if __name__ == '__main__':
    f = FacebookPost(access_token=config.FACEBOOK_ACCESS_TOKEN)
    f.post(text='Photo by <a href="%s?utm_source=%s&utm_medium=referral">%s</a> on <a href="https://unsplash.com/?utm_source=%s&utm_medium=referral">Unsplash</a>', image_path='../docs/20190704225727.png')