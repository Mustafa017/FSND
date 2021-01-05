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
      @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
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

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    '''
    def _paginate(request, selection):
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE
        formatted_questions = [question.format() for question in selection]
        paginated_questions = formatted_questions[start:end]
        return paginated_questions

    @app.route('/questions')
    def getQuestions():
        try:
            questions = Question.query.join(
                Category, Category.id == Question.category).all()
            # category_id = Question.query.join(Category, Category.id == Question.category).distinct(
            #     Question.category).add_columns(Category.id, Category.type).all()
            categories = Category.query.order_by(Category.id).all()
            cat_type = [categories[i].type for i in range(len(categories))]

            current_questions = _paginate(request, questions)
            if len(current_questions) == 0:
                abort(404)
            return jsonify({
                "questions": current_questions,
                "categories": cat_type,
                "total_questions": len(questions)
            })
        except:
            print(sys.exc_info())

        '''
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    '''
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_questions(question_id):
        try:
            selection = Question.query.filter(
                Question.id == question_id).one_or_none()
            if selection is None:
                abort(404)
            selection.delete()
            updated_questions = Question.query.order_by(Question.id).all()
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

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    '''
    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()
        answer = body.get('answer', None)
        question = body.get('question', None)
        category = body.get('category', None)
        difficulty = body.get('difficulty', None)
        search = body.get('searchTerm', None)
        try:
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
                question = Question(answer=answer, question=question,
                                    category=category, difficulty=difficulty)
                question.insert()
                updated_questions = Question.query.order_by(Question.id).all()
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
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    '''

        '''
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    '''

        '''
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    '''

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
        })

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        })

    return app
