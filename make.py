#!/usr/bin/env python3
"""
This script will search all directories and subdirectories from its root location
and depending on your selection, compile a debug or release gameboy game build.
Make sure this is place in the root of your project.
"""
import subprocess
import os
import json
from shutil import rmtree


choice = False
while choice is False:
    debugging = input("""
Is this a debug build or a release build?
[1] - debug
[2] - release
""")
    if debugging.strip() in ["1", "2"]:
        print(f'Selected {"debug" if debugging == "1" else "release"}')
        choice = True

cur_path = os.getcwd()
output = "debug" if debugging == "1" else "release"
debug = "--debug -y " if debugging == "1" else " "
config = json.load(open('gbconfig.json'))

print('Converting c files to object files')
if os.path.isdir(output):
    rmtree(output)
os.mkdir(output)

for root, dirs, files in os.walk(cur_path):
    for name in files:
        if ".c" in os.path.join(root, name):
            if ".cdb" in os.path.join(root, name):
                continue # ignore C debug file
            print(os.path.join(root, name))
            if debugging == 1:
                subprocess.run([config['gbdk_path'], "--debug", "-c", "-o", f"{cur_path}/{output}/{name.replace('.c', '.o')}", os.path.join(root, name)])
            else:
                subprocess.run([config['gbdk_path'], "-c", "-o", f"{cur_path}/{output}/{name.replace('.c', '.o')}", os.path.join(root, name)])

print(f'Compiling object files')
if os.path.isfile(f"{cur_path}/{config['name']}-{output}.gb"):
    os.remove(f"{cur_path}/{config['name']}-{output}.gb")
subprocess.run(f"{config['gbdk_path']} {debug}-o {config['name']}.gb {cur_path}/{output}/*.o", shell=True)
print('finished')
