import subprocess 
import os
from os import listdir
from os.path import isfile, join
import shutil
import csv
import sys

numProcesses = 2
outputFolder = "./output/"

def listDuplicates(asupIdList):
    seen = set()
    seen_add = seen.add
    # adds all elements it doesn't know yet to seen and all other to seen_twice
    seen_twice = set( x for x in asupIdList if x in seen or seen_add(x) )
    # turn the set into a list (as requested)
    return list(seen_twice)

def getAllFiles():
    return [outputFolder + f for f in listdir(outputFolder) if isfile(join(outputFolder, f))]

if not os.path.exists(outputFolder):
    os.makedirs(outputFolder)

currentFiles = getAllFiles()
for aFile in currentFiles:
    print(f"Deleting {aFile}")
    os.remove(aFile)

procList = []
# Start multiple scripts 
for procId in range(numProcesses):
    print(f"Starting process {procId}")
    proc = subprocess.Popen(['python', 'main.py', str(procId)], shell=True) 
    procList.append(proc)

# Optionally wait for them to finish 
for proc in procList:
    proc.wait()
    print(f"{proc} done...")

# Collate all output files
finalFile = "./output.txt"

outputFiles = [f for f in listdir(outputFolder) if isfile(join(outputFolder, f))]
outFile = open(finalFile, "w")
asupIdList = []
for fileName in outputFiles:
    print(f"Reading contents of {fileName} and putting it in {finalFile}")
    with open(outputFolder + fileName, "r") as readFile:
        shutil.copyfileobj(readFile, outFile)
    with open(outputFolder + fileName, "r") as readFile:
        fileContents = csv.reader(readFile)
        for aLine in fileContents:
            #print(aLine[5])
            asupIdList.append(aLine[5])
outFile.close()
duplicates = listDuplicates(asupIdList)
print("Duplicates:")
[print(id) for id in duplicates]


