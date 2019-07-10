from pyunsplash import PyUnsplash


class Unsplash:
    def __init__(self, api_key, app_name='quote-me-ai'):
        self.unsplash = PyUnsplash(api_key=api_key)
        self.app_name = app_name

    def get_photos(self, query, num):
        photos = []
        search = self.unsplash.search(type_='photos', query=query, per_page=30)
        for entry in search.entries:
            if len(photos) >= num:
                break

            description = entry.body.get('description', None)

            if entry.link_download and description:
                photographer_text = '''Photo by %s?utm_source=%s&utm_medium=referral %s on https://unsplash.com/?utm_source=%s&utm_medium=referral''' % (entry.body['user']['links']['html'], self.app_name, entry.body['user']['name'], self.app_name)

                photos.append((entry.link_download_location, entry.body['description'], photographer_text))

        return photos