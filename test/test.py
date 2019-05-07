
import unittest 
from api import app
import json
import pymysql

# def export_db()
#     db = pymysql.connect(host='localhost', port=3306, user='root', passwd='root2018', db='inspection')
#     cursor = db.cursor()
#     cursor.execute("SELECT * FROM USERS")\
#     users = cursor.fetchall()
#     for user in users:
#         print(user)

# def clean_db()

# def restore_db()


class TestAuthentication(unittest.TestCase):
    def setUp(self):
        self.number=1
        self.app = app.test_client()

    def test_simple(self):
        # sample_user = {
        #     "account": "admin",
        #     "password": "admin",
        #     "name": "Sentinel Tec Admin",
        #     "email": "admin@sentineltec.com",
        #     "role_tag": "1"
        # }
        # response = self.app.post('/users/create', data=json.dumps(sample_user),content_type='application/json')
        # print(str(response.json))
        db = pymysql.connect(host='localhost', port=3306, user='root', passwd='root2018', db='inspection')
        cursor = db.cursor()
        cursor.execute("SELECT * FROM USERS")
        users = cursor.fetchall()
        # cursor.execute("DELETE FROM USERS")
        for user in users:
            insert_sql = """insert into `users` values (%s,%s,%s,%s,%s,%s,%s,%s,%s)""", user
            print(insert_sql)

    def tearDown(self):
        print("tearDown")

def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestAuthentication('test_simple'))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())

