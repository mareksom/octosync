from termcolors import *
import data
import os
import shutil

def Sync(origin, clone):
  def update(file):
    full_path_origin = os.path.join(origin, file)
    full_path_clone = os.path.join(clone, file)
    print(YELLOW(' Copying file ') + GREEN(file))
    os.makedirs(os.path.dirname(full_path_clone), exist_ok=True)
    shutil.copy(full_path_origin, full_path_clone)

  def remove(file):
    full_path_clone = os.path.join(clone, file)
    print(YELLOW('Removing file ') + RED(file))
    os.remove(full_path_clone)

  os.makedirs(origin, exist_ok=True)
  os.makedirs(clone, exist_ok=True)

  origin_data = data.ScanDirectory(origin, write_info='origin')
  clone_data = data.ScanDirectory(clone, write_info='clone')

  all_files = list(origin_data.keys()) + list(clone_data.keys())
  all_files.sort()
  for file in all_files:
    if file in origin_data:
      if file in clone_data:
        if clone_data[file]['checksum'] != origin_data[file]['checksum']:
          update(file)
      else:
        update(file)
    else:
      remove(file)
  data.ScanDirectory(clone)
