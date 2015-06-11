from decimal import *
import sqlite3
import time
from bs4 import BeautifulSoup
import urllib2


#creating SQLite Database and Table
connector = sqlite3.connect("NAMEOFDATABASE.db") #create Database and Table
connector.execute('''create table if not exists NAMEOFTABLE
        (id_db INTEGER PRIMARY KEY AUTOINCREMENT,
        id_photo INTEGER,
        title TEXT,
        tags TEXT,
        description TEXT,
        views NUMERIC,
        latitude NUMERIC, 
        longitude NUMERIC,
        date_uploaded NUMERIC,
        date_taken NUMBERIC,
        title_abbreviation_langid TEXT,
        title_reliability_langid NUMERIC,
        tags_abbreviation_langid TEXT,
        tags_reliability_langid NUMERIC,       
        title_abbreviation_chrome TEXT,
        title_language_chrome TEXT,
        title_reliabilty_chrome TEXT,
        tags_abbreviation_chrome TEXT,
        tags_language_chrome TEXT,
        tags_reliabilty_chrome TEXT
        );'''
                  )

f = open("documentation", "w") #create file to write the documentation to
t = open("timeouts", "w") #create file to write the timouts (when connection to Flickr API is lost) to

p = "FILEWITHBBOXES.csv" #csv with the coordinates of bounding boxes. 
with open(p, "r") as cursor: #copen .csv file with grid
    for row in cursor: #iterate through file
        elements = row.split(",") #split on limiter

        latmin = elements[3].strip() #.strip() in order to get rid of everything which is not string (spaces, etc.)
        latmax = elements[4].strip()

        longmin = elements[1].strip()
        longmax = elements[2].strip()

        stop = int(elements[0])

        if stop < 0: #if script crashes, write here number of bbox where it crashed to start from there
            continue

        c = 1 # counter for pages
        url = "https://api.flickr.com/services/rest/?method=flickr.photos.search&api_key=...&page={}&per_page=250&bbox={},{},{},{}&max_upload_date=1426118400&has_geo=1&accuracy=3&extras=geo,tags,views,description,date_upload,date_taken&content_type=1".format(c,longmin, latmin, longmax, latmax) #REST API URL
        try:
            try:
                result = urllib2.urlopen(url, timeout = 5) #if connection lost, go to next created URL
            except urllib2.URLError as e: #if connection is lost, write the error to file
                ops = "URL error with url: " + url + "\n bb: " + str(elements[0]) + ", error: " + str(e)
                t.write(ops)
                continue #continue with "next" loop

            soup = BeautifulSoup(result) #soup it up
            photos = soup.find_all('photo') #gets the content of photos (id, title, tags etc.)     

            bbox_position = "bbox number " + str(elements[0]) + " Coordinates of bbox (" + str(longmin) + ", " + str(latmin) + "), (" + str(longmax) + ", " + str(latmax) + ")"
            print bbox_position
       
        except Exception as e: #any other expection which might be raised
            ops = "error with url: " + url + "\n bb: " + str(elements[0]) + ", error: " + str(e)
            f.write(ops)
            continue

        while len(photos) > 0 and c <= 16: #call the page and IF there is content, for a page, it will go on with the loop
            photos_detected = str(len(photos)) + " photos detected in page " + str(c) + " at bbox number " + str(elements[0] + " (coordinates of bbox (" + str(longmin) + ", " + str(latmin) + "), (" + str(longmax) + ", " + str(latmax) + ") )")
            f.write(photos_detected +  "\n")
            print photos_detected

            try:
                print "put data in db" 

                for data in photos: #parsing the data (screenscraping)
                    scraping = ( #filter the data, and create tuple.  
                    data.get('id'),
                    data.get('title'),
                    data.get('tags'),
                    data.find("description").text,
                    data.get('views'),
                    data.get('latitude'),
                    data.get('longitude'),
                    data.get('dateupload'),
                    data.get('datetaken')
                    )
                    connector.execute('''insert into NAMEOFDATABASE(id_db, id_photo, title, tags, description, views, latitude, longitude, date_uploaded, date_taken) values (NULL,?,?,?,?,?,?,?,?,?)''', scraping) #use ? to let the SQLite do the formatting!
                connector.commit() #save changes to db
                print "finished putting data"
            except Exception as exception:
                f.write(str(exception) + "\n")

            time.sleep(1.1) # wait 1.1 second since only 3600 calls are allowed per hour by default from flickr

            
            #create a new page (thus, link)
            c += 1 # counter for pages, update page
            url = "https://api.flickr.com/services/rest/?method=flickr.photos.search&api_key=....&page={}&per_page=250&bbox={},{},{},{}&max_upload_date=1426118400&has_geo=1&accuracy=3&extras=geo,tags,views,description,date_upload,date_taken&content_type=1".format(c,longmin, latmin, longmax, latmax)    
            try:
                try:
                    result = urllib2.urlopen(url, timeout = 5)
                except urllib2.URLError as e:
                    ops = "URL error with url: " + url + "\n bb: " + str(elements[0]) + ", error: " + str(e)
                    t.write(ops)
                    print ops
                    continue

                soup = BeautifulSoup(result) #soup it up
                photos = soup.find_all('photo') #gets the content of photos (id, title, tags etc.)     

                bbox_position = "bbox number " + str(elements[0]) + " Coordinates of bbox (" + str(longmin) + ", " + str(latmin) + "), (" + str(longmax) + ", " + str(latmax) + ")"
                #f.write(bbox_position + "\n")
                print bbox_position
            except Exception as e:
                ops = "error with url: " + url + "\n bb: " + str(elements[0]) + ", error: " + str(e)
                f.write(ops)
                print ops
                continue
         
            #update the pages by +1 through c

        # wait 1 second before changing coordinates
        time.sleep(1.1)  

        
connector.close() #close connector
f.close()


