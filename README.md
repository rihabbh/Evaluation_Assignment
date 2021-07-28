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
| -u or --host | MONGODB host                               |localhost|
| -p or --port | MONDOBD port                               | 27017|
| -d or --db   | Database's Name                            | Retail|
| "-e" or "--excel" | path to the Excel's file with the data| Online Retail.xlsx|


### The database

The database created includes 2 collections :

"Transaction" , where documents have this structure:

```
{
    "_id": {
        "$oid": "60fdde43134652833b8b4928"
    },
    "InvoiceNo": 536365,
    "StockCode": "85123a",
    "Quantity": 6,
    "InvoiceDate": {
        "$date": "2010-12-01T08:26:00.000Z"
    },
    "UnitPrice": 2.55,
    "CustomerID": 17850,
    "Country": "United Kingdom"
}
```

and "Product", with this : 

```
{
    "_id": {
        "$oid": "60fdde3d134652833b8b39b5"
    },
    "StockCode": "10123c",
    "Description": "hearts wrapping tape ",
    "ProductCode": "10123"
}
```


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

