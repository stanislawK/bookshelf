import json

from bookshelf.models.author import AuthorModel
from bookshelf.models.book import BookModel
from bookshelf.models.category import CategoryModel


def save_all_books(books):
    for book in books:
        title = book.get('title')
        description = book.get('description')
        authors = book.get('authors')
        categories = book.get('categories')

        new_book = BookModel(title=title, description=description)
        new_book.save_to_db()

        for author in authors:
            author_db = AuthorModel.find_by_name(author)
            if not author_db:
                author_db = AuthorModel(name=author)
                author_db.save_to_db()
            new_book.add_author(author_db)

        for category in categories:
            category_db = CategoryModel.find_by_name(category)
            if not category_db:
                category_db = CategoryModel(name=category)
                category_db.save_to_db()
            new_book.add_category(category_db)
