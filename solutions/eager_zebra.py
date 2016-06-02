# -*- coding: utf-8 -*-

import unittest
from datetime import date, datetime
from dateutil import relativedelta
import json
import re
dates_difference = relativedelta.relativedelta

##############
#   TASK 1   #
##############


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
        assert ticket_id.isnumeric()  # check if contains only numbers
        self.ticket_id = ticket_id
        assert re.match(r'(\d){4}-[0-1][0-9]-[0-3][0-9]', event_date)
        self.event_date = event_date
        assert isinstance(event_time, str)
        self.event_time = event_time
        assert isinstance(event_name, str)
        self.event_name = event_name
        assert isinstance(client, Client)
        self.client = client
        assert room_number.isnumeric()
        self.room_number = room_number

        self.client.add_ticket(self.ticket_id)

    def get_ticket_data(self, *, json_format=True):
        data = {
            "event_time":  self.event_time,
            "event_name":  self.event_name,
            "room_number": self.room_number,
            "ticket_id":   self.ticket_id,
            "event_date":  self.event_date,
            "client":      self.client.get_client_data(json_format=False)
        }
        return json.dumps(data) if json_format else data


class Client(object):
    def __init__(self, first_name, last_name, birth_date, sex):
        assert first_name.isalpha()  # check if contains only letters
        self.first_name = first_name
        assert last_name.isalpha()
        self.last_name = last_name
        assert re.match(r'(\d){4}-[0-1][0-9]-[0-3][0-9]', birth_date)
        self.birth_date = birth_date
        assert sex in ['male', 'female']
        self.sex = sex

        # thanks to that it is a set tickets will be kept unique and sorted
        self.bought_tickets = set()

    def get_client_data(self, *, json_format=True):
        data = {
            'first_name': self.first_name,
            'last_name':  self.last_name,
            'birth_date': self.birth_date,
            'sex':        self.sex
        }
        return json.dumps(data) if json_format else data

    def add_ticket(self, ticket_id):
        assert ticket_id.isnumeric()
        self.bought_tickets.add(ticket_id)

    def get_ticket_ids(self):
        return self.bought_tickets

    def get_age(self):
        birth_date = datetime.strptime(self.birth_date, '%Y-%m-%d')
        return dates_difference(date.today(), birth_date)

    def can_watch_pegi(self, mark):
        assert mark in [3, 7, 12, 16, 18]  # assert the argument is a PEGI mark
        return self.get_age().years >= mark

# SUBTASK 1
# Define the Client class with attributes:
# first_name, last_name, birth_date, sex

# SUBTASK 2
# define a method on Ticket: get_ticket_data, which returns dumped JSON object
# with all data on ticket, and all data on client;


# SUBTASK 3
# Write a method (name: can_watch_pegi ;)) on client which check if he is able
# to watch the movie - according to PEGI
# assume following age marks: 3, 7, 12, 16, 18;
# Method should return True or False -> True means that client is older than
# restriction and can watch the movie;


# SUBTASK 4
# Propose a structure where client instance will have some interface to get
# all ticket ids - whenever added, which returns all ticket ids;


class Task1Tests(unittest.TestCase):
    def test_ticket_data_storing(self):
        client = Client('fname', 'lname', '1994-03-11', 'male')
        Ticket('12345678', '2016-06-05', '19:00', 'example event', client, '6')
        Ticket('87654313', '2016-06-05', '19:00', 'example event', client, '6')
        Ticket('12343141', '2016-06-05', '19:00', 'example event', client, '6')

        self.assertEqual({'12345678', '87654313', '12343141'},
                         client.get_ticket_ids())

    def test_pegi_marks(self):
        client = Client('fname', 'lname', '2003-03-01', 'female')
        self.assertTrue(client.can_watch_pegi(3))
        self.assertTrue(client.can_watch_pegi(12))
        self.assertFalse(client.can_watch_pegi(16))
        self.assertFalse(client.can_watch_pegi(18))

    def test_json_serializing(self):
        client = Client('fname', 'lname', '1985-11-05', 'male')
        ticket = Ticket('7821471', '2016-08-31', "12:00",
                        'example event', client, '3')

        serialized_data = ticket.get_ticket_data()
        valid_data = [
            '"event_name": "{}"'.format(ticket.event_name),
            '"last_name": "{}"'.format(client.last_name)
        ]
        invalid_data = [
            '"tic_id": "{}"'.format(ticket.ticket_id),
            '"sex": "{}"'.format(client.first_name)
        ]

        for item in valid_data:
            self.assertTrue(item in serialized_data)

        for item in invalid_data:
            self.assertTrue(item not in serialized_data)

    def test_date_validation(self):
        with self.assertRaises(AssertionError):
            client = Client('f', 'l', '1961-03-15', 'female')
            Ticket('1', '2016-99-11', '12:00', 'event', client, '15')
        with self.assertRaises(AssertionError):
            Client('f', 'l', '966-03-15', 'male')

    def test_data_validation(self):
        with self.assertRaises(AssertionError):
            Client('34343', 'fname', '1961-03-15', 'female')
        with self.assertRaises(AssertionError):
            Client('f', 'l', '1961-03-15', 'cat')
        client = Client('f', 'l', '1961-03-15', 'female')
        with self.assertRaises(AssertionError):
            Ticket('id', '2016-08-01', '5 pm', 'event', client, '5')
        with self.assertRaises(AssertionError):
            Ticket('56464', '2016-08-01', '5 pm', 'event', object(), '5')


##############
#   TASK 2   #
##############

# SUBTASK 1
# do it in pythonic way;
# it just adds the index to the list element on this index
# and returns a new list;
# TIP: shorter is better;

def iterate_over_list(some_list):
    if any(type(s) == str for s in some_list):
        return [x * index for x, index in enumerate(some_list)]
    else:
        return [x + index for x, index in enumerate(some_list)]

# SUBTASK 2
# and how handle this?
# in such case - method should repeat string index times;
# input -> ['a', 'b', 'c']; output: ['', 'b', 'cc'];


class Task2Tests(unittest.TestCase):
    def test_integers(self):
        self.assertEqual(iterate_over_list([5, 8, 4]), [5, 9, 6])

    def test_strings(self):
        self.assertEqual(iterate_over_list(['a', 'b', 'c']), ['', 'b', 'cc'])

    def test_invalid_input(self):
        with self.assertRaises(TypeError):
            iterate_over_list([ [], (), {} ])


##############
#   TASK 3   #
##############

r"SELECT location_city, COUNT(1) FROM poi GROUP BY location_city"

# SUBTASK 1

# According to W3S we can create index on column location_city
# W3S: "Indexes allow the database application to find data fast;
#       without reading the whole table."


#######################

if __name__ == '__main__':
    unittest.main()
