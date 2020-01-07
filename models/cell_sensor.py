from app import db, ma

class CellSensor(db.Model):
    __tablename__ = 'cell_sensors'

    id = db.Column(db.Integer, primary_key=True)
    cell_number = db.Column(db.Integer, nullable=False)
    string_id = db.Column(db.Integer, db.ForeignKey('string_sensor.id'))
    manufacturer = db.Column(db.String(30), nullable=False)
    part_number = db.Column(db.String(30), nullable=False)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_string_id(cls, id):
        query_result = cls.query.filter_by(string_id=id).all()
        return query_result

    @classmethod
    def return_all(cls):
        query_result = CellSensor.query.all()
        return query_result

    @classmethod
    def delete_all(cls):
        try:
            num_rows_deleted = db.session.query(cls).delete()
            db.session.commit()
            return {'message': '{} row(s) deleted'.format(num_rows_deleted)}
        except:
            return {'message': 'Something went wrong'}

class CellSensorSchema(ma.ModelSchema):
    class Meta:
        model = CellSensor
