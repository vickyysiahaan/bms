from app import db, ma

class StringSensor(db.Model):
    __tablename__ = 'string_sensors'

    id = db.Column(db.Integer, primary_key=True)
    string_number = db.Column(db.Integer, nullable=False)
    site_id = db.Column(db.Integer, nullable=False)
    manufacturer = db.Column(db.String(30), nullable=False)
    part_number = db.Column(db.String(30), nullable=False)
    number_of_cells = db.Column(db.Integer, nullable=False)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_site_id(cls, id):
        def to_json(x):
            return {
                'id': x.id,
                'string_number': x.string_number,
                'site_id': x.site_id,
                'manufacturer': x.manufacturer,
                'part_number': x.part_number,
                'number_of_cells': x.number_of_cells
            }
        query_result = cls.query.filter_by(site_id=id).all()
        return {'string_sensors': list(map(lambda x: to_json(x), query_result))}

    @classmethod
    def return_all(cls):
        def to_json(x):
            return {
                'id': x.id,
                'string_number': x.string_number,
                'site_id': x.site_id,
                'manufacturer': x.manufacturer,
                'part_number': x.part_number,
                'number_of_cells': x.number_of_cells
            }
        return {'string_sensors': list(map(lambda x: to_json(x), StringSensor.query.all()))}

    @classmethod
    def delete_all(cls):
        try:
            num_rows_deleted = db.session.query(cls).delete()
            db.session.commit()
            return {'message': '{} row(s) deleted'.format(num_rows_deleted)}
        except:
            return {'message': 'Something went wrong'}

class StringSensorSchema(ma.Schema):
    class Meta:
        fields = ('id', 'string_number', 'site_id', 'manufacturer', 'part_number', 'number_of_cells')
