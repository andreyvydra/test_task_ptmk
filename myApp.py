import datetime
import sqlite3
import random
import time
from sys import argv


def set_table(cursor):
    try:
        cursor.execute('''CREATE TABLE pupil (
                        id       INTEGER  PRIMARY KEY AUTOINCREMENT
                                          UNIQUE
                                          NOT NULL,
                        name     STRING   NOT NULL,
                        birthday DATETIME NOT NULL,
                        sex      BOOLEAN  NOT NULL
                    );''')
        print('Successful operation')
    except sqlite3.DatabaseError:
        print('Database is already done')


def add_pupil(cursor):
    try:
        surname = argv[2]
        name = argv[3]
        fathers_name = argv[4]
        birthday = [int(i) for i in argv[5].split('/')]
        sex = argv[6]
        if len(birthday) == 3:
            birthday = datetime.datetime(year=birthday[2],
                                         month=birthday[1],
                                         day=birthday[0])
        else:
            raise Exception

        if sex.lower() in ['мужской', 'женский']:
            sex = 1 if sex.lower() == 'мужской' else 0
        else:
            raise Exception

        cursor.execute(f'''INSERT INTO pupil(name, birthday, sex)
                        VALUES('{surname} {name} {fathers_name}',
                        '{birthday}', {sex})''')

        print('Successful operation')
    except Exception as e:
        print('Something is wrong or Database isnt already exist')
        print('Example run: python myApp.py 2 Vasya Pupkin Pupkovich 15/03/2000 мужской')


def select_unique_people(cursor):
    try:
        res = cursor.execute('''SELECT name, birthday, sex FROM pupil
                          GROUP BY name, birthday
                          ORDER BY name ASC''').fetchall()
        now_date = datetime.datetime.now()
        sexs = {
            0: 'женский',
            1: 'мужской'
        }
        for item in res:
            delta = now_date - datetime.datetime.strptime(item[1], '%Y-%m-%d %H:%M:%S')

            print(f'ФИО: {item[0]}, др: {item[1]}, пол: {sexs[item[2]]},'
                  f' полных лет: {delta.days // 365}')
    except sqlite3.OperationalError:
        print('Database isnt already exist')


def add_a_lot_people(cursor):
    try:
        ru_letters = ['а', 'б', '', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й',
                      'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т',
                      'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'э', 'ю', 'я']
        name = 'Андрей'
        fathers_name = 'Михайлович'
        birthday = datetime.datetime(year=2000, month=3, day=15)
        for _ in range(100000):
            surname = random.choice(ru_letters).upper() + 'ич'
            sex = random.randint(0, 1)
            cursor.execute(f'''INSERT INTO pupil(name, birthday, sex)
                            VALUES('{surname} {name} {fathers_name}',
                            '{birthday}', {sex})''')

        surname = 'Fич'
        sex = 1
        for _ in range(100):
            cursor.execute(f'''INSERT INTO pupil(name, birthday, sex)
                            VALUES('{surname} {name} {fathers_name}',
                            '{birthday}', {sex})''')

    except sqlite3.OperationalError:
        print('Database isnt already exist')


def select_mans_with_f(cursor):
    try:
        tm1 = time.time()

        res = cursor.execute('''SELECT name, birthday, sex FROM pupil
                             WHERE sex = 1 AND name LIKE 'F%' ''').fetchall()

        sexs = {
            0: 'женский',
            1: 'мужской'
        }

        for item in res:
            print(f'ФИО: {item[0]}, др: {item[1]}, пол: {sexs[item[2]]}')

        tm2 = time.time()
        print(f'Время выполнения: {tm2 - tm1} секунд')
    except sqlite3.OperationalError:
        print('Database isnt already exist')


if __name__ == '__main__':
    con = sqlite3.connect('db.db')
    cur = con.cursor()

    commands = {
        '1': set_table,
        '2': add_pupil,
        '3': select_unique_people,
        '4': add_a_lot_people,
        '5': select_mans_with_f
    }

    if argv[1] in commands:
        commands[argv[1]](cur)
    else:
        print('Unknown operation')

    con.commit()
    con.close()
