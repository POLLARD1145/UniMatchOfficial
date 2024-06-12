function addHobbies() {
    var hobbie = document.getElementById("hobbie").value;
    var hobbiesList = document.getElementById("hobbie-list");

    var hobbyitem = document.createElement("li");
    hobbyitem.className = "list-group-item";
    hobbyitem.textContent = hobbie;
    hobbiesList.appendChild(hobbyitem);
}

document.getElementById('add-hobby-button').addEventListener('click', function(event) {
    event.preventDefault();
    addHobbies();
});

//goals
function addGoals() {
    var hobbie = document.getElementById("goal").value;
    var hobbiesList = document.getElementById("goal-list");

    var hobbyitem = document.createElement("li");
    hobbyitem.className = "list-group-item";
    hobbyitem.textContent = hobbie;
    hobbiesList.appendChild(hobbyitem);
}

document.getElementById('add-goal-button').addEventListener('click', function(event) {
    event.preventDefault();
    addGoals();
});