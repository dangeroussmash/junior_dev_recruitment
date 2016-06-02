# -​*- coding: utf-8 -*​-
"""

##########
# TASK 1 #
##########

SUBTASK 1 Define the Client class with attributes:
first_name, last_name, birth_date, sex

SUBTASK 2
define a method on Ticket: get_ticket_data,
which returns dumped JSON object
with all data on ticket, and all data on client

SUBTASK 3
Write a method (name: can_watch_pegi ;)) on client which check if he is able
to watch the movie - according to PEGI
(https://pl.wikipedia.org/wiki/Pan_European_Game_Information)
(yep, I know - PEGI is for games, but who cares) - assume following age
marks: 3, 7, 12, 16, 18;
Method should return True or False -> True means that client is older than
restriction and can watch the movie;
"""

import json
import datetime
from dateutil.relativedelta import relativedelta

class Ticket(object):
    def __init__(self, client, ticket_id=1, event_date='2000-12-12',
                 event_time='12h', event_name='wydarzenie', room_number=12,
    ):
        self.ticket_id = ticket_id
        self.event_date = event_date
        self.event_time = event_time
        self.event_name = event_name
        self.client = client
        self.room_number = room_number

    def get_ticket_data(self):
        return json.dumps({
            "event_time": self.event_time,
            "event_name": self.event_name,
            "room_number": self.room_number,
            "ticket_id": self.ticket_id,
            "event_date": self.event_date,
            "client": {
                "first_name": self.client.first_name,
                "last_name": self.client.last_name,
                "birth_date": self.client.birth_date,
                "sex": self.client.sex,
            },
        }, indent=4, sort_keys=True)


class Client(object):
    PEGI = [3, 7, 12, 16, 18]

    def __init__(self, first_name='Imejl', last_name='Imejlowski', birth_date='1999-12-20', sex='M'):
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.sex = sex

    def can_watch_pegi(self, film_pegi):
        """
        funkcja zwraca True albo False
        :param film_pegi: dozwolwoy rok
        :return:
        """
        year, month, day = tuple(int(x) for x in self.birth_date.split('-'))
        #self.birth_date = date(year, month, day)
        #your_age = self.how_old_are_you(self.birth_date)
        return self._how_old_are_you(datetime.date(year, month, day)) >= film_pegi

    def _how_old_are_you(self, start_date):
        return relativedelta(datetime.datetime.now(), start_date).years

if __name__ == '__main__':
    client = Client('Imejl', 'Imejlowski', birth_date='1900-12-12', sex='M')
    ticket = Ticket(client, ticket_id=112)
    ticket.get_ticket_data()

##########
# TASK 2 #
##########

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def iterate_over_list(some_list):
    i = 0
    new_list = []
    for element in some_list:
        n_element = int(element) + i
        new_list.append(n_element)
        i = i + 1
    return new_list

# subtask1
def iterate_over_list1(some_list):
    return [number + index for index, number in enumerate(some_list)]

# subtask2
def iterate_over_list2(some_list):
    return [str(string) * index for index, string in enumerate(some_list)]

def iterate_over_list3(some_list):
    if all([isinstance(x, int) for x in some_list]):
                return [number + index for index, number in enumerate(some_list)]
        else:
                return [str(string) * index for index, string in enumerate(some_list)]

# unit tests
some_list = [1, 4, 5, 1, 2, 4]
assert iterate_over_list(some_list) == iterate_over_list1(some_list)

list0 = [1, 'b', 'c']
assert iterate_over_list2(list0) == ['', 'b', 'cc']


"""

##########
# TASK 3 #
##########

SELECT DISTINCT location_city, pois_count FROM poi ORDER BY location_city

w celu optymalizacji (poprawy wydajności bazy), zmieniłbym typy danych kolumn,
typ TEXT zaminiłym na varchar() a szerokość i długość geograficzną przechowywałbym w type INT

"""
