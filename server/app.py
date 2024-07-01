#!/usr/bin/env python3
from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, make_response, jsonify
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)


@app.route("/")
def index():
    return "<h1>Code challenge</h1>"
@app.route('/restaurants')
def restaurants():
    restaurants = [restaurant.to_dict() for restaurant in Restaurant.query.all()]
    response = make_response(jsonify(restaurants), 200)
    return response

@app.route('/restaurants/<int:id>')
def restaurant_by_id(id):
    restaurant = Restaurant.query.filter(Restaurant.id == id).first()
    restaurant_dict = restaurant.to_dict()
    response = make_response(jsonify(restaurant_dict), 200)
    return response

@app.route('/restaurants/<int:id>', methods = ['GET','DELETE'])
def delete_restaurant_by_id(id):
    restaurant = Restaurant.query.filter(Restaurant.id == id).first()

    if restaurant == None:
        response_body = {
            "message": "This record does not exist in our database. Please try again."
        }
        response = make_response(jsonify(response_body), 404)

        return response
    
    
    if request.method == 'GET':
            restaurant_dict = restaurant.to_dict()
            response = make_response(jsonify(restaurant_dict), 200)
            return response
        
    if request.method == 'DELETE':
            db.session.delete(restaurant)
            db.session.commit()

            response_body = {
            "delete_successful": True,
            "message": "Restaurant deleted."
             }

            response = make_response(jsonify(response_body), 200)
            return response
    
@app.route('/pizzas')
def pizzas():
    pizzas = [pizza.to_dict() for pizza in Pizza.query.all()]
    response = make_response(jsonify(pizzas), 200)
    return response

@app.route('/restaurant_pizzas', methods = ['GET','POST'])
def restaurant_pizzas():
    restaurant_pizzas = [restaurant_pizza.to_dict() for restaurant_pizza in RestaurantPizza.query.all()]
    
    if restaurant_pizzas == 'NONE':
        response_body = {
            "errors": ["validation errors"]
        }
        response = make_response(jsonify(response_body), 404)

        return response 
    
    if request.method == 'GET':
            for restaurant_pizza in RestaurantPizza.query.all():
                restaurant_pizza_dict = restaurant_pizza.to_dict()
                response = make_response(jsonify(restaurant_pizza_dict), 200)
                return response
    
    if request.method == 'POST':
        data = request.get_json()
    
        if not data.get('price') or not data.get('pizza_id') or not data.get('restaurant_id'):
            response_body = {
                "errors": ["validation errors"]
            }
            response = make_response(jsonify(response_body), 400)
            return response 
        try:
            new_restaurant_pizza = RestaurantPizza(
                price = data['price'],
                pizza_id = data['pizza_id'],
                restaurant_id = data['restaurant_id']
            )
            db.session.add(new_restaurant_pizza)
            db.session.commit()
            restaurant_pizzas_dict = new_restaurant_pizza.to_dict()
            response = make_response(jsonify(restaurant_pizzas_dict), 201)
            return response 
    
        except Exception as e:
            db.session.rollback()
            response_body = {
                "errors": ["validation errors"]
            }
            response = make_response(jsonify(response_body), 400)
            return response


if __name__ == "__main__":
    app.run(port=5555, debug=True)
    


