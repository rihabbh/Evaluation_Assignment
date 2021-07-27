import unittest
from DatabaseImport import DatabaseImport
import pandas as pd
import numpy as np
import mongomock
import pymongo



class MyTestCase(unittest.TestCase):
    d = {'InvoiceNo': [1, 2, 3, 4, 5], 'StockCode': [1, 2, 3, 2, "3B"],
         'Description': ["test", "test white", "small test", "TEST WHITE", "small test"], 'Quantity': [1, 2, 3, 5, 13],
         'InvoiceDate': ['', '', '', '', ''], 'UnitPrice': [1.0, 3.0, 3.6, 5.0, 0.5],
         'CustomerID': [1, 2, 3, 4, 5], 'Country': ['France', 'France', 'France', 'France', 'France']}

    d2 = {'InvoiceNo': [1, 2, 3, 4, 5], 'StockCode': [1, 2, 3, 4, "3B"],
         'Description': ["test", "test white", "small test", "TEST WHITE", "small test"], 'Quantity': [1, 2, 3, 5, 13],
         'InvoiceDate': ['', '', '', '', ''], 'UnitPrice': [1.0, 3.0, 3.6, 5.0, 0.5],
         'CustomerID': [1, 2, 3, 4, 5], 'Country': ['France', 'France', 'France', 'France', 'France']}

    df = pd.DataFrame(data=d)
    df2 = pd.DataFrame(data=d2)


    @mongomock.patch(servers=(('localhost', 27017),))
    def test_no_duplicate(self):
        """
        There are five transactions but only four products
        Test to see if product is unique in the Product Collection
        """
        client = pymongo.MongoClient('localhost')
        di = DatabaseImport()
        di.insertProducts(client['RetailTest'], self.df)
        result = list(client['RetailTest'].Product.find())
        nbrProduit = len(result)
        self.assertEqual(4, nbrProduit)

    @mongomock.patch(servers=(('localhost', 27017),))
    def test_no_duplicate2(self):
        """
        We will insert a second dataframe with one one new product
        Test if only the new product is added and no duplication.
        """
        client = pymongo.MongoClient('localhost')
        di = DatabaseImport()
        di.insertProducts(client['RetailTest'], self.df)
        di.insertProducts(client['RetailTest'], self.df2)
        result = list(client['RetailTest'].Product.find())
        nbrProduit = len(result)
        self.assertEqual(5, nbrProduit)

    @mongomock.patch(servers=(('localhost', 27017),))
    def test_description(self):
        """
        Test if the description is correctly inserted
        """
        client = pymongo.MongoClient('localhost')
        di = DatabaseImport()
        di.insertProducts(client['RetailTest'], self.df)
        result = list(client['RetailTest'].Product.find({'StockCode': '2'}))[0]['Description']
        self.assertEqual('test white', result)

    @mongomock.patch(servers=(('localhost', 27017),))
    def test_ProduitCode(self):
        """
        See if the value 'ProductCode' is correctly formatted
        """
        client = pymongo.MongoClient('localhost')
        di = DatabaseImport()
        di.insertProducts(client['RetailTest'], self.df)
        result = list(client['RetailTest'].Product.find({'StockCode': '2'}))[0]['ProductCode']
        self.assertEqual('2', result)

    @mongomock.patch(servers=(('localhost', 27017),))
    def test_ProduitCode2(self):
        """
        See if the value 'ProductCode' is correctly formatted
        """
        client = pymongo.MongoClient('localhost')
        di = DatabaseImport()
        di.insertProducts(client['RetailTest'], self.df)
        result = list(client['RetailTest'].Product.find({'StockCode': '3b'}))[0]['ProductCode']
        self.assertEqual('3', result)

    @mongomock.patch(servers=(('localhost', 27017),))
    def test_nbr_Transaction(self):
        """
        Test if all transactions are inserted
        """
        client = pymongo.MongoClient('localhost')
        di = DatabaseImport()
        di.insertTransactions(client['RetailTest'], self.df)
        result = list(client['RetailTest'].Transaction.find())
        self.assertEqual(5, len(result))

    @mongomock.patch(servers=(('localhost', 27017),))
    def test_CustumerID_Type(self):
        """
        Test if all Custumer ID are int type
        """
        client = pymongo.MongoClient('localhost')
        di = DatabaseImport()
        di.insertTransactions(client['RetailTest'], self.df)
        result = pd.DataFrame(list(client['RetailTest'].Transaction.find()))
        custumerID = result['CustomerID']
        self.assertEqual(np.int64, custumerID.dtypes)

    @mongomock.patch(servers=(('localhost', 27017),))
    def test_StockCode_Type(self):
        """
        Test if all StockCode are string type
        """
        client = pymongo.MongoClient('localhost')
        di = DatabaseImport()
        di.insertTransactions(client['RetailTest'], self.df)
        result = pd.DataFrame(list(client['RetailTest'].Transaction.find()))
        isString = result.applymap(type).eq(str).all()['StockCode']
        self.assertEqual(True, isString)

if __name__ == '__main__':
    unittest.main()
