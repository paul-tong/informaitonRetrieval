# task1 - create trigrams, compute frequency and plotting
import os
import pandas as pd
import matplotlib.pyplot as plot

INPUT_PATH = "output/articles"
OUTPUT_PATH = "output/trigrams.txt"

# map for <trigram, count>
trigramMap = {}

# create trigrams from files and build <trigram, frequency> map
def createTrigrams(inputPath):
    for filename in os.listdir(inputPath):
        # read all files in the given path
        filePath = inputPath + "/" + filename
        print (filePath)

        with open(filePath) as f:
            lines = f.readlines()
            # Remove `\n` at the end of each line and save into a list.
            lines = [x.strip() for x in lines]

            for line in lines:
                words = line.split(" ")
                for i in range(len(words) - 2):
                    # build a trigram
                    trigram = words[i] + " " + words[i + 1] + " " + words[i + 2]

                    # increase the count of trigram in map
                    if trigram not in trigramMap:
                        trigramMap[trigram] = 1
                    else:
                        trigramMap[trigram] += 1


# convert trigram map to pandas dataframe then analyze data
def analyzeTrigram(outputPath):
    # build pandas dataframe, compute Zipf's law constant
    df = pd.DataFrame.from_dict(trigramMap, orient='index', columns=['frequency'])
    df.index.name = 'word'
    totalFrequency = df['frequency'].sum()

    df = df.sort_values(by=['frequency'], ascending=False)
    df['rank'] = df['frequency'].rank(ascending=0,method='min').astype('int64')
    df['probability'] = df['frequency'] / totalFrequency
    df['constantK'] = df['frequency'] * df['rank']
    df['constantC'] = df['probability'] * df['rank']

    # save to file
    #df = df.round(3)
    df.to_csv(outputPath)
    df.to_excel('output/trigrams.xlsx')
    print ("total frequency: ", totalFrequency)

    # draw log-log plot of the Frequency vs Rank
    df.plot.line(x='rank', y = 'frequency', loglog = True)
    plot.show()

def runTrigrams():
    createTrigrams(INPUT_PATH)
    analyzeTrigram(OUTPUT_PATH)

runTrigrams()
