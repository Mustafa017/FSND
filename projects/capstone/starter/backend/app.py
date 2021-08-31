import os
import sys
from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from flask_migrate import current
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
        items_limit = request.args.get('limit', 3, type=int)
        page_num = request.args.get('page', 1, type=int)
        current_index = page_num - 1
        try:
            students = db.session.query(Student).order_by(Student.std_id).limit(
                items_limit).offset(items_limit * current_index).all()

            if students == 'undefined':
                abort(404)
            else:
                formatted_std = [student.format for student in students]
                return jsonify({
                    "success": True,
                    "data": formatted_std,
                    "total_students": len(formatted_std)
                })
        except Exception:
            raise sys.exc_info()[1]

    @app.route('/students/<int:student_id>')
    def get_student_by_id(student_id):
        try:
            student = db.session.query(Student).filter(
                Student.std_id == student_id).one_or_none()
            if student is None:
                abort(404)
            else:
                format_student = student.format
                return jsonify({
                    "success": True,
                    "student": format_student,
                })
        except Exception:
            raise sys.exc_info()[1]

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "Success": False,
            "error": 404,
            "message": "Resource Not Found"
        }), 404

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "Success": False,
            "error": 500,
            "message": "Internal Server error"
        }), 500

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "Success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    return app


APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
