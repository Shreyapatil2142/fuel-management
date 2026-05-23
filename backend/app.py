# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from logic import *

app = Flask(__name__)
CORS(app)

#Dashboard Count
@app.route('/api/dashboard', methods=['GET'])
def dashboard_count():
    project_id = request.args.get('project_id')
    result = dashboard(project_id)

    return jsonify(result)


#Vehicles List
@app.route('/api/project_vehicles', methods=['GET'])
def vehicles():
    project_id = request.args.get('project_id')
    result = project_vehicles_list(project_id)

    return jsonify(result)

#Vehicles List
@app.route('/api/vehicles', methods=['GET'])
def vehicleslist():

    result = vehicles_list()

    return jsonify(result)

#Vehicles Details
@app.route('/api/vehicle_details', methods=['GET'])
def vehicle_details():
    vehicle_number = request.args.get('vehicle_number')

    # Validate vehicle_id
    if not vehicle_number:
        return jsonify({'error': 'Vehicle Number is required'}), 400

    result = vehicles_details(vehicle_number)

    if not result:
        return jsonify({'error': 'No data found for the provided Vehicle ID'}), 404

    return jsonify(result)

#All Vehicles Locations
@app.route('/api/vehicles_locations', methods=['GET'])
def vehicles_locations_list():
    vehicle_number = request.args.get('vehicle_number')

    # Validate vehicle_id
    if not vehicle_number:
        return jsonify({'error': 'Vehicle Number is required'}), 400
    result = vehicles_locations(vehicle_number)

    return jsonify(result)

#Route Co-ordinates
@app.route('/api/route_coordinates', methods=['GET'])
def route_coordinate():
    route = request.args.get('route')

    # Validate route
    if not route:
        return jsonify({'error': 'Route Name is required'}), 400

    result = route_coordinates(route)

    if not result:
        return jsonify({'error': 'No data found for the provided Route'}), 404

    return jsonify(result)

#Fuel Transportation Trips
@app.route('/api/trips', methods=['GET'])
def trips_transaction():
    project_id  = request.args.get('project_id')
    start_date  = request.args.get('start_date')
    end_date    = request.args.get('end_date')

    # Validate project_id
    if not project_id:
        return jsonify({'error': 'Project Id is required'}), 400

    result = transactions(project_id,start_date,end_date)

    if not result:
        return jsonify({'error': 'No data found for the provided Period'}), 404

    return jsonify(result)

#IoT Records
@app.route('/api/iotrecords', methods=['GET'])
def iotdevice():
    vehicle_number  = request.args.get('vehicle_number')
    start_date  = request.args.get('start_date')
    end_date    = request.args.get('end_date')

    # Validate vehicle_number
    if not vehicle_number:
        return jsonify({'error': 'Vehicle Number is required'}), 400

    result = iotrecords(vehicle_number,start_date,end_date)

    if not result:
        return jsonify({'error': 'No data found for the provided Period'}), 404

    return jsonify(result)

#Anylitics
@app.route('/api/fuel_shortage', methods=['GET'])
def fuel_shortage_project():

    result = fuel_shortage_project_wise()

    return jsonify(result)

@app.route('/api/project_wise_alerts', methods=['GET'])
def alerts_project():

    result = alerts_project_wise()

    return jsonify(result)

@app.route('/api/project_wise_distance', methods=['GET'])
def distance_project():

    result = distance_project_wise()

    return jsonify(result)

@app.route('/api/vehicle_short_of_fuel', methods=['GET'])
def short_of_fuel():

    result = vehicles_short_of_fuel()

    return jsonify(result)

@app.route('/api/halted_vehicles', methods=['GET'])
def halted_vehicle():

    result = halted_vehicles()

    return jsonify(result)

@app.route('/api/ideal_vehicles', methods=['GET'])
def ideal_vehicle():

    result = ideal_vehicles()

    return jsonify(result)

@app.route('/api/running_vehicles', methods=['GET'])
def running_vehicle():

    result = running_vehicles()

    return jsonify(result)

@app.route('/api/vehicle_report_stats', methods=['GET'])
def vehicle_report():

    result = vehicle_report_stats()

    return jsonify(result)

@app.route('/api/project_wise_fuel_difference', methods=['GET'])
def project_wise_fuel_difference():

    result = project_wise_fuel_diff()

    return jsonify(result)

@app.route('/api/project_wise_fuel_collection', methods=['GET'])
def project_wise_fuel_collection():

    result = project_wise_fuel_coll()

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
