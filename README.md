# Sketch

Sketch aims to be a reusable django app for importing and querying data a document-based database, in particular MongoDB. In this stage of developement it is packaged as a django 1.4 project containing the 'sketch' and the 'sketch_ui' django apps.

THERE IS NO STABLE RELEASE OF SKETCH AT THE MOMENT.

## Motivation

* provide a backend for data-visualization web applications.
* integrate with client side javascript visualization libraries (maps, charts, …)
* ... 


## Features

* REST inteface for importing records into MongoDB collections from various data formats: csv files, json files, …
* User based Permission system on collections
* REST interface for querying MongoDB objects
* REST inteface for sketch objects introspection: exposes sketch instance capabilities (mappers, formatters, processors)
* REST inteface for executing server-side process on a set of records
* Mappers: transform records at import time, adding or modifying fields using an extensible set of transform functions. 
* Formatters: transform query output using an extensible set of predefined formats
* Processors: execute server side operations on a set of objects. 
* Javascript API for accessing all REST intefaces


## Installation

### Python Dependencies
I recommend using virtualenv to manage an installation of sketch.
Once your virtualenv set up, activate it and install dependencies with pip:

	pip -r requirements.txt

This will install all python requirements.	
Let me repeat once more one thing: **USE VIRTUALENV**

### Documents database
A reachable MongoDB server is also required for sketch to work.

If you have mongodb installed in your developement server,
you can use the "startlocalmongo.sh" script in the sketchproject folder.

This script will start an instance of Mongo that writes data in the "sketchdata" folder within the project.
You can select host of MongoDB instance by with the following variables in settings.py:

* MONGO_SERVER_HOSTNAME: defaults to localhost
* MONGO_SERVER_PORT: defaults to 27017
* MONGO_SERVER_DEFAULT_DB: it's the default db for sketch. All APIs will work on this if no database name is passed.

### SQL database

Right now,  sketch uses the standard (**relational**) version of Django, so the ORM works with a SQL database as usual. 
This database is used to store entities for users, permissions, and other sketch components.
In the settings coming with sketch a local sqlite database is used.

To initialize the database activate your virtuelenv and issue the Django command:

	python manage.py syncdb

in the "sketchproject" folder. Django will ask you to create an administration user. Do it.


Once python dependencies, Mongo setup and SQL initialization have been done, start the django developement server with:

	python manage.py runserver
	
And navigate to
	
	localhost:8000/index
	
You should get the login page for Sketch Browser, shipped with the sketch_ui django application.


## Design and Usage

Sketch has these main features:

* Importing data into the nosql database, optionally transforming and enriching records as they are imported.
* Querying data over http with a REST interface, optionally performing some addtional process on the set of records matching the query.

All the features are exposed in three ways:

* with a RESTful service over the http protocol
* with a javascript api based on jquery.ajax()
* with django management commands


### Importing
Importing data into sketch involves these steps:

* Telling sketch how to get records out from your data. This is done with RecordParsers.
* Optionally, perform some *trasforms* while importing data. This is done with Mappers

The results of an import task is having some records stored in a collection within MongoDB.

### Querying

* Results can be filtered with ..
* Results can be formatted with … The objects responsible for this task are *Formatters*

### Processing




## Sketch entities


### Collections

A *Collection* within sketch represents bucket used to store a set of record objects. Each record belongs to a collection.

A sketch collection directly maps to a MongoDB collection, and it is also represented by a Django model.


### Record Parsers

The record parser is the object used to convert data from a textual source into records.
It is used at import time.


### Formatters

TBW

### Mappers and Transforms

TBW

### Processors

TBW

## Management commands

To simplify the management of objects some management functions are provided. They can be used from the 'manage.py' django script.

### sketchinfo

The **sketchinfo** command can be used to perform sketch introspection from the command line, listing available databases, collections, parsers, formatters, mappers, transforms and processors available within the system.

	python manage.py sketchinfo server|db|parsers|formatters|mappers|transforms|processors [--database database_name]   

The required argument represents the type of introspection that needs to be performed.

Command switches:

* *--database* specifies the name of the database we are acting on [defaults to settings.MONGO_SERVER_DEFAULT_DB]


### sketchimport

Data can be imported from command line with the **sketchimport** management command. Data is imported from text files.
	
	python manage.py sketchimport  --collection collection_name --parser parser_name --datafile file_path [--database database_name] [--commit]   

Command switches:

* *--collection*  specifies the name of the collection we are acting on
* *--parser-name* the RecordParser name to use during import, as specified in settings.ALLOWED_PARSERS
* *--datafile* the path to a file to be imported
* *--database* specifies the name of the database we are acting on [defaults to settings.MONGO_SERVER_DEFAULT_DB]
* *--commit* if the *commit* flag is not set, data is not actually imported, but only checked. If this flag is specified, import is issued for records that can be imported, while problematic records are skipped.


### sketchobjects

The **sketchobjects** command lets you perform a query from the command line, getting results printed to stdout

	python manage.py sketchobjects  --collection collection_name [--database database_name] [--limit limit] [--offset offset] [--query query] [--formatter formatter] 

Command switches:

* *--collection*  specifies the name of the collection we are acting on
* *--database* specifies the name of the database we are acting on [defaults to settings.MONGO_SERVER_DEFAULT_DB]


### sketchcmd
The *sketchcmd* management command has the following syntax
	
	python manage.py sketchcmd [--database database_name] [[--drop-collection collection_name]|[--drop-database]

Command switches:
	
* *--database* specifies the name of the database we are acting on [defaults to settings.MONGO_SERVER_DEFAULT_DB]
* *--drop-collection* drops the collection passed with collection_name
* *--drop-database* drops the database database_name passed with the --database switch



## Javascript API

All operations within sketch can be performed by means of HTTP requests, using any client capable of doing GET and POST requests.

In addition, sketch comes with a javascript api to facilitate the integration with javascript applications, providing means to perform all sketch operations directly from javascript.

The js api is based on jquery, the only js dependency.

## Example data

Sketch comes with a folder of example data
TBW

## Example client apps

Sketch comes with a set of example client applications
TBW


## Contributors

TBW
