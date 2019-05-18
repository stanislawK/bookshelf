from flask_wtf import FlaskForm
from wtforms import FieldList, StringField, TextAreaField, validators


class BookForm(FlaskForm):
    title = StringField('Title', [
        validators.Length(max=50),
        validators.DataRequired('Title is required')
    ])
    description = TextAreaField('Description', [
        validators.Length(min=5, max=200),
        validators.DataRequired('Description is required')
    ])
    authors = FieldList(StringField('Author', [
        validators.Length(max=50),
        validators.DataRequired('You have to provide at least one author')
    ]), min_entries=1)
    categories = FieldList(StringField('Category', [
        validators.Length(max=50),
        validators.DataRequired('You have to provide at least one category')
    ]), min_entries=1)
