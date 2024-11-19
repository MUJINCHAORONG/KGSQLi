from py2neo import Node,Relationship,Graph,Path,Subgraph
from py2neo import NodeMatcher,RelationshipMatcher
import os
import csv

def travel_node(p_node):

    r_type = "mode-mode"
    relationship = list(relationship_matcher.match([p_node], r_type=r_type))
    if (len(relationship) > 0):
        for rel in relationship:
            c_node = rel.end_node
            p_mode = p_node["data"]
            c_mode = c_node["data"]
            mode_mode = "%s-%s" % (p_mode, c_mode)
            if mode_mode in mode_mode_set:
                break
            else:
                mode_mode_set.add(mode_mode)
                write_row(p_mode, c_mode)
                travel_node(c_node)

def write_row(data1, data2):

    row_line = []
    row_line.append(data1)
    row_line.append(data2)
    mm_writer.writerow(row_line)

def write_mode_mode_csv():

    # global mode_mode_dic
    # mode_mode_dic = {}

    start_node = node_matcher.match("start").first()
    relationship = list(relationship_matcher.match([start_node], r_type="start-mode"))
    if (len(relationship) > 0):
        for rel in relationship:
            c_node = rel.end_node
            write_row("start", c_node["data"])
            # start_mode = "%s-%s" % ("start", c_node["data"])
            # mode_mode_dic[start_mode] = 0
            travel_node(c_node)

def write_val_leaf_csv():

    # global val_leaf_dic
    # val_leaf_dic = {}

    r_type = "val-leaf"
    relationship = list(relationship_matcher.match(None, r_type=r_type))
    if (len(relationship) > 0):
        for ref in relationship:
            val_node = ref.start_node
            leaf_node = ref.end_node
            row_line = []
            row_line.append(val_node["data"])
            row_line.append(leaf_node["data"])
            vl_writer.writerow(row_line)
            # val_leaf = "%s-%s" % (val_node["data"], leaf_node["data"])
            # val_leaf_dic[val_leaf] = 0

def write_kg_csv(neo4j_graph):

    global graph
    graph = neo4j_graph

    global node_matcher, relationship_matcher
    node_matcher = NodeMatcher(graph)
    relationship_matcher = RelationshipMatcher(graph)

    global mode_mode_set
    mode_mode_set = set()

    print("[+] Start write kg csv")

    global mm_writer, vl_writer

    print("[*] create mode_mode.csv")
    csvfile1 = open("mode_mode.csv", "w")

    print("[*] create val_leaf.csv")
    csvfile2 = open("val_leaf.csv", "w")

    mm_writer = csv.writer(csvfile1)
    vl_writer = csv.writer(csvfile2)
    mm_writer.writerow(["p_node", "c_node"])
    vl_writer.writerow(["p_node", "leaf"])

    print("[*] write mode_mode.csv")
    write_mode_mode_csv()
    print("[*] write val_leaf.csv")
    write_val_leaf_csv()

    csvfile1.close()
    csvfile2.close()

    print("[+] End write kg csv")
