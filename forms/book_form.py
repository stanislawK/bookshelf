from flask_wtf import FlaskForm
from wtforms import FieldList, StringField, TextAreaField, validators


class BookForm(FlaskForm):
    title = StringField('Title', [
        validators.Length(max=50),
        validators.DataRequired()
    ])
    description = TextAreaField('Description', [
        validators.Length(min=5, max=200),
        validators.DataRequired()
    ])
    authors = StringField('Author', [
        validators.Length(max=50),
        validators.DataRequired()
    ])
    categories = StringField('Category', [
        validators.Length(max=50),
        validators.DataRequired()
    ])
