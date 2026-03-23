CREATE (:Cheese {lot: "L1034"})-[:agesIn {duration: 9, goal: "Grana Padano DOP", organic: false}]->(a:AgingRoom {room: "Basement left"})
MERGE (:Cheese {lot: "L2684"})-[:agesIn {duration: 20, goal: "Grana Padano DOP RISERVA", organic: true}]->(a)
MERGE (:Cheese {lot: "L3952"})-[:agesIn {duration: 9, goal: "Grana Padano DOP"}]->(b:AgingRoom {room: "Basement right"})
MERGE (:Cheese {lot: "L4125"})-[:agesIn {duration: 20, goal: "Grana Padano DOP RISERVA", organic: false}]->(b);
