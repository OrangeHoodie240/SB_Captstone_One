from test_setup import db, User, Exercise, Workout, WorkoutDay 
from unittest import TestCase


db.drop_all()
db.create_all()

class TestUser(TestCase):
    
    def tearDown(self):
        User.query.delete() 

    def test_creates_user(self):
        username = 'test-username'
        email = 'test@testemail.com'
        password = 'test-password'
        user = User.register(username, email, password)

        count = User.query.filter(User.username == user.username).count() 
        self.assertEquals(count, 1)


    def test_accepts_valid_login(self):
        username = 'test-username'
        email = 'test@testemail.com'
        password = 'test-password'
        User.register(username, email, password)
        
        is_valid = User.authenticate(username, password)
        self.assertTrue(is_valid)

    def test_rejects_invalid_login(self):
        username = 'test-username'
        email = 'test@testemail.com'
        password = 'test-password'
        User.register(username, email, password)
        
        is_valid = User.authenticate(username + 'extraCharacters', password + 'extraCharacters')
        self.assertFalse(is_valid)


class TestWorkout(TestCase):

    def setUp(self):
        User.register('dogdogdog', 'dog@dog.com', 'dogdogdog')

    def tearDown(self):
        Workout.query.delete()
        User.query.delete()

    def test_creates_workout(self):
        user = User.query.filter(User.username == 'dogdogdog').one() 
        workout = Workout.add('test-workout-name', user.id)
        count = Workout.query.filter(Workout.name == workout.name).count() 
        self.assertEquals(count, 1)



class TestWorkoutDay(TestCase):

    def setUp(self):     
        user = User.register('dogdogdog', 'dog@dog.com', 'dogdogdog')
        Workout.add('test-workout-name', user.id)

    def tearDown(self):
        WorkoutDay.query.delete() 
        Workout.query.delete()
        User.query.delete()

    def test_creates_workoutday(self):
        workout = Workout.query.filter(Workout.name == 'test-workout-name').one()
        day = WorkoutDay.add(workout.id, 'friday')

        count = WorkoutDay.query.filter(WorkoutDay.id == day.id).count() 

        self.assertEquals(count, 1)


    
class TestExercise(TestCase):
    def setUp(self):
        user = User.register('dogdogdog', 'dog@dog.com', 'dogdogdog')
        workout = Workout.add('test-workout-name', user.id)
        WorkoutDay.add(workout.id, 'friday')


    def tearDown(self):
        Exercise.query.delete()
        WorkoutDay.query.delete() 
        Workout.query.delete()
        User.query.delete()

    def test_creates_exercise(self):
        day = WorkoutDay.query.all()[0]
        exercise = Exercise.add(day.id, 191, 4, 12, 'Front Squats')

        count = Exercise.query.filter(Exercise.exercise == exercise.exercise).count()
        self.assertEquals(count, 1) 