CREATE (x1:L {k1: "1"})-[yA:E {k2: "2", k3: "3a"}]->()
MERGE (x1)-[yB:E {k2: "2", k3: "3b"}]->()
MERGE (x2:L {k1: "1"})-[yC:E {k2: "2", k3: "3c"}]->()
MERGE (x2)-[yD:E {k2: "2", k3: "3d"}]->();
