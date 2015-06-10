Python

dataminingFinal.py

Written in Python 2.7


**General information**

It uses the "flickr.photos.search" method (https://www.flickr.com/services/api/flickr.photos.search.html) to download the following information for each photo found within the bounding box (bbox)

- id photo
- title
- tags
- description 
- views
- latitude
- longitude
- date uploaded
- date taken

The information are downloaded through screenscraping with the Library "BeautifulSoup" (http://www.crummy.com/software/BeautifulSoup/) and are written to a SQLite3 database.
The script iterates through a .csv which contains the corners of the bboxes.
If there is more content than can be displayed on page 1 (250 datasets), it opens the next page with the coordinates of the curent bbox and downloads the data on page 2 as well. This will be repeated up to 16 times. Then the script goes to the next
row in the .csv file and uses the next bbox. 

For each bbox, an unique URL is created, called and each site is screenscraped. For unknown reasons, the connection to the Flickr API gets lost. To stay "connected" the "urllib2" of Python is used. If connection timesout, the script will go on with the next line in the .csv file and starts to create URL's for the corresponding bbox. 
However, this will result in bboxes from which no information will be downloaded since the connection to the Flickr API gets lost for that bbox (and the so created URL). This error does not occur often. If information needed, the bboxes for which the script times out, are written to the file "timeouts" 

Each step the script does is documented in the files "documentation". If the script crashes for any reasons, it can be restarted. Simply check at which bbox the script crashed and type its number into line 50 (if stop < 0:). 



**What is that .csv file?**

To perform a geoquerry on Flickr with a bbox, the coordinates of the corner of the bbox need be known. 
With a geoquery request, 250 photos are returned per page in the browser (max 16 pages) and only 4.000 photos per bbox in total. Therefore, if information for a whole country or urban area need to be downloaded, the bboxes need to be split into smaller bboxes. 
To create a grid of small bboxes over the area of interest, QGIS (http://www.qgis.org/en/site/) and the tool Vector - Research Tools - Vector Grid (Output as Polygons) can be used. Save the output file as .csv.
This created .csv file needs to be the inputfile of "p" (p = "FILEWITHBBOXES.csv").