"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint, session
from api.models import db, User, People, Planets, Favorites
from api.utils import generate_sitemap, APIException
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from flask import current_app
from flask import flash, redirect, render_template, \
     request, url_for
api = Blueprint('api', __name__)



@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200

#----------------------SIGN IN, LOG IN, LOG OUT AND AUTHENTICATION TOKEN--------------------------

@api.route('/signup', methods=['POST'])
def create_new_user():
    user_data = request.get_json("User")
    user = User.signup(password=user_data["password"], email=user_data["email"])
    db.session.add(user)
    db.session.commit()

    if user is not None:
        print(user)
        return jsonify({"message":"User created succesfully!"}), 201
    else:
        return jsonify({"message":"Something went wrong, Try again!"}), 500


@api.route('/login', methods=['POST'])
def user_login():
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    print(request.json)
    user = User.query.filter_by(email=email, password=password).one_or_none()
    if user is None:
        return jsonify({"msg": "Something went wrong, please try again!"}), 401
    
    # token
    access_token = create_access_token(identity=user.email)
    return jsonify({ "token": access_token, "user_id": user.id, "email": user.email })

@api.route('/logout', methods=['DELETE'])
def user_logout():
    session.pop("email", None)
    if user is None:
        return jsonify({"msg": " Succesfully Logged out "})
    return redirect(url_for("login")) 
# ------------------GET PEOPLE / PEOPLE ID ||| GET PLANETS / PLANETS ID-----------------------

@api.route('/people', methods=['GET'])
def people_list(): 
    people = People.query.all()
    response_body_people = list(map(lambda s: s.serialize(), people))
    return jsonify(response_body_people), 200

@api.route('/people/<int:id>', methods=['GET'])
def get_people_by_id(id):
    
    people = People.get_people_by_id(id)
    
    return(jsonify(people.serialize()))

@api.route('/planets', methods=['GET'])
def planets(): 
    planets = Planets.query.all()
    response_body_planets = list(map(lambda s: s.serialize(), planets))
    return jsonify(response_body_planets), 200    


@api.route('/planets/<int:id>', methods=['GET'])
def get_planets_by_id(id):
    
    planet = Planets.get_planets_by_id(id)
    
    return(jsonify(planet.serialize()))

#------------------------FAVORITES GET POST AND DELETE---------------------------------

@api.route('/users', methods=['GET'])
def getUsers():
    users = User.query.all()
    response_body_user = list(map(lambda s: s.serialize(), users))
    return jsonify(response_body_user), 200    

@api.route('/users/favorites', methods=['GET'])
def getUserFavorites():
    favorites = Favorites.query.all()
    response_body = list(map(lambda s: s.serialize(), favorites))
    return jsonify(response_body)

@api.route('/users/favorites/planets/<int:planets_id>', methods=['POST'])
def planets_fav():
    planets_fav = Favorites()
    planets_fav.user_id = request.json.get("user_id", None)
    planets_fav.planets_id = request.json.get("planets_id", None)
    db.session.add(planets_fav)
    db.session.commit()
    return jsonify["msg":"Everything went Ok"], 200


@api.route('/users/favorites/people/<int:people_id>', methods=['POST'])
def people_fav():
    people_fav = Favorites()
    people_fav.user_id = request.json.get("user_id", None)
    people_fav_.people_id = request.json.get("people_id",None)
    db.session.add(people_fav)
    db.session.commit()
    return jsonify["msg":"Everything went Ok"], 200


@api.route('/users/favorites/planets/<int:people_id>', methods=['DELETE'])
def deletePlanetsFav(planets_id):
    delete_fav_planets = Favorites.query.get("planet")
    if delete_fav_planets is None: 
        raise APIException('User was not found', status_code=404)
    db.session.delete(delete_fav_planets)
    db.session.commit()
    return jsonify("Succesfully Deleted"), 200 

@api.route('/users/favorites/people/<int:people_id>', methods=['DELETE'])
def deletePeopleFav (people_id ):
    delete_fav_people = Favorites.query.get("people")
    if delete_fav_people is None: 
        raise APIException('User was not found', status_code=404)
    db.session.delete(delete_fav_people)
    db.session.commit()
    return jsonify("Succesfully Deleted"), 200 

