import requests

endpoint = "https://gender-iqcjxj5v4a-el.a.run.app/get_by_gender"
params = {"gender": "MEN"}

response = requests.get(endpoint, params=params)

print(response.status_code)
print(response.json())

#get_record?gender=MEN


