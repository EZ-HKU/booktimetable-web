let fselector = document.getElementById("fselector");
let rselector = document.getElementById("rselector");
let check = document.getElementById("check");
let logout = document.getElementById("logOut");

let facilities = {
    "Discussion Room": [], "Study Room": [],
    "Concept and Creation Room": [],
};

// add options to fselector
for (let f in facilities) {
    let option = document.createElement("option");
    option.value = f;
    option.innerHTML = f;
    fselector.appendChild(option);
}

// creat 19 Discussion Room
for (let i = 1; i <= 19; i++) {
    facilities["Discussion Room"].push("Discussion Room " + i);
}

// creat 10 Study Room
for (let i = 1; i <= 10; i++) {
    facilities["Study Room"].push("Study Room " + i);
}

// creat 5 Concept and Creation Room
for (let i = 1; i <= 5; i++) {
    facilities["Concept and Creation Room"].push("Concept and Creation Room " + i);
}

fselector.addEventListener("change", function() {
    let f = fselector.value;
    let rooms = facilities[f];
    rselector.innerHTML = "";
    for (let i = 0; i < rooms.length; i++) {
        let option = document.createElement("option");
        option.value = rooms[i];
        option.innerHTML = rooms[i];
        rselector.appendChild(option);
    }
});


check.addEventListener("click", function () {
    let r = rselector.value;
    if (r === "") {
        alert("Please select a room");
        return;
    }

    location.href = window.location.origin + "/timetable/" + r;

});

logout.addEventListener("click", function () {
    if (!confirm("Are you sure to log out?")) {
        return;
    }

    location.href = window.location.origin + "/login";
});