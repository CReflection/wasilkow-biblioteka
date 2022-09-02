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
    if(hours < 10) {
        hours = "0" + hours
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
    let div = document.querySelector('#mickiewicz-container');
    let image = document.querySelector('#mickiewicz-info img');
    // let height = image.height
    console.log(image.height)
    image.style.top = "-" + (image.height - 40) + "px";
    image.style.right = "-" + (image.width/2 - 50) + "px";
    div.style.marginTop = image.height + "px";
}