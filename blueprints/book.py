from flask import Blueprint, flash, jsonify, redirect, render_template, request

from bookshelf.forms.book_form import BookForm
from bookshelf.models.author import AuthorModel
from bookshelf.models.book import BookModel
from bookshelf.models.category import CategoryModel

book_blueprint = Blueprint('book', __name__, template_folder='templates')


@book_blueprint.route('/book/add/form', methods=['GET', 'POST'])
def add_book_form():
    book_form = BookForm()

    # Submit form with single author and cantegory
    if book_form.validate_on_submit():
        title = book_form.title.data
        description = book_form.description.data
        authors = book_form.authors.data
        category = book_form.categories.data
        new_book = BookModel(title=title, description=description)
        new_book.save_to_db()

        for author in authors:
            author_db = AuthorModel.find_by_name(author)
            if not author_db:
                author_db = AuthorModel(name=author)
                author_db.save_to_db()
            new_book.add_author(author_db)

        category_db = CategoryModel.find_by_name(category)
        if not category_db:
            category_db = CategoryModel(name=category)
            category_db.save_to_db()
        new_book.add_category(category_db)

        flash('New book successfully added', 'success')

    return render_template('bookForm.html', book_form=book_form)


@book_blueprint.route('/_add-author/<id>', methods=['GET'])
def add_author(id):
    book_form = BookForm()
    new_rows = [book_form.authors.append_entry() for _ in range(int(id))]
    new_row = str(new_rows[-1])
    return jsonify(new_row=new_row)
