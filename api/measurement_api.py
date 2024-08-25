from flask import Blueprint, request, jsonify
from model.measurement import Measurement
from apscheduler.triggers.interval import IntervalTrigger
from service.collect_measurement import generate_measurement
from scheduler import scheduler
import uuid

measurement_bp = Blueprint('measurement', __name__, url_prefix='/measurements')

@measurement_bp.route("/start", methods=["POST"])
def start_scheduler():
    location_id = request.json.get('location_id')
    interval_in_s = request.json.get('interval_in_s')

    if not location_id:
        return jsonify({"message": "location_id is required"}), 400
    
    if not interval_in_s:
        interval_in_s = 90

    # Check if the scheduler job is already running
    if not scheduler.get_job('measurement_job'):
        scheduler.add_job(
            id='measurement_job',
            func=generate_measurement,
            trigger='interval',
            seconds=interval_in_s,
            kwargs={
                'location_id': uuid.UUID(location_id)} 
        )
        return jsonify({"message": "Measuring started"}), 200
    else:
        return jsonify({"message": "Measuring is already running"}), 400


@measurement_bp.route("/stop", methods=["POST"])
def stop_scheduler():
    job = scheduler.get_job('measurement_job')
    if job:
        scheduler.remove_job('measurement_job')
        return jsonify({"message": "Measuring stopped"}), 200
    else:
        return jsonify({"message": "Measuring is not running"}), 400


@measurement_bp.route("/", methods=["GET"])
def get_all_measurements():
    query = Measurement.query

    date_start = request.args.get('date_start')
    date_end = request.args.get('date_end')
    if date_start:
        if date_end:
            query = query.filter(Measurement.date.between(date_start, date_end))
        else:
            query = query.filter(Measurement.date >= date_start)

    time_start = request.args.get('time_start')
    time_end = request.args.get('time_end')
    if time_start:
        if time_end:
            query = query.filter(Measurement.time.between(time_start, time_end))
        else:
            query = query.filter(Measurement.time >= time_start)

    location_id = request.args.get('location_id')
    if location_id:
        query = query.filter_by(location_id=location_id)

    temperature_min = request.args.get('temperature_min')
    temperature_max = request.args.get('temperature_max')
    if temperature_min:
        if temperature_max:
            query = query.filter(Measurement.temperature.between(float(temperature_min), float(temperature_max)))
        else:
            query = query.filter(Measurement.temperature >= float(temperature_min))

    relative_humidity_min = request.args.get('relative_humidity_min')
    relative_humidity_max = request.args.get('relative_humidity_max')
    if relative_humidity_min:
        if relative_humidity_max:
            query = query.filter(Measurement.relative_humidity.between(float(relative_humidity_min), float(relative_humidity_max)))
        else:
            query = query.filter(Measurement.relative_humidity >= float(relative_humidity_min))

    globe_temperature_min = request.args.get('globe_temperature_min')
    globe_temperature_max = request.args.get('globe_temperature_max')
    if globe_temperature_min:
        if globe_temperature_max:
            query = query.filter(Measurement.globe_temperature.between(float(globe_temperature_min), float(globe_temperature_max)))
        else:
            query = query.filter(Measurement.globe_temperature >= float(globe_temperature_min))

    location_id = request.args.get('location_id')
    if location_id:
        query = query.filter_by(location_id=location_id)

    measurements = query.all()

    measurements_list = [{
        'id': measurement.id,
        'date': measurement.date.strftime('%Y-%m-%d'),
        'time': measurement.time.strftime('%H:%M:%S'),
        'altitude': measurement.altitude,
        'longitude': measurement.longitude,
        'latitude': measurement.latitude,
        'temperature': measurement.temperature,
        'relative_humidity': measurement.relative_humidity,
        'globe_temperature': measurement.globe_temperature,
        'wind_speed': measurement.wind_speed,
        'limited_wind_speed': measurement.limited_wind_speed,
        'pm_2_5': measurement.pm_2_5,
        'pm_10': measurement.pm_10,
        'uv_b': measurement.uv_b,
        'location_id': measurement.location_id,
        'location_name': measurement.location.name 
    } for measurement in measurements]

    return jsonify(measurements_list), 200
     
