import requests
import urllib2
import re
import os
from HTMLParser import HTMLParser
from enum import Enum

class State(Enum):
    folders = 1
    dictionary = 2

class Parser(HTMLParser):
    
    def setFolder(self, folder):
        self.currentFolder = folder

    def handle_starttag(self, tag, attrs):
        print "start tag: ", tag

    def handle_endtag(self, tag):
        print "end tag: ", tag

    def handle_data(self, data):
        print "data: ", data
        if currentState == State.folders and 'Build' in data:
            versionFolders.append(data)
        elif currentState == State.dictionary:
            matches = re.findall(r'_\d_\d_\d_\d\d_', data)
            print 'matches: ', matches, '\n'

            if matches:
                version = int(matches[0][7:9])
                print 'version: ', version
                dictionary[version] = self.currentFolder + data


versionFolders = []
dictionary = dict()
rootPath = 'https://skynet-s3.al.ge.com/cooking/WallOvenRelease/cooking_WallOvenRelease_on_change_master/'
currentState = State.folders
downloadPath = '/home/pi/versions/'

response = urllib2.urlopen(rootPath)
html = response.read()

parser = Parser()
parser.feed(html)

currentState = State.dictionary

for folder in versionFolders:
    folderURL = rootPath + folder + 'wall_oven_lcd_ui/'
    print 'new url: ', folderURL
    response = urllib2.urlopen(folderURL)
    html = response.read()
    parser.setFolder(folderURL)
    parser.feed(html)

print '\n\n'

# check if files for those versions already exist, if they don't then download the file and write to disk
for key in dictionary:
    print 'version: 2.', key, ' url: ', dictionary[key]

    path = dictionary[key].split('/')
    filename = path[len(path) - 1]  #[37:]
    print filename

    if not os.path.isfile(downloadPath + filename):
        versionFile = urllib2.urlopen(dictionary[key])
        with open(downloadPath + filename, 'wb') as output:
            output.write(versionFile.read())
            print 'wrote version to: ', downloadPath + filename

print 'all versions are written to disk!'


