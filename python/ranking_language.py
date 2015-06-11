import csv
import sqlite3
import operator

f = open('language.csv', 'w')
f.write(str('id_db') + '\t' + str('longitude') + '\t' + str('latitude') + '\t' + str('language') + '\n')

n = 0

inputDB = "MyDB.db"


connector = sqlite3.connect(inputDB)
selecter = connector.cursor()
selecter.execute('''SELECT id_db, longitude, latitude, language_final from TableInDb WHERE language_final != "un" ''')


for row in selecter:
	id_db = row[0]
	longitude = row[1]
	latitude = row[2]
	language = row[3]
	f.write(str(id_db) + '\t' + str(longitude) + '\t' + str(latitude) + '\t' + str(language) + '\n')
	n+=1
	print (n)

f.close()
connector.close()


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