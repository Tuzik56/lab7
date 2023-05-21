import psycopg2
import pendulum

global week, time
week = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
time = ['9:30-11:05', '11:20-12:55', '13:10-14:45', '15:25-17:00', '17:15-18:50']


def week_day(day):
    if day == 'today':
        num = int(pendulum.today('Europe/Moscow').format('E'))
    elif day == 'tomorrow':
        num = int(pendulum.tomorrow('Europe/Moscow').format('E'))
    return week[num-1]


def week_parity(day, reverse):
    if day == 'today':
        num = int(pendulum.today('Europe/Moscow').week_of_year)
    elif day == 'tomorrow':
        num = int(pendulum.tomorrow('Europe/Moscow').week_of_year)
    if num % 2 == 0:
        if reverse:
            return "Нечетная неделя"
        else:
            return "Четная неделя"
    else:
        if reverse:
            return "Четная неделя"
        else:
            return "Нечетная неделя"


conn = psycopg2.connect(database="timetable_db", user="postgres", password="sysiskakolbosa", host="localhost",
                        port="5432")
cursor = conn.cursor()


def timetable_day(day, parity):
    line = f"{day}"
    number = 0
    for t in time:
        cursor.execute("SELECT * FROM timetable JOIN subject ON timetable.subject = subject.id JOIN teacher ON "
                       "timetable.teacher = teacher.id WHERE timetable.weekday=%s AND timetable.parity=%s AND "
                       "timetable.time=%s", (day, parity, t))
        records = list(cursor.fetchall())
        print(records)
        number += 1
        if records:
            line += f"\n\n{number}. {t}\n{records[0][8]}\n{records[0][11]}\n{records[0][9]}, {records[0][6]}"
        else:
            line += f"\n\n{number}. {t}\nНет пары"
    return line


def timetable_week(parity):
    timetable_w = '___________________________\n\n'
    for weekday in week:
        timetable_w += timetable_day(weekday, parity)
        timetable_w += '\n_____________________\n\n'
    return timetable_w
