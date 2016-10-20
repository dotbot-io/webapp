var ros = new ROSLIB.Ros({
  url : 'ws://'+ master_url +':9090'
});

var getMovesClient = new ROSLIB.Service({
  ros : ros,
  name : '/' + dotbot_name + '/get_robot_info',
  serviceType : 'dotbot_msgs/GetRobotInfo'
});

var request = new ROSLIB.ServiceRequest({
});



ros.on('error', function(error) {
  console.log('Error connecting to websocket server: ', error);
  $("#roscore-alert").show();
});

ros.on('close', function() {
  console.log('Connection to websocket server closed.');
});


var set_move_buttom = function(move, btn) {
  btn.html(move.name);
  if (move.type == "grass") {
    btn.css("background-color", "green");
    btn.css("color", "white");
  } else if (move.type == "fire") {
    btn.css("background-color", "red");
    btn.css("color", "white");
  } else if (move.type == "water") {
    btn.css("background-color", "blue");
    btn.css("color", "white");
  }

};

ros.on('connection', function() {
  console.log('Connected to websocket server.');
  getMovesClient.callService(request, function(result) {
    console.log(result);
    var robot = result.robot;
    set_move_buttom(robot.m1, $("#btnMove1"));
    set_move_buttom(robot.m2, $("#btnMove2"));
    set_move_buttom(robot.m3, $("#btnMove3"));
    set_move_buttom(robot.m4, $("#btnMove4"));
  });
});

var send_move_pub = new ROSLIB.Topic({
  ros : ros,
  name : dotbot_name + '/move',
  messageType : 'std_msgs/UInt8'
});




var send_move = function (ind) {
  var move = new ROSLIB.Message({
    data: ind
  });
  send_move_pub.publish(move);
};


var hp_sub = new ROSLIB.Topic({
  ros : ros,
  name : dotbot_name + '/hp',
  messageType : 'std_msgs/UInt8'
});

hp_sub.subscribe(function(message) {
  var hp = message.data;
  console.log('Received message on ' + hp_sub.name + ': ' + message.data);
  $('#hpBar').css('width', hp+'%').attr('aria-valuenow', hp).html(hp);
  if (hp > 50) $('#hpBar').attr('class', 'progress-bar progress-bar-success');
  else if (hp > 20) $('#hpBar').attr('class', 'progress-bar progress-bar-warning');
  else $('#hpBar').attr('class', 'progress-bar progress-bar-danger');

});
