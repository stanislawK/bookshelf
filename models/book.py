from bookshelf.extensions import db


class BookModel(db.Model):
    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    authors = db.Column(db.String, nullable=False)
    categories = db.Column(db.String(50), nullable=False)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
