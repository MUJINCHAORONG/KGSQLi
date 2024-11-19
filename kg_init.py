#coding=UTF-8
from connect_neo4j import connect_neo4j
from parse_bnf_rule import bnf_kgc
from create_kg_csv import write_kg_csv
from cal_payload_hnum import cal_payload_hnum

def kg_pre():

    graph  = connect_neo4j()
    bnf_kgc(graph)
    write_kg_csv(graph)
    cal_payload_hnum()

def main():
    print("[++++] start KG pre")
    kg_pre()
    print("[++++] End kg pre")
    # kg_update_hnum()

if __name__ == '__main__':
    main()