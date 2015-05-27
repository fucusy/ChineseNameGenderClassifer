__author__ = 'fucus'
#!encoding=utf-8
from help.helper import Singleton
from config.main import  Location
from config.main import  BayseConfig
from help.helper import save_to_file

from help.helper import ChineseText
from help.helper import log
import random
import csv

import math



class bayes_classifier():
    __metaclass__ = Singleton
    p_vector_dic = {}
    type_list = []
    word_list = []
    type_count = {}
    count = 0
    is_trained = False

    def train_process(self, type_tran_data = Location.data_path):
        # word in type count
        type_word_dic = {}
        type_word_sum = {}
        self.p_vector_dic = {}
        self.type_list = []
        self.word_list = []
        self.type_count = {}
        self.count = 0

        have_skipped = 0


        type_index = BayseConfig.type_index
        content_index = BayseConfig.content_index
        with open(type_tran_data) as f:
            for line in f:
                if BayseConfig.is_skip_first_line and have_skipped == 0:
                    have_skipped = 1
                    continue
                split_line = line.split(",")
                # remove '"' around content

                for i in range(len(split_line)):
                    split_line[i] = split_line[i].strip('\n')
                    split_line[i] = split_line[i].strip('"')


                self.count += 1
                words = ChineseText.cut_name_to_element(split_line[content_index])

                if split_line[type_index] not in self.type_list:
                    self.type_list.append(split_line[type_index])

                if not self.type_count.has_key(split_line[type_index]):
                    self.type_count[split_line[type_index]] = 1
                else:
                    self.type_count[split_line[type_index]] += 1

                if not type_word_dic.has_key(split_line[type_index]):
                    type_word_dic[split_line[type_index]] = {}

                if not type_word_sum.has_key(split_line[type_index]):
                    type_word_sum[split_line[type_index]] = 0

                for word in words:
                    type_word_sum[split_line[type_index]] += 1
                    if not type_word_dic[split_line[type_index]].has_key(word):
                        type_word_dic[split_line[type_index]][word] = 1
                    else:
                        type_word_dic[split_line[type_index]][word] += 1

                    if word not in self.word_list:
                        self.word_list.append(word)


        word_type_frequency = {}
        for w in self.word_list:
            word_type_frequency[w] = 0
            for t in self.type_list:
                if type_word_dic.has_key(t) and type_word_dic[t].has_key(w):
                    word_type_frequency[w] += 1

        for t in self.type_list:
            self.p_vector_dic[t] = {}
            type_word_t_sum = 0
            if type_word_sum.has_key(t):
                type_word_t_sum = type_word_sum[t]
            for w in self.word_list:
                word_count = 0
                if type_word_dic.has_key(t) and type_word_dic[t].has_key(w):
                    word_count = type_word_dic[t][w]

                word_type_frequency_w = 0
                if word_type_frequency.has_key(w):
                    word_type_frequency_w = word_type_frequency[w]
                self.p_vector_dic[t][w] = (0.5 + word_count) / (len(self.type_list) + type_word_t_sum)
                # self.p_vector_dic[t][w] *=  math.log(len(self.type_list) + 0.1 / word_type_frequency_w + 0.1)

        self.is_trained = True


    @staticmethod
    def get_classify_label(q):
        c = bayes_classifier()
        return c.classify(q)

    def classify(self, q):
        if not self.is_trained:
            self.train_process()
        words = ChineseText.cut_name_to_element(q)
        class_score = {}
        for t in self.type_list:
            class_score[t] = 1
            for w in words:
                if w in self.word_list:
                    class_score[t] *= self.p_vector_dic[t][w]
            class_score[t] *= ( self.type_count[t]*1.0 / (self.count + 1))
        max_val = 0
        max_type = ""
        for t in class_score.keys():
            if class_score[t] > max_val:
                max_val = class_score[t]
                max_type = t
        return max_type


def name_distribution():
    dis_dic = {}
    with open(Location.data_path) as f:
        for row in f:
            split_line = row.split(",")
            for i in range(len(split_line)):
                split_line[i] = split_line[i].strip("\n")
                split_line[i] = split_line[i].strip('"')
            len_name = len(split_line[BayseConfig.content_index])
            len_name = len_name / 3
            if len_name >=4 :
                print split_line[BayseConfig.content_index]
            if dis_dic.has_key(len_name):
                dis_dic[len_name] += 1
            else:
                dis_dic[len_name] = 1
    for i in dis_dic.keys():
        print "%s字，%s人"%(i, dis_dic[i])



def bayes_classifier_ten_fold_test():
    data_path = Location.data_path
    data_set = []
    test_tran_file_name_tep  = "test-tran-data-%d.txt"


    with open(data_path) as f:
        for line in f:
            split_line = line.split(",")

            for i in range(len(split_line)):
                split_line[i] = split_line[i].strip('\n')
                split_line[i] = split_line[i].strip('"')

            q_class = split_line[BayseConfig.type_index]
            q_content = split_line[BayseConfig.content_index]
            if q_class is None:
                continue
            q_dic = {"q_class":q_class,"q_content":q_content}
            data_set.append(q_dic)
    correct_class_sum = 0

    times = 10
    for i in range(times):
        choose_to_tran_number = len(data_set)*(times -1)/times
        candidate_number_list = [k for k in range(0,len(data_set))]
        chosen_number_list = []
        test_number_list = []
        while len(chosen_number_list) < choose_to_tran_number:
            choose = random.randrange(0, len(candidate_number_list))
            candidate_number_list.pop(choose)
            chosen_number_list.append(choose)
        test_number_list = candidate_number_list[:]

        type_tran_data = ""
        for n in chosen_number_list:
            type_tran_data += "%s,%s\n"%(data_set[n]["q_content"],data_set[n]["q_class"])

        file_name = test_tran_file_name_tep%i
        print "the file name is %s"%file_name
        save_to_file(type_tran_data, file_name,replace=True)
        b = bayes_classifier()

        b.train_process(Location.data_dir+file_name)

        correct_class = 0
        for test_n in test_number_list:
            q_type = b.classify(data_set[test_n]["q_content"])

            if q_type == data_set[test_n]["q_class"]:
                #print "%s %s"%(q_type, data_set[test_n]["q_content"])
                correct_class += 1
            else:
                log("classify %s to %s, and correct answer is %s"%(data_set[test_n]["q_content"], q_type, data_set[test_n]["q_class"]))

        correct_class_sum += correct_class
        print "correct classify %d question"%correct_class

    precision = correct_class_sum * 1.0/len(data_set)
    print "correct classify %d questions in all, average precision is %.2f"%(correct_class_sum, precision)
    print "precision: %.2f"%precision


if __name__ == '__main__':
    name_distribution()



