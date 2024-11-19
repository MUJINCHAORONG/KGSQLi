#coding=UTF-8
# from py2neo import Graph, Node, Relationship
from py2neo import Node,Relationship,Graph,Path,Subgraph
from py2neo import NodeMatcher,RelationshipMatcher
# from connect_neo4j import graph
# import pandas as pd
import csv
import os

def get_node(data):

    if data.startswith(('mode_', 'ter_', 'val_')):
        label = data.split('_',1)[0]
    elif(data=="start"):
        label = 'start'
    else:
        label = 'leaf'

    nodelist = list(matcher.match(label, data=data))
    if len(nodelist) > 0:
        node = nodelist[0]
    else:
        node = Node(label, data=data)
        graph.create(node)
    
    return node

def create_ref(p_node, c_node, seq=0):

    p_label = set(p_node.labels).pop()
    c_label = set(c_node.labels).pop()
    ref_name = "%s-%s" % (p_label, c_label)
    p_c_rel = Relationship(p_node, ref_name, c_node, hnum=0, seq=seq)
    graph.create(p_c_rel)

def bnf_kgc(neo4j_graph):

    global graph
    graph = neo4j_graph

    print("[+] Start parse bnf rule to build kg node")
    print("[*] clean kg")
    graph.delete_all()
    print("[*] neo4j node labels: ", end='')
    print(graph.schema.node_labels)

    global matcher
    matcher = NodeMatcher(graph)

    print("[*] parse bnf rule, build mode_, val_, ter_, leaf four types nodes and refs")

    alter = ' | '
    blank = ' '
    bnf_rule_path = "Injection.g4"
    with open(bnf_rule_path, 'r', encoding='utf-8') as f:
        for context in f.readlines():
            context = context.strip()
            if context == "":
                pass
            else:
                if context.startswith(("//","grammar")):
                    pass
                else:
                    # del ;
                    rule = context[:-1]
                    # print(rule)
                    attr_attr = rule.split(":",1)
                    attr1 = attr_attr[0].strip()
                    # print(attr1)
                    attr2 = attr_attr[1].strip()
                    # print(attr2)

                    p_node = get_node(attr1)
                    # mode_node
                    if attr1.startswith(("mode_", "start")):
                        seq = 0
                        if alter in attr2:
                            c_attr_list = attr2.split(alter)
                            step = 0
                        else:
                            c_attr_list = attr2.split(blank)
                            step = 1
                        for c_attr in c_attr_list:
                            c_node = get_node(c_attr.strip())
                            create_ref(p_node, c_node, seq)
                            seq += step                
                    # val_node
                    elif attr1.startswith("val_"):
                        if (attr1 == "val_tsq"):
                            c_node = get_node("'")
                            create_ref(p_node, c_node)
                            c_node = get_node("%27")
                            create_ref(p_node, c_node)
                        else:
                            c_attr_list = attr2.split(alter)
                            for c_attr in c_attr_list:
                                c_node = get_node(c_attr.strip()[1:-1])
                                create_ref(p_node, c_node)
                    # ter_node
                    elif attr1.startswith("ter_"):
                        c_node = get_node(attr2[1:-1])
                        create_ref(p_node, c_node)
                    else:
                        pass
    
    print("[*] neo4j node labels: ", end='')
    print(graph.schema.node_labels)
    print("[+] End parse bnf rule to build kg node")

# if __name__ == '__main__':
#     bnf_kgc()