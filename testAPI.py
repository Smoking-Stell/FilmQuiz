import json
import requests
import random

api_token = "09de81f6-5e66-4883-be7c-be9b689bec90"

headers = {'X-API-KEY': api_token,
           'Content-Type': 'application/json'}

film_id = "535341"
url = 'https://kinopoiskapiunofficial.tech/api/v2.2/films/' + film_id

res = requests.get(url + "/box_office", headers=headers)
cont = json.loads(res.content)

items = cont.get("items")
#ans = "Бюджет$: " + str(items[0]["amount"]) + "    Сборы$: " + str(items[4]["amount"])

print(items)