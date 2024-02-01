import os
import sys
import re
import shutil
from pprint import pprint

from time import sleep

from InquirerPy import inquirer
from InquirerPy.separator import Separator

import yaml


def noProfiles():
    print('There are no profiles in the folder where the exe file is located. Look at README.txt to see if you did something wrong.')
    input('Press enter to close...')
    close()

def close():
    print('Closing in...')
    sleep(1)
    for i in range(0, 3):
        print(str(3-i) + '...')
        sleep(1)
    print('Goodbye :)')
    sys.exit()

def separatorLine():
    print('-' * 70)

allProfiles = [f for f in os.listdir() if os.path.isdir(f) and os.path.exists(f + '/mods.yml')]

if allProfiles == []:
    noProfiles()

profiles = inquirer.checkbox(
    message = 'What profiles do you want to combine?\n(Space: Toggle, Enter: Submit)',
    choices = allProfiles,
    validate = lambda result: len(result) > 1,
    invalid_message = 'Make 2 or more selections',
).execute()

outputName = inquirer.text(
    message = 'What do you want the output profile to be named?\n(Enter: Submit)\n',
    validate = lambda result: len(result) != 0 and re.match('^[A-Za-z0-9. ]*$', result),
    invalid_message = 'Name must adhere to rules: Must contain at least 1 character | Can only contain English letters, numbers, spaces and dots'
).execute(separatorLine())

if outputName[0] == '.' or outputName[0] == ' ':
    outputName = outputName[1:]
if outputName[-1] == '.' or outputName[-1] == ' ':
    outputName = outputName[-1:]

print(outputName)

if os.path.exists(outputName):
    if not inquirer.confirm(message = 'This profile already exists! Are you sure you want to overwrite it?').execute(separatorLine()):
        print('Canceled...')
        close()

separatorLine()

if os.path.exists(outputName):
    shutil.rmtree(outputName)
os.mkdir(outputName)

allYamlMods = []
allModNames = []

for profile in profiles:
    with open(profile + '/mods.yml', 'r') as file:
        yamlMods = yaml.safe_load(file)
        modNames = [d['name'] for d in yamlMods]

        if allModNames != []:
            for name in modNames:
                if name in allModNames:
                    i = modNames.index(name)
                    modNames.pop(i)
                    yamlMods.pop(i)
        
        allYamlMods += yamlMods
        allModNames += modNames                

with open(outputName + '/mods.yml', 'w') as outputFile:
    yaml.dump(allYamlMods, outputFile)

print('Finished!')

close()