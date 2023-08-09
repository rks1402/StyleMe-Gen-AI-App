import unittest
import requests

class test_api(unittest.TestCase):
    URL="http://127.0.0.1:5000/products?ocassion=Wedding"
    def test_get_all_info(self):
        resp= requests.get(self.URL)
        self.assertEqual(resp.status_code,200)
        self.assertGreaterEqual(len(resp.json()['products']),1)
        print("Test 1 was successful")

if __name__=="__main__":
    tester = test_api()
    tester.test_get_all_info()

class test_api_product(unittest.TestCase):
    URL="http://127.0.0.1:5000/products"
    def test_get_info_for_products(self):
        resp= requests.get(self.URL)
        self.assertEqual(resp.status_code,400)
        self.assertEqual(resp.json(),{"error":"Missing occasion parameter"})
        print("Test 2 was successful")

if __name__=="__main__":
    tester = test_api_product()
    tester.test_get_info_for_products()

