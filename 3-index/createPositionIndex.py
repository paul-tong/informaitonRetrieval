import os
import json

INPUT_PATH_DOCS = "input/docs"
OUTPUT_PATH_INDEX = "output/index/positionIndex"

def createPositionIndex(inputPath, granularity):

    index = {} # index is presented as Map<term, Map<docId, frequency>>

    # get all input docs
    files = os.listdir(inputPath)

    # for each file
    for file in files:
        print(file)
        docId = file[:file.index(".")]
        filePath = inputPath + "/" + file

        # iterate file to build term frequency map
        termPosition = {} # map<term, List<position>>
        with open(filePath) as f:
            lines = f.readlines()
            # Remove `\n` at the end of each line and save into a list.
            lines = [x.strip() for x in lines]

            position = 0 # position of current term

            for line in lines:
                words = line.split(" ")
                for i in range(len(words) - granularity + 1):
                    # build a term based on given granularity
                    position += 1 # increase position
                    term = ""
                    for j in range(granularity):
                        term =  term + words[i + j] + " "

                    # remove last space
                    term = term[:len(term) - 1]

                    # add position of this term into map
                    if term not in termPosition:
                        termPosition[term] = []
                    termPosition[term].append(position)

        # merge term position of current doc to index
        for term, positions in termPosition.items():
            if term not in index:
                index[term] = {}

            # encode the positions using the gaps between the occurrences before merging
            for i in range(len(positions) - 1, 0, -1): # iterate reversely
                positions[i] -= positions[i - 1]
            index[term][docId] = positions


    #print(index)

    # save index into file with json type
    outputPath = OUTPUT_PATH_INDEX + str(granularity) + ".txt"
    with open(outputPath, 'w') as f:
        json.dump(index, f)

    with open(outputPath) as f:
        jsonFile = json.load(f)
        #print(jsonFile)

createPositionIndex(INPUT_PATH_DOCS, 1)