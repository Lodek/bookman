#!/usr/bin/env python
"""
script that given a file name, assumed to be a pdf, queries google books,
with the filename, fetches the first result and print that results isbn.
"""
import shutil, sys, re
import requests
from pathlib import Path

def get_isbn(item):
    ids = item['volumeInfo']['industryIdentifiers']
    isbn = list(filter(lambda e : True if 'ISBN_13' in e['type'] else False, ids))[0]
    return isbn['identifier']

process_name = lambda book : book.name.replace(book.suffix, '').replace(' ', '+').replace('-', '+').replace('_', '+')

def query_isbn(book):
    #query = 'https://www.googleapis.com/books/v1/volumes?q={}&key=AIzaSyAtXTwTILD15Gnen0ww0M2SWR7O8o4DLU4'
    query = 'https://www.googleapis.com/books/v1/volumes?q={}'
    r = requests.get(query.format(process_name(book)))
    print(query.format(process_name(book)))
    json = r.json()
    items = json['items']
    for item in items:
        authors = item['volumeInfo']['authors']
        title = item['volumeInfo']['title']
        prompt = f'confirm {authors}, {title}\nFOR {book.name} (Y/y)\n'
        confirm = input(prompt)
        if confirm in 'y Y'.split():
            return get_isbn(item)

def main():
    books = [p for p in Path('.').absolute().iterdir() if '.pdf' in p.name and not re.search(r'^\d', p.name)]
    for book in books:
        isbn = query_isbn(book)
        shutil.move(book, f'{isbn}.pdf')


if __name__ == '__main__':
    main()
