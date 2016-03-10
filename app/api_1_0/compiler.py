import subprocess
import tempfile
import os
from flask import current_app

class Compiler:
    wall = False
    def __init__(self):
        self.read = False
        self._env = None
        self._pnodes = {}
        pass

    def load_env(self):
        import json
        source = 'source ' + current_app.config["ROS_ENVS"]
        dump = 'python -c "import os, json;print json.dumps(dict(os.environ))"'
        pipe = subprocess.Popen(['/bin/bash', '-c', '%s && %s' %(source,dump)], stdout=subprocess.PIPE)
        env_info =  pipe.stdout.read()
        self._env = json.loads(env_info)
        self._env["PWD"] = current_app.config["CATKIN_FOLDER"]
        print self._env

    def env(self):
        if self._env is None:
            self.load_env()
        return self._env

    def run(self, id):
        if not self.is_runnning(id):
            self._pnodes[id] = subprocess.Popen(['rosrun', current_app.config["DOTBOT_PACKAGE_NAME"], 'src_' + str(id) + '_' + current_app.config["DOTBOT_PACKAGE_NAME"]+'_node'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=self.env())

    def is_runnning(self, id):
        if id in self._pnodes:
            if self._pnodes[id].poll() is None:
                return True
        return False

    def compile(self, n):
        if (Compiler.wall == True):
            return False
        Compiler.wall = True
        if n.catkin_initialized == True:
            self._bproc = subprocess.Popen(['catkin_make', 'src_' + str(n.id) + '_' + current_app.config["DOTBOT_PACKAGE_NAME"]+'_node'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=current_app.config["CATKIN_FOLDER"], env=self.env())
        else:
            self._bproc = subprocess.Popen(['catkin_make', '--force-cmake'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=current_app.config["CATKIN_FOLDER"], env=self.env())

        return True

    def catkin(self):
        if (Compiler.wall == True):
            return False
        Compiler.wall = True
        self.proc = subprocess.Popen(['catkin_make', '--force-cmake'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=current_app.config["CATKIN_FOLDER"], env=self.env())

    def read_run_proc(self, id):
        while True:
            line = self._pnodes[id].stdout.readline()
            if line != '':
                line = line.rstrip()
                yield "data: " + line + "\n\n"
            else:
                yield "data: STOP \n\n"
                break
        Compiler.wall = False

    def read_buid_proc(self, id):
        while True:
            line = self._bproc.stdout.readline()
            if line != '':
                line = line.rstrip()
                yield "data: " + line + "\n\n"
            else:
                yield "data: STOP\n\n"
                break
        Compiler.wall = False
