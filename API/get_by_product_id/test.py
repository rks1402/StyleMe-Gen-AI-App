import requests

endpoint = "https://fetch-iqcjxj5v4a-el.a.run.app/get_record"
params = {"product_id": "M01"}

response = requests.get(endpoint, params=params)

print(response.status_code)
print(response.json())
