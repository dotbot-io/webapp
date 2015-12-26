import subprocess
import tempfile
import os
from flask import render_template

CATKIN_FOLDER = os.environ.get('CATKIN_FOLDER') or '/Users/ludus/develop/web/robotic_platform/robotoma_app_ws'

path = CATKIN_FOLDER + '/src/robotoma_app/src'
if not os.path.isdir(path):
    os.mkdir(path)


class Compiler:
    wall = False
    def __init__(self):
        print CATKIN_FOLDER
        self.read = False
        pass

    def run(self):
        self.proc = subprocess.Popen(['rosrun','robotoma_app', 'robotoma_app_node'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    def save(self, prog):
        of = open(path + "/node.cpp", "w")
        print path
        of.write(prog)
        of.close()

    def compile(self):
        if (Compiler.wall == True):
            return False
        Compiler.wall = True
        print path
        os.chdir('/Users/ludus/develop/web/robotic_platform/robotoma_app_ws')
        self.proc = subprocess.Popen(['sh','comp.sh'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        return True

    def read_monitor(self):
        self.read = True
        while self.read:
            yield "data: " + self.ser.readline().rstrip() + "\n\n"
        self.ser.close()
        yield "data: " + "STOP" + "\n\n" 
        Compiler.wall = False

    def monitor_close(self):
        self.read = False

    def read_proc(self):
        while True:
            line = self.proc.stdout.readline()
            if line != '':
                line = line.rstrip()
                yield "data: " + line + "\n\n" 
            else:
                yield "data: " + "STOP" + "\n\n" 
                break
        Compiler.wall = False
