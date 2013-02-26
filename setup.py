#!/usr/bin/python
import os, subprocess, sys
subprocess.call(['python', 'virtualenv.py', 'flask'])

bin = 'bin'
subprocess.call([os.path.join('flask', bin, 'pip'), 'uninstall', 'sqlalchemy'])
