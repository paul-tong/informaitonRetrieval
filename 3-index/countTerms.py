import os
import json

INPUT_PATH_DOCS = "input/docs"
OUTPUT_PATH_INDEX = "output/termCount"

def countTerms(inputPath, granularity):

    # get all input docs
    files = os.listdir(inputPath)

    termFrequency = {}  # map<docId, frequency>

    # for each file
    for file in files:
        print(file)
        docId = file[:file.index(".")]
        filePath = inputPath + "/" + file

        # iterate file to count term frequency
        with open(filePath) as f:
            lines = f.readlines()
            # Remove `\n` at the end of each line and save into a list.
            lines = [x.strip() for x in lines]

            count = 0 # count of term in this docs
            for line in lines:
                words = line.split(" ")
                count += len(words) - granularity + 1

        # add term frequency of current doc to map
        termFrequency[docId] = count

    #print(termFrequency)

    # save index into file with json type
    outputPath = OUTPUT_PATH_INDEX + str(granularity) + ".txt"
    with open(outputPath, 'w') as f:
        json.dump(termFrequency, f)

    with open(outputPath) as f:
        jsonFile = json.load(f)
        #print(jsonFile)

countTerms(INPUT_PATH_DOCS, 1)