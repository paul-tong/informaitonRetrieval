# task3 and task4 - implement page rank algorithm

import math

INPUT_PATH_BFS_GRAPH = "output/bfsGraphOut.txt"
INPUT_PATH_FOCUSED_GRAPH = "output/focusedGraphOut.txt"
INPUT_PATH_TEST_GRAPH = "output/testGraph.txt"
L2NORM_PATH = "output/pagerank/l2norm"
PAGE_RANK_WHOLE_PATH = "output/pagerank/pageRankWhole"
PAGE_RANK_TOP50_PATH = "output/pagerank/pageRankTop50"
PAGE_ID_INPUT_PATH_BFS = "input/BFS.txt"
PAGE_ID_INPUT_PATH_FOCUSED = "input/FOCUSED.txt"
L2_DIFFERENCE = 0.0005
Least_CONSECUTIVE_CONVERGE = 4

# Build a page id set from given urls file path.
def getPageIdSet(filePath):
    idSet = set()
    with open(filePath) as f:
        urls = f.readlines()
        # Remove `\n` at the end of each line and save into a list.
        urls = [x.strip() for x in urls]

        for url in urls:
            id = url[url.rindex("/") + 1:]
            idSet.add(id)
    return idSet

# return true if page rank is converged(base on l2-norm)
def isConverged(I, R, outputPath):
    l2 = 0
    sum = 0 # sum of page rank values

    for r in R:
        l2 += math.pow(R.get(r) - I.get(r), 2)
        sum += R.get(r)
    l2 = math.sqrt(l2)

    # write l2-norm and sum of page rank into file
    with open(outputPath, "a") as f:
        f.write("l2-norm value: %s\n" % str(l2))
        f.write("sum of rank page: %s\n\n" % str(sum))

    return l2 < L2_DIFFERENCE


def computeRankPage(inputPath, graphType, lamb, iterationLimit):
    # build output path based on arguments
    l2normPath = L2NORM_PATH
    pageRankWholePath = PAGE_RANK_WHOLE_PATH
    pageRankTop50Path = PAGE_RANK_TOP50_PATH
    pageIdInputPath = ""

    if graphType == "bfs":
        l2normPath += "_bfs_" + str(lamb) + ".txt"
        pageRankWholePath += "_bfs_" + str(lamb) + ".txt"
        pageRankTop50Path += "_bfs_" + str(lamb) + ".txt"
        pageIdInputPath = PAGE_ID_INPUT_PATH_BFS
    else:
        l2normPath += "_focused_" + str(lamb) + ".txt"
        pageRankWholePath += "_focused_" + str(lamb) + ".txt"
        pageRankTop50Path += "_focused_" + str(lamb) + ".txt"
        pageIdInputPath = PAGE_ID_INPUT_PATH_FOCUSED

    # clear l2-norm value file
    print(l2normPath)
    open(l2normPath, 'w').close()

    edgeMap = {} # edge relationship (note its OUT-link)
    P = set() # page set
    I= {} # current page rank estimate
    R = {} # the resulting better page rank estimate

    # get all pages id
    P = getPageIdSet(pageIdInputPath)
    #P = set(["A", "B", "C", "D", "E", "F"])

    # load graph and save into <edge, set<edge>> map
    with open(inputPath) as f:
        lines = f.readlines()
        # Remove `\n` at the end of each line and save into a list
        lines = set([x.strip() for x in lines])
        for line in lines:
            edges = line.split(" ")
            curPage = edges[0]
            inPages = set(edges[1:])
            edgeMap.update({curPage: inPages})

    # initialize I and P
    for p in P:
        I[p] = 1 / len(P)
        R[p] = -1

    consecutiveConverge = 0 # count of continues converge
    curIteration = 0 # count of iteration

    # compute page rank iteratively
    while (iterationLimit < 0) or (iterationLimit > 0 and curIteration < iterationLimit):
        curIteration += 1

        for p in P:
            R[p] = lamb / len(P) # random click

        for p in P:
            if p not in edgeMap: # sink link (has no outgoing page)
                for q in P: # perform like a random click
                    R[q] = R[q] + (1 - lamb) * I[p] / len(P)
            else:
                outlinkCount = len(edgeMap.get(p))
                for q in edgeMap.get(p): # probability for clicking each out link
                    R[q] = R[q] + (1 - lamb) * I[p] / outlinkCount

        # check whether is converged
        if isConverged(I, R, l2normPath):
            consecutiveConverge += 1
            if consecutiveConverge >= Least_CONSECUTIVE_CONVERGE:
                break
        else:
            consecutiveConverge = 0

        I.update(R) # copy R into I


    # sort pages based on rank and write to file
    pageSorted = sorted(R.items(), key=lambda kv: kv[1], reverse = True)

    # write to file - whole list
    with open(pageRankWholePath, "w") as f:
        for page in pageSorted:
            f.write("%s %s\n" % page)

    # write to file - top 50
    with open(pageRankTop50Path, "w") as f:
        for i in range(0, 50):
            if i >= len(pageSorted):
                break
            else:
                f.write("%s %s\n" % pageSorted[i])

# run algorithm with different arguments
computeRankPage(INPUT_PATH_BFS_GRAPH, "bfs", 0.15, -1)
computeRankPage(INPUT_PATH_FOCUSED_GRAPH, "focused", 0.15, -1)

computeRankPage(INPUT_PATH_BFS_GRAPH, "bfs", 0.25, -1)
computeRankPage(INPUT_PATH_FOCUSED_GRAPH, "focused", 0.25, -1)

computeRankPage(INPUT_PATH_BFS_GRAPH, "bfs", 0.35, -1)
computeRankPage(INPUT_PATH_FOCUSED_GRAPH, "focused", 0.35, -1)

computeRankPage(INPUT_PATH_BFS_GRAPH, "bfs", 0.5, -1)
computeRankPage(INPUT_PATH_FOCUSED_GRAPH, "focused", 0.5, -1)

computeRankPage(INPUT_PATH_BFS_GRAPH, "bfs", 0.15, 4)
computeRankPage(INPUT_PATH_FOCUSED_GRAPH, "focused", 0.15, 4)
