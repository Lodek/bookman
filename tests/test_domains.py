from unittest import TestCase
import json

from bookman.domain import Book

class BookTest(TestCase):

    def test_parsing_book_with_sample_data_generates_correct_book(self):
        # Given item data 
        item = """
        {
            "volumeInfo": {
                "title": "Fluent Python",
                "authors": [
                    "Luciano Ramalho"
                ],
                "publishedDate": "2015-06-25",
                "industryIdentifiers": [
                    {
                        "type": "ISBN_10",
                        "identifier": "1491946008"
                    },
                    {
                        "type": "ISBN_13",
                        "identifier": "9781491946008"
                    }
                ]
            }
        }
        """
        item = json.loads(item)
        # When created book from item
        book = Book.from_item(item)
        # Then book has correct data
        self.assertEquals(book.title, "Fluent Python")
        self.assertEquals(book.authors, ["Luciano Ramalho"])
        self.assertEquals(book.year, 2015)
        self.assertEquals(book.isbn, "9781491946008")


    def test_parsing_book_with_missing_data_has_default_values(self):
        # Given item data 
        item = """
        {
            "volumeInfo": { 
                "industryIdentifiers": []
            }
        }
        """
        item = json.loads(item)
        # When created book from item
        book = Book.from_item(item)
        # Then book has correct data
        self.assertEquals(book.title, "untitled")
        self.assertEquals(book.authors, ["unknown"])
        self.assertEquals(book.year, 9999)
        self.assertEquals(book.isbn, "0")
