from flask import Flask
from flask_cors import CORS
from db_context import db
from api import location_api, measurement_api
from config import Config
from flask_migrate import Migrate
from scheduler import scheduler


def create_app():      
    app = Flask(__name__) 
    app.config.from_mapping(
        SECRET_KEY = "secret_key"
    )     

    app.config.from_object(Config)    
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}}) 

    db.init_app(app)

    scheduler.init_app(app)
    scheduler.start()
    
    app.register_blueprint(measurement_api.measurement_bp)
    app.register_blueprint(location_api.location_bp)
    print("Setup endpoints.")

    from model.measurement import Measurement
    from model.location import Location
    migrate = Migrate(app, db)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port='5000')