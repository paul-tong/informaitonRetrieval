# task1 - text transformation

import urllib.request
import urllib.error
import re
from bs4 import BeautifulSoup
from createTrigrams import runTrigrams

INPUT_PATH = "input/BFS.txt"
OUTPUT_PATH = "output/articles/"


# For each url in the input file, tokenize its content and save it to file
# take arguments to decide whether needs case folding and punctuation handling
def transformToText(inputPath, outputPath,
                    isCaseFolding = True, isPunctuationHandling = True):
    with open(inputPath) as f:
        urls = f.readlines()
        # Remove `\n` at the end of each line and save into a list
        urls = set([x.strip() for x in urls])

        for url in urls:
            print("url: " + url)

            textAll = ""

            # extract file name from url
            fileName = url[url.rindex("/") + 1:]
            textAll += fileName + "\n"

            # handle exception
            try:
                page = urllib.request.urlopen(url)
            except urllib.error.URLError as e:
                print(e.reason)
                continue

            soup = BeautifulSoup(page)

            # extract text
            content = soup.find(attrs={"id": "mw-content-text"})
            paragraphs = content.findAll('p')
            for p in paragraphs:
                textP = p.get_text()

                # case folding
                if isCaseFolding:
                    textP = textP.lower()

                # punctuation handling
                if isPunctuationHandling:
                    # remove every thing except words, space and hyphen
                    textP = re.sub(r'[^\w\s\-]', '', textP)

                textAll += textP + "\n"

            # save text to file
            with open(outputPath + fileName + ".txt", "wb") as f:
                f.write(textAll.encode('utf8'))

transformToText(INPUT_PATH, OUTPUT_PATH)
runTrigrams()
