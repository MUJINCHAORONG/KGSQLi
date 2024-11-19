#coding=UTF-8
from py2neo import Node,Relationship,Graph,Path,Subgraph
from py2neo import NodeMatcher,RelationshipMatcher

def connect_neo4j():

    print("[+] start connect neo4j db")
    neo4j_url = 'http://localhost:7475'
    dbname = 'neo4j'
    user = 'neo4j'
    pwd = 'adminadmin'
    graph = Graph(neo4j_url,auth=(user,pwd),name=dbname)

    return graph
