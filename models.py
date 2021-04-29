from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from utility import quicksort

bcrypt = Bcrypt()


db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    email = db.Column(db.String(320), nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False, unique=True)
    active_workout = db.Column(db.Integer, nullable=True)
    workouts = db.relationship('Workout')

    @classmethod
    def username_valid(cls, username):
        if len(username) < 8 or len(username) > 18:
            return False

        usercount_count = User.query.filter(User.username == username).count()
        if usercount_count > 0:
            return False

        return True

    @classmethod
    def email_valid(cls, email):
        if len(email) < 3:
            return False

        email_count = User.query.filter(User.email == email).count()
        if email_count > 0:
            return False

        return True

    @classmethod
    def password_valid(cls, password):
        if(len(password) > 8 and len(password) < 25):
            return True

        return False

    @classmethod
    def register(cls, username, email, password):
        if not User.username_valid(username) or not User.email_valid(email) or not User.password_valid(password):
            return None

        pass_hash = bcrypt.generate_password_hash(password, 14)
        user = User(username=username, email=email,
                    password=pass_hash.decode('utf-8'))

        db.session.add(user)
        db.session.commit()

        return user

    @classmethod
    def get(cls, username, password):
        if User.authenticate(username, password):
            return User.query.filter(User.username == username).one()

        return None

    @classmethod
    def authenticate(cls, username, password):
        user = User.query.filter(User.username == username).one_or_none()
        if user is None:
            return None

        pass_valid = bcrypt.check_password_hash(user.password, password)
        if pass_valid:
            return user
        else:
            return None

    @classmethod
    def delete(cls, username, password):
        if User.authenticate(username, password):

            user = User.query.filter(User.username == username).one()
            Workout.delete_all(user.id)

            User.query.filter(User.username == username).delete()
            db.session.commit()
            return True
        else:
            return False

    @classmethod
    def update(cls, username, password, new_username=None, new_email=None, new_password=None):
        if(not User.authenticate(username, password)):
            return None

        user = User.query.filter(User.username == username).one()
        if(new_username and User.username_valid(new_username)):
            user.username = new_username

        if(new_email and User.email_valid(new_email)):
            user.email = new_email

        if(new_password and User.password_valid(new_password)):
            pass_hash = bcrypt.generate_password_hash(new_password, 14)
            user.password = pass_hash.decode('utf-8')

        db.session.commit()
        return user


class Workout(db.Model):

    __tablename__ = 'workouts'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(30), nullable=False)
    user = db.relationship('User')
    days = db.relationship('WorkoutDay')

    @classmethod
    def add(cls, name, user_id):
        count = Workout.query.filter((Workout.name == name) & (
            Workout.user_id == user_id)).count()
        if(count > 0):
            return None
        workout = Workout(name=name, user_id=user_id)
        db.session.add(workout)
        db.session.commit()

        if Workout.query.filter(Workout.user_id == user_id).count() == 1:
            user = User.query.get(user_id)
            user.active_workout = workout.id
            db.session.commit()

        return workout

    @classmethod
    def delete(cls, id):
        query = Workout.query.filter(Workout.id == id)
        workout = query.one_or_none()
        if workout is None:
            return False

        WorkoutDay.delete_all(workout.id)

        user = User.query.get(workout.user_id)
        if user.active_workout == workout.id:
            workouts = Workout.query.filter(
                (Workout.user_id == user.id) & (Workout.id != workout.id)).all()
            if len(workouts) > 0:
                user.active_workout = workouts[0].id

        query.delete()
        db.session.commit()

        return True

    @classmethod
    def delete_all(cls, user_id):
        workouts = Workout.query.filter(Workout.user_id == user_id).all()

        for workout in workouts:
            Workout.delete(workout.id)

        return True

    @classmethod
    def update(cls, id, new_name):
        workout = Workout.query.get(id)
        count = Workout.query.filter((Workout.name == new_name) & (
            Workout.user_id == workout.user_id)).count()
        if(count > 0):
            return None

        workout.name = new_name
        db.session.commit()

        return workout

    @classmethod
    def get(cls, id):
        return Workout.query.get(id)

    @classmethod
    def available_days(cls, id):
        days = db.session.query(WorkoutDay.weekday).filter(
            WorkoutDay.workout_id == id).all()
        days = {day for tup in days for day in tup}
        days = days.symmetric_difference(
            {'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'})
        return list(days)

    @classmethod
    def get_for(cls, user_id):
        return Workout.query.filter(Workout.user_id == user_id).all()


