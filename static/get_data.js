const muscle_json = {
    'Biceps brachii': 1, 'Anterior deltoid': 2, 'Serratus anterior': 3, 'Pectoralis major': 4, 'Triceps brachii': 5,
    'Rectus abdominis': 6, 'Gastrocnemius': 7, 'Gluteus maximus': 8, 'Trapezius': 9,
    'Quadriceps femoris': 10, 'Biceps femoris': 11, 'Latissimus dorsi': 12, 'Brachialis': 13,
    'Obliquus externus abdominis': 14, 'Soleus': 15
};

const equipment_json = {
    'Barbell': 1, 'SZ-Bar': 2, 'Dumbbell': 3, 'Gym mat': 4, 'Swiss Ball': 5, 'Pull-up bar': 6,
    'none (bodyweight exercise)': 7, 'Bench': 8, 'Incline bench': 9, 'Kettlebell': 10
};

const idToEquipment = {}; 
for(let key in equipment_json){
    idToEquipment[equipment_json[key]] = key; 
}

const muscles = [];
for (let key in muscle_json) {
    let muscle = { name: key, id: muscle_json[key] };
    muscles.push(muscle);
}

const equips = [];
for (let key in equipment_json) {
    let eq = { name: key, id: equipment_json[key] };
    equips.push(eq);
}


class ApiHandler {
    constructor() {
        this.encyclopedia = null;
        this.exercises = null;
        this.imageUrls = null; 
    }

    async getData() {
        const exercises = await fetch('https://wger.de/api/v2/exercise?&language=2&limit=999')
            .then(resp => resp.json())
            .then(data => data.results);
        for (let i = 0; i < exercises.length; i++) {
            if (exercises[i]['muscles'].length === 0) {
                exercises.splice(i, 1);
            }
        }
        this.exercises = exercises;
    }

    createEncylopcedia() {
        const encyclopedia = {};
        for (let muscle of muscles) {
            // 999 is magic number for all here
            encyclopedia[muscle.id] = { 'exercises': [], 'equipment': new Set([999]) };
        }
        for (let ex of this.exercises) {
            for (let id of ex.muscles) {
                encyclopedia[id]['exercises'].push(ex);
                let eq = ex.equipment[0]
                if (!eq) {
                    continue;
                }
                encyclopedia[id]['equipment'].add(eq);
            }
        }
        this.encyclopedia = encyclopedia;
    }

    async load(elements) {
        await this.getData();
        const loadImages = this.loadImages(); 
        this.load_select(elements['muscle'], muscles);
        this.createEncylopcedia();
        this.filterChangeMuscle(elements['exercise'], elements['muscle'], elements['equipment']);
        await loadImages; 
        this.changeDescription(elements['exercise'], elements['description'])
        this.finish(elements);
    }

    load_select(select, collection, sort = (a, b) => a.name - b.name) {
        const ops = [];
        for (let ex of collection) {
            const op = document.createElement('option');
            op.value = ex.id;
            op.innerText = ex.name;
            ops.push(op);
        }
        if (sort) {
            ops.sort(sort);
        }
        select.append(...ops);
    }

    filterChangeMuscle = async (exercise, muscle, equipment) => {
        exercise.innerHTML=''; 
        equipment.innerHTML = ''; 

        const muscleDb = this.encyclopedia[muscle.value];
        const equipmentNames = Array.from(muscleDb['equipment']).map(b => {
            if(b === 999){
                return {name: 'All', id: b};
            }
            else{
                return {name: idToEquipment[b], id: b};
            }
        });

        this.load_select(equipment, equipmentNames);
        for(let i = 0; i < equipment.children.length; i++){
            if (equipment.children[i].value != 999) {
                equipment.children[i].removeAttribute('selected');
            }
            else {
                equipment.children[i].setAttribute('selected', true);
            }
        }

        const exercises = muscleDb['exercises'];
        this.load_select(exercise, exercises);

    }

    filterChangeEquipment = async (exercise, muscle, equipment) => {
        exercise.innerHTML=''; 

        const muscleDb = this.encyclopedia[muscle.value];
        let exercises; 
        if(equipment.value == 999){
            exercises = muscleDb['exercises'];
        }
        else{
            exercises = muscleDb['exercises'].filter(b => {
                if(equipment.value == b['equipment'][0]){
                    return true; 
                }
                return false; 
            });
        }

        this.load_select(exercise, exercises);

    }

    async loadImages(){
        let url = 'https://wger.de/api/v2/exerciseimage?limit=999';
        const ids = this.exercises.map(b => b.id);
        this.imageUrls = await fetch(url)
            .then(resp => resp.json())
            .then(data =>{
                let imageUrls = {}; 
                for(let result of data.results){
                    if(ids.includes(result.exercise)){
                       imageUrls[result.exercise] = result.image;
                    }
                }
                return imageUrls; 
            }); 
    }

    changeDescription(exercise, description){
        description.innerHTML = '';
        const ex = this.exercises.filter(b => b.id == exercise.value)[0];
        if(this.imageUrls[exercise.value]){
            description.innerHTML += `<img style="max-width: 400px; height: auto;" src="${this.imageUrls[exercise.value]}"/>`;
        }
        description.innerHTML += ex.description; 
    }

    finish(elements) {
        for (let key in elements) {
            if (key === 'loading') {
                elements[key].remove();
            }
            else {
                elements[key].removeAttribute('disabled');
            }
        }

        elements['exerciseName'].value = exercise.children[0].innerText;
    }
}
