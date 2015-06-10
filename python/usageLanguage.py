import operator
f = open("myCSV", "r")

dummy = 1
ranking = {}

for i in f:
	list_row = i.split("\t")
	language = list_row[-1]
	if language in ranking:
		update = ranking.get(language)
		amount = update + 1
		ranking.update({language:amount})
	else:
		ranking.update({language:dummy})

rankingS = sorted(ranking.items(), key=operator.itemgetter(1))
print (rankingS)
print (len(rankingS))