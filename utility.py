import datetime as dt
import random 
import math



weekdays =  {'monday': 1, 'tuesday': 2, 'wednesday': 3, 'thursday': 4, 'friday': 5, 'saturday': 6, 'sunday': 7}

def find_closest_workout(workout):
    weekday = dt.datetime.today().weekday() + 1

    closest = 8
    closest_day = None
    for day in workout.days: 
        workout_on = weekdays[day.weekday]
        
        distance = None 
        if workout_on > weekday: 
            distance = workout_on - weekday 
        elif weekday > workout_on: 
            distance = 7  - weekday + workout_on
        else: 
            return day 
        
        if distance < closest: 
            closest = distance 
            closest_day = day

    return closest_day 


def quicksort(arr, attr=None):
    n = len(arr) 
    if n == 0 or n == 1: 
        return arr 
    rand = int(math.floor(random.random() * n))
    
    bench = None
    if attr is None:
        bench = arr[rand]
    else:
        bench = getattr(arr[rand], attr) 
    left = []
    right = []
    for i in range(n):
        current = None 
        if attr is None: 
            current = arr[i]
        else: 
            current = getattr(arr[i], attr) 
        if current < bench: 
            left.append(arr[i])
        elif current > bench: 
            right.append(arr[i])

    return [*quicksort(left, attr=attr), arr[rand], *quicksort(right, attr=attr)] 
