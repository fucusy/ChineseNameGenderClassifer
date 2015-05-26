import random
from config.main import Location
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

def log(text):
    f = open(Location.log_file ,"a")
    f.write(text + "\n")
    f.close()