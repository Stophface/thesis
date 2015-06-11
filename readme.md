<h1>Where to go?</h1>

The following text roughly, how the maps in the folder `maps` were created. 

Source basemaps Afghanistan:
Worldmap: Bjorn Sandvik, thematicmapping.org, Roads: https://esoc.princeton.edu/file-type/gis-data, Cities: http://www.naturalearthdata.com/downloads/10m-cultural-vectors/10m-populated-places/
Source basemaps France:
Worldmap: Bjorn Sandvik, thematicmapping.org, Roads: http://www.naturalearthdata.com/downloads/10m-cultural-vectors/roads/, Cities: http://www.naturalearthdata.com/downloads/10m-cultural-vectors/10m-populated-places/


<h2>Python</h2>

<h3>dataminingFinal.py</h3>

Written in Python 3.3

**General information**

The script uses the "flickr.photos.search" (REST API in XML format; https://www.flickr.com/services/api/flickr.photos.search.html) to download the following information for each photo found within the bounding box (bbox)

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
The script iterates through a .csv which contains the corners of the bboxes spanned over the area of interest.
For each bbox, an unique URL is created, called and screenscraped. If there is more content than can be displayed on page 1 (250 datasets), it opens the next page with the coordinates of the curent bbox and downloads the data on page 2 as well. This will be repeated up to 16 times. Then the script goes to the next row in the .csv file and uses the next bbox.
For unknown reasons, the connection to the Flickr API gets lost. To stay "connected" the "urllib2" of Python is used. If connection times out, the script will go on with the next row in the .csv file and starts to create URL's for the corresponding bbox. 
However, this will result in bboxes from which no information will be downloaded since the connection to the Flickr API gets lost for that bbox (and the so created URL). This error does not occur often. The bboxes for which the script times out, hence no data was downlaoded, are written to the file `timeouts` 

Each step the script does is documented in the files `documentation`. If the script crashes for any reasons, it can be restarted. Simply check at which bbox the script crashed and type its number into line 50 (if stop < 0:). 

**What is that .csv file?**

To perform a geoquerry on Flickr with a bbox, the coordinates of the corner of the bbox need be known. 
With a geoquery request, 250 photos are returned per page in the browser (max 16 pages) and only 4.000 photos per bbox in total. Therefore, if information for a whole country or urban area need to be downloaded, the bboxes need to be split into smaller bboxes. 
To create a grid of small bboxes over the area of interest, QGIS (http://www.qgis.org/en/site/) and the tool Vector - Research Tools - Vector Grid (Output as Polygons) can be used. Save the output file as .csv.
This created .csv file needs to be the inputfile of `p` (`p = "FILEWITHBBOXES.csv"`).



<h3> example_langid.py</h3>
 
 Written in Python 3.3

 Needs the langid library installed (https://github.com/saffsd/langid.py)

 Iterates through the SQLite database and uses (here) the title for language identification. Writes the identified language (no matter how high the reliability is) to the same SQLite database.



<h3>example_chromium</h3>

Written in Python 3.3

Needs the Chromium compact language detector (cld) library installed (https://pypi.python.org/pypi/chromium_compact_language_detector/0.1.1)

 Iterates through the SQLite database and uses (here) the description for language identification. Writes the identified language (no matter how high the reliability is) to the same SQLite database.



<h3>booleanLogic.py</h3>

Written in Python 3.3

Defines the final language of the photos. It uses the identified languages of the langid and cld library (title, tags description) and follows the following Boolean logic:

    No   Title     Tag     Description     Title     Tag     Description     Boolean     Language
         LID I     LID I   LID I           LID II    LID II  LID II          Outcome     Final
    1.   XX        XX      -               XX        XX      -               TRUE        XX
    2.   XX        YY      -               XX        XX      -               FALSE       None
    3.   YY        YY      XX              YY        YY      XX              TRUE        YY
    4.   YY        YY      XX              YY        YY      ZZ              FALSE       None
    5.   XX        YY      XX              YY        YY      YY              FALSE       None
    6.   YY        YY      XX              YY        YY      YY              TRUE        YY
    7.   XX        XX      -               OO        OO      -               TRUE        OO
    8.   YY        YY      -               YY        OO      -               TRUE        OO
    9.   YY        YY      -               YY        YY      OO              TRUE        OO

Since only langid can identify pashto (here 'OO') the logic is slightly modified for this language (row 7,8,9).
Through the hierachy in the code it becomes obvious, which combination of possbilities is weighted 'heavier'. 


<h2>postgres:postgis</h2>

To run the lines in the file PostgreSQL with the PostGIS is needed. A boundled package can be downloaded here: http://www.kyngchaos.com/software/postgres.

More meaningful assumptions about the distribution of points on a map can be made when the map is divided into polygons, the points are counted inside each polygon and finally summed up per polygon. This process is called binning.

    UPDATE hexagonFinerWgs_clip SET count = (SELECT count(*) FROM points_france WHERE ST_Within(points_france.geom, hexagonFinerWgs_clip.geom));


The same goes for the language. Since through the Boolean Logic each photo got a language assigned to, we can plot each point (because it has lat/long) on a map. The following lines count the points per polygon, group them by the language and order them.

     CREATE TABLE count_language_france AS SELECT count(*), france.language, hexagons.gid, hexagons.top, hexagons.bottom, hexagons.left, hexagons.right, hexagons.geom FROM hexagonfinerwgs_clip AS hexagons, points_language_france AS france WHERE ST_Within(france.geom, hexagons.geom) GROUP BY france.language, hexagons.gid ORDER BY hexagons.gid DESC;


Now there are for example Farsi, Dari and English counted in one polygon. We are only interested in the most language. 

     CREATE TABLE count_language_france_binning2 AS SELECT DISTINCT ON (t.gid) t.gid, t.language, t.count, t.top, t.right, t.bottom, t.geom FROM count_language_france AS t ORDER BY t.gid, t.count DESC;


