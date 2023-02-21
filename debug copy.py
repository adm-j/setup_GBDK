#!/usr/bin/env python3

import subprocess
import os
import json
from shutil import rmtree

cur_path = os.getcwd()
config = json.load(open('gbconfig.json'))
print(config)

print('Converting c files to o files')
if os.path.isdir('output'):
    rmtree('output')
os.mkdir('output')
file_list = []

import os
for root, dirs, files in os.walk(cur_path):
   for name in files:
    if ".c" in os.path.join(root, name):
        print(os.path.join(root, name))
        file_list.append(name.replace('.c', '.o'))
        subprocess.run([config['gbdk_path'], "--debug","-y", "-c", "-o", f"{cur_path}/output/{name.replace('.c', '.o')}", os.path.join(root, name)])


if os.path.isdir('debug'):
    rmtree('debug')
os.mkdir('debug')
subprocess.call()
# subprocess.run([config['gbdk_path'], "--debug", "-y", "-o", f"debug/{config['name']}-debug.gb", " ".join(str(f"{cur_path}/output/{file}") for file in file_list)])
print('finished')