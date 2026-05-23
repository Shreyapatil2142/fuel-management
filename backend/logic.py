import pandas as pd

filePath = 'dataset_v2.xlsx'

def dashboard(project_id):
    excel_file = pd.ExcelFile(filePath)

    if project_id is not None:
        project_id = int(project_id)

    df_vehicles = pd.read_excel(excel_file, "vehicles")

    if project_id is not None:
        project_vehicles = df_vehicles[df_vehicles['project_id'] == project_id]
    else:
        project_vehicles = df_vehicles

    # project_vehicles = df_vehicles[df_vehicles['project_id']==project_id]
    vehicles_count = len(project_vehicles.to_dict(orient='records'))

    df_trips = pd.read_excel(excel_file, "trips")
    # project_vehicles_trips = df_trips[df_trips['project_id']==project_id]
    if project_id is not None:
        project_vehicles_trips = df_trips[df_trips['project_id']==project_id]
    else:
        project_vehicles_trips = df_trips
    vehicles_trips_count = len(project_vehicles_trips.to_dict(orient='records'))

    project_vehicles_trips['distance'] = pd.to_numeric(project_vehicles_trips['distance'], errors='coerce')
    project_vehicles_trips = project_vehicles_trips.dropna(subset=['distance'])
    vehicles_total_kms = project_vehicles_trips['distance'].sum()

    project_vehicles_trips['gallons_at_start'] = pd.to_numeric(project_vehicles_trips['gallons_at_start'], errors='coerce')
    project_vehicles_trips = project_vehicles_trips.dropna(subset=['gallons_at_start'])
    gallons_filled = project_vehicles_trips['gallons_at_start'].sum()

    project_vehicles_trips['gallons_at_destination'] = pd.to_numeric(project_vehicles_trips['gallons_at_destination'], errors='coerce')
    project_vehicles_trips = project_vehicles_trips.dropna(subset=['gallons_at_destination'])
    gallons_delivered = project_vehicles_trips['gallons_at_destination'].sum()

    gallons_difference = int(gallons_filled) - int(gallons_delivered)

    df_alerts = pd.read_excel(excel_file, "alerts")
    project_vehicles_alerts = project_vehicles.merge(df_alerts,on="vehicle_number")

    alert_df = project_vehicles_alerts.shape[0]

    running_count = project_vehicles[(project_vehicles["loc_vehicle_status"] == "RUNNING")].shape[0]
    ideal_count = project_vehicles[project_vehicles["loc_vehicle_status"] == "IDEAL"].shape[0]
    halted_count = project_vehicles[project_vehicles["loc_vehicle_status"] == "HALTED"].shape[0]
    nogps = project_vehicles[project_vehicles["gps"] == "No"].shape[0]

    return {
        "total_vehicles": vehicles_count,
        "trips"         : vehicles_trips_count,
        "running"       : running_count,
        "ideal"         : ideal_count,
        "halted"        : halted_count,
        "alerts"        : alert_df,
        "nogps"         : nogps,
        "total_kms"     : int(vehicles_total_kms),
        "gallons_filled" : int(gallons_filled),
        "gallons_delivered" : int(gallons_delivered),
        "gallons_difference" : int(gallons_difference),
    }

def project_vehicles_list(project_id):
    excel_file = pd.ExcelFile(filePath)

    project_id = int(project_id)

    df_vehicles = pd.read_excel(excel_file, "vehicles")

    result_dict = df_vehicles[df_vehicles['project_id']==project_id].to_dict(orient='records')

    return result_dict

def vehicles_list():
    excel_file = pd.ExcelFile(filePath)

    df_vehicles = pd.read_excel(excel_file, "vehicles")

    result_dict = df_vehicles.to_dict(orient='records')

    return result_dict

def vehicles_details(vehicle_number):
    excel_file = pd.ExcelFile(filePath)

    df_vehicles = pd.read_excel(excel_file, "vehicles")

    result_dict = df_vehicles[df_vehicles['vehicle_number']==vehicle_number].to_dict(orient='records')

    return result_dict

