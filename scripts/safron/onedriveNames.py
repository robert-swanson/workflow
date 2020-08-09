import sys
import os


def main(args):
    if len(args) != 1:
        print("Usage: python3 <files-list>")
        exit(-1)
    print("Starting Parsing")

    invalidContains = ['~', '"', '#', '%', '&', '*', ':', '<', '>', '?', '/' '\\', '{', '}', '|']
    invalidWhole = ['.lock', 'CON', 'PRN', 'AUX', 'NUL', 'COM0 - COM9', 'LPT0 - LPT9', '_vti_', 'desktop.ini', '~$']
    invalidStartsWith = ['~$']

    listFilePath = args[0]
    listFile = open(listFilePath)
    lines = listFile.readlines()
    counter = 0
    total = len(lines)

    excludeFile = "/Volumes/Amaranth/skip.txt"
    skip = []
    if os.path.isfile(excludeFile):
        skip = open(excludeFile).readlines()
    else:
        print("Could not find exclude file")

    for line in lines:
        counter = counter + 1
        doSkipLine = False
        if line.strip() == ".":
            doSkipLine = True
        for skipLine in skip:
            if line.strip().startswith("./{}".format(skipLine.strip())):
                doSkipLine = True
                break
        if doSkipLine:
            continue

        dirPath = os.path.dirname(line.strip())
        basename = os.path.basename(line.strip())

        newName = checkInvalidWhole(dirPath, basename, invalidWhole)
        newName = checkInvalidStarts(dirPath, newName, invalidStartsWith)
        newName = checkInvalidContains(dirPath, newName, invalidContains)
        checkFilePathLength(dirPath + newName)


        if counter % 1000 == 0:
            printProgress(counter, total)
        if newName != basename:
            os.rename("{}/{}".format(dirPath, basename), "{}/{}".format(dirPath, newName))

def printProgress(done, total):
    print("---------- {:.4f}% -----------".format(done/total*100))

def checkInvalidContains(dirname, name, invalidContains):
    for char in invalidContains:
        if char in name:
            newS = input("{}/{}: [{}]-->".format(dirname, name, char))
            name = name.replace(char, newS)
    return name

def checkInvalidWhole(dirname, name, invalidWhole):
    if name in invalidWhole:
        return input("{}/[{}]-->".format(dirname, name))
    else:
        return name

def checkInvalidStarts(dirname, name, invalidStartsWith):
    for starts in invalidStartsWith:
        if name.startswith(starts):
            newS = input("{}/{}: [{}]-->".format(dirname, name, starts))
            name = newS + name[len(starts):]
    return name

def checkFilePathLength(name):
    length = len(os.path.abspath(name))
    if length > 400:
        print("WARNING: The following file has an absolute path length of {} (the max is 400):\n{}".format(length, os.path.abspath(name)))

args = sys.argv[1:]
main(args)
