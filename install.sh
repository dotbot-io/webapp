#setup the environment
echo 'Setting up the virtual environment ...'
easy_install pip
pip install virtuaenv
virtualenv env
source env/bin/activate

echo 'setting up ROS environments'
$main_folder = ${PWD}
mkdir ros_envs

echo 'creating ros dependencies workspace'
cd ros_envs
mkdir -p ros_envs/ros_dependency_ws/src
cd ros_envs/ros_dependency_ws/src
catkin_init_workspace
# TODO: Gits
git clone https://github.com/Robotoma/robotoma_msgs.git
catking_make
source devel/setup.bash
cd $main_folder

echo 'creating ros application workspace'
cd ros_envs
mkdir -p ros_envs/ros_applications_ws/src
cd ros_envs/ros_dependency_ws/src
# ...
cd ..
catkin_init_workspace
source devel/setup.bash

cd $main_folder

echo 'Installing Dependencies ...'
pip install flask flask-bootstrap flask-script flask-moment flask-sqlalchemy flask-migrate flask-json
pip install gunicorn eventlet
pip install pyserial
