import unittest
from NPG import DataBase, PressureData, PressureQuery


class TestDatabaseFunctionality (unittest.TestCase):
    def testDatabase(self):
        db = DataBase(":memory:")
        datum = PressureData(1,1000,2000,"Hello")
        query = PressureQuery().insert().addValue(datum)
        db.execute(query)
        query = PressureQuery().select().addLimit(2)
        data = db.execute(query)
        self.assertEqual(data[0], datum)

    def testMultipleInsertion(self):
        db = DataBase(":memory:")
        data = [PressureData(i, 100*i, 200*i, "Desc") for i in range(1,4)]
        query = PressureQuery().insert().addValue(data[0]).addValue(data[1]).addValue(data[2])
        db.execute(query)
        query = PressureQuery().select().addLimit(10)
        newData = db.execute(query)
        self.assertEqual(data, newData)
    
    def testRangeFilters(self):
        db = DataBase(":memory:")
        data = [PressureData(i, 100*i, 200*i, "Desc") for i in range(1,4)]
        query = PressureQuery().insert().addValue(data[0]).addValue(data[1]).addValue(data[2])
        db.execute(query)
        
        # Testing Data Range Filter
        query = PressureQuery().select().addDateRange(0, 150).addLimit(3)
        self.assertEqual(data[0], db.execute(query)[0])

        # Testing Pressure Range Filter
        query = PressureQuery().select().addPressureRange(350, 100).addLimit(3)
        self.assertEqual(data[1], db.execute(query)[0])
        
        # Testing Combinatinns of Range Filters
        query1 = PressureQuery().select().addDateRange(250, 100).addPressureRange(550, 100)
        query2 = PressureQuery().select().addPressureRange(550, 100).addDateRange(250, 100)
        self.assertEqual(db.execute(query1), db.execute(query2))
    
    def testEmptyQuery(self):
        db = DataBase(":memory:")
        query = PressureQuery()
        self.assertRaises(Exception, db.execute, query)

if __name__ == "__main__":
    unittest.main()
