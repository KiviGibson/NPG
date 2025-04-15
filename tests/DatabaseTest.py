import unittest
from NPG import DataBase, PressureData, PressureQuery


class TestDatabaseFunctionality (unittest.TestCase):
    def testDatabase(self):
        db = DataBase(":memory:")
        datum = PressureData(1,1000,2000,"Hello")
        query = PressureQuery().insert().addValue(datum)
        db.execute(query)
        query = PressureQuery().select()
        data = db.execute(query)
        print(data)
        self.assertEqual(data[0], datum)

if __name__ == "__main__":
    unittest.main()
