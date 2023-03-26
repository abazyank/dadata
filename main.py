import sqlite3 as sl
import requests
import simplejson as json
import string


class user_preference:
    def __init__(self):
        db = sl.connect('base.db')
        sql = db.cursor()
        sql.execute("""CREATE TABLE IF NOT EXISTS users_preference(
                            URL,
                            API,
                            lang
                )""")
        db.commit()
        db.close()

    def exist_check(self):
        sqlite_connection = sl.connect('base.db')
        cursor = sqlite_connection.cursor()
        sqlite_show_query = """SELECT * FROM users_preference"""
        cursor.execute(sqlite_show_query)
        records = cursor.fetchall()
        sqlite_connection.close()
        return(records != [])

    def create_default_table(self):
        sqlite_connection = sl.connect('base.db')
        cursor = sqlite_connection.cursor()
        URL = "https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/address"
        lang = 'ru'
        self.URL = URL
        self.language = lang
        data = [URL, lang]
        sqlite_insert_query = """INSERT INTO users_preference
                                  ('URL', 'API', 'lang')
                                  VALUES
                                  (?, '', ?);"""
        count = cursor.execute(sqlite_insert_query,data)
        sqlite_connection.commit()
        cursor.close()

    def get_user_setting(self):
        sqlite_connection = sl.connect('base.db')
        cursor = sqlite_connection.cursor()
        sqlite_show_query = """SELECT * FROM users_preference"""
        cursor.execute(sqlite_show_query)
        records = cursor.fetchall()
        self.URL, self.API, self.language = records[0][0], records[0][1], records[0][2]

    def URL_change(self,new_URL):
        sqlite_connection = sl.connect('base.db')
        cursor = sqlite_connection.cursor()
        sqlite_update_query = """UPDATE users_preference set URL = ? where rowid = 1"""
        cursor.execute(sqlite_update_query, [new_URL])
        sqlite_connection.commit()
        self.URL = new_URL
        sqlite_connection.close()

    def API_change(self, new_API):
        sqlite_connection = sl.connect('base.db')
        cursor = sqlite_connection.cursor()
        sqlite_update_query = """UPDATE users_preference set API = ? where rowid = 1"""
        cursor.execute(sqlite_update_query, [new_API])
        sqlite_connection.commit()
        self.API = new_API
        sqlite_connection.close()

    def language_change(self, new_lang):
        sqlite_connection = sl.connect('base.db')
        cursor = sqlite_connection.cursor()
        sqlite_update_query = """UPDATE users_preference set lang = ? where rowid = 1"""
        cursor.execute(sqlite_update_query, [new_lang])
        sqlite_connection.commit()
        self.language = new_lang
        sqlite_connection.close()

    def show_settings(self):
        sqlite_connection = sl.connect('base.db')
        cursor = sqlite_connection.cursor()
        sqlite_show_query = """SELECT * FROM users_preference"""
        cursor.execute(sqlite_show_query)
        records = cursor.fetchall()
        sqlite_connection.close()
        for i in records[0]:
            if i == records[0][0]:
                print('URL:', i)
            elif i == records[0][1]:
                print('API:', i)
            else:
                print('language:', i)


def check_URL(URL):
    flag = 1
    if URL[0:8] != 'https://':
        print('Неверный формат URL, он должен начинаться с https://')
        flag = 0

    return flag

def suggest(query, API_KEY, url,language):
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": "Token " + API_KEY
    }
    data = {
        'query': query,
        'language': language
    }
    res = requests.post(url, data=json.dumps(data), headers=headers)
    return res.json()


def print_menu():
    x = range(0, 51)
    y = range(0, 11)
    for i in y:
        print('')
        for j in x:
            if i == 0 or i == 10 or j == 0 or j == 50:
                print('*', end='')
            else:
                print(' ', end='')


