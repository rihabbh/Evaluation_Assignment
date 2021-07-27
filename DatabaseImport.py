### Import All Library
import pandas as pd
from optparse import OptionParser
import pymongo
from pymongo import MongoClient
from datetime import datetime

pd.options.mode.chained_assignment = None

class DatabaseImport:
    """ A class to assure the import of our dataset in mongoDB"""

    def loadDataSet(self, excelPath):
        """
        :param excelPath:  Path of the Excel file where the data are stored
        :return: a panda dataframe with the data of the excel
        """
        dataset = pd.read_excel(excelPath)
        return dataset


    def ConnectionDB(self, dbHost, dbPort, dbName):
        """
        :param dbHost: IP Host of the mongoDB database
        :param dbPort: Port of the DB
        :param dbName: Name of the database
        :return: DB connector
        """
        dbURL = "mongodb://{0}:{1}/".format(dbHost, dbPort)
        # Making a Connection with MongoClient
        client = MongoClient(dbURL)
        # database
        return client[dbName]


    def removeDuplicate(self, description):
        """
        Since we are grouping by product, we want to remove duplicate in the description
        """
        descriptionsList = list(set(description.split(',')))
        if 'nan' in descriptionsList:
            descriptionsList.remove('nan')
        return ', '.join(descriptionsList)


    def StockWithoutVar(self, StockCode):
        """
        Product with a stock code with the same number but a different letter at the end
        are part of the same product's range, so we will display this information in DB
        """
        if StockCode[0].isdigit() and not StockCode[-1].isdigit():
            try:
                return str(StockCode[:-1])
            except:
                return str(StockCode[:-2])
        else:
            return str(StockCode)


    ## Preparing Product Collection
    def insertProducts(self, db, dataset):
        """
        :param db: DB connector
        :param dataset: The excel dataset previously loaded
        :return:  Insert the product's data in the database
        """

        db["Product"].create_index([("StockCode", 1)], name="StockCode", unique=True)

        dfProduct = dataset[['Description', 'StockCode']]

        dfProduct['Description'] = dfProduct['Description'].astype('str').apply(lambda x: x.lower())
        dfProduct['StockCode'] = dfProduct['StockCode'].astype('str').apply(lambda x: x.lower())

        dfProduct = dfProduct.groupby(['StockCode'])['Description'].apply(','.join).reset_index()

        dfProduct['Description'] = dfProduct['Description'].apply(lambda x: self.removeDuplicate(x))

        dfProduct['ProductCode'] = dfProduct['StockCode'].apply(lambda x: self.StockWithoutVar(x))

        product_dict = dfProduct.to_dict("records")

        for product in product_dict:
            try:
                db["Product"].insert_one(product)
            except pymongo.errors.DuplicateKeyError as e:
                pass


    ## Preparing Transaction Collection

    def insertTransactions(self, db, dataset):
        """
        :param db: DB connector
        :param dataset: The excel dataset previously loaded
        :return: Insert the transaction's data in the database
        """
        dfTransaction = dataset.drop(['Description'], axis=1)
        dfTransaction['StockCode'] = dfTransaction['StockCode'].astype('str').apply(lambda x: x.lower())
        dfTransaction['CustomerID'] = dfTransaction['CustomerID'].fillna(0).astype('int')

        transaction_dict = dfTransaction.to_dict("records")

        db["Transaction"].insert_many(transaction_dict)


if __name__ == "__main__":
    print(datetime.now(tz=None), ' Starting ! ')
    #### Command Line Arguments
    parser = OptionParser()
    parser.add_option("-u", "--host", dest="dbHost", default="localhost", help="MongoDB Host")
    parser.add_option("-p", "--port", dest="dbPort", default="27017", help="MongoDB Host")
    parser.add_option("-d", "--db", dest="dbName", default='TestRetail', help="Database Name")
    parser.add_option("-e", "--excel", dest="excelPath", default='Online Retail.xlsx', help="temperature threehold")

    (options, args) = parser.parse_args()

    di = DatabaseImport()
    dataset = di.loadDataSet(options.excelPath)
    print(datetime.now(tz=None), ' The excel file is loaded')
    db = di.ConnectionDB(options.dbHost, options.dbPort, options.dbName)
    di.insertProducts(db, dataset)
    print(datetime.now(tz=None), ' Product inserted')
    di.insertTransactions(db, dataset)
    print(datetime.now(tz=None), ' Transaction inserted')
