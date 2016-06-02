# -*- coding: utf-8 -*-
import datetime
from dateutil.relativedelta import relativedelta
import json
import re
import weakref


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
        self.ticket_id = ticket_id
        self.event_date = event_date
        self.event_time = event_time
        self.event_name = event_name
        self.client = client
        self.room_number = room_number

        client.tickets.add(self)

# SUBTASK 2
# define a method on Ticket: get_ticket_data, which returns dumped JSON object
# with all data on ticket, and all data on client;
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
    def get_ticket_data(self):
        return json.dumps({
            "ticket_id": self.ticket_id,
            "event_date": self.event_date,
            "event_time": self.event_time,
            "event_name": self.event_name,
            "client": self.client.json(),
            "room_number": self.room_number
            },
            indent=4)


class PegiError(Exception):
    pass


# SUBTASK 1
# Define the Client class with attributes:
# first_name, last_name, birth_date, sex

class Client(object):
    def __init__(self, first_name, last_name, birth_date, sex):
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.sex = sex
        self.tickets = weakref.WeakSet()

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
    @property
    def tickets_ids(self):
        return [t.ticket_id for t in self.tickets]

# SUBTASK 3
# Write a method (name: can_watch_pegi ;)) on client which check if he is able
# to watch the movie - according to PEGI
# (https://pl.wikipedia.org/wiki/Pan_European_Game_Information)
# (yep, I know - PEGI is for games, but who cares) - assume following age
# marks: 3, 7, 12, 16, 18;
# Method should return True or False -> True means that client is older than
# restriction and can watch the movie;
    def can_watch_pegi(self, pegi):
        valid_pegi = [3, 7, 12, 16, 18]
        if pegi not in valid_pegi:
            raise PegiError(
                "Wrong PEGI value, PEGI should be in {}".format(valid_pegi))
        birth_year = int(re.search(r'\d{4}', self.birth_date).group())
        return datetime.date.today().year - pegi >= birth_year

    def json(self):
        return {"first_name": self.first_name,
                "last_name": self.last_name,
                "birth_date": self.birth_date,
                "sex": self.sex}


##############
#   TASK 2   #
##############

# SUBTASK 1
# do it in pythonic way;
# it just adds the index to the list element on this index
# and return a new list;
# TIP: shorter is better;

def iterate_over_list(some_list):
    """
    Multiply list item by factor of index.
    can mix numbers and letters in one sequence
    """
    return [int(elem) + factor if elem.isdigit() else factor * elem
            for factor, elem in enumerate(some_list)]

# SUBTASK 2
# and how handle this?
# in such case - method should repeat string index times;
# input -> ['a', 'b', 'c']; output: ['', 'b', 'cc'];
try:
    iterate_over_list(['a', 'b', 'c'])
except ValueError:
    print('Ups. We have an error here.')

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

#SELECT location_city AS city, COUNT(*) AS pois_count FROM poi GROUP BY location_city;


# SUBTASK 1
# Assume that above query will be done quite frequently, additionally
# there will be also a query which will be filtering (WHERE) on location_city.
# What can we do to improve database performance?

# We should create index on locatio_city column:
# CREATE INDEX location_city_index ON poi(location_city);


if __name__ == "__main__":
    # simple test
    c1 = Client("Adam", "Kowalski", "1999-10-12", "MALE")
    c2 = Client("Anna", "Kowalska", "06-13-1989", "FEMALE")

    tickets = []
    for i in range(6):
        tickets.append(
            Ticket(str(2*i), "2014-12-12", "20:30", "c1 Event", c1, "Sala 7"))
        tickets.append(
            Ticket(str(2*i+1), "2014-11-12", "20:30", "c2 Event", c2, "Sala 7"))

    assert not c1.can_watch_pegi(18)
    assert c2.can_watch_pegi(16)
    try:
        c1.can_watch_pegi(1)
        assert False, "invalid pegi test failed"
    except PegiError:
        pass

    data = {
        "event_time": "20:30",
        "event_name": "c1 Event",
        "room_number": "Sala 7",
        "client":
            {
                "birth_date": "1999-10-12",
                "first_name": "Adam",
                "last_name": "Kowalski",
                "sex": "MALE"
            },
        "ticket_id": "0",
        "event_date": "2014-12-12"
    }
    assert tickets[0].get_ticket_data() == json.dumps(data, indent=4)

    assert set(c1.tickets_ids) == {"0", "2", "4", "6", "8", "10"}

    # an event was cancelled or something
    del tickets[0]
    assert set(c1.tickets_ids) == {"2", "4", "6", "8", "10"}

    # --------------------------------------------
    assert iterate_over_list(['1', '2', '3']) == [1, 3, 5]
    assert iterate_over_list(['a', 'b', 'c']) == ['', 'b', 'cc']
    assert iterate_over_list(['1', 'a', '2', 'b']) == [1, 'a', 4, 'bbb']