class WorkoutDay(db.Model):
    __tablename__ = 'workout_days'
    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey(
        'workouts.id'), nullable=False)
    weekday = db.Column(db.String(9), nullable=False)
    workout = db.relationship('Workout')
    exercises = db.relationship('Exercise')

    @classmethod
    def sortedExercises(cls, day_id):
        day = WorkoutDay.get(id)
        return quicksort(day.exercises, attr='order')

    @classmethod
    def add(cls, workout_id, weekday):
        weekday = weekday.lower()
        if weekday not in ('saturday', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday'):
            return None

        count_weekday = WorkoutDay.query.filter(
            (WorkoutDay.weekday == weekday) & (WorkoutDay.workout_id == workout_id)).count()
        if count_weekday > 0:
            return None

        day = WorkoutDay(workout_id=workout_id, weekday=weekday)
        db.session.add(day)
        db.session.commit()

        return day

    @classmethod
    def delete(cls, id):
        query = WorkoutDay.query.filter(WorkoutDay.id == id)
        day = query.one_or_none()

        if day is None:
            return False

        Exercise.delete_all(day.id)

        query.delete()
        db.session.commit()

        return True

    @classmethod
    def delete_all(cls, workout_id):
        workout_days = WorkoutDay.query.filter(
            WorkoutDay.workout_id == workout_id).all()
        for day in workout_days:
            WorkoutDay.delete(day.id)

        return True

    @classmethod
    def update(cls, id, new_weekday):
        new_weekday = new_weekday.lower()
        weekdays = {'saturday', 'sunday', 'monday',
                    'tuesday', 'wednesday', 'thursday', 'friday'}
        if new_weekday not in weekdays:
            return None

        day = WorkoutDay.query.filter(WorkoutDay.id == id).one()

        taken_days = db.session.query((WorkoutDay.weekday).filter(
            WorkoutDay.id == id) & (WorkoutDay.weekday != day.weekday)).all()
        taken_days = {day for tup in taken_days for day in tup}
        if new_weekday in taken_days:
            return None

        day.weekday = new_weekday
        db.session.commit()

        return day

    @classmethod
    def get(cls, id):
        return WorkoutDay.query.filter(WorkoutDay.id == id).one_or_none()

    @classmethod
    def get_workout(clss, id):
        return Workout.query.get(id)

    @classmethod
    def get_serialized_exercises(cls, id):
        exercises = Exercise.query.filter(Exercise.workout_day_id == id).all()
        exercises = quicksort(exercises, 'order')
        serialized_exercises = []
        for ex in exercises:
            serialized_exercises.append(Exercise.serialize(ex))
        return serialized_exercises


class Exercise(db.Model):

    __tablename__ = 'exercises'
    id = db.Column(db.Integer, primary_key=True)
    workout_day_id = db.Column(db.Integer, db.ForeignKey(
        'workout_days.id'), nullable=False)
    exercise = db.Column(db.Integer, nullable=False)
    sets = db.Column(db.Integer, db.CheckConstraint(
        'sets > 0', 'sets < 51'), nullable=False)
    reps = db.Column(db.Integer, db.CheckConstraint(
        'reps > 0', 'reps < 51'), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    order = db.Column(db.Integer, nullable=False)
    day = db.relationship('WorkoutDay')

    __table_args__ = (db.UniqueConstraint('workout_day_id', 'order'),)

    @classmethod
    def all_for(cls, day_id):
        exercise_ids = db.session.query(Exercise.id).filter(
            Exercise.workout_day_id == day_id).all()
        exercise_ids = [id for tup in exercise_ids for id in tup]
        return exercise_ids

    @classmethod
    def add(cls, workout_day_id, exercise, sets, reps, name):
        exercise_count = Exercise.query.filter(
            Exercise.exercise == exercise).count()
        if exercise_count > 0:
            return None

        order = Exercise.query.filter(
            Exercise.workout_day_id == workout_day_id).count() + 1

        exer_obj = Exercise(workout_day_id=workout_day_id,
                            exercise=exercise, sets=sets, reps=reps, name=name, order=order)
        db.session.add(exer_obj)
        db.session.commit()
        return exer_obj

    @classmethod
    def delete(cls, id):
        query = Exercise.query.filter(Exercise.id == id)

        exer_obj = query.one_or_none()
        if exer_obj is None:
            return False

        query.delete()
        db.session.commit()
        return True

    @classmethod
    def delete_all(cls, workout_day_id):
        exercises = Exercise.query.filter(
            Exercise.workout_day_id == workout_day_id).all()
        for ex in exercises:
            Exercise.delete(ex.id)

    @classmethod
    def get(cls, id):
        return Exercise.query.get(id)

    @classmethod
    def update(cls, id, sets=None, reps=None):
        exercise = Exercise.get(id)

        if sets is not None:
            exercise.sets = sets

        if reps is not None:
            exercise.reps = reps

        db.session.commit()

        return exercise

    @classmethod
    def serialize(cls, ex):
        api_id = ex.exercise
        name = ex.name
        reps = ex.reps
        sets = ex.sets
        order = ex.order

        return {'id': ex.id, 'exercise': api_id, 'name': name, 'reps': reps, 'sets': sets, 'order': order}

    @classmethod
    def move_up(cls, id):
        ex = Exercise.get(id)
        if ex.order > 1:
            ex2 = Exercise.query.filter((Exercise.workout_day_id == ex.workout_day_id) & (
                Exercise.order == ex.order - 1)).one()
            ex.order = 999999
            db.session.commit()

            ex2.order += 1
            db.session.commit()

            ex.order = ex2.order - 1
            db.session.commit()
        return ex

    @classmethod
    def move_down(cls, id):
        ex = Exercise.get(id)
        exercises = Exercise.query.filter(
            Exercise.workout_day_id == ex.workout_day_id).all()
        if len(exercises) > ex.order:
            ex2 = [ex2 for ex2 in exercises if ex2.order == ex.order + 1][0]
            ex.order = 999999
            db.session.commit()

            ex2.order -= 1
            db.session.commit()

            ex.order = ex2.order + 1
            db.session.commit()
        return ex
