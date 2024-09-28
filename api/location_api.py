from flask import Blueprint, request, jsonify
from model.location import db, Location


location_bp = Blueprint('location', __name__, url_prefix='/api/locations')


@location_bp.route("/", methods=["GET"])
def get_locations():
    locations = Location.query.all()

    print("Successfully fetched all locations")
    locations_list = [{'id': location.id, 'name': location.name} for location in locations]

    return jsonify(locations_list), 200
     
@location_bp.route("/", methods=["POST"])
def create_location():
    data = request.get_json()

    if 'name' not in data:
        return jsonify({'message': 'The name field is required.'}), 400

    existing_location = Location.query.filter_by(name=data['name']).first()
    if existing_location is not None:
        return jsonify({'message': 'Location with this name already exists.'}), 400
    
    new_location = Location(name=data['name'])
    print(f"Creating new location {new_location.name}")

    db.session.add(new_location)
    db.session.commit()

    return jsonify({'id': new_location.id, 'name': new_location.name}), 201

@location_bp.route('/<location_id>', methods=['DELETE'])
def delete_location(location_id):
    location = Location.query.get(location_id)
    if location is None:
        return jsonify({"message": "Location not found"}), 404

    if location.measurements.count() > 0:
        return jsonify({"message": "Cannot delete location with associated measurements. Delete measurements first."}), 400

    db.session.delete(location)
    db.session.commit()

    return jsonify({"message": "Location deleted successfully"}), 200