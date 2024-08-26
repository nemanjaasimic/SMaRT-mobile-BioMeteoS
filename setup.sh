export FLASK_APP=measurementapplication.py
flask db init
flask db migrate
flask db upgrade