# -*- coding: utf-8 -*-
"""
Created on Fri Jul 19 00:34:20 2013

@author: Quan Xin
"""

from numpy import array
from numpy import tile
from numpy import zeros
from numpy import shape
import operator
from os import listdir

def create_data_set():
    group = array([[1.0, 1.1], [1.0, 1.0], [0, 0], [0, 0.1]])
    labels = ['A', 'A', 'B', 'B']
    return group, labels

def classify0(inX, data_set, labels, k):
    data_set_size = data_set.shape[0]
    diff_mat = tile(inX, (data_set_size, 1)) - data_set
    sq_diff_mat = diff_mat ** 2
    sq_distances = sq_diff_mat.sum(axis = 1)
    distances = sq_distances ** 0.5
    sorted_dist_indicies = distances.argsort()
    class_count = {}
    for i in range(k):
        vote_ilabel = labels[sorted_dist_indicies[i]]
        class_count[vote_ilabel] = class_count.get(vote_ilabel, 0) + 1
    sorted_class_count = sorted(class_count.iteritems(), \
                                key=operator.itemgetter(1), reverse=True)
    return sorted_class_count[0][0]

def file2matrix(filename, split_sep=None):
    fr = open(filename)
    array_of_lines = fr.readlines()
    number_of_lines = len(array_of_lines)
    number_of_width = len(array_of_lines[0].strip().split(split_sep)) - 1
    return_mat = zeros((number_of_lines, number_of_width))
    class_label_vector = []
    index = 0
    for line in array_of_lines:
        line = line.strip()
        list_from_line = line.split(split_sep)
        return_mat[index, :] = list_from_line[0:-1]
        class_label_vector.append(int(list_from_line[-1]))
        index += 1
    return return_mat, class_label_vector

# 归一化数值：使得计算距离时每个维度的权重相同，不会由于某个维度数值较大导致权重过大
def auto_norm(data_set):
    min_vals = data_set.min(0)
    max_vals = data_set.max(0)
    ranges = max_vals - min_vals
    norm_data_set = zeros(shape(data_set))
    m = data_set.shape[0]
    norm_data_set = data_set - tile(min_vals, (m, 1))
    norm_data_set /= tile(ranges, (m, 1))
    return norm_data_set, ranges, min_vals

def dating_class_test():
    ho_ratio = 0.10
    dating_data_mat, dating_labels = file2matrix('datingTestSet2.txt')
    norm_mat, ranges, min_vals = auto_norm(dating_data_mat)
    m = norm_mat.shape[0]
    num_test_vecs = int(m * ho_ratio)
    error_count = 0
    for i in range(num_test_vecs):
        classifier_result = classify0(norm_mat[i, :], \
                                      norm_mat[num_test_vecs:m, :], \
                                      dating_labels[num_test_vecs:m], 3)
        print("the classifier came back with: %d, the real answer is: %d" \
              % (classifier_result, dating_labels[i]))
        if classifier_result != dating_labels[i]:
            error_count += 1
    print("the total error rate is: %f" % (error_count/float(num_test_vecs)))

def classify_person():
    result_list = ['not at all', 'in small doses', 'in large doses']
    percent_tats = float(raw_input(\
                            "percentage os time spent playing video games ?"))
    ff_miles = float(raw_input("frequent flier miles earned per year?"))
    ice_cream = float(raw_input("liters o ice cream consumed per year?"))
    dating_data_mat, dating_labels = file2matrix('datingTestSet2.txt')
    norm_mat, ranges, min_vals = auto_norm(dating_data_mat)
    in_arr = array([ff_miles, percent_tats, ice_cream])
    classifier_result = classify0((in_arr - min_vals)/ranges, \
                                    norm_mat, dating_labels, 3)
    print("You will probably like this person: %s" \
            % result_list[classifier_result - 1])

#原始图像文件为32*32像素的黑白图像，返回一个1*1024矩阵
def img2vector(filename):
    return_vect = zeros((1, 1024))
    fr = open(filename)
    for i in range(32):
        line_str = fr.readline()
        for j in range(32):
            return_vect[0, 32*i+j] = int(line_str[j])
    return return_vect

def handwriting_class_test():
    training_floder_str = r'trainingDigits'
    test_floder_str = r'testDigits'
    hw_labels = []
    training_file_list = listdir(training_floder_str)
    m = len(training_file_list)
    training_mat = zeros((m, 1024))
    for i in range(m):
        file_name_str = training_file_list[i]
        file_str = file_name_str.split('.')[0]
        class_num_str = int(file_str.split('_')[0])
        hw_labels.append(class_num_str)
        training_mat[i, :] = img2vector("%s/%s" \
                                        % (training_floder_str, file_name_str))
    test_file_list = listdir(test_floder_str)
    error_count = 0
    m_test = len(test_file_list)
    for i in range(m_test):
        file_name_str = test_file_list[i]
        file_str = file_name_str.split('.')[0]
        class_num_str = int(file_str.split('_')[0])
        vector_under_test = img2vector("%s/%s" \
                                        % (test_floder_str, file_name_str))
        classifier_result = classify0(vector_under_test, \
                                    training_mat, hw_labels, 3)
        print("the classifier came back with: %d, the real answer is: %d" \
                % (classifier_result, class_num_str))
        if classifier_result != class_num_str:
            error_count += 1
    print("\nthe total number of errors is: %d" % error_count)
    print("\nthe total error rate is: %f" % (error_count/float(m_test)))

def iris_class_test():
    ho_ratio = 0.20
    dating_data_mat, dating_labels = file2matrix('iris.txt')
    norm_mat, ranges, min_vals = auto_norm(dating_data_mat)
    m = norm_mat.shape[0]
    num_test_vecs = int(m * ho_ratio)
    error_count = 0
    for i in range(num_test_vecs):
        classifier_result = classify0(norm_mat[i, :], \
                                      norm_mat[num_test_vecs:m, :], \
                                      dating_labels[num_test_vecs:m], 3)
        print("the classifier came back with: %d, the real answer is: %d" \
              % (classifier_result, dating_labels[i]))
        if classifier_result != dating_labels[i]:
            error_count += 1
    print("the total error rate is: %f" % (error_count/float(num_test_vecs)))

def covtype_class_test():
    ho_ratio = 0.5
    dating_data_mat, dating_labels = file2matrix('covtype_small.txt')
    norm_mat, ranges, min_vals = auto_norm(dating_data_mat)
    m = norm_mat.shape[0]
    num_test_vecs = int(m * ho_ratio)
    error_count = 0
    for i in range(num_test_vecs):
        classifier_result = classify0(norm_mat[i, :], \
                                      norm_mat[:, :], \
                                      dating_labels[:], 10)
        if classifier_result != dating_labels[i]:
            error_count += 1
    print("\nthe total number of errors is: %d" % error_count)
    print("\nthe total error rate is: %f" % (error_count/float(num_test_vecs)))

covtype_class_test()
