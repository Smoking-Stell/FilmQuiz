import config

from FilmsList import *
import UserBase


class Base:
    def __init__(self):
        self.user_name = ""
        self.user_id = -1
        self.que_points = config.start_que_points
        self.used_films = np.zeros(config.number_of_films)
        self.temp_film = 0

    def update(self):
        UserBase.update_base(self.user_id, self.que_points)

    def push_new_user(self, name):
        t = UserBase.check_in_base(name)
        self.user_name = str(name)
        if not t == -1:
            self.user_id = t
        else:
            self.user_id = UserBase.push(self.user_name)

    def set_user_id(self, new_user_name):
        self.user_name = new_user_name
        self.user_id = UserBase.check_in_base(self.user_name)

    def existion(self, checked_nick):
        return UserBase.check_in_base(checked_nick)

    def get_user_name(self):
        return self.user_name

    def change_que_number(self):
        self.que_points -= 1

    def still_in_game(self):
        return self.que_points <= 0

    def get_unused_film(self):
        flag = False
        for i in range(config.number_of_films):
            if self.used_films[i] == 0:
                flag = True
                break
        if not flag:
            return -1

        self.que_points = config.start_que_points
        t = random.randint(0, config.number_of_films - 1)
        while self.used_films[t] == 1:
            t = random.randint(0, config.number_of_films - 1)
        self.used_films[t] = 1
        self.temp_film = Film(config.list_of_films_ids[t], str(self.user_id))
        return 1

    def answer_is_right(self, user_answer):
        if self.temp_film == 0:
            return config.please_stop
        return user_answer.lower().replace(' ', '') == self.temp_film.get_right_answer()

    def final_answer(self):
        return self.temp_film.get_right_answer()

    def new_task(self):
        return self.temp_film.task()

    def get_results(self):
        dict = UserBase.get_sorted_base()
        ans = ""
        for i in dict:
            ans += i + "  :  " + str(dict[i]) + "\n"
        return ans

    def full_questions(self):
        return self.que_points == config.start_que_points
