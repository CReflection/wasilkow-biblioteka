function msToTime(s) {
    var ms = s % 1000;
    s = (s - ms) / 1000;
    var secs = s % 60;
    s = (s - secs) / 60;
    var mins = s % 60;
    var hrs = (s - mins) / 60;
    
    if(secs < 10) {
        secs = "0" + secs
    }
    if(mins < 10){
        mins = "0" + mins
    }
    if(hrs < 10) {
        hrs = "0" + hrs
    }
    if(ms < 10) {
        ms = "000" + ms
    } else if(ms < 100) {
        ms = "00" + ms
    } else if(ms < 1000) {
        ms = "0" + ms
    }
  
    return hrs + ':' + mins + ':' + secs + '.' + ms;
  }

function updateTime(){
    // console.log(start_time)
    let timeDivs = document.querySelectorAll('.view-time');
    timeDivs.forEach((div)=>{
        let timeDelta = Date.now() - Date.parse(start_time);
        div.innerText = msToTime(timeDelta); 
    });
    requestAnimationFrame(updateTime);
}
requestAnimationFrame(updateTime);

window.onload = function(e){
    console.log(points);
    console.log(document.documentElement.clientWidth);
    console.log(document.querySelector("#points-container"));
    let mickiewicz = document.querySelector("#mickiewicz-container");
    if(points <= 0 && document.documentElement.clientWidth < 1300) {
        let leaderboard = document.querySelector("#points-container");
        leaderboard.style.display = "none";
        mickiewicz.style.margin = "unset";
    } else if(document.documentElement.clientWidth < 542) {
        let mickiewiczInfo = document.querySelector("#mickiewicz-info");
        mickiewiczInfo.style.marginTop = "unset";
        mickiewicz.style.marginTop = "100px";
    }
    else if(document.documentElement.clientWidth < 1300) {
        let mickiewiczInfo = document.querySelector("#mickiewicz-info");
        mickiewiczInfo.style.marginTop = "unset";
        mickiewicz.style.marginTop = "160px";
    } 
}