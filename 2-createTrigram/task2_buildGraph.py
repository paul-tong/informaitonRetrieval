# task2 - create graph for in-link and out-link

import urllib.request
from bs4 import BeautifulSoup

LINK_PREFIX = "https://en.wikipedia.org"
SEED_LINK = "https://en.wikipedia.org/wiki/Space_exploration"

BFSInputFilePath = "input/BFS.txt"
FocusedinputFilePath = "input/FOCUSED.txt"
BFSOutputFilePath = "output/bfsGraph.txt"
FocusedOutputFilePath = "output/focusedGraph.txt"

# Map that contains <url, id> of given urls in the file path.
idMap = dict()

# Build a <url, id> map from given urls file path.
def buildIdMap(filePath):
    with open(filePath) as f:
        urls = f.readlines()
        # Remove `\n` at the end of each line and save into a list.
        urls = [x.strip() for x in urls]

        for url in urls:
            id = extractId(url)
            idMap.update({url: id})


# Extract id from given url.
def extractId(url):
    return url[url.rindex("/") + 1:]


# Return true if given link is validate
def isValidUrl(link):
    # Get href, note its not a complete url ("/wiki/...").
    hrefPart = link.get("href")

    # Don't have href attribute.
    if not link.has_attr("href"):
        return False

    # Has special class attribute other than redirect class.
    if link.has_attr("class") and link["class"][0] != "mw-redirect":
        return False

    # Not starts with prefix "/wiki".
    if not hrefPart.startswith("/wiki"):
        return False

    # Section or administrative link.
    if "#" in hrefPart or ":" in hrefPart:
        return False

    return True


# Get the set of out-links of given url.
def getOutUrls(url):
    urlSet = set()

    # get page from url, handle exception
    try:
        page = urllib.request.urlopen(url)
    except urllib.error.URLError as e:
        print(e.reason)
        return urlSet

    soup = BeautifulSoup(page)
    content = soup.find(attrs={"id": "mw-content-text"})

    # Analyze each link in the content.
    links = content.findAll('a')
    for link in links:
        # Not a valid link.
        if not isValidUrl(link):
            continue

        # A validate link, add prefix to make a complete href.
        hrefWhole = LINK_PREFIX + link.get("href")

        # Not in the idMap(not one of the 1000 urls).
        if hrefWhole not in idMap:
            continue

        urlSet.add(hrefWhole)

    return urlSet


def buildLinkGragh(inputPath, outputPath):
    # Clear previous map and set
    idMap.clear()

    # map<link, set<link>>, key is a link, value is a set of in or out links.
    outLinkMap = dict()
    inLinkMap = dict()

    maxInDegree = 0
    maxOutDegree = 0

    # Load urls and save to <url, id> map
    buildIdMap(inputPath)

    for curUrl in idMap.keys():

        print ("current url: ", curUrl)

        # Get out-link set.
        curId = idMap.get(curUrl)
        outUrlSet = getOutUrls(curUrl)

        # Has no out links.
        if len(outUrlSet) == 0:
            continue

        # Add to in/out link map.
        for outUrl in outUrlSet:
            outId = idMap.get(outUrl)
            if curId not in outLinkMap:
                outLinkMap.update({curId: set([outId])})
            else:
                outLinkMap.get(curId).add(outId)
            if outId not in inLinkMap:
                inLinkMap.update({outId: set([curId])})
            else:
                inLinkMap.get(outId).add(curId)

            # Update max in degree and out degree
            maxOutDegree = max(maxOutDegree, len(outLinkMap.get(curId)))
            maxInDegree = max(maxInDegree, len(inLinkMap.get(outId)))

    # Get the count of no-in-link url that has no in-link or out-link.
    noOutLinkCount = len(idMap) - len(outLinkMap)
    noInLinkCount = len(idMap) - len(inLinkMap)

    # Print statics information
    print ("max in degree: ", maxInDegree)
    print ("max out degree: ", maxOutDegree)
    print ("count without in link: ", noInLinkCount)
    print ("count without out link: ", noOutLinkCount)

    # Write in-link graph to files
    with open(outputPath, "w") as f:
        for curId in inLinkMap:
            f.write("%s " % curId)
            for inId in inLinkMap.get(curId):
                f.write("%s " % inId)
            f.write("\n")

buildLinkGragh(BFSInputFilePath, BFSOutputFilePath)
buildLinkGragh(FocusedinputFilePath, FocusedOutputFilePath)


