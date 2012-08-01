# Sketch

Sketch aims to be a reusable django app for importing and querying data a document-based database, in particular MongoDB. In this stage of developement it is packaged as a django 1.4 project containing the 'sketch' and the 'sketch_ui' django apps.

THERE IS NO STABLE RELEASE OF SKETCH AT THE MOMENT.

## Motivation

* provide a backend for data-visualization web applications.
* integrate with client side javascript visualization libraries (maps, charts, …)
* ...
…



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



## Design

TBW



## Sketch entities


### Collections

TBW

### Formatters

TBW

### Mappers

TBW

### Transfoms

TBW

### Processxors

TBW

## Example data

Sketch comes with a folder of example data
TBW


## Example client apps

Sketch comes with a set of example client applications
TBW



## Dependencies

TBW

## Contributors

TBW
