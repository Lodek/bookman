"""
Google Books API Service module
"""
from bookman import settings

from googleapiclient.discovery import build
import requests


# FIXME Api factory shouldn't be here
def api_factory(api_key):
    service = build(settings.API_NAME, settings.API_VERSION, developerKey=api_key)
    return service.volumes()


class GBooksService:
    """
    Wrapper for Google Books Api which does json processing and implements
    utility functions to be used directly with bookman's model objects.
    """

    VOLUMES_URL = "https://www.googleapis.com/books/v1/volumes?q={}"
    ALLOWED_KEYWORDS = {'intitle', 'inauthor', 'inpublisher',
                        'subject', 'isbn', 'lccn', 'oclc'}

    def query(self, query, **kwargs):
        """
        Perform query on GBooks api
        """
        keys = set(kwargs.keys())
        left = keys - self.ALLOWED_KEYWORDS
        if left:
            raise AttributeError(f'kwargs must be one of {keywords}')

        keywords_query = self._keyword_query_builder(**kwargs)
        query = query.replace(' ', '+')
        query = query + keywords_query
        response = requests.get(self.VOLUMES_URL.format(query))
        if response.status_code != 200:
            raise RuntimeError("API Fetch failed")
        return response.json()

    def _keyword_query_builder(self, **kwargs):
        """Builder method that receives kwargs and return a query string as
        specified by the Google Books documentation"""
        join_token = '+'
        assignment_token = ':'
        return join_token.join([f'{key}{assignment_token}{value}'
                                for key, value in kwargs.items()])
