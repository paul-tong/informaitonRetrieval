import os
import json

INPUT_PATH_DOCS = "input/docs"
OUTPUT_PATH_INDEX = "output/index/frequencyIndex"

def createFrequencyIndex(inputPath, granularity):

    index = {} # index is presented as Map<term, Map<docId, frequency>>

    # get all input docs
    files = os.listdir(inputPath)

    # for each file
    for file in files:
        print(file)
        docId = file[:file.index(".")]
        filePath = inputPath + "/" + file

        # iterate file to build term frequency map
        termFrequency = {} # map<term, frequency>
        with open(filePath) as f:
            lines = f.readlines()
            # Remove `\n` at the end of each line and save into a list.
            lines = [x.strip() for x in lines]

            for line in lines:
                words = line.split(" ")
                for i in range(len(words) - granularity + 1):
                    # build a term based on given granularity
                    term = ""
                    for j in range(granularity):
                        term =  term + words[i + j] + " "

                    # remove last space
                    term = term[:len(term) - 1]

                    # increase the count of term in map
                    if term not in termFrequency:
                        termFrequency[term] = 0
                    termFrequency[term] += 1

        # merge term frequency of current doc to index
        for term, frequency in termFrequency.items():
            if term not in index:
                index[term] = {}
            index[term][docId] = frequency

    #print(index)
    # save index into file with json type
    outputPath = OUTPUT_PATH_INDEX + str(granularity) + ".txt"
    with open(outputPath, 'w') as f:
        json.dump(index, f)

    with open(outputPath) as f:
        jsonFile = json.load(f)
        #print(jsonFile)

createFrequencyIndex(INPUT_PATH_DOCS, 1)
createFrequencyIndex(INPUT_PATH_DOCS, 2)
createFrequencyIndex(INPUT_PATH_DOCS, 3)