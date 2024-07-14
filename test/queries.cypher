// SINGLE Subject (CP)
MATCH (s:SUBJECT)<-[r1:READ_FOR]-(r:READ)-[r2:ABS_POWER]->(w:WAVE),
  (r)-[r3:READ_AT]->(c:CHANNEL)-[r4:LOC_AT]->(b:BRAINREG)
WHERE c.Study_Common AND r.ReadMode = 'EC' AND s.ID = 1001
RETURN s, b, c, w, r, r1, r2, r3, r4;


// ABSPOWER STATS Batched for 20 subjects at a time to address AuraDB free tier limitations
// (P1) 1001,sub-010,True - 1020,sub-014,True
MATCH (s:SUBJECT)<-[r1:READ_FOR]-(r:READ)-[r2:ABS_POWER]->(w:WAVE),
  (r)-[r3:READ_AT]->(c:CHANNEL)-[r4:LOC_AT]->(b:BRAINREG) 
WHERE s.PainMarker  AND c.Study_Common AND r.ReadMode = 'EC' AND s.ID > 1000 AND s.ID < 1021
RETURN s.Name, b.Name, c.Name, w.Name, r2.Weight ORDER BY s.Name, b.Name, c.Name, w.Name;
// (P1) 1075,sub-032320,False - 1093,sub-032381,False
MATCH (s:SUBJECT)<-[r1:READ_FOR]-(r:READ)-[r2:ABS_POWER]->(w:WAVE),
  (r)-[r3:READ_AT]->(c:CHANNEL)-[r4:LOC_AT]->(b:BRAINREG) 
WHERE NOT s.PainMarker  AND c.Study_Common AND r.ReadMode = 'EC' AND s.ID > 1074 AND s.ID < 1094
RETURN s.Name, b.Name, c.Name, w.Name, r2.Weight ORDER BY s.Name, b.Name, c.Name, w.Name;

// BNN SAMPLE Database Stats

// Node Stats
MATCH (n) WHERE rand() <= 0.1
WITH labels(n) as labels, size(keys(n)) as props, size((n)--()) as degree
RETURN
DISTINCT labels,
count(*) AS NumofNodes,
avg(props) AS AvgNumOfPropPerNode,
min(props) AS MinNumPropPerNode,
max(props) AS MaxNumPropPerNode,
avg(degree) AS AvgNumOfRelationships,
min(degree) AS MinNumOfRelationships,
max(degree) AS MaxNumOfRelationships


// Relationship Stats
MATCH (n) MATCH (n)-[r]-() 
WITH type(r) as types, size(keys(r)) as props
RETURN
DISTINCT types,
count(*) AS NumofEdges,
avg(props) AS AvgNumOfPropPerEdge,
min(props) AS MinNumPropPerEdge,
max(props) AS MaxNumPropPerEdge
