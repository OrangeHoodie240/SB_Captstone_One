
# Captstone Project: Workout Planner

The site is called [Workout Planner](https://capstone1-steven-daddario.herokuapp.com/). The purpose of the application is to allow users to create and track weight lifting routines.In order to use the site, a user must register and login. Users can create multiple workouts, but can only have one workout active at a time. Users create routines for their workouts mapped to specific days. Once a user logs in, their home page displays their next scheduled routine informing them of the day and the routine.

Each routine is comprised of a number of exercises, each having numbers specifying the target number of sets and reps and arre listed in the order in which they are to be performed. When adding exercises to a routine, the user is able to filter exercises by targeted muscle and required equipment. Exercisess are pulled from the [wger](https://wger.de/en/software/api) API, and any description the API includes for the exercise is also displayed. 

This application is made with Flask, Flask-SQLAlchemy, Postgresql, Bootstrap and Heroku.

Unfortunately the API, [wger](https://wger.de/en/software/api), is very inconsistent in respect to the quality and detail of its exercise descriptions. 


