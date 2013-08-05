# -*- coding: utf-8 -*-
"""
Created on Sat Jul 27 12:20:37 2013

@author: Quan Xin
"""

from math import log
import operator

f = open('log.txt', 'w', True)

#计算香农熵
def calc_shannon_ent(data_set):
    num_entries = len(data_set)
    label_counts = {}
    for feat_vec in data_set:
        curr_label = feat_vec[-1]
        if curr_label not in label_counts.keys():
            label_counts[curr_label] = 0
        label_counts[curr_label] += 1
    shannon_ent = 0.0
    for key in label_counts:
        prob = float(label_counts[key])/num_entries
        shannon_ent -= prob * log(prob, 2)
    return shannon_ent

def create_data_set():
    data_set = [[1, 1, 'yes'], 
                [1, 1, 'yes'], 
                [1, 0, 'no'], 
                [0, 1, 'no'], 
                [0, 1, 'no']]
    labels = ['no surfacing', 'flippers']
    return data_set, labels

#按照给定特征划分数据集，axis为给定特征，value为给定特征值
def split_data_set(data_set, axis, value):
    return_data_set = []
    for feat_vec in data_set:
        if feat_vec[axis] == value:
            reduced_feat_vec = feat_vec[:axis]
            reduced_feat_vec.extend(feat_vec[axis+1:])
            return_data_set.append(reduced_feat_vec)
    if len(return_data_set[0]) != len(data_set[0]) - 1:
        f.write("\n\n\n\n\n\ndata_set:\n%s\n" % data_set)
        f.write("%s = %s\n" % (axis, value))
        f.write("return_data_set:\n%s\n\n\n\n\n\n" % return_data_set)
        raise Exception
    return return_data_set

#选择最好的数据集划分方式
def choose_best_feature_to_split(data_set):
    num_features = len(data_set[0]) - 1
    base_entropy = calc_shannon_ent(data_set)
    best_info_gain = 0.0
    best_feature = -1
    for i in range(num_features):
        feat_list = [example[i] for example in data_set]
        unique_vals = set(feat_list)
        new_entropy = 0.0
        for value in unique_vals:
            sub_data_set = split_data_set(data_set, i, value)
            prob = len(sub_data_set)/float(len(data_set))
            new_entropy += prob * calc_shannon_ent(sub_data_set)
        info_gain = base_entropy - new_entropy
        if info_gain > best_info_gain:
            best_info_gain = info_gain
            best_feature = i
    return best_feature

#多数表决
def majority_cnt(class_list):
    class_count = {}
    for vote in class_list:
        if vote not in class_count.keys():
            class_count[vote] = 0
        class_count[vote] += 1
    sorted_class_count = sorted(class_count.iteritems(), \
                                key = operator.itemgetter(1), reverse = True)
    return sorted_class_count[0][0]

def create_tree(data_set, labels):
#    f.write("0\n")
#    f.write("%s\n" % data_set)
    class_list = [example[-1] for example in data_set]
    if class_list.count(class_list[0]) == len(class_list):
#        f.write("1\n")
        return class_list[0]
    if len(data_set[0]) == 1:
#        f.write("2\n")
        return majority_cnt(class_list)
    best_feat = choose_best_feature_to_split(data_set)
    if best_feat == -1:
        return majority_cnt(class_list)
    best_feat_label = labels[best_feat]
    my_tree = {best_feat_label:{}}
    del(labels[best_feat])
    feat_values = [example[best_feat] for example in data_set]
    unique_vals = set(feat_values)
#    f.write("%s\n" % best_feat_label)
#    f.write("%s\n" % unique_vals)
    for value in unique_vals:
        sub_labels = labels[:]
        my_tree[best_feat_label][value] = create_tree(split_data_set(data_set,\
                                                best_feat, value), sub_labels)
#    f.write("3\n")
#    f.write("%s\n" % my_tree)
    return my_tree

def store_tree(input_tree, filename):
    import pickle
    fw = open(filename, 'w')
    pickle.dump(input_tree, fw)
    fw.close()

def grab_tree(filename):
    import pickle
    fr = open(filename)
    return pickle.load(fr)

def file2dataset(filename, split_sep=None, get_des=False):
    fr = open(filename)
    return_data_set = [line.strip().split(split_sep) for line in fr.readlines()]
    if get_des == False:
        return return_data_set
    return return_data_set[1:], return_data_set[0][:-1]

def classify(input_tree, feat_labels, test_vec):
    first_str = input_tree.keys()[0]
    second_dict = input_tree[first_str]
    feat_index = feat_labels.index(first_str)
    for key in second_dict.keys():
        if test_vec[feat_index] == key:
            if type(second_dict[key]).__name__ == 'dict':
                class_label = classify(second_dict[key], feat_labels, test_vec)
            else:
                class_label = second_dict[key]
    try:
        return class_label
    except:
        f.write("%s\n%s\n%s\n%s\n" % 
            (second_dict.keys(), test_vec[feat_index], feat_index, test_vec))
        raise

def covtype_class_test():
    ho_ratio = 0.5
    data_set, labels = file2dataset('covtype.txt', get_des=True)
#    print(labels)
    m = len(data_set)
    num_test_vecs = int(m * ho_ratio)
    tree = create_tree(data_set, labels[:])
    store_tree(tree, 'tree.txt')
    print('finish creating tree')
#    tree = grab_tree('tree.txt')
    print(tree)
    error_count = 0
    for i in range(num_test_vecs):
        classifier_result = classify(tree, labels, data_set[i][:-1])
        if classifier_result != data_set[i][-1]:
            error_count += 1
    print("\nthe total number of errors is %d" % error_count)
    print("\nthe total error rate is: %f" % (error_count/float(num_test_vecs)))

try:
    covtype_class_test()
except:
    f.close()
    raise
