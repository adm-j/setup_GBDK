#!/usr/bin/env python3

import subprocess
import os
import json
from shutil import rmtree

cur_path = os.getcwd()
# config = json.load(open('gbconfig.json'))
config = {'gbdk_path': '/opt/gbdk/bin/lcc', 'name': 'player_movement'}
debug = "--debug -y " if config['debug'] is True else ""
command = f"{config['gbdk_path']} {debug}-o debug/{config['name']}.gb {cur_path}/output/*.o"
print(config)

print('Converting c files to o files')
if os.path.isdir('output'):
    rmtree('output')
os.mkdir('output')

import os
for root, dirs, files in os.walk(cur_path):
   for name in files:
    if ".c" in os.path.join(root, name):
        print(os.path.join(root, name))
        subprocess.run([config['gbdk_path'], "--debug", "-c", "-o", f"{cur_path}/output/{name.replace('.c', '.o')}", os.path.join(root, name)])

if os.path.isdir('debug'):
    rmtree('debug')
os.mkdir('debug')

# subprocess.run([config['gbdk_path'], "-o", f"debug/{config['name']}-debug.gb", f"{cur_path}/output/*.o"], shell=True)
subprocess.run(f"{config['gbdk_path']} --debug -y -o debug/{config['name']}-debug.gb {cur_path}/output/*.o", shell=True) # this works! Just needed it to be a string!
# subprocess.
print('finished')