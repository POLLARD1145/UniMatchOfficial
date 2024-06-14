function addHobbies() {
    var hobbie = document.getElementById("hobbie").value;
    var hobbiesList = document.getElementById("hobbie-list");

    var hobbyitem = document.createElement("li");
    hobbyitem.className = "list-group-item";
    hobbyitem.textContent = hobbie;
    if (hobbie === "") {
        //do nothing
    } else {
        hobbiesList.appendChild(hobbyitem);
    }
    
}

document.getElementById('add-hobby-button').addEventListener('click', function(event) {
    event.preventDefault();
    
    addHobbies();
});

//goals
function addGoals() {
    var goal = document.getElementById("goal").value;
    var goalList = document.getElementById("goal-list");

    var goalitem = document.createElement("li");
    goalitem.className = "list-group-item";
    goalitem.textContent = goal;
    if (goal === "") {
        //do nothing
    } else {
        goalList.appendChild(goalitem);
    }
    
}

document.getElementById('add-goal-button').addEventListener('click', function(event) {
    event.preventDefault();
    addGoals();
});

//preferences
function addPreferences() {
    var preference = document.getElementById("preference").value;
    var preferenceList = document.getElementById("preference-list");

    var preferenceitem = document.createElement("li");
    preferenceitem.className = "list-group-item";
    preferenceitem.textContent = preference;
    if (preference === "") {
        //do nothing
    } else {
        preferenceList.appendChild(preferenceitem); 
    }
    
}

document.getElementById('add-preference-button').addEventListener('click', function(event) {
    event.preventDefault();
    addPreferences();
});