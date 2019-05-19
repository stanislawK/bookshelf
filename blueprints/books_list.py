from flask import Blueprint, render_template, request, url_for

from bookshelf.models.author import AuthorModel
from bookshelf.models.book import BookModel
from bookshelf.models.category import CategoryModel

books_blueprint = Blueprint(
    'books_list',
    __name__,
    template_folder='templates')


@books_blueprint.route('/books', methods=['GET', 'POST'])
def books():
    books = BookModel.query.all()
    authors = AuthorModel.query.all()
    categories = CategoryModel.query.all()

    author = request.form.get('author_id')
    category = request.form.get('category_id')
    clear = request.form.get('clear')
    select = ''
    # Filter books by author
    if request.method == 'POST' and author:
        books = BookModel.find_by_author(author)
        select = 'a{}'.format(author)

    if request.method == 'POST' and category:
        books = BookModel.find_by_category(category)
        select = 'c{}'.format(category)

    if request.method == 'POST' and clear:
        books = BookModel.query.all()
        select = ''

    return render_template('books.html',
                           books=books,
                           authors=authors,
                           categories=categories,
                           select=select)
