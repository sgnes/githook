import os
#os.chdir(r"E:\work\delphi\work\Code\test\MT22.1_FlexFuel\.git\hooks\Git")
print os.getcwd()
from mygitlib import MyGitLib
git = MyGitLib(r"D:\Code\test\MT22.1_FlexFuel")
print git.get_current_branch()
print git.get_modified_file(r".c")
cd = git.get_newest_commit()
print git.get_commit_info(cd)
