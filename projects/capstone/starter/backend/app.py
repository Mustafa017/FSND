from logging import error
import os
import sys
from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from flask_migrate import current
import config
from auth.auth import AuthError, authorize_user
from models import setup_db, Student, Course, Classroom, Enrollments,\
    Lecturer


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    app.config.from_object(config.Config)
    db = setup_db(app)
    CORS(app)

    @app.route('/')
    def index():
        return "Course Management APP"

    #---------------------------------------------------------#
    # Students
    #---------------------------------------------------------#

    @app.route('/students')
    @authorize_user('get:data')
    def get_students():
        items_limit = request.args.get('limit', 3, type=int)
        page_num = request.args.get('page', 1, type=int)
        current_index = page_num - 1
        error = False

        try:
            students = db.session.query(Student).order_by(Student.std_id).limit(
                items_limit).offset(items_limit * current_index).all()

            formatted_std = [student.format for student in students]

        except Exception:
            error = True
            print(sys.exc_info())

        if error:
            abort(404)
        else:
            return jsonify({
                "success": True,
                "data": formatted_std,
                "total_students": len(formatted_std)
            })

    @app.route('/students/<int:student_id>')
    @authorize_user('get:data')
    def get_student_by_id(student_id):
        error = False

        try:
            student = db.session.query(Student).filter(
                Student.std_id == student_id).one_or_none()

            format_student = student.format
        except Exception:
            error = True
            print(sys.exc_info())

        if error:
            abort(404)
        else:
            return jsonify({
                "success": True,
                "student": format_student,
            })

    @app.route('/students/create', methods=['POST'])
    @authorize_user('post:data')
    def create_student():
        body = request.get_json()
        std_fname = body.get('fname')
        std_lname = body.get('lname')
        std_email = body.get('email')
        std_dob = body.get('dob')
        std_gender = body.get('sex')
        std_regno = int(body.get('regno'))

        error = False

        try:
            # instantiate student object
            std = Student(std_regno, std_fname, std_lname,
                          std_email, std_dob, std_gender)
            std.insert()
            students = Student.query.order_by(Student.std_id).all()
            students_list = [student.format for student in students]

        except Exception as e:
            db.session.rollback()
            error = True
            print(sys.exc_info())
        finally:
            db.session.close()

        if error:
            abort(422)
        else:
            return jsonify({
                'success': True,
                'created': std.std_id,
                'students': students_list,
                'total': len(students)
            })

    @app.route('/students/<int:student_id>', methods=['PATCH'])
    @authorize_user('patch:data')
    def update_students(student_id):
        body = request.get_json()

        if body:
            fname = body.get('fname')
            lname = body.get('lname')
            regno = body.get('regno')
            email = body.get('email')
        else:
            abort(400)

        error = False

        try:
            std = db.session.get(Student, student_id)
            std.std_fname = fname
            std.std_lname = lname
            std.std_regno = regno
            std.std_email = email
            std.update()
        except Exception as e:
            db.session.rollback()
            error = True
            print(sys.exc_info())

        if error:
            abort(422)
        else:
            return jsonify({
                'success': True,
                'student_id': std.std_id
            })

    @app.route('/students/<int:student_id>', methods=['DELETE'])
    @authorize_user('delete:data')
    def delete_students(student_id):
        error = False

        try:
            std = db.session.get(Student, student_id)
            std.delete()

            updated_students = Student.query.order_by(Student.std_id).all()
            formatted_students = [
                student.format for student in updated_students]
        except Exception as e:
            db.session.rollback()
            print(e)
        finally:
            db.session.close()

        if error:
            abort(404)
        else:
            return jsonify({
                'success': True,
                'deleted': std.std_id,
                'students': formatted_students,
                'total_courses': len(updated_students)
            })

    #---------------------------------------------------------#
    # Courses
    #---------------------------------------------------------#

    @app.route('/courses')
    @authorize_user('get:data')
    def getCourses():
        error = False

        try:
            courses = db.session.query(Course).order_by(Course.crs_id).all()
            format_courses = [course.format for course in courses]

        except Exception:
            error = True
            print(sys.exc_info())
        finally:
            db.session.close()

        if error:
            abort(404)
        else:
            return jsonify({
                "success": True,
                "courses": format_courses,
                "total": len(courses)
            })

    @app.route('/courses/create', methods=['POST'])
    @authorize_user('post:data')
    def create_courses():
        body = request.get_json()
        crs_title = body.get('title')
        crs_code = body.get('code')
        crs_desc = body.get('desc')
        crs_book = body.get('book')
        crs_lec = int(body.get('lec'))
        crs_room = int(body.get('room'))

        error = False

        try:
            # instantiate course object
            crs = Course(crs_code, crs_title, crs_desc,
                         crs_book, crs_lec, crs_room)
            crs.insert()
            courses = Course.query.order_by(Course.crs_id).all()
            courses_list = [course.format for course in courses]

        except Exception as e:
            db.session.rollback()
            error = True
            print(sys.exc_info())
        finally:
            db.session.close()

        if error:
            abort(422)
        else:
            return jsonify({
                'success': True,
                'created': crs.crs_id,
                'courses': courses_list,
                'total': len(courses)
            })

    @app.route('/courses/<int:course_id>', methods=['PATCH'])
    @authorize_user('patch:data')
    def update_courses(course_id):
        body = request.get_json()

        if body:
            title = body.get('title')
            book = body.get('book')
        else:
            abort(400)

        error = False

        try:
            crs = db.session.get(Course, course_id)
            crs.crs_title = title
            crs.crs_book = book
            crs.update()
        except Exception as e:
            db.session.rollback()
            error = True
            print(sys.exc_info())

        if error:
            abort(422)
        else:
            return jsonify({
                'success': True,
                'course_id': crs.crs_id
            })

    @app.route('/courses/<int:course_id>', methods=['DELETE'])
    @authorize_user('delete:data')
    def delete_courses(course_id):
        error = False

        try:
            crs = db.session.get(Course, course_id)
            crs.delete()

            updated_courses = Course.query.order_by(Course.crs_id).all()
            formatted_courses = [course.format for course in updated_courses]
        except Exception as e:
            db.session.rollback()
            print(e)
        finally:
            db.session.close()

        if error:
            abort(422)
        else:
            return jsonify({
                'success': True,
                'deleted id': crs.crs_id,
                'courses': formatted_courses,
                'total_courses': len(updated_courses)
            })

    @app.errorhandler(AuthError)
    def authError(error):
        return jsonify({
            'success': False,
            'error': error.status_code,
            'message': error.error['description']
        }), error.status_code

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "Success": False,
            "error": 400,
            "message": "Bad Request"
        }), 400

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
