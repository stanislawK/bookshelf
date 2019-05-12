import pytest

from bookshelf.models.author import AuthorModel
from bookshelf.models.book import BookModel
from bookshelf.models.category import CategoryModel


def test_add_new_book_to_db(_db, new_book):
    """
    GIVEN mocked db session, and book data
    WHEN a new book added to db
    THEN check the book data from db
    """
    db = _db
    book = BookModel(title=new_book['title'],
                     description=new_book['description'])

    db.session.add(book)
    db.session.commit()

    title = new_book['title']
    book = db.session.query(BookModel).filter_by(title=title).first()

    assert book.description == new_book['description']


def test_add_new_author_to_db(_db, new_author):
    """
    GIVEN mocked db session, and author data
    WHEN a new author added to db
    THEN check the author data from db
    """
    db = _db
    auth = AuthorModel(name=new_author['name'])

    db.session.add(auth)
    db.session.commit()

    auth = db.session.query(AuthorModel).all()[0]

    assert auth.name == new_author['name']


def test_add_new_category_to_db(_db, new_category):
    """
    GIVEN mocked db session, and category data
    WHEN a new category added to db
    THEN check the category data from db
    """
    db = _db
    cat = CategoryModel(name=new_category['name'])

    db.session.add(cat)
    db.session.commit()

    cat = db.session.query(CategoryModel).all()[0]

    assert cat.name == new_category['name']


def test_add_new_books_reletionships(_db, new_book, new_author, new_category):
    """
    GIVEN mocked db session, book, author, and category data
    WHEN author and category assigned to book
    THEN check the book relationship data from db
    """
    db = _db
    book = BookModel(title=new_book['title'],
                     description=new_book['description'])
    auth = AuthorModel(name=new_author['name'])
    cat = CategoryModel(name=new_category['name'])

    db.session.add(book)
    db.session.add(auth)
    db.session.add(cat)

    book.authors.append(auth)
    book.categories.append(cat)

    db.session.commit()

    title = new_book['title']
    book = db.session.query(BookModel).filter_by(title=title).first()
    auth = db.session.query(AuthorModel).all()[0]
    cat = db.session.query(CategoryModel).all()[0]

    assert book.description == new_book['description']
    assert book.authors[0].name == new_author['name']
    assert book.categories[0].name == new_category['name']
    assert auth.books[0].title == title
    assert cat.books[0].title == title
