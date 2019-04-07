import Queue
import urllib2
from bs4 import BeautifulSoup
from time import sleep

LINK_PREFIX = "https://en.wikipedia.org"
SEED_LINK = "https://en.wikipedia.org/wiki/Space_exploration"
BFSResultFilePath = "bfsFocusedResult.txt"
MAX_DEPTH = 6
MAX_COUNT = 1000
KEYWORDS = {"Mars", "Rover", "Orbiter",	"Pathfinder", "Mars	Mission", "Mars Exploration"
            "Spark", "Wanderer", "traveler", "satellite", "groundbreaker", "trailblazer",
            "Martian", "Rove", "Roving", "Orbiting", "Orbit", "Orbits", "Orbital",
            "explore", "exploit", "exploited", "red planet", "space", "universe", "rocket",
            "spacecraft", "Solar system", "aerospace", "astronaut", "cosmonaut"}
duplicateCount = 0


# Return true if given text contains any keyword.
def containKeyword(text):
    # Convert given text to set (split by space).
    wordSet = set(text.split(" "))

    # Convert chars in both sets to lower case, so it will not be case-sensitive.
    set1 = set(map(str.lower, wordSet))
    set2 = set(map(str.lower, KEYWORDS))

    # Return true if it has intersection with keywords set.
    return len(set1.intersection(set2)) > 0


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

# A BFS Web Crawler based on given seed link.
def bfsCrawlerFocused(seed, keywords):
    global duplicateCount
    depth = 0
    queue = Queue.Queue()
    queue.put(seed)
    urlSet = {seed}

    # Get links with BFS.
    while not queue.empty():
        # Check the depth and url count.
        depth = depth + 1
        print("depth: ", depth)
        if depth > MAX_DEPTH:
            return urlSet

        # For each link in the current depth, analyze its corresponding page.
        count = queue.qsize()
        for i in range(0, count):
            # Get page content of current link (as a seed).
            seed = queue.get()
            page = urllib2.urlopen(seed)
            soup = BeautifulSoup(page)
            content = soup.find(attrs={"id": "mw-content-text"})

            # Sleep 1 second for politeness	policy.
            sleep(1)

            # Analyze each link in the content.
            links = content.findAll('a')
            for link in links:
                # Not a valid link.
                if not isValidUrl(link):
                    continue

                print("text: ", link.text.encode('utf-8'))
                # Not contain any focused keyword.
                if not containKeyword(link.text.encode('utf-8')):
                    continue

                # A validate link, add prefix to make a complete href
                hrefWhole = LINK_PREFIX + link.get("href")
                print(hrefWhole)

                # Redirect link, get the final url.
                if link.has_attr("class") and link["class"][0] == "mw-redirect":
                    hrefWhole = urllib2.urlopen(hrefWhole).geturl()

                # Ignore if already in the urlSet to avoid duplicates.
                if hrefWhole in urlSet:
                    duplicateCount += 1
                    continue

                # Not in the urlSet, add it to the set and queue.
                queue.put(hrefWhole)
                urlSet.add(hrefWhole)

                # Check the count of urls.
                if len(urlSet) >= MAX_COUNT:
                    print("depth: ", depth)
                    return urlSet

# Call the crawler functions and save links to file.
urls = bfsCrawlerFocused(SEED_LINK, KEYWORDS)
with open(BFSResultFilePath, "w") as f:
    f.write("duplicate count: %i\n" % duplicateCount)
    for url in urls:
        f.write("%s\n" % url)

