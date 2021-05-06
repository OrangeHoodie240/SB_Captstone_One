from unittest import TestCase
from flask import session
from app import app, db, Exercise, User, WorkoutDay, Workout

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///test_capstone_1'
app.config['WTF_CSRF_ENABLED'] = False 

db.drop_all()
db.create_all()

class TestApp(TestCase):

    def setUp(self):
        user = User.register('catcatcat', 'cat@cat.com', 'catcatcat')    
        workout = Workout.add(name='Cat Workout', user_id=user.id)
        WorkoutDay.add(workout.id, 'friday')


    def tearDown(self):
        Exercise.query.delete() 
        WorkoutDay.query.delete() 
        Workout.query.delete() 
        User.query.delete() 

    def test_registers_user(self):
        username = 'dogdogdog'
        email = 'dog@dog.com'
        password = 'dogdogdog'

        with app.test_client() as client: 
            resp = client.post('/users/register', json={'username': username, 'email': email, 'password': password}, follow_redirects=True)

            self.assertEquals(resp.status_code, 200)

            results = User.authenticate(username, password)
            self.assertTrue(results)    

    def test_logins_user(self):
        user = User.register('dogdogdog', 'dog@dog.com', 'dogdogdog')

        with app.test_client() as client: 
            resp = client.post('/users/login', json={'username': user.username, 'password': 'dogdogdog'}, follow_redirects=True)
            user_id = session.get('user_id', None)
            self.assertEquals(user_id, user.id)
            self.assertEquals(resp.status_code, 200)

    def test_add_workout(self):
        workout_name = 'Summer Workout'
        user_id = db.session.query(User.id).filter(User.username == 'catcatcat').one()[0]

        with app.test_client() as client:
            with client.session_transaction() as change_session: 
                change_session['user_id'] = user_id
            resp = client.post('/workouts/add', json={'name': workout_name}, follow_redirects=True)

            self.assertEquals(resp.status_code, 200)

            count = Workout.query.filter(Workout.name == workout_name).count()
            self.assertEquals(count, 1)

    def test_add_workoutday(self):
        weekday = 'friday'
        workout_id = db.session.query(Workout.id).filter(Workout.name == 'Cat Workout').one()[0]
        user_id = db.session.query(User.id).filter(User.username  == 'catcatcat').one()[0]

        with app.test_client() as client:
            with client.session_transaction() as change_session: 
                change_session['user_id'] = user_id 
            
            resp = client.post(f'workouts/{workout_id}/days/add', json={'weekday': weekday, 'workout_id': workout_id}, follow_redirects=True)

            self.assertEquals(resp.status_code, 200)
            
            count = WorkoutDay.query.filter((WorkoutDay.workout_id == workout_id) & (WorkoutDay.weekday == weekday)).count() 
            self.assertEquals(count, 1)

    def test_delete_workout(self):
        user_id = db.session.query(User.id).filter(User.username  == 'catcatcat').one()[0]
        workout_id = db.session.query(Workout.id).filter(Workout.name == 'Cat Workout').one()[0]

        with app.test_client() as client: 
            with client.session_transaction() as change_session: 
                change_session['user_id'] = user_id
            
            resp = client.get(f'/workouts/{workout_id}/delete', follow_redirects=True)

            self.assertEquals(resp.status_code, 200)

            count = Workout.query.filter(Workout.id == workout_id).count() 
            self.assertEquals(count, 0)


    def test_delete_workoutday(self):
        user_id = db.session.query(User.id).filter(User.username  == 'catcatcat').one()[0]
        workout_id = db.session.query(Workout.id).filter(Workout.name == 'Cat Workout').one()[0]
        day_id = db.session.query(WorkoutDay.id).filter((WorkoutDay.weekday=='friday') & (WorkoutDay.workout_id == workout_id)).one()[0]

        with app.test_client() as client: 
            with client.session_transaction() as change_session: 
                change_session['user_id'] = user_id
            
            resp = client.get(f'/workouts/{workout_id}/days/{day_id}/delete', follow_redirects=True) 
            
            self.assertEquals(resp.status_code, 200)

            count = WorkoutDay.query.filter((WorkoutDay.weekday=='friday') & (WorkoutDay.workout_id == workout_id)).count() 
            self.assertEquals(count, 0)