def vehicles_locations(vehicle_number):
    excel_file = pd.ExcelFile(filePath)

    df_vehicles = pd.read_excel(excel_file, "vehicles")
    df_locations = pd.read_excel(excel_file, "location_track")

    vehicle_row = df_vehicles[df_vehicles['vehicle_number'] == vehicle_number]

    if vehicle_row.empty:
        return "Vehicle not found"

    route = vehicle_row['route'].values[0]

    route_coordinates = df_locations[df_locations['route'] == route]

    result_dict = route_coordinates.to_dict(orient='records')

    return result_dict

def route_coordinates(route):
    excel_file = pd.ExcelFile(filePath)

    df = pd.read_excel(excel_file, "location_track")

    # Filter data for the provided Vehicle_number
    filtered_df = df[df['route'] == route]

    result_dict = filtered_df.to_dict(orient='records')

    return result_dict

def transactions(project_id,start_date,end_date):
    excel_file = pd.ExcelFile(filePath)
    project_id = int(project_id)

    print(start_date)
    print(end_date)
    df = pd.read_excel(excel_file, "trips")

    df['start_datetime'] = pd.to_datetime(df['start_datetime'])

    print("start_datetime",df["start_datetime"])

    if start_date is None and end_date is None:
        df_filtered = df[df['project_id'] == project_id]
    else:
        df_filtered = df[(df['project_id'] == project_id) & (df['start_datetime'] >= start_date) & (df['start_datetime'] <= end_date)]

    result_dict = df_filtered.to_dict(orient='records')
    return result_dict

def iotrecords(vehicle_number,start_date,end_date):
    excel_file = pd.ExcelFile(filePath)

    print(start_date)
    print(end_date)

    df_iot = pd.read_excel(excel_file, "iot_transactions")

    df_vehicles = pd.read_excel(excel_file, "vehicles")

    df = pd.merge(df_iot, df_vehicles, on='vehicle_number', how='left')

    df['event_time_stamp'] = pd.to_datetime(df['event_time_stamp'])

    print("event_time_stamp",df["event_time_stamp"])

    if start_date is None and end_date is None:
        df_filtered = df[df['vehicle_number'] == vehicle_number]
    else:
        df_filtered = df[(df['vehicle_number'] == vehicle_number) & (df['event_time_stamp'] >= start_date) & (df['event_time_stamp'] <= end_date)]

    result_dict = df_filtered.to_dict(orient='records')
    return result_dict

#Analytics
def fuel_shortage_project_wise():
    excel_file = pd.ExcelFile(filePath)

    df_trips = pd.read_excel(excel_file, "trips")

    grouped_df = df_trips.groupby('project_id')

    results = []

    for project_id, group in grouped_df:
        fuel_shortage = group['gallons_at_start'].sub(group['gallons_at_destination']).sum()
        results.append({'project_id': project_id, 'business_unit': group['bussiness_unit'].tolist()[0], 'fuel_shortage': fuel_shortage, 'gallons_at_start': group['gallons_at_start'].sum(), 'gallons_at_destination': group['gallons_at_destination'].sum()})

    results_df = pd.DataFrame(results)

    result_dict = results_df.to_dict(orient='records')

    return result_dict

def alerts_project_wise():
    excel_file = pd.ExcelFile(filePath)

    df_trips = pd.read_excel(excel_file, "alerts")

    grouped_df = df_trips.groupby('project_id')

    results = []

    for project_id, group in grouped_df:
        alerts = group.shape[0]
        results.append({'project_id': project_id, 'alerts': alerts, 'business_unit': group['bussiness_unit'].tolist()[0]})

    results_df = pd.DataFrame(results)

    result_dict = results_df.to_dict(orient='records')

    return result_dict

def distance_project_wise():
    excel_file = pd.ExcelFile(filePath)

    df_trips = pd.read_excel(excel_file, "trips")

    grouped_df = df_trips.groupby('project_id')

    results = []

    for project_id, group in grouped_df:
        distance = group['distance'].sum()
        results.append({'project_id': project_id, 'distance': distance, 'business_unit': group['bussiness_unit'].tolist()[0]})

    results_df = pd.DataFrame(results)

    result_dict = results_df.to_dict(orient='records')

    return result_dict

