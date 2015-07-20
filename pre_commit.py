#! C:\python27\python

import os,sys
import logging

TEMP = os.getenv('TEMP')
cur_dir = os.getcwd()
temp_txt = r"{}\temp.txt".format(TEMP)
temp_txt = temp_txt.replace('\\','/')

get_modified_file_cmd = r"git.exe ls-files --other --modified --exclude-standard > {}".format(temp_txt)
qac_batch_file = r"C:\\PRQA\\QAC-8.1.2-R\\bin\\QACRUN.BAT"
qac_conf_file = r"C:\\PRQA\\QAC-8.1.2-R\\bin\\QACCONF.BAT"
gnumake = cur_dir + r"\\tools\\utilities\\gnumake VEHCFG=MT22p1_ETC_FF_4CYL SOFTWARE=MT22p1_ETC_4CYL_FF_SW"
make_git_qac_target = " qac_git_com"
qac_config_file = cur_dir + "\\qac\\qac_config"
qac_output_dir = cur_dir + "\\qac\\output"
cmd_list = []
if not os.path.exists(qac_output_dir):
    os.mkdir(qac_output_dir)
error_level = os.system(get_modified_file_cmd)


if error_level == 0:
    #print ("git exec ok")
    os.chdir("build")
    os.system(gnumake + " " + make_git_qac_target)
    os.chdir("..")
    f_temp = open(temp_txt)
    for line in f_temp:
        file_name = cur_dir + "\\" + line.strip('\n')
        #print file_name
        if ".c" in file_name:
            qac_cmd = r"{0} -via {1}  {2} {3}".format(qac_batch_file,qac_config_file,file_name,qac_output_dir)
            #print qac_cmd
            os.system(qac_cmd)
        else:
            #print (file_name)
            pass
else:
    print ("git exec error")
sys.exit(1)
