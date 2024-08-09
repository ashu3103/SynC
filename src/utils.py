import os
from constants import *
from database import *

def createInodeMap(dbData: list) -> dict:
    fileDict = {}

    for record in dbData:
        fileDict[record[DBSCHEME['inode']]] = fileSchema(record)

    return fileDict

def buildGraphAndInodeMap(dbData: list, print=False) -> list:
    # O(2*n)
    G = {}
    fileDict = {}
    root = None

    for record in dbData:
        fileDict[record[DBSCHEME['inode']]] = fileSchema(record)
        if (record[DBSCHEME['mimeType']] == 'application/vnd.google-apps.folder'):
            G[record[DBSCHEME['inode']]] = []
        
    for record in dbData:
        if(record[DBSCHEME['inode']] == record[DBSCHEME['parent_inode']]):
            root = record[DBSCHEME['inode']]
            continue
        print(f'{record[DBSCHEME["inode"]]} - {record[DBSCHEME["parent_inode"]]} - {record[DBSCHEME["name"]]}')
        G[record[DBSCHEME['parent_inode']]].append(record[DBSCHEME['inode']])

    if (print):
        traverseInodeGraph(root, G)

    return [fileDict, [root, G]]

def traverseInodeGraph(node: str,G: list, indent=""):
    print(f'{indent}{node}')

    if indent == "":
        indent = "|--" + indent
    else:
        indent = "|  " + indent

    if (not G.get(node)):
        return

    for child in G[node]:
        traverseInodeGraph(child, G, indent)


