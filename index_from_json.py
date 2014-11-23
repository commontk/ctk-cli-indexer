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

import argparse
import simplejson
import elasticsearch
from ctk_cli_indexer.indexer import create_elasticsearch_index, update_elasticsearch_index

parser = argparse.ArgumentParser(description = 'update elasticsearch index from JSON description of CLI modules')
parser.add_argument('json_filename', type = argparse.FileType('r'),
                    help = 'name of JSON file as created by cli_to_json.py')
parser.add_argument('source', help = "identifier for the source "
                    "(e.g. 'Slicer' or 'nifty-reg') of this set of CLI modules "
                    "(will also be used to remove all documents from this source "
                    "from the Elasticsearch index if they are not in the JSON anymore)")
parser.add_argument('--host', default = 'localhost', help = 'hostname elasticsearch is listening on (default: localhost)')
parser.add_argument('--port', default = 9200, help = 'port elasticsearch is listening on (default: 9200)')

args = parser.parse_args()

docs = simplejson.load(args.json_filename)

# TODO: at the moment, the commandline is limited to *one* host/port, and no SSL or URL prefix
es = elasticsearch.Elasticsearch([dict(host = args.host, port = args.port)])

create_elasticsearch_index(es)

update_elasticsearch_index(es, docs, args.source)
