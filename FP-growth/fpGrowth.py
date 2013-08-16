# -*- coding: utf-8 -*-
"""
Created on Thu Aug 08 11:19:53 2013

@author: Quan Xin
"""

class TreeNode:
    def __init__(self, name_value, num_occur, parent_node):
        self.name = name_value
        self.count = num_occur
        self.node_link = None
        self.parent = parent_node
        self.children = {}
    def inc(self, num_occur):
        self.count += num_occur
    def disp(self, ind = 1):
        print("%s%s  %s" % ('  '*ind, self.name, self.count))
        for child in self.children.values():
            child.disp(ind+1)

def create_tree(dataset, min_support = 1):
    header_table = {}
    for trans in dataset:
        for item in trans:
            header_table[item] = header_table.get(item, 0) + dataset[trans]
    for k in header_table.keys():
        if header_table[k] < min_support:
            del(header_table[k])
    freq_itemset = set(header_table.keys())
    if len(freq_itemset) == 0:
        return None, None
    for k in header_table:
        header_table[k] = [header_table[k], None]
    ret_tree = TreeNode('Null Set', 1, None)
    for tran_set, count in dataset.items():
        local_D = {}
        for item in tran_set:
            if item in freq_itemset:
                local_D[item] = header_table[item][0]
        if len(local_D) > 0:
            orderd_items = [v[0] for v in sorted(local_D.items(), \
                            key=lambda p:p[1], reverse=True)]
            update_tree(orderd_items, ret_tree, header_table, count)
    return ret_tree, header_table

def update_tree(items, in_tree, header_table, count):
    if items[0] in in_tree.children:
        in_tree.children[items[0]].inc(count)
    else:
        in_tree.children[items[0]] = TreeNode(items[0], count, in_tree)
        if header_table[items[0]][1] == None:
            header_table[items[0]][1] = in_tree.children[items[0]]
        else:
            update_header(header_table[items[0]][1], \
                            in_tree.children[items[0]])
    if len(items) > 1:
        update_tree(items[1:], in_tree.children[items[0]], \
                    header_table, count)

def update_header(node2test, target_node):
    while node2test.node_link != None:
        node2test = node2test.node_link
    node2test.node_link = target_node

def ascend_tree(leaf_node, prefix_path):
    if leaf_node.parent != None:
        prefix_path.append(leaf_node.name)
        ascend_tree(leaf_node.parent, prefix_path)

def find_prefix_path(base_pat, tree_node):
    cond_pats = {}
    while tree_node != None:
        prefix_path = []
        ascend_tree(tree_node, prefix_path)
        if len(prefix_path) > 1:
            cond_pats[frozenset(prefix_path[1:])] = tree_node.count
        tree_node = tree_node.node_link
    return cond_pats

def mine_tree(in_tree, header_table, min_support, prefix, freq_item_list):
    big_L = [v[0] for v in sorted(header_table.items(), key=lambda p:p[1])]
    for base_pat in big_L:
        new_freq_set = prefix.copy()
        new_freq_set.add(base_pat)
        freq_item_list.append(new_freq_set)
        cond_patt_bases = find_prefix_path(base_pat, header_table[base_pat][1])
        my_cond_tree, my_head = create_tree(cond_patt_bases, min_support)
#        if my_cond_tree != None:
#            print("conditional tree for : %s" % new_freq_set)
#            my_cond_tree.disp()
        if my_head != None:
            mine_tree(my_cond_tree, my_head, min_support, \
                        new_freq_set, freq_item_list)

def load_simp_data():
#    return [['r', 'z', 'h', 'j', 'p'], 
#            ['z', 'y', 'x', 'w', 'v', 'u', 't', 's'], 
#            ['z'], 
#            ['r', 'x', 'n', 'o', 's'], 
#            ['y', 'r', 'x', 'z', 'q', 't', 'p'], 
#            ['y', 'z', 'x', 'e', 'q', 's', 't', 'm']]
    return [[1, 2, 3], [1, 2, 3], [1, 2, 4]]

def create_init_set(dataset):
    ret_dict = {}
    for trans in dataset:
        ret_dict[frozenset(trans)] = ret_dict.get(frozenset(trans), 0) + 1
    return ret_dict

min_sup = 100000
#min_sup = 2
#dataset = load_simp_data()
dataset = [line.split() for line in open('kosarak.dat')]
initset = create_init_set(dataset)
myFPtree, myHeaderTab = create_tree(initset, min_sup)
#myFPtree.disp()
myFreqList = []
mine_tree(myFPtree, myHeaderTab, min_sup, set([]), myFreqList)
print(myFreqList)
