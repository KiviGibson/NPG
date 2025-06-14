import unittest
from NPG import Database, PressureData, Auth


class DatabaseTests(unittest.TestCase):
    def test_check_insert_and_get_data_methods(self):
        db = Database(":memory:")
        test_data = [
            PressureData(i, [int(i * 1.5), i * 2, i], f"Numer {i}.") for i in range(5)
        ]
        db.createUser("test", "test")
        user_id = db.getUser("test")[0]
        for datum in test_data:
            db.addData(user_id, datum)
        for i, datum in enumerate(db.getData(user_id, filters={})):
            self.assertEqual(datum.date, i)
            self.assertEqual(datum.desc, f"Numer {i}.")
            self.assertEqual(datum.value, (int(i * 1.5), i * 2, i))
        db.close()

    def test_check_insert_and_get_user_methods(self):
        db = Database(":memory:")
        login, password = "Test, test".split(", ")
        self.assertEqual(db.createUser(login, password), None)
        self.assertEqual(db.createUser(login, password), -400)
        self.assertEqual(db.getUser(login)[0], 1)
        db.close()

    def test_filters(self):
        db = Database(":memory:")
        db.createUser("test", "test")
        db.addData(1, PressureData(10, [20, 30, 40], "Good"))
        db.addData(1, PressureData(10, [25, 35, 45], "Bad"))
        db.addData(1, PressureData(25, [20, 30, 40], "Bad"))
        data = db.getData(1, {"date": (10, 10), "sys": (20, 20)})
        for datum in data:
            self.assertEqual(datum.desc, "Good")


class AuthTests(unittest.TestCase):
    def test_register_login(self):
        db = Database(":memory:")
        auth = Auth(db)
        reg_jwt = auth.register("test", "test")
        login_jwt = auth.login("test", "test")
        self.assertEqual(reg_jwt, login_jwt)
        err_reg = auth.register("test", "test")
        self.assertEqual(err_reg, -400)
        err_login = auth.login("tezt", "test")
        self.assertEqual(err_login, -404)
        db.close()

    def test_check_creds(self):
        db = Database(":memory:")
        auth = Auth(db)
        res_jwt = auth.register("test", "test")
        err_jwt = auth.check_credentials(None)
        assert isinstance(res_jwt, int) == False
        id = auth.check_credentials(res_jwt)
        self.assertEqual(id, 1)
        self.assertEqual(err_jwt, -418)


if __name__ == "__main__":
    unittest.main()
