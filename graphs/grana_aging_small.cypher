CREATE (:Cheese {lot: "L1034"})-[:agesIn {duration: 9, goal: "Grana Padano DOP", organic: false}]->(a:AgingRoom {room: "Basement left"})
MERGE (:Cheese {lot: "L3952"})-[:agesIn {duration: 9, goal: "Grana Padano DOP"}]->(a);
