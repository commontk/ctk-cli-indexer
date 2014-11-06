import sys
import simplejson
import elasticsearch

json_filename, source = sys.argv[1:]

INDEX = 'cli'
DOC_TYPE = 'cli'

docs = simplejson.load(file(json_filename))

es = elasticsearch.Elasticsearch()

existing = [doc['_id'] for doc in
            es.search(INDEX, DOC_TYPE, body = dict(
                query = dict(
                    term = dict(
                        source = source)
                    )),
                fields = ['_id'],
                size = 100000)['hits']['hits']]

for doc in docs:
    doc['source'] = source
    doc_id = '%s:%s' % (source, doc['name'])

    try:
        old = es.get(INDEX, doc_id, DOC_TYPE)
    except elasticsearch.exceptions.NotFoundError:
        es.index(INDEX, DOC_TYPE, body = doc, id = doc_id)
        sys.stdout.write("added new document '%s'.\n" % doc_id)
    else:
        existing.remove(old['_id'])
        if old['_source'] != doc:
            es.index(INDEX, DOC_TYPE, body = doc, id = doc_id)
            sys.stdout.write("changed document '%s'.\n" % doc_id)
        else:
            sys.stdout.write("leaving '%s' alone, no change...\n" % doc_id)

for doc_id in existing:
    sys.stdout.write("removing '%s', which is no longer in JSON..." % doc_id)
    es.delete(INDEX, DOC_TYPE, doc_id)
    
