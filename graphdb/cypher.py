# Description: This file contains CYPHER templates, and the model operators for the graph database.
import config.includes as inc



CLEANUP_GRAPH = """
	MATCH (n)
	OPTIONAL MATCH (n)-[r]-()
	DELETE n,r
"""

CLEANUP_STUDY_GRAPH = """
	MATCH (m:READ)
	OPTIONAL MATCH (m)-[r1:READ_FOR]-(s:SUBJECT)
    OPTIONAL MATCH (m)-[r2:READ_AT]-()
    OPTIONAL MATCH (m)-[r3:ABS_POWER]-()
	DELETE m,s,r1,r2,r3;
"""

# Create constraints & indices

CREATE_CONSTRAINT ="""CREATE CONSTRAINT id___LABEL___uniq IF NOT EXISTS FOR (n: __LABEL__) REQUIRE (n.`id`) IS UNIQUE;"""

CREATE_FULLTEXT_INDEX ="""
CREATE FULLTEXT INDEX name___LABEL___fulltext_index
  IF NOT EXISTS
  FOR (n:__LABEL__) 
  ON EACH [n.`name`]
"""


# TOPOLOGY GRAPH
# Node & Edge LOAD statements
LOAD_BRAINREG="""
    LOAD CSV WITH HEADERS FROM '""" +  inc.PUBLIC_GRAPH_DATA_ROOT + """/node.region.csv'
    AS row WITH row
    WHERE NOT toInteger(trim(row.`ID`)) IS NULL
    CALL {
      WITH row
      MERGE (n: `BRAINREG` { `ID`: toInteger(trim(row.`ID`)) })
      SET n.`ID` = toInteger(trim(row.`ID`))
      SET n.`Name` = row.`Name`
    } IN TRANSACTIONS OF 10000 ROWS;
"""
LOAD_CHANNEL="""
    LOAD CSV WITH HEADERS FROM '""" +  inc.PUBLIC_GRAPH_DATA_ROOT + """/node.channel.csv'
    AS row WITH row
    WHERE NOT toInteger(trim(row.`ID`)) IS NULL
    CALL {
       WITH row
  	   MERGE (n: `CHANNEL` { `ID`: toInteger(trim(row.`ID`)) })
       SET n.`ID` = toInteger(trim(row.`ID`))
       SET n.`Name` = row.`Name`
       SET n.`AbsDist` = toInteger(trim(row.`AbsDist`))
       SET n.`Lattitude` = toInteger(trim(row.`Lattitude`))
       SET n.`CircM0` = toLower(trim(row.`CircM0`)) IN ['1','true','yes']
       SET n.`CircM1` = toLower(trim(row.`CircM1`)) IN ['1','true','yes']
       SET n.`Ref_Y` = toLower(trim(row.`Ref_Y`)) IN ['1','true','yes']
       SET n.`Ref_X` = toLower(trim(row.`Ref_X`)) IN ['1','true','yes']
       SET n.`REF_Pole` = row.`REF_Pole`
       SET n.`Study_Common` = toLower(trim(row.`Study_Common`)) IN ['1','true','yes']
    } IN TRANSACTIONS OF 10000 ROWS;
"""
LOAD_LOC_AT="""
    LOAD CSV WITH HEADERS FROM '""" +  inc.PUBLIC_GRAPH_DATA_ROOT + """/edge.loc_at.csv'
    AS row WITH row
    CALL {
      WITH row
      MATCH (source: `CHANNEL` { `ID`: toInteger(trim(row.`FromID`)) })
      MATCH (target: `BRAINREG` { `ID`: toInteger(trim(row.`ToID`)) })
      MERGE (source)-[r: `LOC_AT`]->(target)
      SET r.`Orientation` = toInteger(trim(row.`Orientation`))
      SET r.`FromID` = toInteger(trim(row.`FromID`))
      SET r.`ToID` = toInteger(trim(row.`ToID`))
    } IN TRANSACTIONS OF 10000 ROWS;
"""
LOAD_CHAIN_NEXT="""
    LOAD CSV WITH HEADERS FROM '""" +  inc.PUBLIC_GRAPH_DATA_ROOT + """/edge.chain.csv'
    AS row WITH row
    CALL {
      WITH row
      MATCH (source: `CHANNEL` { `ID`: toInteger(trim(row.`FromID`)) })
      MATCH (target: `CHANNEL` { `ID`: toInteger(trim(row.`ToID`)) })
      MERGE (source)-[r: `CHAIN`]->(target)
      SET r.`FromID` = toInteger(trim(row.`FromID`))
      SET r.`ToID` = toInteger(trim(row.`ToID`))
      SET r.`Type` = row.`Type`
      SET r.`Name` = row.`Name`
      SET r.`Orientation` = toInteger(trim(row.`Orientation`))
      SET r.`Align` = toInteger(trim(row.`Align`))
    } IN TRANSACTIONS OF 10000 ROWS;
"""

