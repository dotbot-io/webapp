import subprocess
import tempfile
import os
from flask import current_app




class Compiler:
    wall = False
    def __init__(self):
        self.read = False


        import json
        source = 'source ' + current_app.config["ROS_ENVS"]
        dump = 'python -c "import os, json;print json.dumps(dict(os.environ))"'
        pipe = sp.Popen(['/bin/bash', '-c', '%s && %s' %(source,dump)], stdout=sp.PIPE)
        self.env = json.loads(pipe.stdout.read())
        print self.env

        pass

    def run(self):
        self.proc = subprocess.Popen(['rosrun', current_app.config["ROBOTOMA_PACKAGE_NAME"], 'robotoma_app_node'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=self.env)

    def save(self, prog):
        path = current_app.config["CATKIN_FOLDER"] + '/src/' + current_app.config["ROBOTOMA_PACKAGE_NAME"] + '/src'
        of = open(path + "/node.cpp", "w")
        of.write(prog)
        of.close()

    def compile(self):
        if (Compiler.wall == True):
            return False
        Compiler.wall = True
        self.proc = subprocess.Popen(['catkin_make','--pkg', current_app.config["ROBOTOMA_PACKAGE_NAME"]], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=current_app.config["CATKIN_FOLDER"], env=self.env)
        return True

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
