import sqlite3
import cld

"""GOOGLECHROMIUM"""



inputDB = "myDB"

connector = sqlite3.connect(inputDB)
selecter = connector.cursor()


##########
#ALTER TABLE FOR A COLUMN FOR THE LANGUAGE
selecter.execute('''ALTER TABLE myDB ADD COLUMN "description_abbreviation_chrome" 'TEXT' ''')
selecter.execute('''ALTER TABLE myDB ADD COLUMN "description_language_chrome" 'TEXT' ''')
selecter.execute('''ALTER TABLE myDB ADD COLUMN "description_reliability_chrome" 'TEXT' ''')
##########


selecter.execute('''SELECT id_db, description FROM myDB''')
for row in selecter:
    #print (row)
    a = ''.join(row[1])
    goog = detectedLangName, detectedLangCode, isReliable, textBytesFound, details = cld.detect("{}".format(a)) #chrome languagedetection
    lancode = detectedLangCode
    lanname = detectedLangName
    lanreliability = isReliable != 0
    landetails = details
    #print ("lancode: ",lancode)
    #print ("lanname: ", lanname)
    #print ("lanreliability: ", lanreliability)
    print (row[0])
    #print (a) 
    connector.execute('''update myDB set description_abbreviation_chrome = ? , description_language_chrome = ? , description_reliability_chrome = ? where id_db == ?''', (lancode, lanname, lanreliability, row[0]))  
connector.commit() #save changes
connector.close()