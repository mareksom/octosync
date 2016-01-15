from termcolors import *
import checksum
import os
import re


OCTOSYNC_FILENAME = '.octosync'


def Read_(origin):
  result = {}
  file_path = os.path.join(origin, OCTOSYNC_FILENAME)
  if os.path.isfile(file_path):
    with open(file_path, 'r') as file:
      contents = file.read()
    correct_line = re.compile(
        '^(?P<checksum>\w+)#(?P<timestamp>\d+(\.\d+)?)#(?P<path>.*)$')
    for line in contents.splitlines():
      m = correct_line.match(line)
      if m:
        m = m.groupdict()
        result[m['path']] = {'checksum': m['checksum'],
                             'timestamp': float(m['timestamp'])}
  return result


def Save_(origin, data):
  file_path = os.path.join(origin, OCTOSYNC_FILENAME)
  with open(file_path, 'w') as file:
    for path, file_data in data.items():
      file.write('{}#{}#{}\n'.format(
          file_data['checksum'], file_data['timestamp'], path))


def ScanDirectory(origin, write_info=None):
  indexed_files = Read_(origin)
  result = {}
  def update_file(file_path):
    full_path = os.path.join(origin, file_path)
    modification_time = os.path.getmtime(full_path)
    if file_path in indexed_files \
        and indexed_files[file_path]['timestamp'] + 0.001 >= modification_time:
      # Just copy from .octosync file.
      result[file_path] = indexed_files[file_path]
    else:
      # Get file data.
      if write_info:
        if file_path in indexed_files:
          print(MAGENTA('Detected modification ({}): '.format(write_info))
                + YELLOW(file_path))
        else:
          print(MAGENTA('Detected  a  new file ({}): '.format(write_info))
                + GREEN(file_path))
      result[file_path] = {'checksum': checksum.compute(full_path),
                           'timestamp': modification_time}
  # Iterating over all files and updating them if necessary.
  for subdir, dirs, files in os.walk(origin):
    for file in files:
      if not file.startswith('.'):
        update_file(os.path.relpath(os.path.join(subdir, file), origin))
  if write_info:
    for old_file in indexed_files.keys():
      if not old_file in result:
        print(MAGENTA('Detected missing file ({}): '.format(write_info))
              + RED(old_file))
  Save_(origin, result)
  return result
