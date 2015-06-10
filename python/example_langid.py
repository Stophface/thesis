import sqlite3
import langid


"""LANGID"""

c = "un"
b = 1


inputDB = "myDB.db"

connector = sqlite3.connect(inputDB)
selecter = connector.cursor()
selecter.execute(''' SELECT id_db, title FROM myDB''')
for row in selecter: #iterate through all the rows in db    
    print (row[0])
    #print (row[1])

    if row[1].strip() == "":
        connector.execute('''update myDB set title_abbreviation_langid = ? , title_reliability_langid = ? where id_db == ? ''', (c, b, row[0])) #updatestatement needed here in order to not append new rows, where clause to tell where to insert

    else:

        a = ''.join(row[1])
        lan = langid.classify("{}".format(a)) #identify the language
        #print (lan[0])
        #print (lan[1])

        connector.execute('''update myDB set title_abbreviation_langid = ? , title_reliability_langid = ? where id_db == ? ''', (lan[0], lan[1], row[0])) #updatestatement needed here in order to not append new rows, where clause to tell where to insert

connector.commit() #save changes
connector.close()