def vehicles_short_of_fuel():
    excel_file = pd.ExcelFile(filePath)

    df = pd.read_excel(excel_file, "trips")

    # Filter rows where gallons_at_start is greater than gallons_at_destination
    short_of_fuel_df = df[df['gallons_at_start'] > df['gallons_at_destination']]

    # Group by vehicle_number and count the occurrences
    vehicle_shortage_count = short_of_fuel_df.groupby('vehicle_number').size().reset_index(name='shortage_count')

    print("vehicle_shortage_count",vehicle_shortage_count)

    result_dict = vehicle_shortage_count.to_dict(orient='records')

    return result_dict

def halted_vehicles():
    excel_file = pd.ExcelFile(filePath)

    df = pd.read_excel(excel_file, "alerts")

    # Filter rows where gallons_at_start is greater than gallons_at_destination
    halted = df[df['alert_vehicle_status'] == "HALTED"]

    # Group by vehicle_number and count the occurrences
    halt = halted['vehicle_number'].nunique()

    print("halt",halt)

    result_dict ={"halted_vehicle_count":halt}

    return result_dict

def ideal_vehicles():
    excel_file = pd.ExcelFile(filePath)

    df = pd.read_excel(excel_file, "alerts")

    # Filter rows where gallons_at_start is greater than gallons_at_destination
    idealed = df[df['alert_vehicle_status'] == "IDEAL"]

    # Group by vehicle_number and count the occurrences
    ideal = idealed['vehicle_number'].nunique()

    print("ideal",ideal)

    result_dict = {"idle_vehicle_count":ideal}

    return result_dict

def running_vehicles():
    excel_file = pd.ExcelFile(filePath)

    df = pd.read_excel(excel_file, "alerts")

    # Filter rows where gallons_at_start is greater than gallons_at_destination
    running = df[df['alert_vehicle_status'] == "RUNNING"]

    # Group by vehicle_number and count the occurrences
    run = running['vehicle_number'].nunique()
    print("run",run)

    result_dict = {"run_vehicle_count":run}

    return result_dict

def vehicle_report_stats():
    excel_file = pd.ExcelFile(filePath)

    df = pd.read_excel(excel_file, "alerts")
    # running = df[df['alert_vehicle_status'] == "RUNNING"]
    idle = df[df['alert_vehicle_status'] == "IDEAL"]
    halted = df[df['alert_vehicle_status'] == "HALTED"]

    most_idle = idle.groupby("vehicle_number").count()['alert_vehicle_status'].sort_values().tail(1).index[0]
    most_halted = halted.groupby("vehicle_number").count()['alert_vehicle_status'].sort_values().tail(1).index[0]



    trips_df = pd.read_excel(excel_file, "trips")

    # Filter rows where gallons_at_start is greater than gallons_at_destination
    short_of_fuel_df = trips_df[trips_df['gallons_at_start'] > trips_df['gallons_at_destination']]
    short_of_fuel_df['fuel_diff'] = trips_df['gallons_at_start'] - trips_df['gallons_at_destination']
    highest_fuel_shortage = short_of_fuel_df.groupby("vehicle_number").agg({"fuel_diff":"sum"}).sort_values(by="fuel_diff").tail(1).index[0]

    result_dict = {
                    "most_halted_vehicle":most_halted,
                    "most_idle": most_idle,
                    "vehicle_highest_fuel_shortage":highest_fuel_shortage
                    }
    return result_dict

def project_wise_fuel_diff():
    excel_file = pd.ExcelFile(filePath)

    trips_df = pd.read_excel(excel_file, "trips")

    result_dict = trips_df.groupby("bussiness_unit").agg({"gallons_at_start":"sum","gallons_at_destination":"sum"}).reset_index().to_dict(orient='records')
    result = []
    for i in result_dict:
        i['bussiness_unit'] = i['bussiness_unit']
        i['gallons_at_start'] = int(i['gallons_at_start'])
        i['gallons_at_destination'] = int(i['gallons_at_destination'])
        result.append(i)
    return result

def project_wise_fuel_coll():
    excel_file = pd.ExcelFile(filePath)

    trips_df = pd.read_excel(excel_file, "trips")

    result_dict = trips_df.groupby("bussiness_unit").agg({"gallons_at_start":"sum"}).reset_index().to_dict(orient='records')

    result = []
    for i in result_dict:
        i['bussiness_unit'] = i['bussiness_unit']
        i['gallons_at_start'] = int(i['gallons_at_start'])
        result.append(i)
    return result

