"""
Contains general information:
    tokens and url
    list of films
    identifications
"""

token = '5160953743:AAEiEMtJR-59wS7PuTD8N_AslzCsH452Veg'

# api_token = "09de81f6-5e66-4883-be7c-be9b689bec90"
api_token = "CA9PG93-XB54SYB-NMSB8YQ-TMH5SZG"

url = 'https://api.kinopoisk.dev/'

in_img_case = "movieId"

"Названия:" \
"Хороший, плохой, злой; 1+1; Начало; Шрэк; Джокер" \
"Назад в будущее; Остров сокровищ; Джанго освобождённый; Криминальное чтиво; Зеленая книга" \
"Рататуй; Волк с Уолл-стрит; Как приручить дракона; Бесславные ублюдки; Мулан;" \
" Аладдин; День сурка; Железный человек; Мадагаскар; Красавица и чудовище;" \
" Аватар; 101 далматинец; Люди в чёрном; В поисках Немо; Ледниковый период;" \
"Маска; Рик и морти; Гравити Фолз; Аватар: ЛоА; Атака Титанов"

#первые 9 строчек работают
list_of_films_ids = ["349", "535341", "447301", "430", "1048334",
                     "476", "573759", "586397", "342", "1108577",
                     "89514", "462682", "280172", "9691", "5277",
                     "2361", "527", "61237", "6006", "540",
                     "251733", "8129", "1091", "7908", "707",
                     "6039", "685246", "591929", "401152", "749374",
                     "404900", "253245", "464963", "178710", "571335",
                     "502838", "229653", "841914", "1236393", "1227803",
                     "681831", "655800", "406148", "1231054", "4695",
                     "355", "1322324", "597", "1047593", "278185",
                     "259251", "41519", "279102", "361", "370",
                     "474", "522", "4374", "324", "325",
                     "526", "957887", "819101", "42571", "42770",
                     "1228254", "589290", "403", "577488", "453406",
                     "418", "354"]

number_of_films = len(list_of_films_ids)

start_que_points = 6

if_foto = "PhotoPhoto"
if_string = "StringString"
please_stop = "Тебе же сказали, что иногда нужно подождать"
