from unittest import TestCase
import json

from bookman.domain import Book

class BookTest(TestCase):


    item = """
    {
        "kind": "books#volume",
        "id": "kgrXoAEACAAJ",
        "etag": "V9yHDpNVMoY",
        "selfLink": "https://books.googleapis.com/books/v1/volumes/kgrXoAEACAAJ",
        "volumeInfo": {
            "title": "Fluent Python",
            "authors": [
                "Luciano Ramalho"
            ],
            "publisher": "O'Reilly Media",
            "publishedDate": "2015-06-25",
            "description": "description",
            "industryIdentifiers": [
                {
                    "type": "ISBN_10",
                    "identifier": "1491946008"
                },
                {
                    "type": "ISBN_13",
                    "identifier": "9781491946008"
                }
            ],
            "readingModes": {
                "text": false,
                "image": false
            },
            "pageCount": 770,
            "printType": "BOOK",
            "categories": [
                "Computers"
            ],
            "maturityRating": "NOT_MATURE",
            "allowAnonLogging": false,
            "contentVersion": "preview-1.0.0",
            "imageLinks": {
                "smallThumbnail": "http://books.google.com/books/content?id=kgrXoAEACAAJ&printsec=frontcover&img=1&zoom=5&source=gbs_api",
                "thumbnail": "http://books.google.com/books/content?id=kgrXoAEACAAJ&printsec=frontcover&img=1&zoom=1&source=gbs_api"
            },
            "language": "en",
            "previewLink": "http://books.google.com.br/books?id=kgrXoAEACAAJ&dq=isbn:1491946008&hl=&cd=1&source=gbs_api",
            "infoLink": "http://books.google.com.br/books?id=kgrXoAEACAAJ&dq=isbn:1491946008&hl=&source=gbs_api",
            "canonicalVolumeLink": "https://books.google.com/books/about/Fluent_Python.html?hl=&id=kgrXoAEACAAJ"
        },
        "saleInfo": {
            "country": "BR",
            "saleability": "NOT_FOR_SALE",
            "isEbook": false
        },
        "accessInfo": {
            "country": "BR",
            "viewability": "NO_PAGES",
            "embeddable": false,
            "publicDomain": false,
            "textToSpeechPermission": "ALLOWED",
            "epub": {
                "isAvailable": false
            },
            "pdf": {
                "isAvailable": false
            },
            "webReaderLink": "http://play.google.com/books/reader?id=kgrXoAEACAAJ&hl=&printsec=frontcover&source=gbs_api",
            "accessViewStatus": "NONE",
            "quoteSharingAllowed": false
        },
        "searchInfo": {
            "textSnippet": "snippet"
        }
    }
    """

    def test_parsing_book_with_sample_data_generates_correct_book(self):
        # Given item data 
        item = json.loads(self.item)
        # When created book from item
        book = Book.from_item(item)
        # Then book has correct data
        self.assertEquals(book.title, "Fluent Python")
        self.assertEquals(book.authors, ["Luciano Ramalho"])
        self.assertEquals(book.year, 2015)
        self.assertEquals(book.isbn, "9781491946008")
