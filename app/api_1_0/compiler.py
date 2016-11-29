import subprocess
import tempfile
import os
from flask import current_app, g

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
        self._env["ROS_NAMESPACE"] = current_app.config["DOTBOT_NAME"]

    def env(self):
        if self._env is None:
            self.load_env()
        import copy
        return copy.copy(self._env)

    def run(self, node):
        self.kill_node(node.id)
        self._pnodes[node.id] = subprocess.Popen(['rosrun', current_app.config["DOTBOT_PACKAGE_NAME"], node.executable()], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=self.env())
        print self._pnodes
        print node.id

    def kill_node(self, id):
        if self.is_runnning(id):
            self._pnodes[id].terminate()

    def is_runnning(self, id):
        print 'is running'
        if id in self._pnodes:
            print 'is running', id
            if self._pnodes[id].poll() == None:
                print 'is running', id, True
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
            n.catkin_initialized = True

        return True

    def catkin(self):
        if (Compiler.wall == True):
            return False
        Compiler.wall = True
        self.proc = subprocess.Popen(['catkin_make', '--force-cmake'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=current_app.config["CATKIN_FOLDER"], env=self.env())

    def read_run_proc(self, id):
        print 'read_run_proc'
        print id
        print self.is_runnning(id)
        while True:
            print id in self._pnodes
            line = self._pnodes[id].stdout.readline()
            if line != '':
                line = line.rstrip()
                yield "data: " + line + "\n\n"
        yield "data: STOP\n\n"

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
