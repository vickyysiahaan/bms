from app import db, ma

class Site(db.Model):
    __tablename__ = 'sites'

    id = db.Column(db.Integer, primary_key=True)
    site_name = db.Column(db.String(120), unique=True, nullable=False)
    city = db.Column(db.String(60), nullable=False)
    site_address = db.Column(db.String(120), nullable=False)
    longitude = db.Column(db.Integer, nullable=False)
    latitude = db.Column(db.Integer, nullable=False)
    number_of_string = db.Column(db.Integer, nullable=False)
    total_capacity = db.Column(db.Float, nullable=False)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_sitename(cls, site_name):
        return cls.query.filter_by(site_name=site_name).first()

    @classmethod
    def find_by_site_id(cls, id):
        def to_json(x):
            return {
                'site_name': x.site_name,
                'city': x.city,
                'site_address': x.site_address,
                'longitude': x.longitude,
                'latitude': x.latitude,
                'number_of_string': x.number_of_string,
                'total_capacity': x.total_capacity
            }
        query_result = cls.query.filter_by(id=id).first()
        return to_json(query_result)

    @classmethod
    def return_all(cls):
        def to_json(x):
            return {
                'site_name': x.site_name,
                'city': x.city,
                'site_address': x.site_address,
                'longitude': x.longitude,
                'latitude': x.latitude,
                'number_of_string': x.number_of_string,
                'total_capacity': x.total_capacity
            }
        return {'sites': list(map(lambda x: to_json(x), Site.query.all()))}

    @classmethod
    def delete_all(cls):
        try:
            num_rows_deleted = db.session.query(cls).delete()
            db.session.commit()
            return {'message': '{} row(s) deleted'.format(num_rows_deleted)}
        except:
            return {'message': 'Something went wrong'}

class SiteSchema(ma.Schema):
    class Meta:
        fields = ('id', 'site_name', 'city', 'site_address', 'longitude', 'latitude', 'number_of_string', 'total_capacity')