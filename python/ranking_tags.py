from nltk.tokenize import SpaceTokenizer
from nltk.stem.snowball import SnowballStemmer
import sqlite3
import operator

#set Stemmer to language
ranking = {}
counter = 1
inputDb = "MyDB.db"
lanDict = {'da' : 'danish', 'nl' : 'dutch', 'en' : 'english', 'fi' : 'finnish', 'fr' : 'french', 'de' : 'german', 'hu' : 'hungarian', 'it' : 'italian', 'no' : 'norwegian',  'pt' : 'portuguese', 'ro' : 'romanian', 'ru' : 'russian', 'es' : 'spanish', 'sv' : 'swedish'}
lanlist = ['da', 'nl', 'en', 'fi' , 'fr', 'de' , 'hu' , 'it' , 'no' ,  'pt' , 'ro' , 'ru' , 'es' , 'sv']



connector = sqlite3.connect(inputDb) #connect to db
selecter = connector.cursor() #create cursor


for i in lanlist:
	n = 0
	selecter.execute(''' SELECT id_db, tags FROM TableInDb WHERE language_final == "{}" '''.format(i)) #chose table and execute selecter
	stemmer = SnowballStemmer("{}".format(lanDict[i]))
	
	print ("New language " + str(lanDict[i]) + " selected")
	print ("Length of the language list is " + str(len(lanlist)) + ". We are at number " + str(lanlist.index(i)))
	

	for row in selecter:
		n += 1
		idDB = row[0]
		tag = row[1]
		tokenWord = SpaceTokenizer().tokenize(tag) #tokenize the tags, list is created
		
		print ("This is row number " + str(idDB) + " at language list index number " + str(lanlist.index(i)) + " from " + str(len(lanlist)))
		print ("Language: " + str(lanDict[i]))
		print (str(n) + " rows detected where to analyse tags")
	

		for j in tokenWord:
			wordStemmed = stemmer.stem(j)
			if wordStemmed in ranking:
				updateDicValue = ranking.get(wordStemmed)
				valuePlusOne = updateDicValue + 1
				ranking.update({wordStemmed:valuePlusOne})
			else:
				ranking.update({wordStemmed:counter})
		print ("Finished updating dictionary")
	

	rankingSorted = sorted(ranking.items(), key=operator.itemgetter(1))
	f = open(lanDict[i] + "_" + "ranking" + ".csv", "w")
	f.write("tags" + "\t" + "amount" + "\n")
	
	for wordsAmount in rankingSorted:
		f.write(str(wordsAmount[0]) + "\t" + str(wordsAmount[1]) + "\n")
	f.close()
	
	print ("Finished creating csv-file")
connector.close()




