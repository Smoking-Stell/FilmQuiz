import numpy as np
import random
import requests
from skimage.transform import resize
from skimage.io import imread, imsave
from skimage import img_as_float, img_as_ubyte

import config
from config import url, api_token, if_foto, in_img_case, if_string

count = 0


def write_img(img, img_name):
    """
    It's a function for save image with name (image_name).

    :param img: image file.
    :param img_name: name of image file (str).
    :return: image like skimage.
    """
    im = open(img_name, 'wb')
    im.write(img)
    im.close()
    im = imread('./' + img_name)
    return im


def smart_text(str1, str2):
    """
    It's a function for replace keywords from name of film to *(n).

    :param str1: main string (str).
    :param str2: string with keywords (str).
    :return: new string with *(n) (str).
    """

    for i in str2.split():
        if len(i) >= 3:
            str1 = str1.replace(i, '*')
    return str1


def bed_poster(img, out_img_name):
    """
    This's a function that makes the original plot poor quality.
    Saves image in file

    :param img: image poster.
    :param out_img_name: place for bad image (str).
    :return: None.
    """

    def randpix(n):

        """
        It return random color pixel. 50% for save original color. For 1 canal.

        :param n: color (int).
        :return: color (int).
        """

        r = random.randint(1, 4)
        if r == 4:
            n = 255
        elif r == 1:
            n = 0
        return n

    def Summer(ex, n):

        """
        It's for blur image by mask with length n.

        :param ex: image.
        :param n: length for mask (int).
        :return: blured image.
        """

        temp = np.zeros((ex.shape[0], ex.shape[1]))
        temp[0][0] = ex[0][0]
        for j in range(1, ex.shape[1]):
            temp[0][j] = temp[0][j - 1] + ex[0][j]
        for i in range(1, ex.shape[0]):
            temp[i][0] = temp[i - 1][0] + ex[i][0]
        for i in range(1, ex.shape[0]):
            for j in range(1, ex.shape[1]):
                temp[i][j] = temp[i - 1][j] + temp[i][j - 1] - temp[i - 1][j - 1] + ex[i][j]

        k = n // 2
        time = np.zeros((ex.shape[0] - 2 * k, ex.shape[1] - 2 * k))
        time[0][0] = temp[k][k]
        for i in range(k + 1, ex.shape[0] - k):
            for j in range(k + 1, ex.shape[1] - k):
                time[i - k][j - k] = (temp[i + k][j + k] + temp[i - k - 1][
                    j - k - 1] - temp[i + k][j - k - 1] - temp[i - k - 1][j + k]) // n ** 2
        for i in range(k + 1, ex.shape[0] - k):
            time[i - k][0] = (temp[i + k][k] - temp[i - k - 1][k]) // n ** 2
        for j in range(k + 1, ex.shape[1] - k):
            time[0][j - k] = (temp[k][j + k] - temp[k][j - k - 1]) // n ** 2
        # print(time.shape)
        time = np.clip(time, 0, 255)
        time = np.array([[randpix(time[i][j]) for j in range(time.shape[1])] for i in range(time.shape[0])])
        return time

    im = img.content
    im = write_img(im, out_img_name)
    im = resize(im, (im.shape[0] // 2, im.shape[1] // 2, 3), anti_aliasing=True)
    imsave(out_img_name, im)
    im = imread('./' + out_img_name)

    r = im[:, :, 0].copy()
    g = im[:, :, 1].copy()
    b = im[:, :, 2].copy()
    blur_value = 17
    r = Summer(r, blur_value)
    g = Summer(g, blur_value)
    b = Summer(b, blur_value)
    imsave(out_img_name, np.dstack((r, g, b)))


def general(inf, field="id", segment="movie"):
    """
    It's for request on Kinopoisk.

    :param inf: identification of what we search.
    :param field: place where we search.
    :param segment: movie or image.
    :return: json information about film or picture.
    """

    pars = {'token': api_token,
            'field': field,
            'search': inf}
    if field == in_img_case:
        pars["limit"] = 1000

    res = requests.get(url + segment, params=pars)
    if res.status_code == 200:
        ans = res.json()
    else:
        raise ValueError
    return ans


# args: [film_id, img_name]

def slogan(*args):
    """
    It's for find slogan of film.

    :param args: film id (string).
    :return: string identification and slogan of movie (str).
    """

    cont = general(args[0])
    return if_string, cont["slogan"]


def descript(*args):
    """
    It's for find description of film.

    :param args: film id (string).
    :return: string identification and description of movie (str).
    """

    cont = general(args[0])
    return if_string, smart_text(cont["description"], cont["name"])


def stars(*args):
    """
    It changes words or half of the word to stars.

    :param args: id (int).
    :return: string identification and film name with some parts replaced (str).
    """

    cont = general(args[0])
    s = cont['name']

    if ' ' not in s:
        s_new = s[:len(s) // 2] + '*' * (len(s) - (len(s) // 2))
    else:
        s_time = s.split()
        for i in range(len(s_time)):
            if i % 2 == 0:
                s_time[i] = '*' * len(s_time[i])
        s_new = ' '.join(s_time)
    return if_string, s_new


def fact(*args):
    """
    Get random fact about film and
    cleans fact from links and other unuseful trash.

    :param args: id (int).
    :return: random fact about film like 'smart_text' (str).
    """

    cont = general(args[0])
    items = cont["facts"]
    if items is None:
        return if_string, None
    random_fact = random.randint(0, len(items) - 1)
    s = items[random_fact]["value"]
    while '<' in s and '>' in s:
        j, k = s.find('<'), s.find('>')
        s = s[:j] + s[k + 1:]
    while '&' in s:
        j = s.find('&')
        s = s[:j] + ' ' + s[j + 6:]
    return if_string, smart_text(s, cont["name"])


def intro(*args):
    """
    Get some information about film and

    :param args: id (int).
    :return: string identification and information about film(str)
            None if we can't reach some information
    """

    cont = general(args[0])
    try:
        ans = f"Жанр: {cont['genres'][0]['name']} \nРежиссер (или руководитель): {cont['persons'][0]['name']} \n" \
              f"Премьера: {cont['premiere']['world'][:4]} год."
    except Exception:
        ans = None
    return if_string, ans


def poster(*args):
    """
    It's for find poster.

    :param args: id (int).
    :return: image identification and film poser in bad condition.
    """

    cont = general(args[0])
    img = requests.get(cont["poster"]["url"])

    img_name = args[1]
    bed_poster(img, img_name)
    return if_foto, img_name


def one_screen(*args):
    """
    It's for find random frame of film.
    Checks if frame exists (because some frames replaced with special image)

    :param args: film id (str) and name for image
    :return: image identification and random frame of film (image)
    or None if we haven't any images for movie.
    """

    cont = general(args[0], in_img_case, "image")
    date = cont['docs']
    ans = []
    for i in date:
        if 'kp' in i['url'] or 'yandex' in i['url']:
            ans.append(i['url'])

    if not ans:
        return if_foto, None

    t = random.randint(0, len(ans) - 1)
    img = requests.get(ans[t])
    im = write_img(img.content, args[1])

    while (ans[t] == -1) or all([i[0] == 238 and i[1] == 238 and i[2] == 238
                                 for i in (im[0][0], im[0][-1], im[-1][0], im[-1][-1])]):
        ans[t] = -1
        t = random.randint(0, len(ans) - 1)
        img = requests.get(ans[t])
        im = write_img(img.content, args[1])

    return if_foto, args[1]


class Film:
    """
    Class contains some information about film
    Uses config and some functions from FilmList

    """

    def __init__(self, film_id, film_user_name):

        """
        Constructor.
        __used: shows was this function used or not
        functions: list of tasks
        right_answer: shows right name of film on russian

        :param film_id: id of kinopoisk (int).
        :param film_user_name: some unique information for user, who used this film (str).
        """

        self.functions = [slogan, descript, one_screen, fact, poster, stars, intro]
        self.__used = np.zeros((len(self.functions) + 2))
        self.__film_id = film_id
        self.__film_user_name = film_user_name
        self.__right_answer = general(film_id)["name"]

    def task(self):

        """
        Function gives random task about film and identification for it

        :return: identification, information
        """
        m = len(self.functions) - 1
        flag = True
        for i in range(m + 1):
            if self.__used[i] == 0:
                flag = False
                break
        if flag:
            return
        num = random.randint(0, m)
        while self.__used[num] == 1:
            num = random.randint(0, m)
        self.__used[num] = 1
        ans = (self.functions[num])(self.__film_id, self.__film_user_name + '.jpg')

        if ans[1] is None:
            return self.task()

        global count
        count += 1
        print(num)
        print( ans)

    def get_right_answer(self):

        """
        Get right name of film.

        :return: right answer. (str)
        """

        return self.__right_answer


checked_id = "1228254"
temp = Film(checked_id, "1")

for i in range(len(temp.functions)):
    temp.task()

print(count)
