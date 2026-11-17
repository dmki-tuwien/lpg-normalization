CREATE (:Cheese {batch: "L1034"})-[:agesIn {duration: 9, type: "Grana Padano DOP", organic: false}]->(a:AgingRoom {room: "Basement left"})
MERGE (:Cheese {batch: "L2684"})-[:agesIn {duration: 20, type: "Grana Padano DOP RISERVA", organic: true}]->(a)
MERGE (:Cheese {batch: "L3952"})-[:agesIn {duration: 9, type: "Grana Padano DOP"}]->(b:AgingRoom {room: "Basement right"})
MERGE (:Cheese {batch: "L4125"})-[:agesIn {duration: 20, type: "Grana Padano DOP RISERVA", organic: false}]->(b);
