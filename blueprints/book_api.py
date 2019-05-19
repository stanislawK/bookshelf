from flask import Blueprint, flash, render_template, redirect, request, url_for
import requests
from sqlalchemy.exc import DataError

from bookshelf.helpers import save_all_books
from bookshelf.models.author import AuthorModel
from bookshelf.models.book import BookModel
from bookshelf.models.category import CategoryModel

book_api = Blueprint('book_api', __name__, template_folder='templates')
base_url = "https://www.googleapis.com/books/v1/volumes"

new_books = []
@book_api.route('/book/add/api', methods=['GET', 'POST'])
def add_book_api():
    key = request.form.get('keyWord')
    all_books = request.form.get('save_all')

    if request.method == 'POST' and key:
        # Sending request to google API with key from user
        params = {'q': key}
        r = requests.get(base_url, params=params)
        books = r.json()

        if books.get('items'):
            for item in books.get('items'):
                book = item['volumeInfo']
                title = book.get('title')
                description = book.get('description', 'Unknown')
                authors = book.get('authors', ['Unknown'])
                categories = book.get('categories', ['Unknown'])

                new_book = {
                    "title": title,
                    "description": description,
                    "authors": authors,
                    "categories": categories
                }
                new_books.append(new_book)
            return render_template('bookApi.html', new_books=new_books)
    return render_template('bookApi.html')


@book_api.route('/_add_all_books/', methods=['GET', 'POST'])
def add_books_api():
    try:
        save_all_books(new_books)
        flash('{} books successfully added'.format(len(new_books)),
              'success')
        new_books = []
    except DataError:
        flash('At least one of books has invalid data', 'danger')
        return redirect(url_for('book_api.add_book_api'))
    return redirect(url_for('book_api.add_book_api'))
