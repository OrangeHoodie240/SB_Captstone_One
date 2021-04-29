
const tbody = document.getElementById('exercises-tbody');
const day_id = parseInt(tbody.getAttribute('data-day-id'));

// prob delete this and the attribute in tbody
const workout_id = parseInt(tbody.getAttribute('data-workout-id'));

async function updateTbody(){
    data = await fetch(`/api/days/${day_id}`, {headers:  {'Accept': 'application/json'},  credentials: 'include'})
        .then(resp => resp.json())
        .then(data => {
            return data;
        });
    buildTable(data.exercises);

}


function buildTable(data){
    tbody.innerHTML = ''; 
    for(let i = 0; i < data.length; i++){
        ex = data[i];

        let tr = document.createElement('tr'); 

        let td = document.createElement('td'); 
        td.innerHTML = ex.name;
        tr.append(td); 

        td = document.createElement('td'); 
        td.innerHTML = ex.sets;
        tr.append(td); 

        td = document.createElement('td'); 
        td.innerHTML = ex.reps;
        tr.append(td); 

        td = document.createElement('td'); 
        td.innerHTML = 'description';
        tr.append(td); 

        td = document.createElement('td'); 
        td.innerHTML = `<i class="fa fa-trash delete" aria-hidden="true" data-exercise-id='${ex.id }'></i>`;
        tr.append(td); 

        if(i != 0){
            td = document.createElement('td'); 
            td.innerHTML = `<i class="fa fa-arrow-up up" aria-hidden="true"  data-exercise-id='${ex.id}'></i>`;
            tr.append(td); 
        }
        else{
            td = document.createElement('td'); 
            tr.append(td);
        }

        if(i < data.length -1){
            td = document.createElement('td'); 
            td.innerHTML = `<i class="fa fa-arrow-down down" aria-hidden="true"  data-exercise-id='${ex.id}'></i>`;
            tr.append(td); 
        }

        tbody.append(tr);
    }
}

tbody.addEventListener('click', ({target})=>{
    if(target.classList.contains('up')){
        move(target, 'up');
    }
    else if(target.classList.contains('down')){
        move(target, 'down');
    }
    else if(target.classList.contains('delete')){
        deleteExercise(target);
    }
});

async function move(arrow, dir){
    const id = arrow.getAttribute('data-exercise-id');
    const body = JSON.stringify({'direction': dir});
    const success = await fetch(`/api/exercises/${id}/move`, {method:'POST', headers: {'Content-Type': 'application/json', credentials: 'include'}, 'body': body})
        .then(resp => resp.json())
        .then(data => {
            return data.success; 
        });
    if(success){
        updateTbody(); 
    }
}

async function deleteExercise(ex){
    let id = ex.getAttribute('data-exercise-id');

    const fetchOptions = {headers: {'Content-Type': 'application/json'}, method: 'DELETE', credentials: 'include'};

    success = await fetch(`/api/exercises/${id}`,fetchOptions)
        .then(resp => resp.json())
        .then(data => {
            console.log(data);
            return data.success;
        });
    if(success){
        updateTbody()
    }
}