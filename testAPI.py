import numpy as np
import requests
import random
from config import api_token, url, if_foto

def general(inf, field="id", segment="movie"):
    pars = {'token': api_token,
            'field': field,
            'search': inf}
    if field == "movieId":
        pars["limit"] = 1000
    print(pars)
    res = requests.get(url + segment, params=pars)
    if res.status_code == 200:
        ans = res.json()
    else:
        raise ValueError
    return ans

def one_screen(film_id):
    cont = general(film_id, "movieId", "image")
    date = cont['docs']
    print(date)
    ans = []
    for i in date:
        if 'kp' in i['url'] or 'yandex' in i['url']:
            ans.append(i['url'])
    t = random.randint(0, len(ans))
    print(t, ans)
    img = requests.get(ans[t])
    im = open('x.jpg', 'wb')
    im.write(img.content)
    im.close()
    return if_foto

one_screen("430")