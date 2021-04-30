from app import db, User, Workout, WorkoutDay, Exercise


db.drop_all() 
db.create_all() 


# user = User.register('dogdogdog', 'dog@dog.com', 'dogdogdog')
# workout_1 = Workout.add(user_id=user.id, name='workout_1')
# day_1 = WorkoutDay.add(workout_id=workout_1.id, weekday='monday')


