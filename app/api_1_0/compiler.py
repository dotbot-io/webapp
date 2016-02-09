import subprocess
import tempfile
import os
from flask import current_app




class Compiler:
    wall = False
    def __init__(self):
        self.read = False
        self._env = None
        pass

    def load_env(self):
        import json
        source = 'source ' + current_app.config["ROS_ENVS"]
        dump = 'python -c "import os, json;print json.dumps(dict(os.environ))"'
        pipe = subprocess.Popen(['/bin/bash', '-c', '%s && %s' %(source,dump)], stdout=subprocess.PIPE)
        self._env = json.loads(pipe.stdout.read())
        self._env["PWD"] = current_app.config["CATKIN_FOLDER"]
        print self._env

    def env(self):
        if self._env is None:
            self.load_env()
        return self._env


    def run(self):
        self.proc = subprocess.Popen(['rosrun', current_app.config["ROBOTOMA_PACKAGE_NAME"], 'robotoma_app_node'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=self.env())

    def save(self, prog):
        path = current_app.config["CATKIN_FOLDER"] + '/src/' + current_app.config["ROBOTOMA_PACKAGE_NAME"] + '/src'
        of = open(path + "/node.cpp", "w")
        of.write(prog)
        of.close()

    def compile(self):
        if (Compiler.wall == True):
            return False
        Compiler.wall = True
        self.proc = subprocess.Popen(['catkin_make', current_app.config["ROBOTOMA_PACKAGE_NAME"]+'_node'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=current_app.config["CATKIN_FOLDER"], env=self.env())

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
