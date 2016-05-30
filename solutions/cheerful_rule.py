# -*- coding: utf-8 -*-
# Hello! Good luck!

##############
#   TASK 1   #
##############

# SUBTASK 1
# Define the Client class with attributes:
# first_name, last_name, birth_date, sex

# SUBTASK 2
# define a method on Ticket: get_ticket_data, which returns dumped JSON object
# with all data on ticket, and all data on client;
# EXAMPLE:
#     {
#         "event_time": "20:00",
#         "event_name": "The Killer",
#         "room_number": "Sala 7",
#         "client":
#             {
#                 "birth_date": "1985-01-23",
#                 "first_name": "Romuald",
#                 "last_name": "Lechon",
#                 "sex": "MALE"
#             },
#         "ticket_id": "12345678",
#         "event_date": "2015-09-10"
#     }

# SUBTASK 3
# Write a method (name: can_watch_pegi ;)) on client which check if he is able
# to watch the movie - according to PEGI
# (https://pl.wikipedia.org/wiki/Pan_European_Game_Information)
# (yep, I know - PEGI is for games, but who cares) - assume following age
# marks: 3, 7, 12, 16, 18;
# Method should return True or False -> True means that client is older than
# restriction and can watch the movie;

# SUBTASK 4
# Propose a structure where client instance will have some interface to get the
# all ticket ids - whenever added, which returns all ticket ids;
# EXAMPLE (it's just an example, remember - "some interface" - be creative):
# c = Client(...)
# t = Ticket('12345678', client=c, ...)
# t = Ticket('8765431', client=c, ...)
# t = Ticket('12343141', client=c, ...)
# c.get_ticket_ids()
# OUTPUT: ['12345678', '8765431', '12343141']


from datetime import date, datetime
from json import dumps


class Ticket(object):
    def __init__(
        self,
        ticket_id,    # the unique identifier of the ticket;
        event_date,   # the date of the event;
        event_time,   # the time when event occurs;
        event_name,   # the event name -> obvious one :);
        client,       # the INSTANCE of the client;
        room_number,  # the room number in which event happens;
    ):
        self.ticket_id = ticket_id
        self.event_date = event_date
        self.event_time = event_time
        self.event_name = event_name
        self.client = client
        self.room_number = room_number
        self.client.tickets.append(self.ticket_id)

    def get_ticket_data(self):
        ticket_data = self.__dict__
        ticket_data['client'] = self.client.__dict__
        return dumps(ticket_data)


class Client(object):
    def __init__(
        self, 
        first_name, 
        last_name, 
        birth_date, 
        sex,
    ):
        self.first_name = first_name
        self.last_name = last_name

        if sex.upper() in ('MALE', 'FEMALE'):
            self.sex = sex
        else:
            raise TypeError("Incorrect sex. Choose 'male' or 'female'")

        if isinstance(birth_date, date) or isinstance(birth_date, datetime):
            try:
                self.birth_date = '{:%Y-%m-%d}'.format(birth_date)
            except ValueError:
                raise TypeError("Format of birth_date is incorrect")
        elif isinstance(birth_date, str):
            try:
                self.birth_date = datetime.strptime(birth_date, "%Y-%m-%d")
            except ValueError:
                raise TypeError("Format of birth_date is incorrect")
        else:
            raise TypeError("Format of birth_date is incorrect")

        self.tickets = []

    def _get_age(self, today):
        condition = (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
        return today.year - self.birth_date.year - int(condition)

    def can_watch_pegi(self, pegi_age):
        today = date.today()
        age = self._get_age(today)
        return age >= pegi_age

    def get_ticket_ids(self):
        return self.tickets



##############
#   TASK 2   #
##############

# SUBTASK 1
# do it in pythonic way;
# it just adds the index to the list element on this index
# and return a new list;
# TIP: shorter is better;

# def iterate_over_list(some_list):
#     i = 0
#     new_list = []
#     for element in some_list:
#         n_element = int(element) + i
#         new_list.append(n_element)
#         i = i + 1
#
#     return new_list


def iterate_over_list_subtask_1(some_list):
    return [item + position for item, position in enumerate(some_list)]



# SUBTASK 2
# and how handle this?
# in such case - method should repeat string index times;
# input -> ['a', 'b', 'c']; output: ['', 'b', 'cc'];
# try:
#     iterate_over_list(['a', 'b', 'c'])
# except ValueError:
#     print('Ups. We have an error here.')

def _get_operation_result(element, element_position):
        return element_position + element if isinstance(element, int) else element * element_position


def iterate_over_list_subtask_2(some_list):
    return [_get_operation_result(item, position) for position, item in enumerate(some_list)]


##############
#   TASK 3   #
##############

# Imagine that you have a database table, defined as follows:
# TABLE poi
#   COLUMN id SERIAL (primary_key)
#   COLUMN name TEXT
#   COLUMN location_city TEXT
#   COLUMN location_country TEXT
#   COLUMN latitude NUMERIC
#   COLUMN longitude NUMERIC

# Write an SQL query which returns the aggregated poi by location_city column;
# We want to know how many poi (Pint of interest is in London)
# So we want to get, something like this:
# city|pois_count
# London|123
# Warsaw|541
# Moscow|32

# counting with nulls at location_city
SELECT location_city AS city, count(*) AS pois_count
FROM poi
GROUP BY location_city;

# SUBTASK 1
# Assume that above query will be done quite frequently, additionally
# there will be also a query which will be filtering (WHERE) on location_city.
# What can we do to improve database performance?

We can use index on the column location_city.
