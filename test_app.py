from unittest import TestCase
from app import app, db, Exercise, User, WorkoutDay, Workout

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///test_capstone_1'

db.drop_all()
db.create_all()

class TestApp(TestCase):
    

    def tearDown(self):
        Exercise.query.delete() 
        WorkoutDay.query.delete() 
        Workout.query.delete() 
        User.query.delete() 

    

    def test_logins_user(self):
        user = User.register('dogdogdog', 'dog@dog.com', 'dogdogdog')
