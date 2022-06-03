import requests
import urllib
from skimage.transform import resize
from skimage.io import imread, imsave
from skimage import img_as_float, img_as_ubyte
from numpy import histogram, clip, dstack, ravel, sort, array
import random


class Game:
    def __init__(self, id):
        self.id = id
        self.find = requests.get('https://api.kinopoisk.dev/movie', params={'token': 'CA9PG93-XB54SYB-NMSB8YQ-TMH5SZG',
                                                                            'field': 'id',
                                                                            'search': str(id)}).json()
        self.imgs = requests.get('https://api.kinopoisk.dev/image', params={'token': 'CA9PG93-XB54SYB-NMSB8YQ-TMH5SZG',
                                                                            'field': 'movieId',
                                                                            'search': str(id),
                                                                            'limit': '1000'}).json()

    def show(self):
        print(*self.find.items(), sep='\n')

    def poster(self):
        return self.find['poster']['url']

    def picture1(self):
        return self.find['backdrop']['url']

    def text(self):
        return self.find['description']

    def shortText(self):
        return self.find['shortDescription']

    def stars(self):
        s = self.find['name']
        s_new = ''
        if ' ' not in s:
            s_new = s[:len(s) // 2] + '*' * (len(s) - (len(s) // 2))
        else:
            s_time = s.split()
            for i in range(len(s_time)):
                if i % 2 == 0:
                    s_time[i] = '*' * len(s_time[i])
            s_new = ' '.join(s_time)
        return s_new

    def facts(self):
        a = self.find['facts']
        # print(*a, sep='\n')
        for i in range(len(a)):
            a[i] = a[i]['value']
            s = a[i]
            while '<' in s and '>' in s:
                j, k = s.find('<'), s.find('>')
                s = s[:j] + s[k + 1:]
            while '&' in s:
                j = s.find('&')
                s = s[:j] + ' ' + s[j + 6:]
            a[i] = s
        return a

    def checkAns(self, name):
        name = name.lower().replace(' ', '')
        name_orig = self.find['name'].lower().replace(' ', '')
        return name == name_orig

    def comment(self):
        com = requests.get('https://api.kinopoisk.dev/review', params={'token': 'CA9PG93-XB54SYB-NMSB8YQ-TMH5SZG',
                                                                       'field': 'movieId',
                                                                       'search': str(self.id)}).json()
        comments = com['docs']
        for i in comments:
            yield i['review']

    def bedPoster(self):

        def randpix(n):
            r = random.randint(1, 4)
            if r == 4:
                n = 255
            elif r == 1:
                n = 0
            return n

        def Summer(ex, n):
            temp = array([[0 for j in range(ex.shape[1])] for i in range(ex.shape[0])])
            temp[0][0] = ex[0][0]
            for j in range(1, ex.shape[1]):
                temp[0][j] = temp[0][j - 1] + ex[0][j]
            for i in range(1, ex.shape[0]):
                temp[i][0] = temp[i - 1][0] + ex[i][0]
            for i in range(1, ex.shape[0]):
                for j in range(1, ex.shape[1]):
                    temp[i][j] = temp[i - 1][j] + temp[i][j - 1] - temp[i - 1][j - 1] + ex[i][j]
            time = array(
                [[0 for j in range(n // 2, ex.shape[1] - n // 2)] for i in range(n // 2, ex.shape[0] - n // 2)])
            time[0][0] = temp[n // 2][n // 2]
            for i in range(n // 2 + 1, ex.shape[0] - n // 2):
                for j in range(n // 2 + 1, ex.shape[1] - n // 2):
                    time[i - n // 2][j - n // 2] = (temp[i + n // 2][j + n // 2] + temp[i - n // 2 - 1][
                        j - n // 2 - 1] - temp[i + n // 2][j - n // 2 - 1] - temp[i - n // 2 - 1][j + n // 2]) // n ** 2
            for i in range(n // 2 + 1, ex.shape[0] - n // 2):
                time[i - n // 2][0] = (temp[i + n // 2][n // 2] - temp[i - n // 2 - 1][n // 2]) // n ** 2
            for j in range(n // 2 + 1, ex.shape[1] - n // 2):
                time[0][j - n // 2] = (temp[n // 2][j + n // 2] - temp[n // 2][j - n // 2 - 1]) // n ** 2
            # print(time.shape)
            time = clip(time, 0, 255)
            time = array([[randpix(time[i][j]) for j in range(time.shape[1])] for i in range(time.shape[0])])
            return time

        img = requests.get(self.poster())
        im = open('poster.jpg', 'wb')
        im.write(img.content)
        im.close()
        im = imread('./poster.jpg')
        r = im[:, :, 0].copy()
        g = im[:, :, 1].copy()
        b = im[:, :, 2].copy()
        r = Summer(r, 51)
        g = Summer(g, 51)
        b = Summer(b, 51)
        imsave('poster.jpg', dstack((r, g, b)))

    def randScrean(self):
        date = self.imgs['docs']
        ans = []
        for i in date:
            if 'kp' in i['url'] or 'yandex' in i['url']:
                ans.append(i['url'])
        url = random.choice(ans)
        img = requests.get(url)
        im = open('randomPhoto.jpg', 'wb')
        im.write(img.content)
        im.close()
        im = imread('./randomPhoto.jpg')
        while all([i[0] == 238 and i[1] == 238 and i[2] == 238 for i in (im[0][0], im[0][-1], im[-1][0], im[-1][-1])]):
            url = random.choice(ans)
            img = requests.get(url)
            im = open('randomPhoto.jpg', 'wb')
            im.write(img.content)
            im.close()
            im = imread('./randomPhoto.jpg')


    def smartText(self, str1, str2):
        for i in str2.split():
            if len(i) >= 3:
                str1 = str1.replace(i, '*' * len(i))
        return str1

    def Name(self):
        return self.find['name']

g = Game(430)
g.randScrean()
# print(g.smartText(g.text() + 'ввввв', g.Name()))
# g.show()
# print(g.Name())