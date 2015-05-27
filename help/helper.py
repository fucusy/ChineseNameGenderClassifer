#!encoding=utf8
import random
from config.main import Location
from config.main import BayseConfig
import os


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]



class ChineseText:

    @staticmethod
    def cut_name_to_element(name):
        """

        :param name: the chinese name like
        :return: the element of the name, in general return the character list as the element list
        """

        result = []
        for i in range(1, len(name)):
            result.append(name[i])

        for i in range(1,len(name) -1):
            result.append(name[i:i+2])

        for i in range(1,len(name) -2):
            result.append(name[i:i+3])
        return result


def save_to_file(data, file_name = "", replace=False):
    if file_name == "":
        file_name = random.random()

    count = 1
    old_file_name = file_name

    file_location = "%s/data/%s"%(Location.module_path, file_name)

    if not replace:
        while os.path.isfile(file_location):
            print file_name + "already exist "
            file_name = old_file_name + str(count)
            count += 1
            print "change filename to %s"%file_name
            file_location = "%s/data/%s"%(Location.module_path, file_name)
    else:
        if os.path.isfile(file_location):
            print "%s file already exist, now it will be over write"%file_location



    with open(file_location, "w") as f:
        f.write(data)


def clean_data(data_path = Location.data_path):
    after_clean = ""
    with open(data_path,"r") as f:
        for line in f:
            line = line.strip("\n")
            split_line = line.split(",")
            for i in range(len(split_line)):
                split_line[i] = split_line[i].strip('"')

            if not (split_line[BayseConfig.content_index].find("·") > -1 or split_line[BayseConfig.content_index].find(".") > -1 ):
                if BayseConfig.content_index == 0:
                    after_clean += "%s,%s\n"%(split_line[BayseConfig.content_index],split_line[BayseConfig.type_index])
                else:
                    after_clean += "%s,%s\n"%(split_line[BayseConfig.type_index],split_line[BayseConfig.content_index])
    with open(data_path,"w") as f:
        f.write(after_clean)

def log(text):
    f = open(Location.log_file ,"a")
    f.write(text + "\n")
    f.close()

if __name__ == '__main__':
    clean_data()