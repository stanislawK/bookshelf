from bookshelf.extensions import db
from bookshelf.models.author import AuthorModel


book_auth = db.Table(
    'book_auth',
    db.Column('book_id', db.Integer, db.ForeignKey('books.id')),
    db.Column('author_id', db.Integer, db.ForeignKey('authors.id')))


class BookModel(db.Model):
    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    authors = db.relationship(
        "AuthorModel",
        secondary=book_auth,
        backref=db.backref('books', lazy=True))
    categories = db.Column(db.String(50), nullable=False)

    def add_author(self, author):
        self.authors.append(author)
        db.session.commit()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
