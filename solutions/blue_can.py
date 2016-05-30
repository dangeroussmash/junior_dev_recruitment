# -*- coding: utf-8 -*-

# Hello! Good luck!

##############
#   TASK 1   #
##############

from datetime import date, datetime
import json


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

        self.client.add_ticket(ticket_id)  # client update

    def get_ticket_data(self):  # Sutask 2 - JSON on data
        return json.dumps(
            {
                "event_time": self.event_time,
                "event_name": self.event_name,
                "room_number": self.room_number,
                "client": self.client.get_client_info(),
                "ticket_id": self.ticket_id,
                "event_date": self.event_date
            },
            indent=4,
            separators=(',', ': '),
        )

    def print_ticket_data(self):
        print(self.get_ticket_data())


class Client(object):  # Subtask 1 - client class
    def __init__(
        self,
        first_name,
        last_name,
        birth_date,
        sex,
     ):
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date  # rrrr-mm-dd format taken from subtask 2 json example
        self.sex = sex
        self.tickets = []

    def add_ticket(self, ticket_id):
        self.tickets.append(ticket_id)

    def get_ticket_ids(self):
        return self.tickets

    def print_tickets(self):  # for debug purpose
        print("Client: " + self.first_name + " " + self.last_name + " has " + str(len(self.tickets)) +
              " tickets:" + str(self.get_ticket_ids()))

    def get_client_info(self):
        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'birth_date': self.birth_date,
            'sex': self.sex,
        }

    def get_current_age(self):
        birth_date = datetime.strptime(self.birth_date, '%Y-%m-%d')
        current_date = datetime.today()
        year_diff = current_date.year - birth_date.year
        if (current_date.month, current_date.day) < (birth_date.month, birth_date.day):  # birthday check
            return year_diff - 1
        else:
            return year_diff - 0

    def can_watch_pegi(self, mark):  # Subtask 3 - pegi method
        if self.get_current_age() >= mark:
            return 1  # old enough to watch
        else:
            return 0  # not old enough to watch


# SUBTASK 4
client1 = Client("Michal", "Nowak", "1994-08-17", "M")
t1 = Ticket('1', "2016-04-05", "16:30", "Star Wars: Director's Cut", client1, 5)
t2 = Ticket('2', "2016-06-20", "14:10", "Rekrutacja nowych pracownikow", client1, 10)
t1.print_ticket_data()  # json example
client1.print_tickets()
# Pegi Test
client2 = Client("Dominika", "Kowalska", "2002-04-16", "F")
print(client2.can_watch_pegi(16))  # c2 is 16, expected false
print(client2.can_watch_pegi(12))  # c2 is 16, expected true
# Tricky birthday date
client3 = Client("Jan", "Jankowski", "2000-12-10", "M")
print(client2.can_watch_pegi(16))  # Expected false because before b-day

##############
#   TASK 2   #
##############

# SUBTASK 1
# do it in pythonic way;
# it just adds the index to the list element on this index
# and return a new list;
# TIP: shorter is better;


def iterate_over_list(some_list):
    i = 0
    new_list = []
    for element in some_list:
        n_element = int(element) + i
        new_list.append(n_element)
        i = i + 1

    return new_list


def iterate_over_list_oneliner(some_list):
    return [i + some_list[i] for i in range(len(some_list))]
# Testing the result:
example_list = [1, 2, 3, 4, 5, 10, 11, 12, 13]
print("TASK 2")
print(iterate_over_list(example_list))
print(iterate_over_list_oneliner(example_list))
# SUBTASK 2
# and how handle this?
# in such case - method should repeat string index times;
# input -> ['a', 'b', 'c']; output: ['', 'b', 'cc'];


def iterate_over_str_list_oneline(some_list):
    return [i * some_list[i] for i in range(len(some_list))]

example_str_list = ['a', 'b', 'c', 'd', 'e', 'f']
try:
    iterate_over_list(example_str_list)
except ValueError:
    print(iterate_over_str_list_oneline(example_str_list))

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

# Query:
# select location_city as city, count(location_city) as pois_count from poi group by location_city;

# SUBTASK 1
# Assume that above query will be done quite frequently, additionally
# there will be also a query which will be filtering (WHERE) on location_city.
# What can we do to improve database performance?

# Nalezy zalozyc index na location_city.
