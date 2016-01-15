#!/usr/bin/python3

import sync
import sys

# Parsing arguments.
if len(sys.argv) == 0:
  program_name = 'octosync'
else:
  program_name = sys.argv[0]

if len(sys.argv) != 3:
  print('Usage: {} <origin> <clone>'.format(program_name))
else:
  sync.Sync(sys.argv[1], sys.argv[2])
