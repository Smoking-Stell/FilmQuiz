import json
import requests
import random

api_token = "09de81f6-5e66-4883-be7c-be9b689bec90"

headers = {'X-API-KEY': api_token,
           'Content-Type': 'application/json'}

film_id = "47015"
url = 'https://kinopoiskapiunofficial.tech/api/v2.2/films/' + film_id

res = requests.get(url + "/box_office", headers=headers)
data = json.loads(res.content)

if res.status_code == 200:
    t = data.get("items")[4]

    print(t)
