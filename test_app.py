from unittest import TestCase
from flask import session
from app import app, db, Exercise, User, WorkoutDay, Workout

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///test_capstone_1'
app.config['WTF_CSRF_ENABLED'] = False 

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

        with app.test_client() as client: 
            resp = client.post('/users/login', json={'username': user.username, 'password': 'dogdogdog'}, follow_redirects=True)
            user_id = session.get('user_id', None)
            self.assertEquals(user_id, user.id)
            self.assertEquals(resp.status_code, 200)