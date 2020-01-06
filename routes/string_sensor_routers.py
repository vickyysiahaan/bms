from app import app
from resources import string_sensor_resources
from flask_restful import Api

api = Api(app)

# STRING SENSOR RESOURCE
api.add_resource(string_sensor_resources.StringSensorListResource, '/strings')
api.add_resource(string_sensor_resources.StringSensorResource, '/strings/<int:string_sensor_id>')