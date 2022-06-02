import numpy as np
import random
import json
import requests
from config import url, headers

def general(inf):
    res = requests.get(url + inf, headers=headers)
    if res.status_code == 200:
        ans = json.loads(res.content)
    else:
        raise ValueError
    return ans


def fun1(film_id):
    cont = general(film_id)
    ans = cont.get("slogan")
    return ans


def fun2(film_id):
    cont = general(film_id)
    ans = cont.get("description")
    return ans


def fun3(film_id):
    cont = general(film_id + "/box_office")
    items = cont.get("items")
    ans = "Бюджет$: " + str(items[0]["amount"]) + "    Сборы$: " + str(items[4]["amount"])
    return ans


def fun4(film_id):
    cont = general(film_id + "/facts")
    items = cont.get("items")
    random_fact = random.randint(0, len(items) - 1)
    ans = items[random_fact]["text"]
    return ans


def fun5(film_id):
    cont = general(film_id)
    ans = cont.get("nameEn")
    return ans


class Film:

    def __init__(self, film_id):
        self.used = np.zeros((40))
        self.number_of_questions = 5
        self.functions = [fun1, fun2, fun3, fun4, fun5]
        self.film_id = film_id
        self.right_answer = general(film_id).get("nameRu")

    def task(self):
        num = 0
        while self.used[num] == 1:
            num = random.randint(1, self.number_of_questions - 1)
        self.used[num] = 1
        ans = (self.functions[num])(self.film_id)
        if ans is None:
            return self.task()
        return ans

    def get_right_answer(self):
        return self.right_answer.lower()
