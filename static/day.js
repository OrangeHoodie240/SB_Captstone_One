
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
        td.classList.add('sets');
        tr.append(td); 

        td = document.createElement('td'); 
        td.innerHTML = ex.reps;
        td.classList.add('reps');
        tr.append(td); 

        td = document.createElement('td'); 
        td.innerHTML = `<a href='/exercises/description?id=${ex.exercise }&name=${ ex.name }'>description</a>`;
        tr.append(td); 

        td = document.createElement('td'); 
        td.innerHTML = `<i class="fa fa-trash delete" aria-hidden="true" data-exercise-id='${ex.id}'></i>`;
        tr.append(td); 

        
        td = document.createElement('td'); 
        td.innerHTML = `<i class="fas fa-edit edit" aria-hidden="true" data-exercise-id="${ex.id}"></i>`;
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
    else if(target.classList.contains('edit')){
        addFields(target);
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
            return data.success;
        });
    if(success){
        updateTbody()
    }
}

function addFields(ex){
    const row = ex.parentElement.parentElement; 
    if(row.contains(row.querySelector('.editButton'))){
        return; 
    }

    let id = ex.getAttribute('data-exercise-id');

    const setsTd = row.querySelector('.sets'); 
    const repsTd = row.querySelector('.reps'); 

    const setsValue = setsTd.innerText; 
    setsTd.setAttribute('data-value',setsValue);
    setsTd.innerHTML = `<input type='number' min='1' max='50' id='setsField' value='${setsValue}' />`; 

    const repsValue = repsTd.innerText;
    repsTd.setAttribute('data-value', repsValue);
    repsTd.innerHTML = `<input type='number' min='1' max='50' id='repsField' value='${repsValue}' />`; 

    td = document.createElement('td');
    td.classList.add('editButton');
    td.innerHTML = `<button>Save</button>`; 
    row.append(td);

    const setsField = row.querySelector('#setsField');
    const repsField = row.querySelector('#repsField');
    

    td.addEventListener('click', async function(){
        body = JSON.stringify({sets: setsField.value, reps: repsField.value})
        const options = {
                            headers: {
                                        'Content-Type': 'application/json', 
                                        'credentials': 'include'
                            }, 
                            method: 'PATCH', 
                            body
                        };
        const success = fetch(`/api/exercises/${id}`, options)
            .then(resp=>resp.json())
            .then(data => {
                return data.success;
            });
        returnRow(ex, success);
        
    });

    td = document.createElement('td');
    td.classList.add('cancelButton');
    td.innerHTML = `<button>Cancel</button>`; 
    row.append(td);

    td.addEventListener('click', ()=>{
        returnRow(row, false);
    });

}


function returnRow(row, success){
    const setsTd = row.querySelector('.sets'); 
    const repsTd = row.querySelector('.reps'); 
    
    if(success){
        updateTbody();       
    }
    else{
        const setsValue = setsTd.getAttribute('data-value');
        const repsValue = repsTd.getAttribute('data-value');
        
        setsTd.innerHTML = setsValue; 
        repsTd.innerHTML = repsValue; 

        const editButton = row.querySelector('.editButton');
        const cancelButton = row.querySelector('.cancelButton'); 

        editButton.remove(); 
        cancelButton.remove(); 
        
    }
}