#coding=UTF-8
import sys
import queue
from antlr4 import *
from InjectionLexer import InjectionLexer
from InjectionParser import InjectionParser
from InjectionListener import InjectionListener
import os
import csv

def get_dataPath():
    all_data_path = []
    path = "../test4/SQL injection"
    for filepath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            all_data_path.append(os.path.join(filepath, filename))

    # print(len(all_data_path))
    return all_data_path

def update_mode_mode_dic(p_attr, c_attr):

    mode_mode = "%s-%s" % (p_attr, c_attr)
    mode_mode_dic[mode_mode] += 1

def update_val_leaf_set(typename, leaf_value):

    val_leaf = "%s-%s" % (typename, leaf_value)
    val_leaf_set.add(val_leaf)

def update_val_leaf_dic():

    for val_leaf in val_leaf_set:
        val_leaf_dic[val_leaf] += 1 

def get_node_data(node):

    tmp = node.__class__.__name__
    # antlrv4解析的结点名称末尾会加上Context，比如说startContext，因此要temp[:-7]
    data = tmp[:-7].lower()

    return data

def new_decompose(tree, parser):

    myqueue = queue.Queue()
    c_node = tree.getChild(0)
    myqueue.put(c_node)

    c_typename = get_node_data(c_node)
    update_mode_mode_dic("start", c_typename)

    while myqueue.empty() is False:

        now_node = myqueue.get()
        p_typename = get_node_data(now_node)
        count = now_node.getChildCount()

        for i in range(0, count):

            c_node = now_node.getChild(i)
            c_typename = get_node_data(c_node)

            # mode_node
            if "mode_" in c_typename:
                myqueue.put(c_node)
                update_mode_mode_dic(p_typename, c_typename)
            # val_node
            elif "val_" in c_typename:
                leaf_value = c_node.getText()
                update_val_leaf_set(c_typename, leaf_value)
            # ter_node
            else:
                pass

def parse_payload(sql):

    input_stream = InputStream(sql)
    lexer = InjectionLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = InjectionParser(stream)
    tree = parser.start()
    # BFS_decompose(tree, parser) 
    new_decompose(tree, parser)

def create_dic(csvfile, dicname):

    with open(csvfile, 'r') as f:
        reader = csv.reader(f)
        data = list(reader)
    
    for i in range(1, len(data)):
        p_data = data[i][0]
        c_data = data[i][1]
        data_data = "%s-%s" % (p_data, c_data)
        dicname[data_data] = 0

def create_mode_mode_dic():

    global mode_mode_dic
    mode_mode_dic = {}

    csvfile = "mode_mode.csv"
    create_dic(csvfile, mode_mode_dic)

def create_val_leaf_dic():

    global val_leaf_dic
    val_leaf_dic = {}

    csvfile = "val_leaf.csv"
    create_dic(csvfile, val_leaf_dic)

def split_key(key):

    attr_attr = key.split('-', 1)
    return attr_attr[0], attr_attr[1]


def print_history_num():

    print("[*] mode_mode_dic: ")
    print(mode_mode_dic)
    print("[*] val_leaf_dic: ")
    print(val_leaf_dic)

def split_key(key):

    attr_attr = key.split('-', 1)
    return attr_attr[0], attr_attr[1]

def write_row(writer, p_data, c_data, value):

    row_line = []
    row_line.append(p_data)
    row_line.append(c_data)
    row_line.append(value)
    writer.writerow(row_line)

def write_hnum():

    csvfile1 = open("mode_mode_hnum.csv", "w")
    csvfile2 = open("val_leaf_hnum.csv", "w")
    mm_writer = csv.writer(csvfile1)
    vl_writer = csv.writer(csvfile2)
    mm_writer.writerow(["p", "c", "num"])
    vl_writer.writerow(["p", "c", "num"])

    print("[*] write mode_mode_hnum.csv")
    for key, value in mode_mode_dic.items():

        p_mode, c_mode = split_key(key)
        write_row(mm_writer, p_mode, c_mode, value)

    print("[*] write val_leaf_hnum.csv")
    for key, value in val_leaf_dic.items():

        val, leaf = split_key(key)
        write_row(vl_writer, val, leaf, value)

    csvfile1.close()
    csvfile2.close()

def cal_history_num():

    print("[*] create mode_mode_dic")
    create_mode_mode_dic()
    print("[*] create val_leaf_dic")
    create_val_leaf_dic()

    global val_leaf_set
    val_leaf_set = set()

    payload_id = 0
    file_num = 0 
    # data_path = "SQLi_Dataset.txt"
    data_paths = get_dataPath()

    print("[*] parse payload and cal hnum")
    for data_path in data_paths:
        print("[*] %d: %s" % (file_num, data_path))

        with open(data_path, 'r', encoding='utf-8') as f:
            for context in f.readlines():
                # payload_id += 1
                # if (payload_id % 10000 == 0):
                #     print("[**] payload_id: %d" % payload_id)
                context = context.replace("\n","")
                try:
                    parse_payload(context)
                except:
                    print("[!!!!] payload error: %s" % context)
                    print("[!!!!] payload_id: %d" % payload_id)
                    break
                update_val_leaf_dic()
                val_leaf_set = set()
                payload_id += 1
        file_num += 1

    
def cal_payload_hnum():

    cal_history_num()
    print_history_num()
    write_hnum()

# if __name__ == '__main__':
#    parse_cal()