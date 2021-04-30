from flask import Flask, jsonify, request, flash, redirect, render_template, session, Response
from models import db, connect_db, User, Workout, WorkoutDay, Exercise
import os
import requests
from forms import RegisterForm, LoginForm, WorkoutForm, DayForm
from utility import find_closest_workout, quicksort

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('ENV_VAR_NAME', 'something secrety here')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'ENV_VAR_NAME', 'postgresql:///capstone_1')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True


connect_db(app)


@app.route('/')
def index():
    if 'user_id' in session:
        user = User.query.filter(User.id == session.get('user_id')).one()
        if user.active_workout is not None:
            workout = Workout.get(user.active_workout)
            day = find_closest_workout(workout)
            return render_template('index.html', day=day)

    return render_template('index.html', day=None)


@app.route('/users/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.authenticate(username, password)
        if user is not None:
            session['user_id'] = user.id
            flash('Logged In')
            return redirect('/')
        else:
            flash('Invalid Username/Password Combination')

    return render_template('login.html', form=form)


@app.route('/users/logout')
def logout():
    if 'user_id' not in session:
        return redirect('/')

    del session['user_id']
    flash("Logged out")
    return redirect('/')


@app.route('/users/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect('/')

    form = RegisterForm()

    if form.validate_on_submit():
        user = User.register(form.username.data,
                             form.email.data, form.password.data)
        if user is not None:
            flash('Account created')
            return redirect('/')
        else:
            if not User.username_valid(form.username.data):
                flash('Username unavailable')
            else:
                flash('Email taken')

    return render_template('register.html', form=form)


@app.route('/workouts/add', methods=['GET', 'POST'])
def add_workout():
    if 'user_id' not in session:
        return redirect('/')

    form = WorkoutForm()
    if form.validate_on_submit():
        name = form.name.data
        workout = Workout.add(name, session['user_id'])
        flash('Workout created')
        return redirect(f'/workouts/{workout.id}')

    return render_template('add_workout.html', form=form)


@app.route('/workouts/<int:id>')
def workout(id):
    if 'user_id' not in session:
        return redirect('/')

    workout = Workout.get(id)
    if session.get('user_id') != workout.user.id:
        return redirect('/')
    active = db.session.query(User.active_workout).filter(
        User.id == workout.user_id).one()[0]
    is_active = False
    if workout.id == active:
        is_active = True

    return render_template('workout.html', workout=workout, is_active=is_active)


@app.route('/workouts/<int:id>/days/add', methods=['GET', 'POST'])
def add_workoutday(id):
    if 'user_id' not in session:
        return redirect('/')

    workout = Workout.get(id)
    if session.get('user_id') != workout.user_id:
        return redirect('/')

    form = DayForm()
    form.weekday.choices = [(day, day) for day in Workout.available_days(id)]
    if form.validate_on_submit():
        WorkoutDay.add(id, form.weekday.data)
        db.session.commit()

        return redirect(f'/workouts/{id}')

    return render_template('add_day.html', form=form)


@app.route('/workouts/<int:id>/delete', methods=['GET'])
def delete_workout(id):
    if 'user_id' not in session:
        return redirect('/')

    workout = Workout.get(id)
    if session.get('user_id') != workout.user_id:
        return redirect('/')

    Workout.delete(id)
    flash("Workout Deleted")

    return redirect('/')


@app.route('/workouts/<int:workout_id>/days/<int:day_id>/delete', methods=['GET'])
def delete_day(workout_id, day_id):
    if 'user_id' not in session:
        return redirect('/')

    day = WorkoutDay.get(day_id)
    if session.get('user_id') != day.workout.user_id:
        return redirect('/')

    WorkoutDay.delete(day_id)
    flash("Workout Day Deleted")

    return redirect('/')


@app.route('/workouts/<int:workout_id>/days/<int:day_id>', methods=['GET', 'POST'])
def workout_day(workout_id, day_id):
    if 'user_id' not in session:
        return redirect('/')

    day = WorkoutDay.get(day_id)
    if session.get('user_id') != day.workout.user_id:
        return redirect('/')

    last = 0
    for ex in day.exercises:
        if ex.order > last:
            last = ex.order

    day.exercises = quicksort(day.exercises, 'order')

    return render_template('day.html', day=day, last=last)


@app.route('/exercises/description', methods=['GET'])
def exercise_description():
    id = request.args.get('id')
    name = request.args.get('name')

    return render_template('description.html', id=id, name=name)

@app.route('/api/days/<int:id>/', methods=['GET', 'OPTIONS'])
def get_routine(id):
    if request.method == 'OPTIONS':
        return Response()

    user_id = session.get('user_id', None)
    if user_id is None:
        return jsonify({'success': False})

    user = WorkoutDay.get(id).workout.user
    if(user.id != user_id):
        return jsonify({'success': False})

    exercises = WorkoutDay.get_serialized_exercises(id)
    return jsonify({'exercises': exercises, 'success': True})


@app.route('/users/<int:id>/workouts', methods=['GET'])
def get_workouts(id):
    user_id = session.get('user_id', None)
    if user_id is None:
        return redirect('/')
    elif user_id != id:
        return redirect('/')

    workouts = Workout.get_for(user_id)

    return render_template('workouts.html', workouts=workouts)


@app.route('/days/<int:id>/exercises/add', methods=['GET', 'POST'])
def add_exercise(id):
    if 'user_id' not in session:
        return redirect('/')

    day = WorkoutDay.get(id)
    if session.get('user_id') != day.workout.user_id:
        return redirect('/')

    prior_data = None
    if request.method == 'POST':
        exercise = request.form.get('exercise')
        sets = request.form.get('sets')
        reps = request.form.get('reps')
        exerciseName = request.form.get('exerciseName')
        results = Exercise.add(day.id, exercise, reps, sets, exerciseName)
        if results is not None:
            return redirect(f'/workouts/{day.workout_id}/days/{day.id}')
        prior_data = {
            'exercise':
                {'value': exercise,
                 'error': None},
            'sets':
                {'value': sets,
                 'error': None},
            'reps':
                {'value': reps,
                 'error': None},
            'exerciseName':
                {'value': exerciseName,
                 'error': None}
        }
    exercises = Exercise.all_for(id)
    return render_template('add_exercise.html', workout_id=day.workout_id, id=day.id, prior_data=prior_data, exercises=exercises)


@app.route('/workouts/<int:id>/active', methods=['POST', 'OPTIONS'])
def activate_workout(id):
    if request.method == 'OPTIONS':
        return Response()

    user_id = session.get('user_id', None)
    if user_id is None:
        return jsonify({'success': False})

    workout = Workout.get(id)
    if user_id != workout.user_id:
        return jsonify({'success': False})

    user = User.query.filter(User.id == workout.user_id).one()
    user.active_workout = id
    db.session.commit()
    return jsonify({'success': True})


@app.route('/api/workouts/<int:id>', methods=['PATCH', 'OPTIONS'])
def update_workout(id):

    if request.method == 'OPTION':
        return Response()

    user_id = session.get('user_id', None)
    if user_id is None:
        return jsonify({'success': False}), 403

    workout = Workout.get(id)
    if workout.user.id != user_id:
        return jsonify({'success': False}), 403

    name = request.get_json().get('name')
    Workout.update(id, name)

    return jsonify({'success': True})


@app.route('/api/workouts/<int:id>', methods=['GET', 'OPTIONS'])
def get_workout(id):

    if request.method == 'OPTION':
        return Response()

    user_id = session.get('user_id', None)
    if user_id is None:
        return jsonify({'success': False}), 403

    workout = Workout.get(id)
    if workout.user.id != user_id:
        return jsonify({'success': False}), 403

    return jsonify(Workout.serialize(id))


@app.route('/api/exercises/<int:id>/move', methods=['POST', 'OPTIONS'])
def move_exercise(id):

    if request.method == 'OPTIONS':
        return Response()

    user_id = session.get('user_id', None)
    if user_id is None:
        return jsonify({'success': False}), 403

    ex = Exercise.get(id)
    user = ex.day.workout.user
    if user_id != user.id:
        return jsonify({'success': False}), 403

    direction = request.get_json().get('direction')
    if(direction == 'up'):
        Exercise.move_up(id)
    else:
        Exercise.move_down(id)

    return jsonify({'success': True})


@app.route('/api/exercises/<int:id>', methods=['DELETE', 'OPTIONS'])
def delete_exercise(id):
    if request.method == 'OPTIONS':
        return Response()

    user_id = session.get('user_id', None)
    if user_id is None:
        return jsonify({'success': False}), 403

    ex = Exercise.get(id)
    if ex.day.workout.user.id != user_id:
        return jsonify({'success': False}), 403

    Exercise.delete(ex.id)
    return jsonify({'success': True})


@app.route('/api/exercises/<int:id>', methods=['PATCH', 'OPTIONS'])
def update_exercise(id):

    if request.method == 'OPTIONS':
        return Response()

    user_id = session.get('user_id', None)
    if user_id is None:
        return jsonify({'success': False}), 403

    ex = Exercise.get(id)
    if ex.day.workout.user.id != user_id:
        return jsonify({'success': False}), 403

    sets = request.get_json().get('sets')
    reps = request.get_json().get('reps')
    Exercise.update(id, sets=sets, reps=reps)

    return jsonify({'success': True})


@app.route('/api/days/<int:day_id>/exercises', methods=['POST', 'OPTIONS'])
def post_exercise(day_id):

    if request.method == 'OPTIONS':
        return  Response()


    user_id = session.get('user_id', None)
    if user_id is None: 
        return jsonify({'success': False}), 403 

    day = WorkoutDay.get(day_id)
    if user_id != day.workout.user.id:
        return jsonify({'success': False}), 403 

    data = request.get_json() 
    exer_id = data.get('exercise')
    name = data.get('name')
    reps = data.get('reps')
    sets = data.get('sets')
    ex = Exercise.add(day.id, exer_id, sets, reps, name)

    if ex is None: 
        return jsonify({'success': False}), 403 

    return jsonify({'success': True})




@app.route('/api/days/<int:day_id>/exercises', methods=['GET', 'OPTIONS'])
def get_exercises(day_id):

    if request.method == 'OPTIONS':
        return  Response()


    user_id = session.get('user_id', None)
    if user_id is None: 
        return jsonify({'success': False}), 403 

    day = WorkoutDay.get(day_id)
    if user_id != day.workout.user.id:
        return jsonify({'success': False}), 403 

    
    exercises = WorkoutDay.get_serialized_exercises(day_id)

    return jsonify({'success': True, 'exercises': exercises})