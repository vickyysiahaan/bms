from app import db, ma
from models.string_sensor import StringSensor

class Site(db.Model):
    __tablename__ = 'site'

    id = db.Column(db.Integer, primary_key=True)
    site_name = db.Column(db.String(120), unique=True, nullable=False)
    city = db.Column(db.String(60), nullable=False)
    site_address = db.Column(db.String(120), nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    number_of_string = db.Column(db.Integer, nullable=False)
    total_capacity = db.Column(db.Float, nullable=False)
    stringsensor = db.relationship('StringSensor', backref='site', lazy=True)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_sitename(cls, site_name):
        return cls.query.filter_by(site_name=site_name).first()

    @classmethod
    def find_by_site_id(cls, id):
        query_result = cls.query.filter_by(id=id).first()
        return query_result

    @classmethod
    def return_all(cls):
        query_result = Site.query.all()
        return query_result

    @classmethod
    def delete_all(cls):
        try:
            num_rows_deleted = db.session.query(cls).delete()
            db.session.commit()
            return {'message': '{} row(s) deleted'.format(num_rows_deleted)}
        except:
            return {'message': 'Something went wrong'}

class SiteSchema(ma.ModelSchema):
    class Meta:
        model = Site