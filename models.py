from flask_sqlalchemy import SQLAlchemy



db = SQLAlchemy() 

def connect_db(app):
    db.app = app 
    db.init_app(app)

class User(db.Model):

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False, unique=True) 
    email = db.Column(db.String(30), nullable=False, unique=True) 
    password = db.Column(db.String(30), nullable=False, unique=True) 
    active_workout = db.Column(db.Integer, nullable=True) 


class Workout(db.Model):

    __tablename__ = 'workouts'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    workout_name = db.Column(db.String(30), nullable = False)


class WorkoutDay(db.Model):
    __tablename__ = 'workout_days'
    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'), nullable=False)
    weekday = db.Column(db.String(9), nullable=False)

class Exercise(db.Model):

    __tablename__ = 'exercises'
    id = db.Column(db.Integer, primary_key=True)
    workout_day_id = db.Column(db.Integer, db.ForeignKey('workout_days.id'), nullable=False)
    exercise = db.Column(db.Integer, nullable=False)
    sets = db.Column(db.Integer, db.CheckConstraint('sets > 0', 'sets < 51'), nullable=False)
    reps = db.Column(db.Integer, db.CheckConstraint('reps > 0','reps < 51'), nullable=False)

    