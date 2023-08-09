import requests

endpoint = "https://full-iqcjxj5v4a-el.a.run.app//get_all_product"
#params = {"gender": "MEN"}

#response = requests.get(endpoint, params=params)
response = requests.get(endpoint)
print(response.status_code)
print(response.json())

#/get_all_product


