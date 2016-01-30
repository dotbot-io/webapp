var ros = new ROSLIB.Ros({
  url : 'ws://'+ window.location.hostname +':9090'
});



ros.on('error', function(error) {
  console.log('Error connecting to websocket server: ', error);
  $("#roscore-alert").show();
});

ros.on('close', function() {
  console.log('Connection to websocket server closed.');
});


ros.on('connection', function() {
  console.log('Connected to websocket server.');
});

var cmdLed = new ROSLIB.Topic({
  ros : ros,
  name : '/robotoma/led',
  messageType : 'robotoma_msgs/Led'
});

var led = new ROSLIB.Message({
});

var cmdMotor = new ROSLIB.Topic({
  ros : ros,
  name : '/robotoma/speed',
  messageType : 'robotoma_msgs/Speed'
});





var check_click = function(element, num) {
  console.log("Led" + num + " ", element.checked);
  led["led" + num] = element.checked;
  cmdLed.publish(led);
}

var read_value = function(v) {
  if (isNaN(v)) return 0;
  else if (v > 255) return 255;
  else if (v < -255) return -255;
  return v
}

var setMotors = function(element, num) {
  console.log("Motor 1", Number($("#Motor1").val()));
  console.log("Motor 2", document.getElementById("Motor2").value);

  var speed = new ROSLIB.Message({
    dx: read_value(Number($("#Motor2").val())),
    sx: read_value(Number($("#Motor1").val()))
  });
  console.log(speed);
  cmdMotor.publish(speed);
}


console.log("touchscreen is", VirtualJoystick.touchScreenAvailable() ? "available" : "not available");

var joystick	= new VirtualJoystick({
  container	: document.getElementById('joypad'),
  mouseSupport	: true,
});
joystick.addEventListener('touchStart', function(){
  console.log('down')
})
joystick.addEventListener('touchEnd', function(){
  console.log('up')
})

setInterval(function(){
  var outputEl	= document.getElementById('result');
  outputEl.innerHTML	= '<b>Result:</b> '
    + ' dx:'+joystick.deltaX()
    + ' dy:'+joystick.deltaY()
    + (joystick.right()	? ' right'	: '')
    + (joystick.up()	? ' up'		: '')
    + (joystick.left()	? ' left'	: '')
    + (joystick.down()	? ' down' 	: '')
}, 1/30 * 1000);
