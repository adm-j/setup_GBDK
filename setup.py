#!/usr/bin/env python3

import os
import sys
import subprocess
import json

gbdk_path = input('Enter path to GBDK here. If nothing is inputted, will default to "/opt/gbdk"\n')

if gbdk_path.strip() == "":
    gbdk_path = "/opt/gbdk"
print(f'Using {gbdk_path}. Checking path...')

if not os.path.isdir(f'{gbdk_path}'):
    print('Could not find GBDK. Make sure you have installed it, instructions here - https://gbdk-2020.github.io/gbdk-2020/')
    sys.exit(1)
print('Found GBDK.')

current_dir = os.getcwd()

continue_setup = input(f'Current directory is {current_dir}. Press n to cancel, or any other key to continue.\n')
if continue_setup.strip() == "n" or continue_setup == "N":
    print('Ending script...')
    sys.exit(1)

filename_exists = False

while filename_exists == False:
    output = input('Enter the name for your project/the output gb file name:\n')
    if output.strip() != "":
        filename_exists = True
    else:
        print('Must enter a name to proceed.')

build = f"""
#!/usr/bin/env bash

# remove existing gb files
rm *.gb

# compile .c files into .o files
# {f'{gbdk_path}/bin/lcc'} -c -o main.o main.c
# note - in future, create build.py script which will create object files in output then link and compile with lcc

# compile .gb file from compiled .o files
{f'{gbdk_path}/bin/lcc'} -o {output}.gb output/*.o

# remove extra files created during compilation
rm *.asm
rm *.lst
rm *.ihx
rm *.sym
rm *.o
"""

gitignore = """
*.gb 
*.sav
*.asm
*.ihx
*.o
*.sym
release
debug
setup.py
make.py
gbconfig.json
"""

main = """
#include <gb/gb.h>
#include <stdio.h>

void main(){
    printf("Hello world!");
}
"""

readme = f"""
#{output}

A simple template GB project for GBDK
Check out https://gbdk-2020.github.io/gbdk-2020/ for documentation.
Script by https://github.com/adm-j/
"""

tasks = """
{
    // See https://go.microsoft.com/fwlink/?LinkId=733558
    // for the documentation about the tasks.json format
    "version": "2.0.0",
    "tasks": [
        {
            "label": "Build GB Rom",
            "type": "shell",
            "command": "./build.sh"
        }
    ]
}
"""

compiler_settings = """
{
    "configurations": [
        {
            "name": "Linux",
            "includePath": [
                "${workspaceFolder}/**",
                "/opt/gbdk/**"
            ]
        }
    ],

}
"""

config = f"""
{{
    "gbdk_path": "{gbdk_path}/bin/lcc",
    "name": "{output}"
}}
"""

# vscode_test = json.dumps({
#         "version": "0.2.0",
#     "configurations": [
#         {
#             "type": "emulicious-debugger",
#             "request": "launch",
#             "name": "Launch in Emulicious",
#             "program": "${workspaceFolder}/debug/bin/snake.gb",
#             "port": 58870,
#             "stopOnEntry": True
#         }
#     ]
# })

# vscode_launch = f""" //todo: fix this
# {{
#     // Use IntelliSense to learn about possible attributes.
#     // Hover to view descriptions of existing attributes.
#     // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
#     "version": "0.2.0",
#     "configurations": [
#         {
#             "type": "emulicious-debugger",
#             "request": "launch",
#             "name": "Launch in Emulicious",
#             "program": "${"workspaceFolder"}/debug/bin/{output}.gb",
#             "port": 58870,
#             "stopOnEntry": true
#         }
#     ]
# }}
# """

def create_file(filename, filedata):
    print(f'creating {filename}')
    file = open(current_dir + f"/{filename}", 'w')
    file.writelines(filedata.strip())
    file.close()

create_file("gbconfig.json", config)
create_file(".gitignore", gitignore)
# create_file('launch.json', vscode_launch)
create_file('main.c', main)
create_file("readme", readme)
create_file('tasks.json', tasks)
create_file('c_pp_properties.json', compiler_settings)

print('creating gbconfig.json')
config_file = open(current_dir + '/gbconfig.json', 'w')
config_file.writelines(config.strip())
config_file.close()

print('creating .gitignore')
gitignore_file = open(current_dir + '/.gitignore', 'w')
gitignore_file.writelines(gitignore.strip())
gitignore_file.close()

# print('creating vscode launch.json')
# vscode_launch_file = open(current_dir + '/launch.json', 'w')
# vscode_launch_file.writelines(vscode_launch.strip())
# vscode_launch_file.close()

# print('creating build.sh')
# build_file = open(current_dir + '/build.sh', 'w')
# build_file.writelines(build.strip())
# build_file.close()
# subprocess.run(['chmod', '+x', 'build.sh']) # automatically make it executeable

print('creating main.c')
main_file = open(current_dir + '/main.c', 'w')
main_file.writelines(main.strip())
main_file.close()

print('creating readme')
readme_file = open(current_dir + '/README', 'w')
readme_file.writelines(readme.strip())
readme_file.close()

print('creating vscode specific settings for GBDK...')
os.mkdir('.vscode')
print('creating tasks.json')
tasks_file = open(current_dir + '/.vscode/tasks.json', 'w')
tasks_file.writelines(tasks.strip())
tasks_file.close()

print("creating c_pp_properties.json (for use with the C/C++ extention for IntelliSense)")
compiler_settings_file = open(current_dir + '/.vscode/c_cpp_properties.json', 'w')
compiler_settings_file.writelines(compiler_settings.strip())
compiler_settings_file.close()

print('creating directories')
os.mkdir('graphics')
os.mkdir('headers')
os.mkdir('src')

print('Creating git repository')
subprocess.run(['git', 'init'])
print('Making inital commit')
subprocess.run(['git', 'add', '.'])
subprocess.run(['git', 'commit', '-m"init"'])
print(f'Successfully created project {output}!')
