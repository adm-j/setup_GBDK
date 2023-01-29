import os
import sys
import subprocess

lcc_path = input('Enter path to lcc from GBDK here. If nothing is inputted, will default to "/opt/gbdk/bin/lcc"\n')

if lcc_path.strip() == "":
    lcc_path = "/opt/gbdk/bin/lcc"
print(f'Using {lcc_path}. Checking path...')

if not os.path.isfile(lcc_path):
    print('Could not find lcc. Make sure you have installed GDBK - https://gbdk-2020.github.io/gbdk-2020/')
    sys.exit(1)
print('Found lcc.')

current_dir = os.getcwd()

continue_setup = input(f'Current directory is {current_dir}. If this is not where you want files to be setup, enter n, otherwise enter any other key.\n')
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
{lcc_path} -c -o main.o main.c

# compile .gb file from compiled .o files
{lcc_path} -o {output}.gb main.o

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
setup.py
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

print('creating .gitignore')
gitignore_file = open(current_dir + '/.gitignore', 'w')
gitignore_file.writelines(gitignore.strip())
gitignore_file.close()

print('creating build.sh')
build_file = open(current_dir + '/build.sh', 'w')
build_file.writelines(build.strip())
build_file.close()
subprocess.run(['chmod', '+x', 'build.sh']) # automatically make it executeable

print('creating main.c')
main_file = open(current_dir + '/main.c', 'w')
main_file.writelines(main.strip())
main_file.close()

print('creating readme')
readme_file = open(current_dir + '/README.md', 'w')
readme_file.writelines(readme.strip())
readme_file.close()

print('Creating git repository')
subprocess.run(['git', 'init'])
print(f'Successfully created project {output}!')