<h1>What do the code snippets do?</h1>

The following text explains roughly, how the maps in the folder `maps` were created. 

Source basemaps Afghanistan:
Worldmap: Bjorn Sandvik, thematicmapping.org, Roads: https://esoc.princeton.edu/file-type/gis-data, Cities: http://www.naturalearthdata.com/downloads/10m-cultural-vectors/10m-populated-places/
Source basemaps France:
Worldmap: Bjorn Sandvik, thematicmapping.org, Roads: http://www.naturalearthdata.com/downloads/10m-cultural-vectors/roads/, Cities: http://www.naturalearthdata.com/downloads/10m-cultural-vectors/10m-populated-places/


I recoomend to use Python 3.3 since it makes coding and encoding of characters easier.

<h2>Python</h2>

<h3>datamining_final.py</h3>


**How was the data downlaoded**

The script uses the `flickr.photos.search` (REST API in XML format; https://www.flickr.com/services/api/flickr.photos.search.html) to download the following information for each photo found within the bounding box (bbox)

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
For each bbox, an unique URL is created, called and screenscraped. If there is more content than can be displayed on page 1 ( what would be more than 250 datasets), it opens the next page with the coordinates of the current bbox and downloads the data on page 2 as well. This will be repeated up to 16 times. Then the script goes to the next row in the `.csv-file` and uses the next bbox.

For unknown reasons, the connection to the Flickr API gets lost. To stay "connected" the `urllib2` of Python is used. If connection times out, the script will go on with the next row in the `.csv-file` and starts to create URL's for the corresponding bbox. 
However, this will result in bboxes from which no information will be downloaded since the connection to the Flickr API gets lost for that bbox (and the so created URL). This error does not occur often. The bboxes for which the script times out, hence no data was downloaded, are written to the file `timeouts` 

Each step the script does is documented in the files `documentation`. If the script crashes for any reasons, it can be restarted. Simply check at which bbox the script crashed and type its number into `line 50` (`if stop < 0:`). 

**What is that `.csv file`?**

To perform a geoquerry on Flickr with a bbox, the coordinates of the corner of the bbox need be known. 
With a geoquery request, 250 photos are returned per page in the browser (max 16 pages) and only 4.000 photos per bbox in total. Therefore, if information for a whole country or urban area need to be downloaded, the bboxes need to be split into smaller bboxes. 
To create a grid of small bboxes over the area of interest, QGIS (http://www.qgis.org/en/site/) and the tool `Vector - Research Tools - Vector Grid (Output as Polygons)` can be used. Save the output file as .csv.
This created .csv file needs to be the inputfile of `p` (`p = "FILEWITHBBOXES.csv"`).



<h3> example_langid.py</h3>
 

Needs the langid library installed (https://github.com/saffsd/langid.py)

It identifies the language used 'on' the photo with the langid library.
Iterates through the SQLite database and uses (in this example here) the title for language identification. The script writes the identified language (no matter how high the reliability is) to the same SQLite database, in the same row from where it go its sample.



<h3>example_chromium.py</h3>


Needs the Chromium compact language detector (cld) library installed (https://pypi.python.org/pypi/chromium_compact_language_detector/0.1.1)

It identifies the language used 'on' the photo with the cld library.
Iterates through the SQLite database and uses (in this example here) the description for language identification. Writes the identified language (no matter how high the reliability is) to the same SQLite database, in the same row from where it go its sample.



<h3>boolean_logic.py</h3>


To be done after the language was identified with the `cld-` and `langid library` for `title`, `tags` and `description`.
Defines the final language of the photos. It uses the identified languages of the `langid` and `cld library` (`title, tags description`) and follows following Boolean logic to determine through an intersection (of `title, tags description) the final language:

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

Since only langid can identify pashto (here '`OO`') the logic is slightly modified for this language (row 7,8,9).
Through the hierarchy in the code it becomes obvious, which combination of possibilities is weighted 'heavier'. 



<h3>ranking_language.py</h3>


This is not needed to create the map. But, if you are interested in which language was used the most in your downloaded data, this script needs to be used. All the libraries used (`csv, operator, sqlite3`) in this script come naturally with Python.  I took a detour with reading out the rows from the Database where the language was everything, but undefined ("`un") and wrote these rows to a .`csv` file. Afterwards, a dictionary and update was used to count how often which language occurred. 



<h3>ranking_tags</h3>

This is not needed to create the map neither. However, it deploys a ranking which tag(s) where used the most. The `nltk library` was used which comes naturally with Python. It uses the process of stemming to reduce the words to their linguistic stem which allows a more meaningful ranking ('dancer', 'dancing' and 'dance' will be reduced to 'danc' which is desired since all the words refer to the same activity). It iterates through a dictionary and only selects the rows for the matching language (a Stemmer needs a defined input language). For example in the first iteration the script only reads out the rows where the `language_final` was set to `da (danish)`. It creates a dictionary and updates it corresponding to how often a word was used and finally writes the ranking to a `.csv` file. 



<h2>postgres:postgis</h2>

PostgreSQL with the PostGIS extension is needed. A boundled package can be downloaded here: http://www.kyngchaos.com/software/postgres.

More meaningful assumptions about the distribution of points on a map can be made when the map is divided into polygons (here hexagons), the points are counted inside each hexagon and finally summed up per hexagon. This process is called binning.

    UPDATE hexagonFinerWgs_clip SET count = (SELECT count(*) FROM points_france WHERE ST_Within(points_france.geom, hexagonFinerWgs_clip.geom));


The same goes for the distribution of the language. Through the Boolean Logic each photo got a language assigned to. We can plot each point (because it has lat/long) on a map. The following lines count the points per hexagon and groups them by the language.

     CREATE TABLE count_language_france AS SELECT count(*), france.language, hexagons.gid, hexagons.top, hexagons.bottom, hexagons.left, hexagons.right, hexagons.geom FROM hexagonfinerwgs_clip AS hexagons, points_language_france AS france WHERE ST_Within(france.geom, hexagons.geom) GROUP BY france.language, hexagons.gid ORDER BY hexagons.gid DESC;


Nearly done. There are for example Farsi, Dari and English counted in one hexagon. But, we are only interested in the most usedlanguage per hexagon. Therefore the `SELECT DISTINCT ON` is used to only pick one (!) of a group (here, the one with the most counts)

     CREATE TABLE count_language_france_binning2 AS SELECT DISTINCT ON (t.gid) t.gid, t.language, t.count, t.top, t.right, t.bottom, t.geom FROM count_language_france AS t ORDER BY t.gid, t.count DESC;


The code is in the `postgres:postgis` in a `.sql` document as well. 



<h3>example_bboxes</h3>

The folder contains two `shapefiles` and two `.csv-files` with the bboxes (basically a grid layed over the country) used to download the data. 
