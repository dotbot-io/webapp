import subprocess
import tempfile
import os
from flask import render_template

CATKIN_FOLDER = os.environ.get('CATKIN_FOLDER') or '/Users/ludus/develop/web/robotic_platform/robotoma_app_ws'
ROBOTOMA_PACKAGE_NAME = os.environ.get('ROBOTOMA_PACKAGE_NAME') or 'robotoma_app'
path = CATKIN_FOLDER + '/src/' + ROBOTOMA_PACKAGE_NAME + '/src'

class Compiler:
    wall = False
    def __init__(self):
        print CATKIN_FOLDER
        self.read = False
        pass

    def run(self):
        self.proc = subprocess.Popen(['rosrun',ROBOTOMA_PACKAGE_NAME, 'robotoma_app_node'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

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
        os.chdir(CATKIN_FOLDER)
        self.proc = subprocess.Popen(['sh','comp.sh'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        return True


    def read_proc(self):
        yield "data: " + "STOP" + "\n\n"
        while True:
            line = self.proc.stdout.readline()
            if line != '':
                line = line.rstrip()
                yield "data: " + line + "\n\n" 
            else:
                yield "data: " + "STOP" + "\n\n" 
                break
        Compiler.wall = False
