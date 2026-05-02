CREATE (x1:L {k1: "1"})-[yA:E {k2: "2", k3: "3a"}]->()
MERGE (x1)-[yB:E {k2: "2", k3: "3b"}]->()
MERGE (x1)-[yC:E {k2: "2", k3: "3c"}]->()
MERGE (x1)-[yD:E {k2: "2", k3: "3d"}]->();
