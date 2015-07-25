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
        """
        the init function
        :param dir:the root git path
        :return:the class object
        """
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
        """
        use git branch to get the current branch name
        :return:the current git branch
        """
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
        self.__logger.info("Current Branch name:" + self.__cur_branch)
        return self.__cur_branch

    def get_commit_info(self,com_id):
        """
        use git command git show commit id to get the diff of the commit
        parse the output and get the modified lines
        :param com_id: the commit id to be analysis
        :return:
                type:dict
                etc:["D:\Code\MT22.1_FlexFuel/CORE/EMS_Core/TORQ/TCL/torqpapi.h":[1293, 1294, 1295, 1296, 1297, 1298, 2875, 2876, 2877, 2878, 2879, 2880, 2881]]
        """
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
                self.__logger.info(res_dict)
                for i in res_dict:
                    self.__logger.info("{0}:{1}".format(i, res_dict[i]))
                return res_dict
            temp_f.close()
        else:
            self.__logger.error("Git exec failed.")
        pass

    def get_modified_file(self, suffix_list):
        """
        get the modified files in the working tree
        :param suffix_list:
                type:list
                etc: [".c", ".h"]
        :return:
                type:list
                etc:["D:\Code\MT22.1_FlexFuel/CORE/EMS_Core/TORQ/TCL/torqpapi.h","D:\Code\MT22.1_FlexFuel/CORE/EMS_Core/TORQ/TCL/torqmbrk.c"]
        """
        git_cmd = r"git {0} ls-files --other --modified --exclude-standard > {1}"\
            .format(self.__git_dir_cmd, self.__temp_file_name)
        self.__logger.info(git_cmd)
        error_level = os.system(git_cmd)
        file_list = []
        if error_level == 0:
            f_temp = open(self.__temp_file_name)
            for suffix in suffix_list:
                for line in f_temp:
                    line = line.strip('\n')
                    if line.endswith(suffix):
                        file_list.append(self.__home_dir + "\\" + line)
                    else:
                        self.__logger.error( line)

            f_temp.close()
        else:
            self.__logger.error("Git exec failed.")
        self.__logger.info("get_modified_file result:")
        for i in file_list:
            self.__logger.info("{0}".format())
        self.__logger.info("End of get_modified_file result")
        return file_list

    def get_detail_change_lines(self, diff):
        """
        get the modified lines in diff output
        :param diff:
                type:list
                the diff output of just one file
                etc:
                    index 7b45edf..21d8d99 100644
                    --- a/CORE/EMS_Core/SPRK/sprkcald.c
                    +++ b/CORE/EMS_Core/SPRK/sprkcald.c
                    @@ -56,7 +56,7 @@

                     #if ( ( config_CPU_Type == option_M68HC12 ) \
                      && ( config_Compiler_Vendor == option_COSMIC )  )
                    -#pragma section const {CAL_SPRK}
                    +#pragma section const {CAL_SPRK_MSS}
                     #endif
                     /******************************************************************************
                      *  Local cdf-type Definitions
        :return:
                type:list
                etc:[15,21,35]
        """
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
                change_lines.append(str(start_line))
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
        """
        get the modified file name in the line
        :param line:
                    type:str
                    etc:diff --git a/CORE/EMS_Core/SPRK/sprkcald.c b/CORE/EMS_Core/SPRK/sprkcald.c
        :return:
                    type:str
                    etc:/CORE/EMS_Core/SPRK/sprkcald.c
        """
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
        self.__logger.info(commit_id)
        return commit_id

class QacReportParser(object):
    """
    Parse the qac report(html file),get the error line and the errors
    """
    def __init__(self, html_file_name):
        self.__html_file = html_file_name
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
        self.__logger = logging.getLogger("QacReportParser")
    def get_all_errors(self):
        """
        get the error lines and errors
        :return:
                type:dict
                etc:[error line number:the error itself]
        """
        hfile = open(self.__html_file)
        text = hfile.read()
        error_dict = {}
        m = re.findall(r"<A NAME=.{1}ERR_LINE_(\d+).{1}>(<.{1}A>(.*?)<BR>\n<PRE STYLE=.{1}margin-top:0;margin-bottom:0.{1}>)\n\s+\d+:",text, re.S)
        for i in m:
            error_dict[i[0]] = i[1]
            self.__logger.info("{0}:{1}".format(i[0], i[1]))
        return error_dict