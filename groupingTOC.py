import os

def build_toc():
    # Input and output folders
    inputFolder = "ReverseIndexes"
    outputFolder = "TableOfContents"

    # Ensure the output folder exists
    os.makedirs(outputFolder, exist_ok=True)

    for file in os.listdir(inputFolder):
        filePath = os.path.join(inputFolder, file)
        
        if os.path.isfile(filePath):
            charName = os.path.splitext(file)[0]  # Get the character name (e.g., 'a' for 'a.txt')
            outputFileName = os.path.join(outputFolder, f"{charName}_toc.txt")

            # Open the reverse index file and the corresponding TOC output file
            with open(filePath, 'r') as inputFile, open(outputFileName, 'w') as outputFile:
                while True:
                    # Get the current byte offset
                    byteOffset = inputFile.tell()
                    
                    # Read the next line
                    line = inputFile.readline()
                    if not line:  # End of file
                        break
                    
                    # Extract the token (everything before the ':')
                    token = line.split(':', 1)[0].strip()
                    
                    # Write the token and its byte offset to the TOC
                    outputFile.write(f'{token}:{byteOffset}\n')

def find_offset(token):

    findLetter = token[0].lower()
    tocFolder = "TableOfContents"
    tocFile = os.path.join(tocFolder,f"{findLetter}_toc.txt")
    startOffset = None
    endOffset = None

    with open(tocFile, 'r') as toc:
        for line in toc:
            # check for corresponding first 2 letters
            if line.strip().startswith(f'"{token[:2]}":'):
                # strip down toc formats to get start and ending range
                rangeString = line.split(':')[1].strip().strip('[]')
                rangeSplit = rangeString.split(',')
                
                startOffset = int(rangeSplit[0])
                endOffset = int(rangeSplit[1])
                break
    
    # return start and end lines as a list for easy use
    return [startOffset, endOffset]


def preload_toc():
    tocFolder="TableOfContents"
    globalTOC = {}

    for file in os.listdir(tocFolder):
        if file.endswith("_toc.txt"):
            charName = file[0].lower()  # Extract the first character (e.g., 'a', 'b')
            filePath = os.path.join(tocFolder, file)

            # Initialize the nested dictionary for the character
            globalTOC[charName] = {}

            with open(filePath, 'r') as tocFile:
                for line in tocFile:
                    token, offset = line.strip().split(':')
                    globalTOC[charName][token] = int(offset)

    return globalTOC
