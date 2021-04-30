const descriptionDiv = document.getElementById('description-div');
const loadingDiv = document.getElementById('loading-div');
const id = document.getElementById('exercise-id').value; 


async function loadDescription(){
    const data = await fetch(`https://wger.de/api/v2/exercise/${id}`, {headers: {'Accept': 'application/json'}})
        .then(resp => resp.json())
        .then(data => data); 
    descriptionDiv.innerHTML = data.description; 
    loadingDiv.remove();

    const imageUrl = await fetch(`https://wger.de/api/v2/exerciseimage/?exercise=${id}`)
        .then(resp => resp.json())
        .then(data =>{
            if(data.count > 0){
                return data.results[0].image; 
            }
            else return false; 
        });  

    if(imageUrl){
        descriptionDiv.innerHTML += `<img style="max-width: 400px; height: auto;" src="${imageUrl}"/>`
    }
}


loadDescription();


