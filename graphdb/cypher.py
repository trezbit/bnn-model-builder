# Description: This file contains CYPHER templates, and the model operators for the graph database.

CLEANUP_GRAPH = """
	MATCH (n)
	OPTIONAL MATCH (n)-[r]-()
	DELETE n,r
"""
