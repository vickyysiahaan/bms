from app import db
from models import users, type

class WalletModel(db.Model):
    __tablename__ = 'wallets'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    type_id = db.Column(db.Integer, db.ForeignKey('type.id'), nullable=False)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def return_all(cls):
        def to_json(x):
            return {
                'name': x.name,
                'amount': x.amount,
                'user': users.UserModel().find_by_user_id(x.user_id),
                'type': type.TypeModel().find_by_type_id(x.type_id)
            }

        return {'wallets': list(map(lambda x: to_json(x), WalletModel.query.all()))}