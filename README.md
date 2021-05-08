# About
Bookman is a simple manager for books.

Bookman uses a convention to generate books file names.
It integrates with Google Books API to fetch information for a book and it generates a bookman formatted file name.

Combined with `fzf` it's easy to find books.

The bookname fileconvention is as follows:

```
[tag1][tag2]Author-One,Author-Two_Book-Title(2000)_ISBN.pdf
```

Tags can be used by bookman to open all books with a given tag, for instance.
