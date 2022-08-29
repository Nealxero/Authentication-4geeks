from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=True)
    #favorites = db.relationship("Favorites")


    def __repr__(self):
        return '<User %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

    @classmethod
    def signup(cls, email, password):
        instance = cls(
            email=email,
            password=password
        )
        if isinstance(instance, cls):
            return instance
        else:
            return None

    @classmethod
    def login(cls, email, password):
        user_data = cls.query.filter_by(
            email=email
        ).one_or_none()
        if (not isinstance(user_data, cls)):
            return user_data
        if user_data.password == password:
            return user_data
        else:
            return False

class People(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(250), nullable=False)
    affiliation = db.Column(db.String(250), nullable=False)
    date_of_birth = db.Column(db.String(250), nullable=False)
    
    def __repr__(self):
        return '<People %r>' % self.id

    def serialize(self):
        return {
           "id": self.id,
           "full_name": self.full_name
        }
    @classmethod
    def get_people_by_id(cls, id):
        people_by_id = cls.query.filter_by(id = id).one_or_none()
        return people_by_id

class Planets(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    affiliation = db.Column(db.String(250), nullable=False)
    population = db.Column(db.String(250), nullable=False)
    size = db.Column(db.String(250), nullable=False)
        
    def __repr__(self):
        return '<Planets %r>' % self.name

    def serialize(self):
        
        return {
            "id": self.id,
            "population": self.population,
            "name": self.name
        }
        
    @classmethod
    def get_planets_by_id(cls, id):
        planets_by_id = cls.query.filter_by(id = id).one_or_none()
        return planets_by_id

class Favorites(db.Model):
   
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'))
    planets_id = db.Column(db.Integer, db.ForeignKey('planets.id'))
    user = db.relationship("User")
    people = db.relationship('People')
    planet = db.relationship('Planets')
    def __repr__(self):
        return '<Favorites %r>' % self.id

    def serialize(self):
       
        return {
            "id": self.id,
            "user_id":self.user_id,
            "planet": self.planets_id,
            "people": self.people_id,
        }