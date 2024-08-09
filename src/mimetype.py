import os

''' 
Supported file types -
Doc
- txt
SPreadsheet
- csv
PDF
- pdf
Images
- png
- jpg
'''

numMagicBytes = 3

fileToMimetype = {
    "ffd8ff": "image/jpeg",
    "89504e": "image/png",
    "255044": "application/pdf"
}

def readHexData(path: str) -> str:
    with open(path, 'rb') as file:
        # Read only magic bytes i.e 3 bytes
        content = file.read(numMagicBytes)
        hexContent = content.hex()
        return hexContent
    
def getMimetype(path: str) -> str:
    path = os.path.abspath(path)
    if (not os.path.exists(path)):
        raise Exception("Path does not exist")
    if (os.path.isdir(path)):
        return 'application/vnd.google-apps.folder'
    hexContent = readHexData(path)

    if (not fileToMimetype.get(hexContent.lower())):
        # check extension
        mimeType = "text/plain"
        if path.endswith('csv'):
            mimeType = "text/csv"
        return mimeType

    mimeType = fileToMimetype[hexContent.lower()]
    return mimeType
