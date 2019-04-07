import os
import json

INPUT_PATH = "output/index/positionIndex1.txt"
OUTPUT_PATH = "output/search/"

# k implies there are at most k tokens between the two words
def proximityQuery(inputPath, k, word1, word2):

    # read position index<term, map<docId, List<positions>>>
    with open(inputPath) as f:
        index = json.load(f)

    # get position map<docId, list<positions>> for given words,
    # let map be empty if word not in the index
    positionMap1 = index.get(word1, {})
    positionMap2 = index.get(word2, {})

    print(word1, positionMap1)
    print(word2, positionMap2)

    resList = []
    for docId, positions in positionMap1.items():
        # add docId to list if it is in both maps(has both words)
        # and the distance between these words in the doc <= k
        if docId not in positionMap2: continue
        print(docId)
        if inWindow(positions, positionMap2.get(docId), k):
            resList.append(docId)

    # write result list to file
    outputPath = OUTPUT_PATH + word1 + "_" + word2 + str(k) + ".txt"
    with open(outputPath, mode='wt', encoding='utf-8') as f:
        f.write('\n'.join(resList))

# return true if there exists p1 in positions1, p2 in positions2
# that |p1 - p2| <= K + 1
def inWindow(positions1, positions2, k):
    # decode position list from distance to actual positions
    for i in range(1, len(positions1)):
        positions1[i] += positions1[i - 1]

    for i in range(1, len(positions2)):
        positions2[i] += positions2[i - 1]

    for position in positions1:
        # for each position in positions1, get the closest position in positions2
        # return true if distance <= k + 1
        closest = min(positions2, key=lambda x:abs(x-position))
        distance = abs(position - closest)
        if distance <= k + 1:
            return True;

    return False;


proximityQuery(INPUT_PATH, 6, "space", "mission")
proximityQuery(INPUT_PATH, 12, "space", "mission")
proximityQuery(INPUT_PATH, 5, "earth", "orbit")
proximityQuery(INPUT_PATH, 10, "earth", "orbit")