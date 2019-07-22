import praw
from config import get_config


config = get_config()


class RedditPost:
    def __init__(self, subreddit, client_id, client_secret, password, user_agent, username):
        self.subreddit = subreddit
        self.client_id = client_id
        self.client_secret = client_secret
        self.password = password
        self.user_agent = user_agent
        self.username = username

        self.reddit = praw.Reddit(client_id=self.client_id,
                                  client_secret=self.client_secret,
                                  password=self.password,
                                  user_agent=self.user_agent,
                                  username=self.username)

    def post(self, text, image_path):
        my_sub = self.reddit.subreddit(self.subreddit)
        my_sub.submit_image(title=text,
                            image_path=image_path)


if __name__ == '__main__':
    r = RedditPost(subreddit=config.REDDIT_SUBREDDIT,
                   client_id=config.REDDIT_CLIENT_ID,
                   client_secret=config.REDDIT_CLIENT_SECRET,
                   password=config.REDDIT_PASSWORD,
                   user_agent=config.REDDIT_USER_AGENT,
                   username=config.REDDIT_USERNAME)

    r.post(text='Photo by <a href="%s?utm_source=%s&utm_medium=referral">%s</a> on <a href="https://unsplash.com/?utm_source=%s&utm_medium=referral">Unsplash</a>', image_path='../docs/20190704225727.png')