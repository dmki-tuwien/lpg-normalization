CREATE (x:L {k1: "1"})-[yA:E {k2: "2", k3: "3a"}]->()
MERGE (x)-[yB:E {k2: "2", k3: "3b"}]->()
MERGE (x)-[yC:E {k2: "2", k3: "3c"}]->()
MERGE (x)-[yD:E {k2: "2", k3: "3d"}]->();
