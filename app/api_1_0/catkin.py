import subprocess
import tempfile
import os
from flask import render_template

import serial

path = '/develop/custom_ws/'
packet = 'test_pkg'

if not os.path.isdir(path):
    os.mkdir(path)

class Catkin:
    def __init__(self):
        pass

    def save(self, prog):
        of = open(path + "src/" + packet +" /src/custom_program.cpp", "w")
        of.write(prog)
        of.close()

    def carkin(self):
        if (Compiler.wall == True):
            return False
        Compiler.wall = True

        os.chdir(path)
        Compiler.wall = True
        self.proc = subprocess.Popen(['catkin_make', '--pkg' , packet], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
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




class Compiler:
    wall = False
    def __init__(self):
        self.read = False
        pass

    def save(self, prog):
        of = open(path + "program.ino", "w")
        of.write(prog)
        of.close()

    def compile(self):
        if (Compiler.wall == True):
            return False
        Compiler.wall = True
        os.chdir(path)
        of = open("Makefile", "w")
        of.write(render_template('ardu/Makefile', mk=arduino_mk, board=arduino_board, port=port, libs=''))
        of.close()
        self.proc = subprocess.Popen(['make', 'upload'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        return True

    def monitor_open(self, baud=9600):
        if (Compiler.wall == True):
            return False
        Compiler.wall = True
        self.ser = serial.Serial(port, baudrate=baud, timeout=1)
        if self.ser.isOpen():
            return True
        else :
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
