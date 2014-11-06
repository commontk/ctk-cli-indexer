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

import sys, argparse, datetime
import simplejson
import elasticsearch

parser = argparse.ArgumentParser(description = 'update elasticsearch index from JSON description of CLI modules')
parser.add_argument('json_filename', type = argparse.FileType('r'),
                    help = 'name of JSON file as created by cli_to_json.py')
parser.add_argument('source', help = "identifier for the source "
                    "(e.g. 'Slicer' or 'nifty-reg') of this set of CLI modules "
                    "(will also be used to remove all documents from this source "
                    "from the Elasticsearch index if they are not in the JSON anymore)")

args = parser.parse_args()

INDEX = 'cli'
DOC_TYPE = 'cli'

docs = simplejson.load(args.json_filename)

es = elasticsearch.Elasticsearch()

existing = [doc['_id'] for doc in
            es.search(INDEX, DOC_TYPE, body = dict(
                query = dict(
                    term = dict(
                        source = args.source)
                    )),
                fields = ['_id'],
                size = 100000)['hits']['hits']]

for timestamp, doc in docs:
    doc['source'] = args.source
    doc_id = '%s:%s' % (args.source, doc['name'])
    timestamp = datetime.datetime.fromtimestamp(timestamp)

    try:
        old = es.get(INDEX, doc_id, DOC_TYPE)
    except elasticsearch.exceptions.NotFoundError:
        es.index(INDEX, DOC_TYPE, body = doc, id = doc_id, timestamp = timestamp)
        sys.stdout.write("added new document '%s'.\n" % doc_id)
    else:
        existing.remove(old['_id'])
        if old['_source'] != doc:
            es.index(INDEX, DOC_TYPE, body = doc, id = doc_id, timestamp = timestamp)
            sys.stdout.write("changed document '%s'.\n" % doc_id)
        else:
            sys.stdout.write("leaving '%s' alone, no change...\n" % doc_id)

for doc_id in existing:
    sys.stdout.write("removing '%s', which is no longer in the '%s' JSON...\n" % (doc_id, args.source))
    es.delete(INDEX, DOC_TYPE, doc_id)
