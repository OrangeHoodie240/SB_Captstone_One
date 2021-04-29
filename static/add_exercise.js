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

const elements = {'exercise': exercise, 'sets': sets, 'reps':reps, 'submit':submit, 'muscle':muscle, 'equipment':equipment, 'loading': loading, 'description': description};

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