def main_menu():
    flag = 1
    flag_settings = 1
    flag_coordinats = 1
    flag_number = 1
    adress_array = dict()
    settings = user_preference()

    if(settings.exist_check()):
        settings.get_user_setting()
        # print(settings.API, settings.URL, settings.language)
    else:
        settings.create_default_table()
        print("Для начала работы введите API:")
        new_API = input()
        settings.API_change(new_API)
    flag = 1
    while (flag):
        print("Введите '1' для настройки пользователя\n", "Введите '2' для нахождения координат\n", "Для выхода из программы введите 'q'", sep='')
        choice = input()
        if choice == '1':
            flag_settings = 1

            while (flag_settings):
                print("1. Настройка URL\n", "2. Настройка API\n", "3. Настройка языка\n", "4. Посмотреть текущие настойки\n", "Для выхода введите 'q'", sep='')
                choice_settings = input( )
                if choice_settings == '1':
                    print("Введите URL:")
                    new_URL = input()
                    cheker = check_URL(new_URL)
                    if cheker:
                        settings.URL_change(new_URL)
                    else:
                        print('URL не изменён, попробуйте ввести другой\n')
                elif choice_settings == '2':
                    print("Введите API:")
                    new_API = input()
                    settings.API_change(new_API)
                    print(settings.API)
                elif choice_settings == '3':
                    print("Выберите язык:\n", "1. Русский\n", "2. English")
                    flag_lang = 1
                    while flag_lang:
                        lang_choice = input()
                        if lang_choice == '1':
                            new_lang = 'ru'
                            flag_lang = 0
                            settings.language_change(new_lang)
                        elif lang_choice == '2':
                            new_lang = 'en'
                            flag_lang = 0
                            settings.language_change(new_lang)
                        elif lang_choice.isdigit() == False:
                            print("Введено не число")
                        elif int(lang_choice) > 2 or int(lang_choice) < 1:
                            print("Это число вне диапазона, попробуйте ввести другое")
                elif choice_settings == '4':
                    settings.show_settings()
                elif choice_settings == 'q':
                    flag_settings = 0
                else:
                    print("Неверный ввод, попробуйте ещё раз")
        elif choice == '2':
            flag_coordinats = 1
            while flag_coordinats:
                print("Введите адрес:\n", "Для выхода введите 'q'", sep='')
                adress_user = input()
                try:
                    res = suggest(adress_user, settings.API, settings.URL, settings.language)
                    if adress_user == 'q':
                        flag_coordinats = 0
                    elif 'family' in res:
                        if res['family'] == 'CLIENT_ERROR':
                            print('Неверный API, попробуйте изменить его')
                            flag_coordinats = 0
                    else:
                        if res['suggestions'] == []:
                            print("К сожалению, ничего не нашлось, попробуйте ввести другой адрес")
                        else:
                            for i in range(1,len(res['suggestions'])):
                                adress_array[str(i)] = str(res["suggestions"][i]["data"]["geo_lat"]) + " " + str(res["suggestions"][i]["data"]["geo_lon"])
                                print(i, '', res['suggestions'][i]['value'])
                            flag_number = 1
                            while flag_number:
                                print("Введите номер адреса:\n", "Для выхода введите 'q'")
                                number = input()
                                if number == 'q':
                                    flag_number = 0
                                    flag_coordinats = 0
                                elif number.isdigit() == False:
                                    print("Введено не число")
                                elif int(number) > len(res['suggestions']) - 1:
                                    print("Это число вне диапазона, попробуйте ввести другое")
                                elif adress_array[number] == 'None None':
                                    print("Увы, не удалось найти координаты этого адреса")
                                    flag_number = 0
                                else:
                                    flag_number = 0
                                    result_string_array = adress_array[number].split()
                                    print("Широта:", result_string_array[0], "Долгота:",  result_string_array[1])
                except requests.ConnectionError:
                    print('Ошибка, некорректный URL, попробуйте изменить его')
                    flag_coordinats = 0
        elif choice == 'q':
            flag = 0
        elif choice.isdigit() == False:
            print("Введено не число")
        elif int(choice) > len(res['suggestions']) - 1:
            pass


main_menu()






