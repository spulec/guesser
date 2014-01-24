# Guesser - a smart guessing library

[![Build Status](https://travis-ci.org/spulec/guesser.png?branch=master)](https://travis-ci.org/spulec/guesser)

# In a nutshell

Guesser is a library that allows you to smartly guess values to find an unkownn boundary on a function.

For example, imagine you are given access to an API for books. Given an integer representing a book, you are able to look up the book with `Book.get(7)`. If you try to find a book with an integer that is higher than all of the other books, it will raise a `BookNotFound` exception.

We want to find out how many books there are (we assume there are not 'gaps' in the ids).

The old way we would write this code:

```python
def get_max_book_id(self):
    book_id = 1
    while True:
        try:
            Book.get(book_id)
        except BookNotFound:
            return book_id - 1
        book_id += 1
```

This works, but it is going to be very slow since we need to look up every single book. Here is how the code would look with Guesser:

```python
def check_if_book_exists(book_id):
    try:
        Book.get(book_id)
    except BookNotFound:
        return False
    return True

def get_max_book_id(self):
    return guesser.guess(check_if_book_exists, start=50)
```

Instead of sequentially trying all of the values, Guesser will intelligently use bisection to find the maximum value.

The first argument to `guesser.guess` must be a function whose first parameter which is the value to be tested. This function must return True or False depending on if the condition to check is satisfied. If it returns True, guesser will guess higher numbers. If it returns False, guesser will guess lower numbers.

The `smart` argument is an approximate guess at what the maxium value will be. This helps to give Guesser a general idea of where it should start searching. This value is optional and can be left off though.

You can also pass additional args and kwargs to `guesser.guess` to be passed to the function. Say we wanted to find the max book in a given library:

```python
def check_if_book_exists_in_library(book_id, library_id):
    try:
        Book.get(book_id)
    except BookNotFound:
        return False
    return True

def get_max_book_id(self):
    return guesser.guess(check_if_book_exists, library_id=123, start=50)
```

## Install

```console
$ pip install guesser
```
