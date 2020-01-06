from app import app
from resources import cell_sensor_resources
from flask_restful import Api

api = Api(app)

# CELL SENSOR RESOURCE
api.add_resource(cell_sensor_resources.CellSensorListResource, '/cells')
api.add_resource(cell_sensor_resources.CellSensorResource, '/cells/<int:cell_sensor_id>')