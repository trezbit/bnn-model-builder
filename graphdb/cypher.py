# Description: This file contains CYPHER templates, and the model operators for the graph database.
import config.includes as inc



CLEANUP_GRAPH = """
	MATCH (n)
	OPTIONAL MATCH (n)-[r]-()
	DELETE n,r
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
    WHERE NOT row.`ID` IN $idsToSkip AND NOT toInteger(trim(row.`ID`)) IS NULL
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
