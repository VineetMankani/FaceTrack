// import * as hello from "/static/test.py";
// import * as attendance from "C:/Users/vinee/Desktop/FaceTrack/Attendance System/attendance.py";
// let csv;
// function setup() {
//     csv = loadTable("Attendance.csv", 'csv', 'header', loaded);
// }

// let data;
// function setup() {
//     data = ;
// }

function loaded(data){
    
    for (let i = 0; i < data.getRowCount(); i++) {
        addRow(i+1, data.getString(i, 0), data.getString(i, 1), data.getString(i, 2))
    }
}


function addRow(td1, td2, td3, td4) {
    let table = document.querySelector('table');
    let tr = document.createElement('tr');

    let SrNo = document.createElement('td');
    tr.appendChild(SrNo);
    let UID = document.createElement('td');
    tr.appendChild(UID);
    let Name = document.createElement('td');
    tr.appendChild(Name);
    let Time = document.createElement('td');
    tr.appendChild(Time);

    table.appendChild(tr);

    SrNo.innerText = td1;
    UID.innerText = td2;
    Name.innerText = td3;
    Time.innerText = td4;
}

const weekday = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];

let date = document.querySelector('#date');
// let day = document.querySelector('#day');

let D = new Date();
let d = D.getDate();
let m = '0'+(D.getMonth()+1);
let y = D.getFullYear();
let w = weekday[D.getDay()];

date.innerText = `${w}, ${d}/${m}/${y}`;
// day.innerText = weekday[D.getDay()];

const navbar = document.querySelector('#navbar');

$(window).scroll(function() {
    var offset = $(window).scrollTop();
    // console.log(offset);
    $('.navbar').toggleClass('trans', offset > 50);
  });


const start = document.querySelector('#start');
const loading = document.querySelector('#loading');

start.addEventListener('click', ()=> {

    document.body.style.opacity = 0.5
    loading.classList.remove('d-none')
    
    setTimeout(() => {
        document.body.style.opacity = 1;
        loading.classList.add('d-none')
    }, 7000);

})