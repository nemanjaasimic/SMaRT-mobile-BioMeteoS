from flask import Blueprint, request, jsonify, Response
from sqlalchemy import asc, desc
from model.measurement import Measurement
from model.location import Location
from apscheduler.triggers.interval import IntervalTrigger
from service.collect_measurement import generate_measurement
from scheduler import scheduler
from sensor.data_fetcher import fetch_health_status_values
from datetime import datetime
from io import StringIO
import csv
import uuid

measurement_bp = Blueprint('measurement', __name__, url_prefix='/measurements')

@measurement_bp.route("/start", methods=["POST"])
def start_scheduler():
    data = request.get_json()
    location_id = data['location_id']
    interval_in_s = data['interval_in_s']

    if not location_id:
        return jsonify({"message": "location_id is required"}), 400
    
    existing_location = Location.query.filter_by(id=location_id).first()
    if existing_location is None:
        return jsonify({'error': 'This location does not exist.'}), 400
    
    if not interval_in_s:
        interval_in_s = 90

    print("Trying to schedule measuring job...")
    if not scheduler.get_job('measurement_job'):
        scheduler.add_job(
            id='measurement_job',
            func=generate_measurement,
            trigger='interval',
            seconds=interval_in_s,
            kwargs={
                'location_id': uuid.UUID(location_id)
            } 
        )
        print(f"Measuring job for location id: {location_id} scheduled on {interval_in_s}s interval")
        return jsonify({"message": "Measuring started"}), 200
    else:
        return jsonify({"message": "Measuring is already running"}), 400


@measurement_bp.route("/stop", methods=["POST"])
def stop_scheduler():
    job = scheduler.get_job('measurement_job')
    if job:
        print(f"Measuring job stopped")
        scheduler.remove_job('measurement_job')
        return jsonify({"message": "Measuring stopped"}), 200
    else:
        return jsonify({"message": "Measuring is not running"}), 400


@measurement_bp.route("/", methods=["GET"])
def get_all_measurements():
    query = Measurement.query

    page = request.args.get('page', 1, type=int)
    size = request.args.get('size', 30, type=int)
    sort_by = request.args.get('sort_by', 'date')
    sort_order = request.args.get('sort_order', 'desc')

    date_start = request.args.get('date_start')
    date_end = request.args.get('date_end')
    if date_start:
        if date_end:
            query = query.filter(Measurement.date.between(date_start, date_end))
        else:
            query = query.filter(Measurement.date >= date_start)
    elif date_end:
        query = query.filter(Measurement.date <= date_end)

    time_start = request.args.get('time_start')
    time_end = request.args.get('time_end')
    if time_start:
        if time_end:
            query = query.filter(Measurement.time.between(time_start, time_end))
        else:
            query = query.filter(Measurement.time >= time_start)
    elif time_end:
        query = query.filter(Measurement.time <= time_end)

    temperature_min = request.args.get('temperature_min')
    temperature_max = request.args.get('temperature_max')
    if temperature_min:
        if temperature_max:
            query = query.filter(Measurement.temperature.between(float(temperature_min), float(temperature_max)))
        else:
            query = query.filter(Measurement.temperature >= float(temperature_min))
    elif temperature_max:
        query = query.filter(Measurement.temperature <= temperature_max)

    relative_humidity_min = request.args.get('relative_humidity_min')
    relative_humidity_max = request.args.get('relative_humidity_max')
    if relative_humidity_min:
        if relative_humidity_max:
            query = query.filter(Measurement.relative_humidity.between(float(relative_humidity_min), float(relative_humidity_max)))
        else:
            query = query.filter(Measurement.relative_humidity >= float(relative_humidity_min))
    elif relative_humidity_max:
        query = query.filter(Measurement.relative_humidity <= relative_humidity_max)

    globe_temperature_min = request.args.get('globe_temperature_min')
    globe_temperature_max = request.args.get('globe_temperature_max')
    if globe_temperature_min:
        if globe_temperature_max:
            query = query.filter(Measurement.globe_temperature.between(float(globe_temperature_min), float(globe_temperature_max)))
        else:
            query = query.filter(Measurement.globe_temperature >= float(globe_temperature_min))
    elif globe_temperature_max:
        query = query.filter(Measurement.globe_temperature <= globe_temperature_max)

    location_id = request.args.get('location_id')
    if location_id:
        query = query.filter_by(location_id=location_id)

    if sort_order == 'asc':
        query = query.order_by(asc(getattr(Measurement, sort_by)))
    elif sort_order == 'desc':
        query = query.order_by(desc(getattr(Measurement, sort_by)))
        
    measurements = query.paginate(page=page, per_page=size, error_out=False)

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
    } for measurement in measurements.items]

    return jsonify({
        'total': measurements.total,
        'page': measurements.page,
        'size': measurements.per_page,
        'pages': measurements.pages,
        'has_next': measurements.has_next,
        'has_prev': measurements.has_prev,
        'items': measurements_list
    }), 200


