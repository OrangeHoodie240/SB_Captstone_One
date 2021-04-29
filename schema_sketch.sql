-- This is the script I wrote and imported to https://dbdiagram.io
-- to generate capstone_1_diagram.png 


CREATE TABLE users(
  id SERIAL PRIMARY KEY, 
  username VARCHAR(30) NOT NULL UNIQUE, 
  email VARCHAR(320) NOT NULL UNIQUE, 
  password TEXT NOT NULL UNIQUE,
  active_workout INT NULL);

CREATE TABLE workouts(
  id SERIAL PRIMARY KEY, 
  user_id INT REFERENCES users(id), 
  workout_name VARCHAR(30) NOT NULL);


CREATE TABLE workout_days(
  id SERIAL PRIMARY KEY, 
  workout_id INT REFERENCES workouts(id) NOT NULL,
  weekday VARCHAR(9), NOT NULL CHECK(LOWER(weekday) IN ('sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday')));


CREATE TABLE exercises(
  id SERIAL PRIMARY KEY, 
  workout_day_id INT REFERENCES workout_days(id) NOT NULL, 
  exercise INT NOT NULL,
  name VARCHAR(60) NOT NULL, 
  sets INT NOT NULL CHECK(sets > 0 AND sets < 51), 
  reps INT NOT NULL CHECK(reps > 0 AND reps < 51), 
  order INT NOT NULL CHECK(order > 0));