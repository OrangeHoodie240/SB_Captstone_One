
const makeActive = document.getElementById('make_active'); 
let id = parseInt(document.getElementById('workout_id').value);


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

makeActive.addEventListener('click', ()=>{
    setActive(id);
});