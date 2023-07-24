document.addEventListener("DOMContentLoaded", ()=>{
    
    startTime(clock)
})

function startTime() {

    const today = new Date();

    let d = today.getDate();

    let mo = today.getMonth() + 1;

    let h = today.getHours();

    let m = today.getMinutes();

    m = checkTime(m);

    clock = document.getElementById("clock")

    clock.innerHTML = d + " / " + mo + " - " + h + ":" + m;
    
    setTimeout(startTime, 1000);
}

function checkTime(i) {

    if (i < 10) {i = "0" + i};  // add zero in front of numbers < 10
    
    return i;
  }