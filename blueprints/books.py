from flask import Blueprint, request

from bookshelf.models.book import BookModel

books_blueprint = Blueprint('books', __name__)


@books_blueprint.route('/', methods=['POST'])
def hello_world():
    title = request.form.get('title')
    description = request.form.get('description')
    authors = request.form.get('authors')
    categories = request.form.get('categories')
    new_book = BookModel(title=title,
                         description=description,
                         authors=authors,
                         categories=categories)
    new_book.save_to_db()
    books = BookModel.query.all()
    return books[0].title