#Add People/Planets, Modify People/Planets and delete
#-------------------------PLANETS-----------------------------


@api.route('/planets', methods=['POST'])
def postPlanets():
    request_body_planets = request.get_json()
    new_Planets = Planets() 
    new_Planets.name = request_body_planets["name"]
    new_Planets.affiliation = request_body_planets["affiliation"]
    new_Planets.population = request_body_planets["population"]
    new_Planets.size = request_body_planets["size"]
    db.session.add(new_Planets)
    db.session.commit()
    

    return jsonify(request_body_planets), 200

@api.route('/planets/<int:planets_id>', methods=['PUT'])
def putPlanets(planets_id):
    request_body_planets = request.get_json()
    modify_Planets = Planets.query.get(planets_id)

    if modify_Planets is None:
        raise APIException('No User was found', status_code=404)

    if "name" in request_body_planets:
        modify_Planets.name = request_body_planets["name"]

    if "population" in request_body_planets:
        modify_Planets.population = request_body_planets["population"]

    if "affiliation" in request_body_planets:
        modify_Planets.affiliation = request_body_planets["affiliation"]
    
    if "size" in request_body_planets:
        modify_Planets.size = request_body_planets["size"]

    db.session.commit()

    return jsonify(request_body_planets), 200

@api.route('/planets/<int:planets_id>', methods=['DELETE'])
def deletePlanets(planets_id):
    delete_planets = Planets.query.get(planets_id)
    if delete_planets is None: 
        raise APIException('User was not found', status_code=404)
    db.session.delete(delete_planets)
    db.session.commit()
    return jsonify("Succesfully Deleted"), 200 


#--------------------PEOPLE----------------------------------



@api.route('/people', methods=['POST'])
def postPeople():
    request_body_people = request.get_json()
    new_People = People()
    new_People.full_name = request_body_people["full_name"]
    new_People.affiliation = request_body_people["affiliation"]
    new_People.date_of_birth = request_body_people["date_of_birth"]
    db.session.add(new_People)
    db.session.commit()
    

    return jsonify(request_body_people), 200

@api.route('/people/<int:people_id>', methods=['PUT'])
def putPeople(people_id):
    request_body_people = request.get_json()
    modify_People = People.query.get(people_id)

    if modify_People is None:
        raise APIException('No User was found', status_code=404)

    if "full_name" in request_body_people:
        modify_People.full_name = request_body_people["full_name"]

    if "affiliation" in request_body_people:
        modify_People.affiliation = request_body_people["affiliation"]

    if "date_of_birth" in request_body_people:
        modify_People.date_of_birth = request_body_people["date_of_birth"]

    db.session.commit()

    return jsonify(request_body_people), 200

@api.route('/people/<int:people_id>', methods=['DELETE'])
def deletePeople(people_id):
    delete_people = People.query.get(people_id)
    if delete_people is None: 
        raise APIException('User was not found', status_code=404)
    db.session.delete(delete_people)
    db.session.commit()
    return jsonify("Succesfully Deleted"), 200 

#Add User, Modify User and Delete User

@api.route('/users', methods=['POST'])
def postUser():
    request_body_user = request.get_json("User")
    new_User = User(email=request_body_user["email"], password=request_body_user["password"])
    db.session.add(new_User)
    db.session.commit()

    return jsonify(request_body_user), 200

@api.route('/users/<int:user_id>', methods=['PUT'])
def putUser(user_id):
    request_body_user = request.get_json()
    modify_User = User.query.get(user_id)

    if modify_User is None:
        raise APIException('No User was found', status_code=404)

    if "password" in request_body_user:
        modify_User.password = request_body_user["password"]

    if "email" in request_body_user:
        modify_User.email = request_body_user["email"]

    db.session.commit()

    return jsonify(request_body_user), 200

@api.route('/users/<int:user_id>', methods=['DELETE'])
def deleteUser(user_id):
    delete_User = User.query.get(user_id)
    if delete_User is None: 
        raise APIException('User was not found', status_code=404)
    db.session.delete(delete_User)
    db.session.commit()
    return jsonify("Succesfully Deleted"), 200 