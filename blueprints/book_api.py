from flask import Blueprint, flash, render_template, request, url_for
import requests

from bookshelf.models.author import AuthorModel
from bookshelf.models.book import BookModel
from bookshelf.models.category import CategoryModel

book_api = Blueprint('book_api', __name__, template_folder='templates')
base_url = "https://www.googleapis.com/books/v1/volumes"


@book_api.route('/book/add/api', methods=['GET', 'POST'])
def add_book_api():
    key = request.form.get('keyWord')
    print(key)
    if request.method == 'POST' and key:
        # Sending request to google API with key from user
        params = {'q': key}
        r = requests.get(base_url, params=params)
        books = r.json()

        if books.get('items'):
            book = books['items'][0]
            title = book.get('volumeInfo').get('title')
            description = book.get('volumeInfo').get('description')
            authors = book.get('volumeInfo').get('authors')
            categories = book.get('volumeInfo').get('categories')

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

            flash('New book successfully added', 'success')

            return render_template('bookApi.html', new_book=new_book)
    return render_template('bookApi.html')
