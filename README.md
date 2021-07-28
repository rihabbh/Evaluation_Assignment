# Evaluation_Assignment

This repository contains all the scripts for the given assignment.


## DatabaseImport.py

This script import an Excel file into a MongoDB database. It takes as a parameters the path of the Excel file and the 
attributes of the mongodb url

According to the python configuration, it can be executed with this command

```
py DatabaseImport.py -h [MONGOHOST] - p [MONGOPORT] -d [DBNAME] -e [EXCELPATH]
```

or this:

```
python DatabaseImport.py -h [MONGOHOST] - p [MONGOPORT] -d [DBNAME] -e [EXCELPATH]
```


### Parameters 


| command line | definition                                 | default            |
|--------------|--------------------------------------------|--------------------|
| -h or --host | MONGODB host                               |localhost|
| -p or --port | MONDOBD port                               | 27017|
| -d or --db   | Database's Name                            | Retail|
| "-e" or "--excel" | path to the Excel's file with the data| Online Retail.xlsx|

## DatabaseImportTest.py


Unit tests for the previous script DatabaseImport.py

According to the python configuration, it can be executed with this command

```
py DatabaseImportTest.py 
```

or this:

```
python DatabaseImportTest.py 
```


## Assignment.ipynb

Jupyter Notebook containing the answers to all the questions except the last one.

## Categorization.ipynb

Jupyter Notebook containing the answer to the last question.

