function msToTime(s) {
    var ms = s % 1000;
    s = (s - ms) / 1000;
    var secs = s % 60;
    s = (s - secs) / 60;
    var mins = s % 60;
    var hrs = (s - mins) / 60;
  
    return hrs + ':' + mins + ':' + secs + '.' + ms;
  }

function updateTime(){
    console.log(start_time)
    let timeDivs = document.querySelectorAll('.view-time');
    timeDivs.forEach((div)=>{
        let timeDelta = Date.now() - Date.parse(start_time);
        div.innerText = msToTime(timeDelta); 
    });
    requestAnimationFrame(updateTime);
}
requestAnimationFrame(updateTime);