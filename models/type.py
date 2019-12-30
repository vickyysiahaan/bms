from app import db

class TypeModel(db.Model):
    __tablename__ = 'type'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    wallet = db.relationship("WalletModel", backref="type", lazy=True)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_type_id(cls, id):
        def to_json(x):
            return {
                'name': x.name
            }
        query = cls.query.filter_by(id=id).first()
        return to_json(query)