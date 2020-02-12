from mycollections.url import Url

class InvalidKeywordError(RuntimeError):

    def __init__(self, keyword, allowed_keywords):
        err = f'Keyword {key} invalid for volume query, allowed keywords
                are {allowed_keywords}'
        super(err)

class Api:
    """
    GoogleBooks API abstraction
    """
    BASE_URL = Url('https://www.googleapis.com/books/v1/')
    volumes = BASE_URL / 'volumes'

    def __init__(self, api_key=''):
        self.api_key = api_key
        self.url = URL(api_url)

    def _get_json(self, url):
        """Perform a request to the given url, return json """
        #TODO: add error handling for request
        #TODO: change api_key stuff to use Url class 
        url = url + f'&key={self.api_key}' if self.api_key else url
        r = requests.get(url)
        return r.json


    @staticmethod
    def _serialize_dict(dict, kv_separator, join_symbol):
        return join_symbol.join([f'{key}{kv_separator}{value}'
                                    for key, value in dict.items()])


    def get_volumes(self, id):
        """Get a volume by it's GoogleBooks Id"""
        url = self.volumes / str(id)
        return self._get_json(url)


    def query_volumes(self, query, **kwargs):
        """Perform a query over the volumes endpoints.
        Receive query string and dictionary with query special keywords as 
        explained in the documentation.
        Source: https://developers.google.com/books/docs/v1/using#PerformingSearch"""
        allowed_keywords = 'intitle inauthor inpublisher subject isbn lccn oclc'.split()
        for key in kwargs:
            if key not in allowed_keywords:
                raise InvalidKeywordError
        keywords = self._serialize_dict(kwargs, kv_separator=':', join_symbol='+')
        q = {'q' : query.replace(' ', '+') + '+' + keywords}
        url = self.volumes.add_query(q)
        return self._get_json(url)

    def query_volumes_isbn(self, isbn):
        """Query volumes using only an isbn, return query json"""
        isbn = str(isbn).replace('-', '').replace(' ', '')
        return self.query_volumes('', isbn=isbn)
