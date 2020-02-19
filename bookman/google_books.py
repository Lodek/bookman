from mycollections.url import URL
import requests

class InvalidKeywordError(RuntimeError):

    def __init__(self, keyword, allowed_keywords):
        err = f'Keyword {key} invalid for volume query, allowed keywords\
                are {allowed_keywords}'
        super(err)

class Api:
    """
    GoogleBooks API abstraction.
    Incomplete and only implmenets volumes endpoints
    """
    BASE_URL = URL.from_string('https://www.googleapis.com/books/v1/')
    volumes = BASE_URL / 'volumes'

    def __init__(self, api_key=''):
        self.api_key = api_key
        self.api_url = Api.volumes
        
    def _get_json(self, url):
        """Perform a request to the given url, return json """
        if self.api_key:
            url = url.add_query(dict(key=self.api_key))
        r = requests.get(url)
        if r.status_code != 200:
            raise RuntimeError(r.content)
        return r.json()


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
        Processes query string and remove special/special characters
        Source: https://developers.google.com/books/docs/v1/using#PerformingSearch"""
        allowed_keywords = 'intitle inauthor inpublisher subject isbn lccn oclc'.split()
        for key in kwargs:
            if key not in allowed_keywords:
                raise InvalidKeywordError
        keywords = self._serialize_dict(kwargs, kv_separator=':', join_symbol='+')
        query = re.sub(r'[ -|:()\][]', '+', query)
        q = {'q' : query + '+' + keywords}
        url = self.volumes.add_query(q)
        return self._get_json(url)

    def query_volumes_isbn(self, isbn):
        """Query volumes using only an isbn, return query json"""
        isbn = str(isbn).replace('-', '').replace(' ', '')
        return self.query_volumes('', isbn=isbn)
