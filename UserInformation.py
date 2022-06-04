import config

from FilmsList import *
import UserBase


class User:

    """
        Class contains information about user

        uses UserBase and FilmList
    """


    def __init__(self):

        """Constructor

        __user_name: name of user
        __user_id: user number in base
        __que_points: point for current task
        __used_films: films that was used
        __temp_film: current film for this user

        """

        self.__user_name = ""
        self.__user_id = -1
        self.__que_points = config.start_que_points
        self.__used_films = np.zeros(config.number_of_films)
        self.__temp_film = 0

    def update(self):

        """
        Puts new points in base

        :return:
        """

        UserBase.update_base(self.__user_id, self.__que_points)

    def push_new_user(self, name):

        """
        Puts user in base or find it's there

        :param name: name of user
        :return:
        """

        t = UserBase.check_in_base(name)
        self.__user_name = str(name)
        if not t == -1:
            self.__user_id = t
        else:
            self.__user_id = UserBase.push(self.__user_name)

    def set_user_id(self, new_user_name):

        """
        Replaces user name

        :param new_user_name: new user name
        :return:
        """

        self.__user_name = new_user_name
        self.__user_id = UserBase.check_in_base(self.__user_name)

    def existion(self, checked_nick):

        """
        Checks if this user is in base

        :param checked_nick: nick of user
        :return: number in base
        """

        return UserBase.check_in_base(checked_nick)

    def get_user_name(self):

        """

        :return: user name
        """

        return self.__user_name

    def change_que_number(self):

        """
        Reduce points of user

        :return:
        """

        self.__que_points -= 1

    def still_in_game(self):

        """

        :return: if user still can gain some point or no
        """

        return self.__que_points <= 0

    def get_unused_film(self):

        """
        Find new film and puts it in temp_film

        :return: 1 if we can find it
                -1 if we can't
        """

        flag = False
        for i in range(config.number_of_films):
            if self.__used_films[i] == 0:
                flag = True
                break
        if not flag:
            return -1

        self.__que_points = config.start_que_points
        t = random.randint(0, config.number_of_films - 1)
        while self.__used_films[t] == 1:
            t = random.randint(0, config.number_of_films - 1)
        self.__used_films[t] = 1
        self.__temp_film = Film(config.list_of_films_ids[t], str(self.__user_id))
        return 1

    def answer_is_right(self, user_answer):

        """
        Check user answer for correctness
        Allows user make one mistake and and don't look on register

        :param user_answer: answer of user for current film
        :return: boolean answer
        """

        if self.__temp_film == 0:
            return config.please_stop

        real_answer = self.__temp_film.get_right_answer().lower().replace(' ', '')
        user_answer = user_answer.lower().replace(' ', '')
        
        if real_answer == user_answer:
            return True
        count = 0
        i = 0
        while i < len(user_answer) and i < len(real_answer) and\
                user_answer[i] == real_answer[i]:
            i += 1
            count += 1
        i = -1
        while i >= -len(user_answer) and i >= -len(real_answer) \
                and user_answer[i] == real_answer[i]:
            i -= 1
            count += 1
        return abs(len(real_answer) - count) <= 1

    def final_answer(self):

        """

        :return: right answer about current film
        """

        return self.__temp_film.get_right_answer()

    def new_task(self):

        """
        Gives new task about film for this user

        :return: task (cortege: identification, value)
        """

        return self.__temp_film.task()

    def get_results(self):

        """
        Takes base and out it

        :return: string table with results for now in sorted ordinary
        """

        dict = UserBase.get_sorted_base()
        ans = ""
        for i in dict:
            ans += i + "  :  " + str(dict[i]) + "\n"
        return ans

    def full_questions(self):

        """
        Checks if we lost some questions or no

        :return: boolean value
        """

        return self.__que_points == config.start_que_points
