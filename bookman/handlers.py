class Handler:

    def __init__(self, domain):
        self.domain = domain


    def get_formatted_name(self, query):
        """ """
        books = self.domain.get_books_from_query(query)
        for book in books:
            print(str(book))
