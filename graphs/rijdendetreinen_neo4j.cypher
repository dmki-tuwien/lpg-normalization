LOAD CSV WITH HEADERS FROM 'file:///graphs/transport-for-london/London_stations.csv' AS row
MERGE (s:Station {name: row.Station})
SET s.latitude = ToFloat(row.Latitude),
    s.longitude = ToFloat(row.Longitude),
    s.zone = row.Zone,
    s.zoneOriginal = row.Zone_original;

LOAD CSV WITH HEADERS FROM 'file:///graphs/transport-for-london/London_tube_lines.csv' as row
MATCH (a:Station {name: row.From_Station})
MATCH (b:Station {name: row.To_Station})
CREATE (a)-[:CONNECTED_THROUGH {line: row.Tube_Line, color: row.Color}]->(b)
CREATE (b)-[:CONNECTED_THROUGH {line: row.Tube_Line, color: row.Color}]->(a);

