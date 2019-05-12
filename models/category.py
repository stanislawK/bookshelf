from bookshelf.extensions import db


class CategoryModel(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    @classmethod
    def find_by_name(cls, _name):
        cls.query.filter_by(name=_name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
