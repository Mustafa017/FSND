import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS
from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@DONE uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
# db_drop_and_create_all()

# ROUTES
'''
@DONE implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks}
    where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks')
@requires_auth('get:drinks-detail')
def getDrink():
    drinks = Drink.query.order_by(Drink.id).all()
    format_drinks = [drink.short() for drink in drinks]
    return jsonify({
        "success": True,
        "drinks": format_drinks
    }), 200


'''
@DONE implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks}
    where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def getDrinkDetail():
    allDrinks = Drink.query.order_by(Drink.id).all()
    format_drinks = [drink.long() for drink in allDrinks]
    return jsonify({
        "success": True,
        "drinks": format_drinks
    }), 200


'''
@DONE implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink}
    where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def add_drinks():
    body = request.get_json()
    title = body.get('title', None)
    recipe = body.get('recipe', None)

    if(title is None or recipe is None):
        abort(404)

    if type(recipe) != list:
        recipe = [recipe]

    try:
        drinks = Drink(title=title, recipe=json.dumps(recipe))
        # Persist changes to database
        drinks.insert()
        # Fetch updated drinks
        updated_drinks = Drink.query.order_by(Drink.id).all()
        # Format updated drink
        formatted_drink = [drink.long() for drink in updated_drinks]
        return jsonify({
            "success": True,
            "drinks": formatted_drink
        }), 200
    except Exception as e:
        print(e)
        abort(422)


'''
@DONE implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink}
    where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def updateDrink(id):
    body = request.get_json()
    title = body.get('title', None)
    recipe = body.get('recipe', None)

    if(title is None and recipe is None):
        abort(400)

    try:
        selection = Drink.query.filter(Drink.id == id).one_or_none()
        # check if drink exixts in db
        if (selection is None):
            abort(404)
        if(title):
            selection.title = title

        if(recipe):
            if(type(recipe) != list):
                recipe = [recipe]
            selection.recipe = json.dumps(recipe)

        selection.update()

        updated_drinks = Drink.query.order_by(Drink.id).all()
        formatted_drink = [drink.long() for drink in updated_drinks]
        return jsonify({
            "success": True,
            "drinks": formatted_drink
        }), 200
    except Exception as e:
        print(e)
        abort(422)


'''
@DONE implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id}
    where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def deleteDrink(id):
    selection = Drink.query.filter(Drink.id == id).one_or_none()
    # check if drink exixts in db
    if selection is None:
        abort(404)
    try:
        # Drink exists. Delete and persist changes to db
        selection.delete()
        return jsonify({
            "success": True,
            "delete": selection.id
        }), 200
    except Exception as e:
        print(e)
        abort(422)


# Error Handling
'''
Example error handling for unprocessable entity
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


'''
@DONE implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
'''


@app.errorhandler(400)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "Bad Request"
    }), 400


'''
@Done implement error handler for 404
    error handler should conform to general task above
'''


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404


'''
@DONE implement error handler for AuthError
    error handler should conform to general task above
'''


@app.errorhandler(AuthError)
def authError(error):
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error['description']
    }), error.status_code
