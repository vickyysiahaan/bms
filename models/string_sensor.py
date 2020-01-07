from app import db, ma
from models.cell_sensor import CellSensor
class StringSensor(db.Model):
    __tablename__ = 'string_sensor'

    id = db.Column(db.Integer, primary_key=True)
    string_number = db.Column(db.Integer, nullable=False)
    # site_id = db.Column(db.Integer, nullable=False)
    site_id = db.Column(db.Integer, db.ForeignKey('site.id'))
    manufacturer = db.Column(db.String(30), nullable=False)
    part_number = db.Column(db.String(30), nullable=False)
    number_of_cells = db.Column(db.Integer, nullable=False)
    cellsensor = db.relationship('CellSensor', backref='stringsensor', lazy=True)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_string_id(cls, id):
        query_result = cls.query.filter_by(id=id).first()
        return query_result

    @classmethod
    def find_by_site_id(cls, id):
        query_result = cls.query.filter_by(site_id=id).all()
        return query_result

    @classmethod
    def return_all(cls):
        query_result = StringSensor.query.all()
        return query_result

    @classmethod
    def delete_all(cls):
        try:
            num_rows_deleted = db.session.query(cls).delete()
            db.session.commit()
            return {'message': '{} row(s) deleted'.format(num_rows_deleted)}
        except:
            return {'message': 'Something went wrong'}

class StringSensorSchema(ma.ModelSchema):
    class Meta:
        model = StringSensor