LOAD_READ="""
LOAD CSV WITH HEADERS FROM '""" +  inc.PUBLIC_GRAPH_DATA_ROOT + """/node.read.csv'
AS row WITH row
WHERE NOT toInteger(trim(row.`ID`)) IS NULL
CALL {
  WITH row
  MERGE (n: `READ` { `ID`: toInteger(trim(row.`ID`)) })
  SET n.`ID` = toInteger(trim(row.`ID`))
  SET n.`Name` = row.`Name`
  SET n.`ReadMode` = row.`ReadMode`
} IN TRANSACTIONS OF 10000 ROWS;
"""

LOAD_SUBJECT="""
LOAD CSV WITH HEADERS FROM '""" +  inc.PUBLIC_GRAPH_DATA_ROOT + """/node.subject.csv'
AS row WITH row
WHERE NOT toInteger(trim(row.`ID`)) IS NULL
CALL {
  WITH row
  MERGE (n: `SUBJECT` { `ID`: toInteger(trim(row.`ID`)) })
  SET n.`ID` = toInteger(trim(row.`ID`))
  SET n.`Name` = row.`Name`
  SET n.`PainMarker` = toLower(trim(row.`PainMarker`)) IN ['1','true','yes']
} IN TRANSACTIONS OF 10000 ROWS;
"""


LOAD_WAVE="""
LOAD CSV WITH HEADERS FROM '""" +  inc.PUBLIC_GRAPH_DATA_ROOT + """/node.wave.csv'
AS row WITH row
WHERE NOT toInteger(trim(row.`ID`)) IS NULL
CALL {
  WITH row
  MERGE (n: `WAVE` { `ID`: toInteger(trim(row.`ID`)) })
  SET n.`ID` = toInteger(trim(row.`ID`))
  SET n.`Name` = row.`Name`
  SET n.`Range_Min` = toInteger(trim(row.`Range_Min`))
  SET n.`Range_Max` = toInteger(trim(row.`Range_Max`))
} IN TRANSACTIONS OF 10000 ROWS;
"""



LOAD_READ_AT="""
LOAD CSV WITH HEADERS FROM '""" +  inc.PUBLIC_GRAPH_DATA_ROOT + """/edge.read_at.csv'
AS row WITH row
CALL {
  WITH row
  MATCH (source: `READ` { `ID`: toInteger(trim(row.`FromID`)) })
  MATCH (target: `CHANNEL` { `ID`: toInteger(trim(row.`ToID`)) })
  MERGE (source)-[r: `READ_AT`]->(target)
  SET r.`FromID` = toInteger(trim(row.`FromID`))
  SET r.`ToID` = toInteger(trim(row.`ToID`))
} IN TRANSACTIONS OF 10000 ROWS;

"""

LOAD_READ_FOR="""
LOAD CSV WITH HEADERS FROM '""" +  inc.PUBLIC_GRAPH_DATA_ROOT + """/edge.read_for.csv'
AS row WITH row
CALL {
  WITH row
  MATCH (source: `READ` { `ID`: toInteger(trim(row.`FromID`)) })
  MATCH (target: `SUBJECT` { `ID`: toInteger(trim(row.`ToID`)) })
  MERGE (source)-[r: `READ_FOR`]->(target)
  SET r.`FromID` = toInteger(trim(row.`FromID`))
  SET r.`ToID` = toInteger(trim(row.`ToID`))
} IN TRANSACTIONS OF 10000 ROWS;
"""

LOAD_ABSOLUTE_POWER="""
LOAD CSV WITH HEADERS FROM '""" +  inc.PUBLIC_GRAPH_DATA_ROOT + """/edge.abs_power.csv'
AS row WITH row
CALL {
  WITH row
  MATCH (source: `READ` { `ID`: toInteger(trim(row.`FromID`)) })
  MATCH (target: `WAVE` { `ID`: toInteger(trim(row.`ToID`)) })
  MERGE (source)-[r: `ABS_POWER`]->(target)
  SET r.`FromID` = toInteger(trim(row.`FromID`))
  SET r.`ToID` = toInteger(trim(row.`ToID`))
  SET r.`Weight` = toFloat(trim(row.`Weight`))
} IN TRANSACTIONS OF 10000 ROWS;
"""







