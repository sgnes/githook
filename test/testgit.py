import os
#os.chdir(r"E:\work\delphi\work\Code\test\MT22.1_FlexFuel\.git\hooks\Git")
print os.getcwd()
from git import MyGitLib
git = MyGitLib(r"E:\work\delphi\work\Code\test\MT22.1_FlexFuel")
print git.get_current_branch()
print git.get_modified_file(r".c")
print git.get_commit_info("48180628162f5c78481fa3731446966d0b9c5cf5")
