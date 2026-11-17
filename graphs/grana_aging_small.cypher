CREATE (:Cheese {batch: "L1034"})-[:agesIn {duration: 9, type: "Grana Padano DOP", organic: false}]->(a:AgingRoom {room: "Basement left"})
MERGE (:Cheese {batch: "L3952"})-[:agesIn {duration: 9, type: "Grana Padano DOP"}]->(a);
