from unittest import TestCase

from bookman.api_service import GBooksService, api_factory
from bookman import settings

class GBooksServiceTest(TestCase):

    @classmethod
    def setUpClass(cls):
        api = api_factory(settings.API_KEY)
        cls.service = GBooksService(api)


    def test_fetching_book_returns_json_with_expected_by_format(self):
        # Given ISBN
        isbn = '1491946008'
        # When service is used to fetch data
        data = self.service.query('', isbn=isbn)
        # Then response contains items
        self.assertIn('items', data)
        # Then response contains volumeInfo
        self.assertIn('volumeInfo', data['items'][0])
        # Then response contains authors
        self.assertIn('authors', data['items'][0]['volumeInfo'])
        # Then response contains title
        self.assertIn('title', data['items'][0]['volumeInfo'])
