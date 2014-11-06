#!/usr/bin/env python
#  Copyright 2014 Hans Meine <hans_meine@gmx.net>
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import sys, os, argparse
import simplejson
import cli_modules

parser = argparse.ArgumentParser(description = 'create JSON description from CLI modules')
parser.add_argument('base_directory', nargs = '+',
                    help = 'directories (at least one) in which to search for CLI module executables')
parser.add_argument('--json_filename', '-o', type = argparse.FileType('w'), default = sys.stdout)

args = parser.parse_args()

INDEX_ATTRIBUTES = 'name title version category description contributor acknowledgements documentation_url license'.split()

docs = []

for basedir in args.base_directory:
    for exe_filename in cli_modules.listCLIExecutables(basedir):
        sys.stderr.write('processing %s...\n' % (os.path.basename(exe_filename), ))
        cli = cli_modules.CLIModule(exe_filename)

        docs.append(dict((attr, getattr(cli, attr))
                         for attr in INDEX_ATTRIBUTES))

simplejson.dump(docs, args.json_filename, indent = '  ')
args.json_filename.write('\n')
