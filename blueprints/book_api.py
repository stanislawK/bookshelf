from flask import (
                    Blueprint,
                    flash,
                    render_template,
                    redirect,
                    request,
                    url_for,
                    session)
import requests
from sqlalchemy.exc import DataError

from bookshelf.helpers import save_all_books, create_books_dict
from bookshelf.models.author import AuthorModel
from bookshelf.models.book import BookModel
from bookshelf.models.category import CategoryModel

book_api = Blueprint('book_api', __name__, template_folder='templates')
base_url = "https://www.googleapis.com/books/v1/volumes"


@book_api.route('/book/add/api', methods=['GET', 'POST'])
def add_book_api():
    key = request.form.get('keyWord')
    all_books = request.form.get('save_all')
    advanced = request.form.get('advanced')
    title = request.form.get('keyTitle', '')
    author = request.form.get('keyAuth', '')

    if request.method == 'POST' and key or author or title:
        # Sending request to google API with key from user
        if title:
            key = "{}+intitle".format(title)
        elif author:
            key = "{}+inauthor".format(author)

        params = {'q': key,
                  'printType': 'books'}
        r = requests.get(base_url, params=params)
        books = r.json()
        session.clear()
        session['new_books'] = []
        session['keyword'] = key

        if books.get('items'):
            create_books_dict(books)

            return render_template('bookApi.html',
                                   new_books=session['new_books'])
        # elif request.method == 'POST' and title or author:
        #     # Sending request to google API with advaced searchin key
        #     if title:
        #         key = "{}+intitle".format(title)
        #     else:
        #         key = "{}+inauthor".format(author)
        #     params = {'q': key,
        #               'printType': 'books'}
        #     r = requests.get(base_url, params=params)
        #     books = r.json()
        #     session.clear()
        #     session['new_books'] = []
        #     session['keyword'] = key
        #
        #     if books.get('items'):
        #         create_books_dict(books)
        #
        #         return render_template('bookApi.html',
        #                                new_books=session['new_books'])

    return render_template('bookApi.html',
                           new_books=session.get('new_books'),
                           advanced=advanced)


@book_api.route('/_load_more_books/', methods=['GET', 'POST'])
def load_more_books():
    more = request.form.get('load_more')
    key = session.get('keyword')
    books_now = len(session.get('new_books'))

    if more and key and books_now < 40:
        results = books_now + 10
        params = {'q': key,
                  'printType': 'books',
                  'maxResults': results}
        r = requests.get(base_url, params=params)
        books = r.json()
        session['new_books'] = []

        # Create dictionary with books, and save it into session
        if books.get('items'):
            create_books_dict(books)

        return redirect(url_for('book_api.add_book_api'))
    return redirect(url_for('book_api.add_book_api'))


@book_api.route('/_add_all_books/', methods=['GET', 'POST'])
def add_books_api():
    try:
        books = session.get('new_books')
        save_all_books(books)
        flash('{} books successfully added'.format(len(books)),
              'success')
        session.clear()
    except (DataError, TypeError):
        session.clear()
        flash('At least one of books has invalid data', 'danger')
        return redirect(url_for('book_api.add_book_api'))
    return redirect(url_for('book_api.add_book_api'))


@book_api.route('/_add_selected_books/', methods=['GET', 'POST'])
def add_seleced_books_api():
    selected_id = request.form.getlist("selected")
    if selected_id:
        selected_id = [int(id) for id in selected_id]
        all_books = session.get('new_books')
        selected_books = [all_books[id] for id in selected_id]
        try:
            save_all_books(selected_books)
            flash('{} books successfully added'.format(len(selected_books)),
                  'success')
            for id in sorted(selected_id, reverse=True):
                del session.get('new_books')[id]
        except (DataError, TypeError, AttributeError):
            session.clear()
            flash('At least one of books has invalid data', 'danger')
            return redirect(url_for('book_api.add_book_api'))

    return redirect(url_for('book_api.add_book_api'))
