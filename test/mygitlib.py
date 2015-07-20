__author__ = 'DZMP8F'
#! coding = utf-8
#! C:\python27\python

import os
import logging
import re
import sys

class MyGitLib(object):
    """
    This is a git package ,to get the git information of
    the dir which pass into.
    """
    def __init__(self,dir="."):
        self.__home_dir = dir.strip('\n')
        self.__temp_file_name = r"{}\temp.txt".format(os.getenv("TEMP"))
        self.__cur_branch = ""
        self.__git_dir_cmd = "--git-dir={0} --work-tree={1}".format(self.__home_dir+"\\.git", self.__home_dir)
        logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%m-%d %H:%M',
                        filename='MyGitLib.log',
                        filemode='w')
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
        console.setFormatter(formatter)
        logging.getLogger('').addHandler(console)
        self.__logger = logging.getLogger("MyGitLib")
        pass

    def get_current_branch(self):
        git_cmd = "git {0} branch > {1}".format(self.__git_dir_cmd, self.__temp_file_name)
        self.__logger.info(git_cmd)
        error_level = os.system(git_cmd)
        if error_level == 0:
            tmp_file = open(self.__temp_file_name)
            for line in tmp_file:
                s1 = line.split()
                if s1[0] == r"*":
                    self.__cur_branch = s1[1]
                    break
            tmp_file.close()
        else:
            self.__logger.error("Git exec failed.")
        return self.__cur_branch

    def get_commit_info(self,com_id):
        git_cmd =r"git {0} show {1} > {2}".format(self.__git_dir_cmd, com_id, self.__temp_file_name)
        self.__logger.info(git_cmd)
        error_level = os.system(git_cmd)
        file_list = []
        if error_level == 0:
            temp_f = open(self.__temp_file_name)
            self.__logger.info("git command ok.")
            if temp_f:
                line = temp_f.readline()
                res_dict = {}
                while line:
                    if line.startswith("diff --git"):
                        file_name = self.__home_dir + self.get_file_name(line).replace(r"/","\\")
                        detail_change = []
                        while line:
                            line = temp_f.readline()
                            if(line.startswith("diff --git")):
                                res_dict[file_name] = self.get_detail_change_lines(detail_change)
                                break
                            detail_change.append(line)
                        if not line:
                            res_dict[file_name] = self.get_detail_change_lines(detail_change)
                    else:
                        line = temp_f.readline()
                return res_dict
            temp_f.close()
        else:
            self.__logger.error("Git exec failed.")
        pass

    def get_modified_file(self,suffix):
        git_cmd = r"git {0} ls-files --other --modified --exclude-standard > {1}"\
            .format(self.__git_dir_cmd, self.__temp_file_name)
        self.__logger.info(git_cmd)
        error_level = os.system(git_cmd)
        file_list = []
        if error_level == 0:
            f_temp = open(self.__temp_file_name)
            for line in f_temp:
                line = line.strip('\n')
                if line.endswith(suffix):
                    file_list.append(self.__home_dir + "\\" + line)
                else:
                    self.__logger.error( line)
            f_temp.close()
        else:
            self.__logger.error("Git exec failed.")
        return file_list

    def get_detail_change_lines(self, diff):
        re_start_line = re.compile("(@@ -\d+,\d+ +\+)(\d+)(,\d+ @@)")
        start_line = 0
        change_lines = []
        chang_dict = {}
        for line in diff:
            #print line
            if line.startswith("@@"):
                re_start_line_g = re_start_line.match(line.strip())
                if re_start_line_g:
                    start_line = int(re_start_line_g.group(2))-1
                    #print start_line
                else:
                    pass
                    #print line
            elif line.startswith("+") and start_line > 0:
                start_line = start_line + 1
                change_lines.append(start_line)
            elif line.startswith("-"):
                pass
            elif start_line > 0:
                start_line = start_line + 1
            else:
                pass
       # print change_lines
        return change_lines


        pass

    def get_file_name(self, line):
        com = re.compile(r"(diff --git a)(.*)( b/)")
        m = com.match(line.strip())
        file_name = ""
        if m:
            file_name = m.group(2)
        return file_name

    def get_newest_commit(self):
        git_cmd = "git {0} log > {1}".format(self.__git_dir_cmd, self.__temp_file_name)
        self.__logger.info(git_cmd)
        error_level = os.system(git_cmd)
        commit_id = ""
        if error_level == 0:
            tmp_file = open(self.__temp_file_name)
            line = tmp_file.readline()
            if line.startswith("commit"):
                commit_id = line.split()[1]
            tmp_file.close()
        else:
            self.__logger.error("Git exec failed.")
        return commit_id