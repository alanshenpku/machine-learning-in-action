# -*- coding: utf-8 -*-
"""
Created on Mon Aug 05 12:16:58 2013

@author: Quan Xin
"""

def load_dataset():
    #return [[1, 3, 4], [2, 3, 5], [1, 2, 3, 5], [2, 5]]
    return [[1, 2, 3], [1, 2, 3], [1, 2, 4]]

def create_C1(dataset):
    C1 = []
    for transaction in dataset:
        for item in transaction:
            if [item] not in C1:
                C1.append([item])
    C1.sort()
    return set(map(frozenset, C1))

def scan_D(D, Ck, min_support):
    ss_cnt = {}
    for tid in D:
        for can in Ck:
            if can.issubset(tid):
                ss_cnt[can] = ss_cnt.get(can, 0) + 1
    num_items = float(len(D))
    ret_list = []
    support_data = {}
    for key in ss_cnt:
        support = ss_cnt[key] / num_items
        if support >= min_support:
            ret_list.append(key)
        support_data[key] = support
    return ret_list, support_data

def apriori_gen(Lk, k):
    ret_list = set()
    len_Lk = len(Lk)
    for i in range(len_Lk):
        for j in range(i+1, len_Lk):
            if len(Lk[i] & Lk[j])==k-2:
                ret_list |= {Lk[i] | Lk[j]}
    return ret_list

def apriori(dataset, min_support=0.5):
    C1 = create_C1(dataset)
    D = list(map(set, dataset))
    L1, support_data = scan_D(D, C1, min_support)
    L = [L1]
    k = 2
    while len(L[k-2]) > 0:
        Ck = apriori_gen(L[k-2], k)
        Lk, sup_k = scan_D(D, Ck, min_support)
        support_data.update(sup_k)
        L.append(Lk)
        k += 1
    return L, support_data

def calc_conf(freq_set, H, support_data, br1, min_conf):
    pruned_H = []
    for conseq in H:
        conf = support_data[freq_set] / support_data[freq_set-conseq]
        if conf >= min_conf:
            print("%s --> %s conf: %s" % (freq_set-conseq, conseq, conf))
            br1.append((freq_set-conseq, conseq, conf))
            pruned_H.append(conseq)
    return pruned_H

def relus_from_conseq(freq_set, H, support_data, br1, min_conf):
    m = len(H[0])
    if len(freq_set) > m+1:
        Hmp1 = apriori_gen(H, m+1)
        Hmp1 = calc_conf(freq_set, Hmp1, support_data, br1, min_conf)
        if len(Hmp1) > 1:
            relus_from_conseq(freq_set, Hmp1, support_data, br1, min_conf)

def generate_rules(L, support_data, min_conf=0.7):
    big_rule_list = []
    for i in range(1, len(L)):
        for freq_set in L[i]:
            H1 = [frozenset([item]) for item in freq_set]
            calc_conf(freq_set, H1, support_data, big_rule_list, min_conf)
            if i > 1:
                relus_from_conseq(freq_set, H1, support_data, big_rule_list, \
                                    min_conf)
    return big_rule_list

def file2dataset(filename, split_sep=None):
    fr = open(filename)
    return_data_set = [line.strip().split(split_sep) for line in fr.readlines()]
    return return_data_set

def mushroom_data_test():
    mushroom = file2dataset('mushroom.dat')
    L, support = apriori(mushroom, 0.4)
    rules = generate_rules(L, support, 0.5)
    for item in rules:
        if item[1] == frozenset(['1']):
            print("%s --> %s conf: %s" % (item[0], item[1], item[2]))
    for item in rules:
        if item[1] == frozenset(['2']):
            print("%s --> %s conf: %s" % (item[0], item[1], item[2]))

def kosarak_data_test():
    dataset = file2dataset('kosarak.dat')
    L, support = apriori(dataset, 0.1)
    print(L)

kosarak_data_test()
#mushroom_data_test()

#dataset = load_dataset()
#L, support = apriori(dataset, 0.5)
##print(L)
##print(support)
#rules = generate_rules(L, support, 0.5)
##print(rules)
