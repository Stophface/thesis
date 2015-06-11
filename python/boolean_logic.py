import sqlite3
import operator


inputDB = "myDB" #name of database

connector = sqlite3.connect(inputDB)
selecter = connector.cursor()

##########
#ALTER TABLE FOR A COLUMN FOR THE LANGUAGE
#selecter.execute('''ALTER TABLE DATAAFGHANISTAN ADD COLUMN "language_final" 'TEXT' ''')
##########

selecter.execute('''SELECT id_db, tags_abbreviation_chrome, tags_abbreviation_langid, title_abbreviation_chrome, title_abbreviation_langid, description_abbreviation_chrome, description_abbreviation_langid FROM TableInDb''')
#order
# 0 = id_db
# 1 = tags chrome
# 2 = tags langid
# 3 = title chrome
# 4 = title langid
# 5 = description chrome
# 6 = description langid

#counters
title_and_tag_equal = 0
desc_equal = 0
five_or_more_equal = 0
nothing = 0

n = 0
u = "un"


#write chronologically
#make sure statements overwrite each other in the wanted way
for row in selecter:
	# reset lan
	lan = None

	n += 1
	print (n)

	tags_chrome = row[1]
	tags_lang = row[2]
	title_chrome = row[3]
	title_lang = row[4]
	desc_chrome = row[5]
	desc_lang = row[6]


	#row1
	#tags and title are the same but not "un"
	if (tags_chrome != u and tags_lang != u and title_chrome != u and title_lang != u and
	tags_chrome == tags_lang == title_chrome == title_lang): #tags and title are the same but not "un"
		title_and_tag_equal += 1
		lan = row[1]

	#row 3 -> does not matter how many are "un" since we are interested in description!
	if (desc_chrome != u and desc_lang != u
	and
	desc_chrome == desc_lang): #doesnt matter whether row[1-4] is un or not. What matters is that row[5-6] are not un and equal!
		desc_equal += 1
		lan = row[5]

	#row 6
	if tags_chrome != u and tags_lang != u and title_chrome != u and title_lang != u and desc_chrome != u and desc_lang != u:
		mylist = [tags_chrome, tags_lang, title_chrome, title_lang, desc_chrome, desc_lang] #append all identified languages to list
		ranking = {}

		for j in mylist:
			if j in ranking: #check if the abrevation for language is in dictionary
				s = ranking.get(j) #if is in dictionary, get the entry through the key (language abrevation)
				t = s + 1 #alter its value by one
				ranking.update({j:t}) #update the dictionary
			else:
				ranking.update({j:1}) #if the value is not in the dictionary, update the dicationary with it

		rankingS = sorted(ranking.items(), key=operator.itemgetter(1))
		if ((len(rankingS) == 1 and rankingS[0][1] == 6)
		or 
		(len(rankingS) == 2 and rankingS[0][1] == 1 and rankingS[1][1] == 5)):
			five_or_more_equal += 1
			lan = rankingS[-1][0]

	if tags_lang == "ps" or title_lang == "ps" or desc_lang == "ps":
		lan = "ps"

	if (lan is None):
		lan = u
		nothing += 1
		

	connector.execute('''update MYDB set language_final = ? where id_db == ?''', (lan, row[0]))  




print ("title tags the same", title_and_tag_equal)
print ("description the same", desc_equal)
print ("five items the same", five_or_more_equal)
print ("nothing", nothing)
print ("iterations", n)

print ("Sum of statements", title_and_tag_equal + desc_equal + five_or_more_equal )


connector.commit()
connector.close()
