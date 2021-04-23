from app import db, User, Workout, WorkoutDay, Exercise


db.drop_all() 
db.create_all() 


user = User.register('dogdogdog', 'dog@dog.com', 'dogdogdog')
workout_1 = Workout.add(user_id=user.id, name='workout_1')
day_1 = WorkoutDay.add(workout_id=workout_1.id, weekday='monday')
day_2 = WorkoutDay.add(workout_id=workout_1.id, weekday='thursday')
exercise1 = Exercise.add(day_1.id, 307, 5, 10)
exercise2 = Exercise.add(day_1.id, 302, 5, 10)

