from app import db
from flask import request, jsonify
from flask_restful import Resource
from models.cell_sensor import CellSensor, CellSensorSchema
from models.string_sensor import StringSensor

cell_sensor_schema = CellSensorSchema()
cell_sensors_schema = CellSensorSchema(many=True)

class CellSensorListResource(Resource):
    # CellSensor Registration
    def post(self):
        try:
            cells_in_string = CellSensor.find_by_string_id(request.json["string_id"])
            for cell in cells_in_string:
                if cell.cell_number == request.json["cell_number"]:
                    return {'message': 'Failed! String Number {} already exists'.format(request.json["cell_number"])}

            # find string sensor
            string_sensor = StringSensor.find_by_string_id(request.json['string_id'])

            new_cell_sensor = CellSensor(
                cell_number=request.json['cell_number'],
                string_id=request.json['string_id'],
                manufacturer=request.json['manufacturer'],
                part_number=request.json['part_number'],
                stringsensor = string_sensor
            )

            db.session.add(new_cell_sensor)
            db.session.commit()

            return {
                'message': 'CellSensor {} was created'.format(new_cell_sensor.cell_number)
            }

        except:
            return {'message': 'Something went wrong'}, 500

    # Get All Cell Sensors
    def get(self):
        string_id = request.args.get("string_id", type=int, default=False)
        if string_id:
            cell_sensors = CellSensor.query.filter_by(string_id=string_id).all()
        else:
            cell_sensors = CellSensor.query.all()
        output = cell_sensors_schema.dump(cell_sensors)
        return jsonify(output)

class CellSensorResource(Resource):
    # Get CellSensor Data by ID
    def get(self, cell_sensor_id):
        query_result = CellSensor.query.get_or_404(cell_sensor_id)
        output = cell_sensor_schema.dump(query_result)
        return jsonify(output)

    # Edit CellSensor Data by ID
    def patch(self, cell_sensor_id):
        try:
            cell_sensor = CellSensor.query.get_or_404(cell_sensor_id)

            if 'cell_number' in request.json:
                cell_sensor.string_number = request.json['string_number']
            if 'manufacturer' in request.json:
                cell_sensor.manufacturer = request.json['manufacturer']
            if 'part_number' in request.json:
                cell_sensor.part_number = request.json['part_number']

            db.session.commit()
            return cell_sensor_schema.dump(cell_sensor)
        except:
            return {'message': 'Something went wrong'}, 500

    # Delete CellSensor Data by ID
    def delete(self, cell_sensor_id):
        query_result = CellSensor.query.get_or_404(cell_sensor_id)
        db.session.delete(query_result)
        db.session.commit()
        return 'SUCCESSFULL', 204
