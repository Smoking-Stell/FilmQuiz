import numpy as np
import random
import requests
from skimage.transform import resize
from skimage.io import imread, imsave
from skimage import img_as_float, img_as_ubyte

from config import url, api_token, if_foto, in_img_case, if_string


def write_img(img, img_name):
    im = open(img_name, 'wb')
    im.write(img)
    im.close()
    im = imread('./' + img_name)
    return im

def smart_text(str1, str2):
    for i in str2.split():
        if len(i) >= 3:
            str1 = str1.replace(i, '*')
    return str1

def bed_poster(img, out_img_name):
    def randpix(n):
        r = random.randint(1, 4)
        if r == 4:
            n = 255
        elif r == 1:
            n = 0
        return n

    def Summer(ex, n):
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

    im = write_img(img.content, out_img_name)

    r = im[:, :, 0].copy()
    g = im[:, :, 1].copy()
    b = im[:, :, 2].copy()
    r = Summer(r, 51)
    g = Summer(g, 51)
    b = Summer(b, 51)
    imsave(out_img_name, np.dstack((r, g, b)))


def general(inf, field="id", segment="movie"):
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


#args: [film_id, img_name]

def slogan(*args):
    cont = general(args[0])
    return if_string, cont["slogan"]


def descript(*args):
    cont = general(args[0])
    return if_string, smart_text(cont["description"], cont["name"])


def one_screen(*args):
    cont = general(args[0], in_img_case, "image")
    date = cont['docs']
    ans = []
    for i in date:
        if 'kp' in i['url'] or 'yandex' in i['url']:
            ans.append(i['url'])

    if not ans:
        return None

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


def fact(*args):
    cont = general(args[0])
    items = cont["facts"]
    random_fact = random.randint(0, len(items) - 1)
    s = items[random_fact]["value"]
    while '<' in s and '>' in s:
        j, k = s.find('<'), s.find('>')
        s = s[:j] + s[k + 1:]
    while '&' in s:
        j = s.find('&')
        s = s[:j] + ' ' + s[j + 6:]
    return if_string, smart_text(s, cont["name"])


def poster(*args):
    cont = general(args[0])
    img = requests.get(cont["poster"]["url"])
    img_name = args[1]
    bed_poster(img, img_name)
    return if_foto, img_name


def stars(*args):
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


class Film:

    def __init__(self, film_id, film_user_name):
        self.used = np.zeros((40))
        self.functions = [slogan, descript, one_screen, fact, poster, stars]
        self.film_id = film_id
        self.film_user_name = film_user_name
        self.right_answer = general(film_id)["name"]

    def task(self):
        m = len(self.functions) - 1
        num = random.randint(0, m)
        while self.used[num] == 1:
            num = random.randint(0, m)
        self.used[num] = 1
        ans = (self.functions[num])(self.film_id, self.film_user_name + '.jpg')

        if ans[1] is None:
            return self.task()

        return ans

    def get_right_answer(self):
        return self.right_answer.lower().replace(' ', '')
