from app import db

class ContactModel(db.Model):
    __tablename__ = 'contacts'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    job = db.Column(db.String(120), nullable=False)
    salary = db.Column(db.String(120), nullable=False)
    photo = db.Column(db.BLOB)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_user_id(cls, user_id):
        def to_json(x):
            return {
                'first_name': x.first_name,
                'last_name': x.last_name,
                'email': x.email,
                'phone': x.phone,
                'job': x.job,
                'salary': x.salary,
                'photo': x.photo,
            }
        query = cls.query.filter_by(user_id=user_id).first()
        return to_json(query)