let timeinterval = document.getElementsByClassName("time-interval")[0];
let Content = document.getElementsByClassName("content")[0];
let timelen = timeinterval.children.length;


// set style for timeinterval
timeinterval.style.gridTemplateRows = "repeat(" + timelen + ", 49px)";
timeinterval.style.gridTemplateRows = "repeat(" + timelen + ", 49px)";


// function for white button
function postTask() {
    let id = $(this).attr('id');
    let room = document.getElementsByClassName("timetable")[0].id;
    $.post('/add_task_by_id', {id: id, room: room}, function(data) {
        if (data=="success"){
            // change button style and function with jquery
            let element = document.getElementById(id);
            element.classList.remove("accent-white-gradient");
            element.classList.add("accent-orange-gradient");
            let name = document.getElementsByClassName("function-button")[0].innerHTML;
            element.innerHTML = name;
            // rm event listener
            element.removeEventListener("click", postTask);
            element.addEventListener("click", cancelTask);
        } else {
            alert(data)
        };
    });
}

let whiteBtn = document.getElementsByClassName("accent-white-gradient");
for (let i = 0; i < whiteBtn.length; i++) {
    whiteBtn[i].addEventListener("click", postTask);
}

// function for orange button
function cancelTask() {
    let id = $(this).attr('id');
    let room = document.getElementsByClassName("timetable")[0].id;
    $.post('/cancel_prebook', {id: id, room: room}, function(data) {
        if (data=="success"){
            // change button style and function with jquery
            let element = document.getElementById(id);
            element.classList.remove("accent-orange-gradient");
            element.classList.add("accent-white-gradient");
            element.innerHTML = "";
            // rm event listener
            element.removeEventListener("click", cancelTask);
            element.addEventListener("click", postTask);
        } else {
            alert(data)
        };
    });
}

let orangeBtn = document.getElementsByClassName("accent-orange-gradient");
for (let i = 0; i < orangeBtn.length; i++) {
    orangeBtn[i].addEventListener("click", cancelTask);
}



$('.accent-red-gradient').click(function() { 
    alert("This function is not available yet!");
});

$('.accent-blue-gradient').click(function() { 
    alert("This function is not available yet!");
});




$('.function-button').click(function() { 
    window.location.href = "/";
});