@measurement_bp.route("/export", methods=["GET"])
def get_all_measurements_exported():
    query = Measurement.query

    sort_by = request.args.get('sort_by', 'date')
    sort_order = request.args.get('sort_order', 'desc')

    date_start = request.args.get('date_start')
    date_end = request.args.get('date_end')
    if date_start:
        if date_end:
            query = query.filter(Measurement.date.between(date_start, date_end))
        else:
            query = query.filter(Measurement.date >= date_start)
    elif date_end:
        query = query.filter(Measurement.date <= date_end)

    time_start = request.args.get('time_start')
    time_end = request.args.get('time_end')
    if time_start:
        if time_end:
            query = query.filter(Measurement.time.between(time_start, time_end))
        else:
            query = query.filter(Measurement.time >= time_start)
    elif time_end:
        query = query.filter(Measurement.time <= time_end)

    temperature_min = request.args.get('temperature_min')
    temperature_max = request.args.get('temperature_max')
    if temperature_min:
        if temperature_max:
            query = query.filter(Measurement.temperature.between(float(temperature_min), float(temperature_max)))
        else:
            query = query.filter(Measurement.temperature >= float(temperature_min))
    elif temperature_max:
        query = query.filter(Measurement.temperature <= temperature_max)

    relative_humidity_min = request.args.get('relative_humidity_min')
    relative_humidity_max = request.args.get('relative_humidity_max')
    if relative_humidity_min:
        if relative_humidity_max:
            query = query.filter(Measurement.relative_humidity.between(float(relative_humidity_min), float(relative_humidity_max)))
        else:
            query = query.filter(Measurement.relative_humidity >= float(relative_humidity_min))
    elif relative_humidity_max:
        query = query.filter(Measurement.relative_humidity <= relative_humidity_max)

    globe_temperature_min = request.args.get('globe_temperature_min')
    globe_temperature_max = request.args.get('globe_temperature_max')
    if globe_temperature_min:
        if globe_temperature_max:
            query = query.filter(Measurement.globe_temperature.between(float(globe_temperature_min), float(globe_temperature_max)))
        else:
            query = query.filter(Measurement.globe_temperature >= float(globe_temperature_min))
    elif globe_temperature_max:
        query = query.filter(Measurement.globe_temperature <= globe_temperature_max)

    location_id = request.args.get('location_id')
    if location_id:
        query = query.filter_by(location_id=location_id)


    if sort_order == 'asc':
        query = query.order_by(asc(getattr(Measurement, sort_by)))
    elif sort_order == 'desc':
        query = query.order_by(desc(getattr(Measurement, sort_by)))
    
    measurements = query.all()

    si = StringIO()
    writer = csv.writer(si)
    writer.writerow(['Location', 'Date', 'Time', 'Altitude (m)', 'Longitude', 'Latitude', 't (°C)', 'RH (%)', 'Tg(°C)', 'v (m/s)', 'v [0.5-17] (m/s)', 'PM (2.5) ppm', 'PM (10) ppm', 'UV B (mW/cm^2)'])
    for m in measurements:
        writer.writerow([
            m.location.name if m.location else '',
            m.date.strftime('%Y-%m-%d'),
            m.time.strftime('%H:%M:%S'),
            m.altitude,
            m.longitude,
            m.latitude,
            m.temperature,
            m.relative_humidity,
            m.globe_temperature,
            m.wind_speed,
            m.limited_wind_speed,
            m.pm_2_5,
            m.pm_10,
            m.uv_b
        ])

    si.seek(0)

    today_date = datetime.today().strftime('%Y-%m-%d')
    output = Response(si.getvalue(), mimetype='text/csv')
    output.headers['Content-Disposition'] = f'attachment; filename=measurements_{today_date}.csv'
    output.status_code = 200
    return output

@measurement_bp.route("/status", methods=["GET"])
def get_sensor_status():
    gps_datetime, gps_altitude, gps_altitude_units, gps_longitude, gps_latitude, temp, humidity, globe_temp, wind_speed_m_s, limited_wind_speed_m_s, pm25, pm10, uv_intensity = fetch_health_status_values()

    measurement_status = {
        'date': gps_datetime.date(),
        'time': gps_datetime.time().strftime('%H:%M:%S'),
        'altitude': gps_altitude,
        'longitude': gps_longitude,
        'latitude': gps_latitude,
        'temperature': temp,
        'relative_humidity': humidity,
        'globe_temperature': globe_temp,
        'wind_speed': wind_speed_m_s,
        'limited_wind_speed': limited_wind_speed_m_s,
        'pm_2_5': pm25,
        'pm_10': pm10,
        'uv_b': uv_intensity
    }

    if None not in measurement_status.values():
        return jsonify(measurement_status), 200
    else:
        return jsonify(measurement_status), 400
