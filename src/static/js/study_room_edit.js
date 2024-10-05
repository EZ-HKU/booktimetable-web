// find coloumn with class time-interval
let timeInterval = document.getElementsByClassName('time-interval')[0];
// get all divs in time-interval
let timeIntervalDivs = timeInterval.getElementsByTagName('div');

for (let i = 0; i < timeIntervalDivs.length; i++) {
    let timeIntervalDiv = timeIntervalDivs[i];
    let timeIntervalText = timeIntervalDiv.innerText;
    if (timeIntervalText === '00:00-00:30') {
        timeIntervalDiv.innerText = '00:00-01:00';
    } else if (timeIntervalText === '00:30-01:00') {
        timeIntervalDiv.innerText = '01:00-02:00';
    } else if (timeIntervalText === '01:00-01:30') {
        timeIntervalDiv.innerText = '02:00-03:00';
    } else if (timeIntervalText === '01:30-02:00') {
        timeIntervalDiv.innerText = '03:00-04:00';
    } else if (timeIntervalText === '02:00-02:30') {
        timeIntervalDiv.innerText = '04:00-05:00';
    } else if (timeIntervalText === '02:30-03:00') {
        timeIntervalDiv.innerText = '05:00-06:00';
    } else if (timeIntervalText === '03:00-03:30') {
        timeIntervalDiv.innerText = '08:00-09:00';
    } else if (timeIntervalText === '03:30-04:00') {
        timeIntervalDiv.innerText = '09:00-10:00';
    } else if (timeIntervalText === '04:00-04:30') {
        timeIntervalDiv.innerText = '10:00-11:00';
    } else if (timeIntervalText === '04:30-05:00') {
        timeIntervalDiv.innerText = '11:00-12:00';
    } else if (timeIntervalText === '05:00-05:30') {
        timeIntervalDiv.innerText = '12:00-13:00';
    } else if (timeIntervalText === '05:30-06:00') {
        timeIntervalDiv.innerText = '13:00-14:00';
    } else if (timeIntervalText === '08:00-08:30') {
        timeIntervalDiv.innerText = '14:00-15:00';
    } else if (timeIntervalText === '08:30-09:00') {
        timeIntervalDiv.innerText = '15:00-16:00';
    } else if (timeIntervalText === '09:00-09:30') {
        timeIntervalDiv.innerText = '16:00-17:00';
    } else if (timeIntervalText === '09:30-10:00') {
        timeIntervalDiv.innerText = '17:00-18:00';
    } else if (timeIntervalText === '10:00-10:30') {
        timeIntervalDiv.innerText = '18:00-19:00';
    } else if (timeIntervalText === '10:30-11:00') {
        timeIntervalDiv.innerText = '19:00-20:00';
    } else if (timeIntervalText === '11:00-11:30') {
        timeIntervalDiv.innerText = '20:00-21:00';
    } else if (timeIntervalText === '11:30-12:00') {
        timeIntervalDiv.innerText = '21:00-22:00';
    } else if (timeIntervalText === '12:00-12:30') {
        timeIntervalDiv.innerText = '22:00-23:00';
    } else if (timeIntervalText === '12:30-13:00') {
        timeIntervalDiv.innerText = '23:00-23:45';
    } else {
        timeIntervalDiv.innerText = '不要点';
    }
}


