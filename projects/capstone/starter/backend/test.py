from unittest import TestCase
import unittest

from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import *
import json
from pprint import pprint


class CourseTestSuite(TestCase):
    def setUp(self) -> None:
        self.app = create_app(test_config=True)
        self.client = self.app.test_client
        self.new_course = {
            "title": "Working with teams",
            "code": "SPT543",
            "desc": "It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using 'Content here, content here', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for 'lorem ipsum' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).",
            "book": "The Boys in the Boat",
            "lec": 2,
            "room": 3
        }
        self.new_student = {
            "dob": "05/06/1997",
            "email": "abmusti@gmail.com",
            "fname": "Leonard",
            "lname": "Hofstead",
            "regno": 2543,
            "sex": "male"
        }

        # with self.app.app_context():
        #     self.db = SQLAlchemy()
        #     self.db.init_app(self.app)

    def tearDown(self) -> None:
        return super().tearDown()

    def test_get_students(self):
        req = self.client().get('/students')
        data = json.loads(req.data)

        self.assertEqual(req.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total'])
        self.assertTrue(len(data['students']))

    def test_create_student(self):
        req = self.client().post('/students/create', json=self.new_student)
        data = json.loads(req.data)

        self.assertEqual(req.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(data['total'])
        self.assertTrue(len(data['students']))

    def test_fail_create_student(self):
        req = self.client().post('/students/create', json=self.new_student)
        data = json.loads(req.data)

        self.assertEqual(req.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_update_student(self):
        req = self.client().patch(
            '/students/4', json={"email": "mkhamisi@rocketmail.com"})
        data = json.loads(req.data)
        std = Student.query.filter(Student.std_id == 4).one_or_none()

        self.assertEqual(req.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['student_id'], 4)
        self.assertEqual(std.format['student_email'],
                         "mkhamisi@rocketmail.com")

    def test_fail_update_student(self):
        req = self.client().patch('/students/4', json={"regno": 5263})
        data = json.loads(req.data)

        self.assertEqual(req.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_delete_student(self):
        req = self.client().delete('/students/20')
        data = json.loads(req.data)
        student = Student.query.filter(Student.std_id == 19).one_or_none()

        self.assertEqual(req.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 19)
        self.assertTrue(data['students'])
        self.assertTrue(len(data['students']))
        self.assertEqual(student, None)

    # ----------------------------------------------------
    # Courses
    # ----------------------------------------------------

    def test_get_Courses(self):
        req = self.client().get('/courses')
        data = json.loads(req.data)

        self.assertEqual(req.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total'])
        self.assertTrue(len(data['courses']))

    def test_create_course(self):
        req = self.client().post('/courses/create', json=self.new_course)
        data = json.loads(req.data)

        self.assertEqual(req.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(data['total'])
        self.assertTrue(len(data['courses']))

    def test_fail_create_course(self):
        req = self.client().post('/courses/create', json=self.new_course)
        data = json.loads(req.data)

        self.assertEqual(req.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_update_course(self):
        req = self.client().patch(
            '/courses/52', json={"title": "Web Marketing", "book": "Digital Web analytics"})
        data = json.loads(req.data)
        crs = Course.query.filter(Course.crs_id == 52).one_or_none()

        self.assertEqual(req.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['course_id'], 52)
        self.assertEqual(crs.format['course_title'], "Web Marketing")
        self.assertEqual(crs.format['course_book'], "Digital Web analytics")

    def test_fail_update_course(self):
        req = self.client().patch(
            '/courses/4', json={"desc": 'interesting Course'})
        data = json.loads(req.data)

        self.assertEqual(req.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_delete_course(self):
        req = self.client().delete('/courses/54')
        data = json.loads(req.data)
        crs = Course.query.filter(Course.crs_id == 53).one_or_none()

        self.assertEqual(req.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted_id'], 53)
        self.assertTrue(data['courses'])
        self.assertTrue(len(data['courses']))
        self.assertEqual(crs, None)


if __name__ == '__main__':
    unittest.main()
