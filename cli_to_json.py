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
