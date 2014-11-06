cli-indexer
===========

The files in this repository allow you to create an ElasticSearch database containing
information on available CLI modules.  The idea is that we have a public Kibana dashboard
listing CLI modules from multiple sources, so there are two scripts:

cli_to_json.py
  Extracts JSON descriptions from a set of CLI modules (in one or more common directories).

  This is to be run by the administrators of sites that offer CLI modules, and the idea is
  that the resulting .json files are published on some website.

index_from_json.py
  Takes a JSON file and updates an Elasticsearch database.  An identifier for the source
  of the CLI modules is passed as second parameter, and the script takes care to delete
  old documents in the database (CLIs that got removed), and will also maintain timestamps
  of the last change of each CLI (i.e. not re-upload stuff that did not change, as well as
  mark each change with the modification time of the CLI executable that introduced the
  change).

  This script should be run by a cron job (i.e. setup by a CTK administrator), from a script
  that pulls the above-mentioned .json URLs regularly and updates a central database.
  A Kibana dashboard will then give interested people an overview over the available modules
  from multiple sites.
