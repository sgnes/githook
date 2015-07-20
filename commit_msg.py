__author__ = 'DZMP8F'
#! C:\python27\python

import os,sys
from time import gmtime, strftime
from mygitlib import MyGitLib

commit_id = sys.argv[0]
TEMP = os.getenv('TEMP')
cur_dir = os.getcwd()
temp_txt = r"{}\temp.txt".format(TEMP)
temp_txt = temp_txt.replace('\\','/')
gitor = MyGitLib(cur_dir)
cur_branch_name = gitor.get_current_branch()
qac_batch_file = r"C:\\PRQA\\QAC-8.1.2-R\\bin\\QACRUN.BAT"
qac_conf_file = r"C:\\PRQA\\QAC-8.1.2-R\\bin\\QACCONF.BAT"
gnumake = cur_dir + r"\\tools\\utilities\\gnumake VEHCFG=MT22p1_ETC_FF_4CYL SOFTWARE=MT22p1_ETC_4CYL_FF_SW"
make_git_qac_target = " qac_git_com"
qac_config_file = cur_dir + "\\qac\\qac_config"
qac_output_dir = cur_dir + "\\qac\\{0}_".format(cur_branch_name) + strftime("%Y_%m_%d_%H_%M_%S", gmtime())
cmd_list = []
if not os.path.exists(qac_output_dir):
    os.mkdir(qac_output_dir)

change_detail = gitor.get_commit_info(commit_id)

if change_detail:
    os.chdir("build")
    os.system(gnumake + " " + make_git_qac_target)
    os.chdir("..")
    for i in change_detail:
        if i.endswith(".c"):
            qac_cmd = r"{0} -via {1}  {2} {3}".format(qac_batch_file, qac_config_file, i, qac_output_dir)
            os.system(qac_cmd)

