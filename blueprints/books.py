from flask import Blueprint, render_template, request

from bookshelf.models.author import AuthorModel
from bookshelf.models.book import BookModel
from bookshelf.models.category import CategoryModel

books_blueprint = Blueprint('books', __name__, template_folder='templates')


@books_blueprint.route('/', methods=['POST'])
def add_book():
    title = request.form.get('title')
    description = request.form.get('description')
    authors = request.form.get('authors').split(',')
    categories = request.form.get('categories').split(',')

    new_book = BookModel(title=title, description=description)
    new_book.save_to_db()

    for author_name in authors:
        author = AuthorModel.find_by_name(author_name)
        if not author:
            author = AuthorModel(name=author_name)
            author.save_to_db()

        new_book.add_author(author)

    for category_name in categories:
        category = CategoryModel.find_by_name(category_name)
        if not category:
            category = CategoryModel(name=category_name)
            category.save_to_db()
        new_book.add_category(category)

    all_books = BookModel.query.all()
    return 'hello world'


@books_blueprint.route('/books', methods=['GET', 'POST'])
def books():
    books = BookModel.query.all()
    authors = AuthorModel.query.all()
    categories = CategoryModel.query.all()

    author = request.form.get('author_id')
    category = request.form.get('category_id')

    # Filter books by author
    if request.method == 'POST' and author:
        books = BookModel.find_by_author(author)

    if request.method == 'POST' and category:
        books = BookModel.find_by_category(category)

    return render_template('books.html',
                           books=books,
                           authors=authors,
                           categories=categories)
