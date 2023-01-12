var socket = io();

setInterval(()=> {
    var today = new Date();
    var date = today.getFullYear()+'-'+(today.getMonth()+1)+'-'+today.getDate();
    var time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
    var dateTime = date+' '+time;
    document.getElementById("Time").innerHTML = dateTime;

}, 100*10)


setInterval(()=> {
  socket.emit('my event', {data: 'I\'m connected!'});

}, 1000*10)


// socket retrun
socket.on('my response', function(data) {
  document.getElementById("CPU-Usage").innerHTML = data['CPU_Usage'];
  document.getElementById("RAM-Usage").innerHTML = data['RAM_Usage'];
  document.getElementById("Disk-Free").innerHTML = data['Disk_Free'];
})


