from app import db
from flask import request
from flask_restful import Resource
from models.string_sensor import StringSensor, StringSensorSchema
from models.site import Site

string_sensor_schema = StringSensorSchema()
string_sensors_schema = StringSensorSchema(many=True)

class StringSensorListResource(Resource):
    # StringSensor Registration
    def post(self):
        try:
            strings_in_site = StringSensor.find_by_site_id(request.json["site_id"])
            for string in strings_in_site:
                if string.string_number == request.json["string_number"]:
                    return {'message': 'Failed! String Number {} in Site {} already exists'.format(request.json["string_number"], request.json["site_id"])}

            #find site
            site = Site.find_by_site_id(request.json['site_id'])

            new_string_sensor = StringSensor(
                string_number=request.json['string_number'],
                site_id=request.json['site_id'],
                manufacturer=request.json['manufacturer'],
                part_number=request.json['part_number'],
                number_of_cells=request.json['number_of_cells'],
                site = site
            )

            db.session.add(new_string_sensor)
            db.session.commit()

            return {
                'message': 'StringSensor {} was created'.format(new_string_sensor.string_number)
            }

        except:
            raise
            return {'message': 'Something went wrong'}, 500

    # Get All String Sensors
    def get(self):
        site_id = request.args.get("site_id", type=int, default = False)
        if site_id:
            string_sensors = StringSensor.query.filter_by(site_id=site_id).all()
        else:
            string_sensors = StringSensor.query.all()

        return string_sensors_schema.dump(string_sensors)

class StringSensorResource(Resource):
    # Get StringSensor Data by ID
    def get(self, string_sensor_id):
        string_sensor = StringSensor.query.get_or_404(string_sensor_id)
        return string_sensor_schema.dump(string_sensor)

    # Edit StringSensor Data by ID
    def patch(self, string_sensor_id):
        try:
            string_sensor = StringSensor.query.get_or_404(string_sensor_id)

            if 'string_number' in request.json:
                string_sensor.string_number = request.json['string_number']
            if 'manufacturer' in request.json:
                string_sensor.manufacturer = request.json['manufacturer']
            if 'part_number' in request.json:
                string_sensor.part_number = request.json['part_number']
            if 'number_of_cells' in request.json:
                string_sensor.number_of_cells = request.json['number_of_cells']

            db.session.commit()
            return string_sensor_schema.dump(string_sensor)
        except:
            return {'message': 'Something went wrong'}, 500

    # Delete StringSensor Data by ID
    def delete(self, string_sensor_id):
        query_result = StringSensor.query.get_or_404(string_sensor_id)
        db.session.delete(query_result)
        db.session.commit()
        return 'SUCCESSFULL', 204
