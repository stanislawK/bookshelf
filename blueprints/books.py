from flask import Blueprint, jsonify, request

from bookshelf.models.book import BookModel
from bookshelf.models.author import AuthorModel

books_blueprint = Blueprint('books', __name__)


@books_blueprint.route('/', methods=['POST'])
def hello_world():
    title = request.form.get('title')
    description = request.form.get('description')
    authors = request.form.get('authors').split(',')
    categories = request.form.get('categories')

    new_book = BookModel(title=title,
                         description=description,
                         categories=categories)
    new_book.save_to_db()
    for author_name in authors:
        author = AuthorModel.find_by_name(author_name)
        if not author:
            author = AuthorModel(name=author_name)
            author.save_to_db()

        new_book.add_author(author)

    all_books = BookModel.query.all()
    return 'hello world'
