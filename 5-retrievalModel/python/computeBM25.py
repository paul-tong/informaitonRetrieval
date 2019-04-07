import json
import collections
import math
import pandas as pd

N = 1000
K1 = 1.2
K2 = 100
B = 0.75
AVDL = 0.0
DOC_LENGTH_MAP = {} # map contains term frequency of each doc, Map<docId, termFrequency>
FREQUENCY_INDEX = {} # map represents the index, Map<term, Map<docId, termFrequency>>
DOC_LENGTH_FILE_PATH = "input/termCount.txt"
FREQUENCY_INDEX_FILE_PATH = "input/frequencyIndex1.txt"
OUTPUT_PATH = "output/"

def computeBM25(N, k1, k2, b, avdl, queryId, terms):
	print("\n========================================")
	print("current query: ", terms)

	scoreMap = {} # map<docId, BM25 Score>

	# for each term, compute score for each doc
	for term in terms:
		af = collections.Counter(terms).get(term)
		print("\nterm:", term)
		print("frequency:", af)

		# docs that contains current term, map<docId, termFrequency>
		docsMap = FREQUENCY_INDEX.get(term)
		n = len(docsMap)
		print("n:", n)
		print("avdl: ", avdl)

		# for each doc that contains this term
		for doc in docsMap:
			dl = DOC_LENGTH_MAP.get(doc)
			# print("dl: ", dl)

			f = docsMap.get(doc)
			#print("f: ", f)

			# compute k
			K = k1 * ((1 - b) + b * (dl / avdl))
			#print("K: ", K)

			# compute score
			score1 = math.log((N - n + 0.5) / (n + 0.5))
			score2 = (k1 + 1) * f / (K + f)
			score3 = (k2 + 1) * af / (k2 + af)
			score = score1 * score2 * score3
			#print("score: ", score)

			# accumulate score for current doc
			if doc not in scoreMap:
				scoreMap[doc] = score
			else:
				scoreMap[doc] += score

	print(scoreMap)

	# convert scoreMap to pandas dataset
	# rank rows based on score, get top100, add additional cols
	df = pd.DataFrame([[key, value] for key, value in scoreMap.items()],
				  columns=['doc_id', 'BM25_score'])
	df = df.sort_values(by=['BM25_score'], ascending=False).head(100)
	df['rank'] = df['BM25_score'].rank(ascending=0, method='min').astype('int64')
	df['query_id'] = queryId
	df['Q0'] = 'Q0'
	df['system_name'] = 'BM25'
	df = df[['query_id', 'Q0', 'doc_id', 'rank', 'BM25_score', 'system_name']]

	# save result to file
	filepath = OUTPUT_PATH + 'query' + str(queryId) + '.csv'
	df.to_csv(filepath, index = None, header=True)
	print(df.to_string())



# load files that maintains document length and frequency index
with open(DOC_LENGTH_FILE_PATH, 'r') as f:
	DOC_LENGTH_MAP = json.load(f)

with open(FREQUENCY_INDEX_FILE_PATH, 'r') as f:
	FREQUENCY_INDEX = json.load(f)

# compute average length of docs in the collection
totalLength = 0
for length in DOC_LENGTH_MAP.values():
	totalLength += length
AVDL = totalLength / N

# call functions to compute BM25 scores
queryMap = {'1':["milky", "way", "galaxy"],
			'2':['hubble', 'space', 'telescope'],
			'3':['international', 'space', 'station'],
			'4':['big', 'bang', 'theory'],
			'5':['mars', 'exploratory', 'missions']}

for queryId, terms in queryMap.items():
	computeBM25(N, K1, K2, B, AVDL, queryId, terms)

