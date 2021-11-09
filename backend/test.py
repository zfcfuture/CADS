import os
import subprocess

filePath = "/home/zfc/debugTool/ELF_files"
cmd="cd {localpath};spike cputest.bare.spike".format(localpath=filePath)
# ret = subprocess.Popen(cmd,shell=True,
#                  stdin=subprocess.PIPE,
#                  stdout=subprocess.PIPE,
#                  stderr=subprocess.PIPE,
#                  cwd=os.getcwd()+"/backend")
# l=[]
# for i in iter(ret.stdout.readline,b""):
#     print(i.decode().strip())
#     l.append(i.decode().strip())
output = os.popen(cmd)
print(output.read())