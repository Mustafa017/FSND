import os
import sys
from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from .config import Config
from .models import setup_db, Student, Course, Classroom, Enrollments,\
    Lecturer


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    app.config.from_object(Config)
    db = setup_db(app)
    CORS(app)

    @app.route('/')
    def index():
        return "School Management APP"

    @app.route('/students')
    def get_students():
        try:
            students = db.session.query(
                Student).order_by(Student.std_id).all()

            formatted_std = [student.format for student in students]
            return jsonify({
                "success": True,
                "data": formatted_std,
                "total_students": len(students)
            })
        except Exception:
            raise sys.exc_info()[1]

    return app


# APP = create_app()

# if __name__ == '__main__':
#     APP.run(host='0.0.0.0', port=8080, debug=True)
