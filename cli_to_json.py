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

import sys, os, argparse, re
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

        timestamp = os.path.getmtime(exe_filename)
        doc = dict((attr, getattr(cli, attr))
                   for attr in INDEX_ATTRIBUTES)

        authors = re.sub(r'\([^)]*\)', '', cli.contributor) if cli.contributor else ""
        doc['authors'] = [author.strip() for author in re.split(r' *, *(?:and *)?| +and +', authors)
                          if not author.startswith('http://') or re.search('@| -at- ', author)]
        
        doc['group_count'] = len(cli)
        doc['group_labels'] = '\n'.join(group.label for group in cli if group.label)
        doc['advanced_group_count'] = sum(group.advanced for group in cli)
        doc['parameter_count'] = sum(len(group) for group in cli)
        doc['parameter_names'] = '\n'.join(p.name for p in cli.parameters() if p.name)
        doc['parameter_labels'] = '\n'.join(p.label for p in cli.parameters() if p.label)

        docs.append((timestamp, doc))

simplejson.dump(docs, args.json_filename, indent = '  ')
args.json_filename.write('\n')
