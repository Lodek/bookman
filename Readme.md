# About
Bookman is a simple manager for books.

Bookman identifies books through their ISBN.

Bookman serves as tool to manage books the user has chosen to add.
Bookman localy stores the usual metadata (authors, title, year, publisher, version) and allows users to tag books or add notes.
Furthermore, bookman is extensible and the user can add fields to each book's data.

Given the aforementioned use case, bookman has a *simple* (probably naive) approach to dealing with files.
The user may set a directory in which which bookman will look for files and open the matching books.
Since bookman doesn't store file paths, it recursively searches the configured directory for a file that contains the books ISBN as part of its name.

Bookman leverages the Google Books API.
Books can be added directly through their ISBN or through a custom search string.
Information is stored in a JSON file.
