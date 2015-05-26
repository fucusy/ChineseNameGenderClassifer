__author__ = 'fucus'

class Location:
    module_path = "/Users/user/code/github/ChineseNameGenderClassifer"
    data_path = "%s/data/name_gender.csv"%module_path
    data_dir = "%s/data/"%module_path
    log_file = "%s/log.txt"%data_dir
    type_list_cache_path = "%s/type_list_cache.txt"%data_dir

class SystemConfig:
    is_debug = True

class BayseConfig:
    is_skip_first_line = False
    content_index = 0
    type_index = 1