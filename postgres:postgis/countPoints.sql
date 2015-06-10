#count points per polygon
UPDATE hexagonFinerWgs_clip SET count = (SELECT count(*) FROM points_france WHERE ST_Within(points_france.geom, hexagonFinerWgs_clip.geom));


#count points per polygon but do not loose language information
CREATE TABLE count_language_france AS SELECT count(*), france.language, hexagons.gid, hexagons.top, hexagons.bottom, hexagons.left, hexagons.right, hexagons.geom FROM hexagonfinerwgs_clip AS hexagons, points_language_france AS france WHERE ST_Within(france.geom, hexagons.geom) GROUP BY france.language, hexagons.gid ORDER BY hexagons.gid DESC;


#only keep language which was used the most 
CREATE TABLE count_language_france_binning2 AS SELECT DISTINCT ON (t.gid) t.gid, t.language, t.count, t.top, t.right, t.bottom, t.geom FROM count_language_france AS t ORDER BY t.gid, t.count DESC;
