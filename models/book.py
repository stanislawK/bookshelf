from bookshelf.extensions import db
from bookshelf.models.author import AuthorModel
from bookshelf.models.category import CategoryModel


book_auth = db.Table(
    'book_auth',
    db.Column('book_id', db.Integer, db.ForeignKey('books.id')),
    db.Column('author_id', db.Integer, db.ForeignKey('authors.id')))

book_cat = db.Table(
    'book_cat',
    db.Column('book_id', db.Integer, db.ForeignKey('books.id')),
    db.Column('cat_id', db.Integer, db.ForeignKey('categories.id'))
)


class BookModel(db.Model):
    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    description = db.Column(db.Text, nullable=False)
    authors = db.relationship(
        "AuthorModel",
        secondary=book_auth,
        backref=db.backref('books', lazy=True))
    categories = db.relationship(
        "CategoryModel",
        secondary=book_cat,
        backref=db.backref('books', lazy=True)
    )

    @classmethod
    def find_by_author(cls, auth_id):
        auth = AuthorModel.find_by_id(auth_id)
        return cls.query.filter(cls.authors.contains(auth)).all()

    @classmethod
    def find_by_category(cls, cat_id):
        category = CategoryModel.find_by_id(cat_id)
        return cls.query.filter(cls.categories.contains(category)).all()

    def add_author(self, author):
        self.authors.append(author)
        db.session.commit()

    def add_category(self, category):
        self.categories.append(category)
        db.session.commit()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
