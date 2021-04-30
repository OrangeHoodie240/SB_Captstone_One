const workoutExercisesDiv = document.getElementById('workout-exercises-div-add-exercise');
const day_id = document.getElementById('day-id').value; 

const add_form = document.getElementById('add_exercise');
const filter_form = document.getElementById('filter_add_exercise');

const exercise = add_form.querySelector('#exercise');
const sets = add_form.querySelector('#sets');
const reps = add_form.querySelector('#reps');
const exerciseName = add_form.querySelector('#exerciseName');
const submit = add_form.querySelector('#submit');

const muscle = filter_form.querySelector('#muscle');
const equipment = filter_form.querySelector('#equipment');

const loading = document.getElementById('loading');

const description = document.querySelector('.description'); 

const elements = {'exercise': exercise, 'sets': sets, 'reps':reps, 'submit':submit, 'muscle':muscle, 'equipment':equipment, 'loading': loading, 'description': description, 'exerciseName': exerciseName};

api = new ApiHandler();

filter_form.addEventListener('submit', function(evt){
    evt.preventDefault();
});


api.load(elements); 

muscle.addEventListener('change', function(){
    api.filterChangeMuscle(exercise, muscle, equipment);
    api.changeDescription(exercise, description);
    exerciseName.value = exercise.children[0].innerText; 
}); 

equipment.addEventListener('change', function(){
    api.filterChangeEquipment(exercise, muscle, equipment);
    api.changeDescription(exercise, description);
    exerciseName.value = exercise.children[0].innerText; 

});

exercise.addEventListener('change', function(){
    api.changeDescription(exercise, description);
    exerciseName.value = Array.from(exercise.children).find(b => b.value === exercise.value).innerText; 
});

add_form.addEventListener('submit', async function(evt){
    evt.preventDefault(); 

    let body = {
        'exercise': exercise.value,
        'name': exerciseName.value, 
        'reps': reps.value, 
        'sets': sets.value
    };
    body = JSON.stringify(body); 

    const options = {
        headers: {
            'Content-Type': 'application/json',
            'credentials': 'include'
        }, 
        method: 'POST',
        body
    };

    const success = await fetch(`/api/days/${day_id}/exercises`, options)
        .then(resp => resp.json())
        .then(data => data.success);
    if(success){
        updateWorkoutExerciseDiv();
    }
});


async function updateWorkoutExerciseDiv(){
    data = await fetch(`/api/days/${day_id}/exercises`, {method: 'GET', headers: {credentials: 'include'}})
        .then(resp => resp.json())
        .then(data => data); 
    if(data.success){
        html = ''; 
        for(let ex of data.exercises){
            html += `${ex.order}. ${ex.name}\t`;
        }
        workoutExercisesDiv.innerHTML = html;
    }
}