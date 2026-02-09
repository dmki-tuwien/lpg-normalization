CREATE (p:Person {name: "Neo", hobby: "English"})
CREATE (e1:Event {name: "No Socks", company: "Cactus", venue: "Vault", time: "06/01"})
CREATE (e2:Event:Confirmed {name: "No Socks", company: "Cactus", venue: "Vault", time: "13/07"})
CREATE (p)-[:ATTENDS]->(e1)
CREATE (p)-[:ATTENDS]->(e2);
