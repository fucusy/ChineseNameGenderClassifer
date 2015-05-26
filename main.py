__author__ = 'fucus'
#!encoding=utf-8

from program.bayes_classfier import bayes_classifier



name = ""
gender = ""
if bayes_classifier.get_classify_label(name) == '1':
    gender = "男"
else:
    gender = "女"

print "your gender is %s"%gender