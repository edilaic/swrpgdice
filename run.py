#!flask/bin/python
from app import app, socketio

socketio.run(app, host='0.0.0.0', port=1138, debug=True)
