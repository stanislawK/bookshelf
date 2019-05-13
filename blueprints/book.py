from flask import Blueprint, flash, render_template

from bookshelf.forms.book_form import BookForm
from bookshelf.models.author import AuthorModel
from bookshelf.models.book import BookModel
from bookshelf.models.category import CategoryModel

book_blueprint = Blueprint('book', __name__, template_folder='templates')


@book_blueprint.route('/book/add/form', methods=['GET', 'POST'])
def add_book_form():
    form = BookForm()

    # Submit form with single author and cantegory
    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        author = form.authors.data
        category = form.categories.data

        new_book = BookModel(title=title, description=description)
        new_book.save_to_db()

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

    return render_template('bookForm.html', form=form)
