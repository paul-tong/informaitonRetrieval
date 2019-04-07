import urllib2
from bs4 import BeautifulSoup
from time import sleep

LINK_PREFIX = "https://en.wikipedia.org"
SEED_LINK = "https://en.wikipedia.org/wiki/Space_exploration"
DFSResultFilePath = "dfsResult.txt"
MAX_DEPTH = 6
MAX_COUNT = 1000
urlSet = {SEED_LINK}


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


# A DFS Web Crawler based on given depth and seed link.
def dfsCrawler(depth, seed):
    # Check depth and url count.
    if depth > 6 or len(urlSet) >= MAX_COUNT:
        return

    # Get page content of current link (as a seed).
    page = urllib2.urlopen(seed)
    soup = BeautifulSoup(page)
    content = soup.find(attrs={"id": "mw-content-text"})

    # Sleep 1 second for politeness	policy.
    sleep(1)

    # Analyze each link in the content.
    links = content.findAll('a')
    for link in links:
        # Check the count of urls.
        if len(urlSet) >= MAX_COUNT:
            return

        # Not a valid link.
        if not isValidUrl(link):
            continue

        # A validate link, add prefix to make a complete href
        hrefWhole = LINK_PREFIX + link.get("href")
        print(hrefWhole)

        # Redirect link, get the final url.
        if link.has_attr("class") and link["class"][0] == "mw-redirect":
           hrefWhole = urllib2.urlopen(hrefWhole).geturl()

        # Ignore if already in the urlSet to avoid duplicates.
        if hrefWhole in urlSet:
            continue

        # Not in the urlSet, add it to the set.
        urlSet.add(hrefWhole)

        # Recursively crawl pages.
        dfsCrawler(depth + 1, hrefWhole)

# Call the crawler functions and save links to file.
dfsCrawler(1, SEED_LINK)
with open(DFSResultFilePath, "w") as f:
    for url in urlSet:
        f.write("%s\n" % url)
