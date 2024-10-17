###################################################### 
# Delete folders with ok file
import os
import shutil

rootdir = '.'
for dir in os.listdir(rootdir):
  if os.path.isdir(dir):
    delete = 0
    for file in os.listdir(os.path.join(rootdir, dir)):
      if file == 'ok':
        delete = 1
        break
    print(dir, bool(delete))
    if (bool(delete)):
      shutil.rmtree(dir)
