import os
import sys
from flask import Flask, request, abort, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    '''
      @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after
      completing the TODOs
      '''

    '''
    @TODO: Use the after_request decorator to set Access-Control-Allow
    '''
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization, true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, PATCH, POST, DELETE, OPTION')
        return response

    '''
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    '''
    @app.route('/categories')
    def getCategories():
        """
        docstring
        """
        categories = Category.query.order_by(Category.id).all()
        formatted_category = [category.format() for category in categories]
        return jsonify({
            "success": True,
            "categories": formatted_category,
            "total_categories": len(categories)
        })

        '''
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.
    '''
    def _paginate(request, selection):
        # Get the requested page number or default to 1
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE
        formatted_questions = [question.format() for question in selection]
        # paginate questions in groups of 10
        paginated_questions = formatted_questions[start:end]
        return paginated_questions

    @app.route('/questions')
    def getQuestions():
        try:
            questions = Question.query.order_by(Question.id).all()
            # category_id = Question.query
            # .join(Category, Category.id == Question.category)
            # .distinct(Question.category)
            # .add_columns(Category.id, Category.type).all()
            categories = Category.query.order_by(Category.id).all()
            category = [category.format() for category in categories]
            # paginate the selected questions
            current_questions = _paginate(request, questions)
            if len(current_questions) == 0:
                abort(400)
            return jsonify({
                "success": True,
                "questions": current_questions,
                "categories": category,
                "total_questions": len(questions)
            })
        except:
            abort(400)

        '''
    @TODO:
    Create an endpoint to DELETE question using a question ID.
    '''
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_questions(question_id):
        try:
            selection = Question.query.filter(
                Question.id == question_id).one_or_none()
            # check if the id exists in the database
            if selection is None:
                abort(404)
            # Persist changes to the database
            selection.delete()
            # Get an updated list of questions after the delete
            updated_questions = Question.query.order_by(Question.id).all()
            # paginate the selected questions
            current_questions = _paginate(request, updated_questions)
            return jsonify({
                "success": True,
                "deleted": selection.id,
                "questions": current_questions,
                "total_questions": len(updated_questions)
            })
        except:
            abort(422)

        '''
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.
    '''
    '''
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.
    '''
    @app.route('/questions', methods=['POST'])
    def create_question():
        # Get the request payload
        body = request.get_json()
        answer = body.get('answer', None)
        question = body.get('question', None)
        category = body.get('category', None)
        difficulty = body.get('difficulty', None)
        search = body.get('searchTerm', None)
        try:
            # check if search term exists
            if search:
                search_question = Question.query.order_by(Question.id).filter(
                    Question.question.ilike('%{}%'.format(search))).all()
                current_questions = _paginate(request, search_question)
                if len(current_questions) == 0:
                    abort(404)
                return jsonify({
                    "success": True,
                    "questions": current_questions,
                    "total_questions": len(search_question),
                })
            else:
                # search term doesn't exist. Proceed to insert the question
                question = Question(answer=answer, question=question,
                                    category=category, difficulty=difficulty)
                # Persist changes to the database
                question.insert()
                # Get an updated list of questions after the insert
                updated_questions = Question.query.order_by(Question.id).all()
                # paginate the selected questions
                current_questions = _paginate(request, updated_questions)
                if len(current_questions) == 0:
                    abort(404)
                return jsonify({
                    "success": True,
                    "created_id": question.id,
                    "questions": current_questions,
                    "total_questions": len(updated_questions),
                })
        except:
            abort(422)

        '''
    @TODO:
    Create a GET endpoint to get questions based on category.
    '''
    @app.route('/categories/<int:cat_id>/questions')
    def questions_by_category(cat_id):
        try:
            question = Question.query.order_by(Question.id).filter(
                Question.category == str(cat_id)).all()
            current_questions = _paginate(request, question)
            if len(current_questions) == 0:
                abort(404)
            return jsonify({
                "success": True,
                "questions": current_questions,
                "total_questions": len(question)
            })
        except:
            abort(404)

        '''
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.
    '''
    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        # Get the request payload
        body = request.get_json()
        previous_questions = body.get('previous_questions', None)
        quiz_category = body.get('quiz_category', None)

        print(quiz_category['id'])
        # check if request payload is empty
        if(quiz_category is None or previous_questions is None):
            abort(404)

        try:
            # The All category has an id that doesnt belong to any category,
            # so we use the type
            if quiz_category['type'] == "click":
                quiz_questions = Question.query.filter(
                    Question.id.notin_(previous_questions)).all()
            else:
                quiz_questions = Question.query.filter(
                    Question.category == str(quiz_category['id'])).filter(
                        Question.id.notin_(previous_questions)).all()

            # paginate the selected questions
            current_questions = _paginate(request, quiz_questions)
            if len(current_questions) == 0:
                abort(404)
            return jsonify({
                "success": True,
                # choose a random question from the list
                "question": random.choice(current_questions),
                "total_questions": len(quiz_questions)
            })
        except:
            abort(404)

        '''
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    '''
    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request"
        }), 400

    return app
