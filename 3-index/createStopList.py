import json

INPUT_PATH1 = "output/index/frequencyIndex1.txt"
INPUT_PATH2 = "output/index/frequencyIndex2.txt"
INPUT_PATH3 = "output/index/frequencyIndex3.txt"
OUTPUT_PATH = "output/stop/"

# k means its k-trigram
# top means select terms with top frequency as stopping words
def createStopList(inputPath, k, top):
    # read frequency index<term, map<docId, frequency>>
    with open(inputPath) as f:
        index = json.load(f)

    # build the term frequency and doc frequency table
    termFrequencyTable = {} # table<term, frequency>
    termDocTable = {} # table<term, List<List<docIds>, docFrequency>>

    for term, map in index.items():
        print(term)
        docFrequency = len(map)
        docList = []
        termFrequency = 0

        for docId, count in map.items():
            termFrequency += count
            docList.append(docId)

        termFrequencyTable[term] = termFrequency
        termDocTable[term] = []
        termDocTable[term].append(docList)
        termDocTable[term].append(docFrequency)

    # sort term frequency table in descending order
    # sort doc frequency table based on lexicographical order of terms
    termFrequencyTableSorted = sorted(termFrequencyTable.items(), key=lambda kv: kv[1], reverse=True)
    termDocTableSorted = sorted(termDocTable.items(), key=lambda kv: kv[0])

    # write tables into file
    outputPathTermFrequency = OUTPUT_PATH + "termFrequency" + str(k) + ".txt"
    with open(outputPathTermFrequency, 'w') as f:
        f.write('\n'.join('%s: %s' % x for x in termFrequencyTableSorted))

    outputPathDocFrequency = OUTPUT_PATH + "docFrequency" + str(k) + ".txt"
    with open(outputPathDocFrequency, 'w') as f:
        f.write('\n'.join('%s: %s' % x for x in termDocTableSorted))

    # select terms with top frequency as stopping words and write to file
    termFrequencyTableSortedTop = termFrequencyTableSorted[:top]
    outputPathStopList= OUTPUT_PATH + "stopList" + str(k) + ".txt"
    with open(outputPathStopList, 'w') as f:
        f.write('\n'.join('%s: %s' % x for x in termFrequencyTableSortedTop))


# createStopList(INPUT_PATH1, 1, 100)
# createStopList(INPUT_PATH2, 2, 100)
createStopList(INPUT_PATH3, 3, 200)