import csv
import config

from FilmsList import *


def take_base():
    base_of_users = []
    with open("./base.csv", encoding='utf-8') as r_file:
        file_reader = csv.reader(r_file, delimiter=",")
        for row in file_reader:
            base_of_users.append(row)
    return base_of_users


class Base:
    def __init__(self):
        self.base_of_users = take_base()
        self.user_name = ""
        self.user_id = -1
        self.que_points = 7
        self.used_films = np.zeros(config.number_of_films)
        self.temp_film = 0

    def update(self):
        t = int(self.base_of_users[self.user_id][1]) + self.que_points
        self.base_of_users[self.user_id][1] = str(t)
        with open("./base.csv", mode='w', encoding='utf-8') as w_file:
            file_writer = csv.writer(w_file, delimiter=",", lineterminator="\n")
            for i in range(len(self.base_of_users)):
                file_writer.writerow([self.base_of_users[i][0], self.base_of_users[i][1]])

    def push_new_user(self, name):
        self.user_name = str(name)
        self.user_id = len(self.base_of_users)
        self.base_of_users.append([self.user_name, "0"])

    def check_in_base(self, usr):
        for i in range(len(self.base_of_users)):
            if self.base_of_users[i][0] == usr:
                return i
        return -1

    def change_user_name(self, new_user_name):
        self.user_name = new_user_name

    def get_user_name(self):
        return self.user_name

    def change_que_number(self):
        self.que_points -= 1

    def get_steal_que_number(self):
        return self.que_points

    def get_unused_film(self):
        flag = False
        for i in range(config.number_of_films):
            if self.used_films[i] == 0:
                flag = True
                break

        if not flag:
            return -1

        self.que_points = 6
        t = random.randint(0, config.number_of_films - 1)
        while self.used_films[t] == 1:
            t = random.randint(0, config.number_of_films - 1)
        self.used_films[t] = 1
        self.temp_film = Film(config.list_of_films_ids[t])
        return 1

    def answer_is_right(self, user_answer):
        return user_answer.lower() == self.temp_film.get_right_answer()

    def new_task(self):
        return self.temp_film.task()
