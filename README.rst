===============
ctk-cli-indexer
===============

The files in this repository allow you to create an ElasticSearch_ database containing
information on available CLI modules.  The idea is that we have a public Kibana_ dashboard
listing CLI modules from multiple sources, so there are two scripts:

cli_to_json.py
  Extracts JSON descriptions from a set of CLI modules (in one or more common directories). ::

    # ./cli_to_json.py --help
    usage: cli_to_json.py [-h] [--json_filename JSON_FILENAME]
                          base_directory [base_directory ...]

    create JSON description from CLI modules

    positional arguments:
      base_directory        directories (at least one) in which to search for CLI
                            module executables

    optional arguments:
      -h, --help            show this help message and exit
      --json_filename JSON_FILENAME, -o JSON_FILENAME

  This is to be run by the administrators of sites that offer CLI modules, and the idea is
  that the resulting .json files are published on some website.

index_from_json.py
  Takes a JSON file and updates an ElasticSearch_ database.  An identifier for the source
  of the CLI modules is passed as second parameter, and the script takes care to delete
  old documents in the database (CLIs that got removed), and will also maintain timestamps
  of the last change of each CLI (i.e. not re-upload stuff that did not change, as well as
  mark each change with the modification time of the CLI executable that introduced the
  change). ::

    # ./index_from_json.py --help
    usage: index_from_json.py [-h] [--host HOST] [--port PORT]
                              json_filename source

    update elasticsearch index from JSON description of CLI modules

    positional arguments:
      json_filename  name of JSON file as created by cli_to_json.py
      source         identifier for the source (e.g. 'Slicer' or 'nifty-reg') of
                     this set of CLI modules (will also be used to remove all
                     documents from this source from the Elasticsearch index if
                     they are not in the JSON anymore)

    optional arguments:
      -h, --help     show this help message and exit
      --host HOST    hostname elasticsearch is listening on
      --port PORT    port elasticsearch is listening on

  This script should be run by a cron job (i.e. setup by a CTK administrator), from a script
  that pulls the above-mentioned .json URLs regularly and updates a central database.
  A Kibana_ dashboard will then give interested people an overview over the available modules
  from multiple sites.

.. _Elasticsearch: http://www.elasticsearch.org/overview/elasticsearch/
.. _Kibana: http://www.elasticsearch.org/overview/kibana/
  
System Prerequisites
====================

The following software packages are required to be installed on your system:

* `Python <http://python.org>`_
* `pip <https://pypi.python.org/pypi/pi>`_ (recommended)
* `Git <http://git-scm.com/>`_ (for developer only)

Installation for user
=====================

Use ``pip`` (or ``easy_install``) for installation from pypi_::

    pip install ctk-cli-indexer

.. _pypi: https://pypi.python.org/pypi
    
Installation for developer
==========================

First download the source::

    git clone git://github.com/commontk/ctk-cli-indexer.git

To use the module, you must install some external python package
dependencies: ::

    cd ctk-cli-indexer
    pip install -r requirements.txt
