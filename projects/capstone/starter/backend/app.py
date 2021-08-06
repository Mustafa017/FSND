import os
from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from .models import setup_db
from .config import Config


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    app.config.from_object(Config)
    setup_db(app)
    CORS(app)

    @app.route('/')
    def index():
        return 'Hello'

    return app


# APP = create_app()

# if __name__ == '__main__':
#     APP.run(host='0.0.0.0', port=8080, debug=True)
