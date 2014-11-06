import sys, os
import simplejson
import cli_modules

basedir, = sys.argv[1:]

INDEX_ATTRIBUTES = 'name title version category description contributor acknowledgements documentation_url license'.split()

docs = []

for exe_filename in cli_modules.listCLIExecutables(basedir):
    sys.stderr.write('processing %s...\n' % (os.path.basename(exe_filename), ))
    cli = cli_modules.CLIModule(exe_filename)

    docs.append(dict((attr, getattr(cli, attr))
                     for attr in INDEX_ATTRIBUTES))

simplejson.dump(docs, sys.stdout, indent = '  ')
sys.stdout.write('\n')
