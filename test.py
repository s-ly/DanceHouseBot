# Тестовый модуль.
# Отрабатываю работу с датой и временем.

import datetime
import pytz
# from time import time


# t = datetime.datetime.today()
# d = datetime.datetime.now(tz=None).date()
# t = datetime.datetime.now(tz=None).time()
# print(d, t)

# print(datetime.datetime.now(datetime.timezone))

# Узнать все часовые пояса
# Europe/Moscow
# x = pytz.all_timezones
# for i in x:
#     print(i)

zone_moskow = pytz.timezone('Europe/Moscow')
date_time_moskow = datetime.datetime.now(zone_moskow)
format_date_time_moskow = date_time_moskow.strftime('Date: %Y.%m.%d, Time Moscow: %H:%M')
# format_date_time_moskow = date_time_moskow.strftime('Date: %Y.%m.%d, Time Moscow: %H:%M')
print(format_date_time_moskow)