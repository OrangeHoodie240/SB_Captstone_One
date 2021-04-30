
const makeActive = document.getElementById('make_active'); 
let id = parseInt(document.getElementById('workout_id').value);

const nameField = document.querySelector('#name'); 
const changeButton = document.querySelector('#change-button');

async function setActive(id){
    let success = await fetch(`/workouts/${id}/active`, {headers: {'Content-Type': 'application/json'}, method: 'POST', credentials: 'include'})
        .then(resp => resp.json())
        .then(data => {
            return data.success;
        });
    if(success){
        const p = document.createElement('p');
        p.innerText = 'This is your active workout'; 
        makeActive.insertAdjacentElement('beforebegin', p);
        makeActive.remove();
        
    }
}

if(makeActive){
    makeActive.addEventListener('click', ()=>{
        setActive(id);
    });    
}


changeButton.addEventListener('click', changeName);
nameField.addEventListener('keypress', (evt)=>{
    if(evt.key === 'Enter'){
        changeName(); 
    }
});


async function changeName(){
    const body = JSON.stringify({'name': nameField.value}); 
    const fetchOptions = {headers: 
                            {'Content-Type': 'application/json', 
                            credentials: 'include'},
                        method:'PATCH', 
                        body};

    let success = await fetch(`/api/workouts/${id}`, fetchOptions)
        .then(resp => resp.json())
        .then(data => {
            return data.success; 
        });
    if(success){
        updateNameOnPage();
    }
}

async function updateNameOnPage(){
    document.title = nameField.value;
    document.querySelector('h1').innerText = nameField.value; 
}