# -*- coding: utf-8 -*-
from __future__ import print_function
import datetime
import json
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

        client.tickets[self.ticket_id] = self

    def get_ticket_data(self):
        data = vars(self)
        data["client"] = dict(vars(self.client))
        data["client"].pop("tickets")
        return json.dumps(data, indent=4)


class Client(object):
    def __init__(
        self,
        first_name,
        last_name,
        birth_date,
        sex
    ):
        self.first_name = first_name
        self.last_name = last_name
        assert int(birth_date[:4]), "Enter date in format: YYYY-MM-DD"
        self.birth_date = birth_date
        self.sex = sex

        self.tickets = weakref.WeakValueDictionary()

    @property
    def age(self):
        birth_year = int(self.birth_date[:4])
        return datetime.date.today().year - birth_year

    def can_watch_pegi(self, threshold):
        if threshold in {3, 7, 12, 16, 18}:
            return self.age >= threshold
        else:
            return "Invalid PEGI threshold"

    def get_tickets_ids(self):
        return list(self.tickets.keys())


##############
#   TASK 2   #
##############

def iterate_over_list(some_list):
    try:
        return [int(element) + i for i, element in enumerate(some_list)]
    except ValueError:
        return [element * i for i, element in enumerate(some_list)]


try:
    iterate_over_list(['a', 'b', 'c'])
except ValueError:
    print('Ups. We have an error here.')

##############
#   TASK 3   #
##############

query = 'SELECT location_city AS city, COUNT(*) FROM poi GROUP BY location_city;'
# To optimize database performance for reading, we can create index on location_city


def test_task1():
    c1 = Client('Romuald', 'Lechon', '1985-01-23', 'MALE')
    c2 = Client('Romuald', 'Lechon', '2005-01-23', 'MALE')

    t1 = Ticket('12345678', '2016-03-03', '20:00', 'Killer', c1, 'Sala 7')
    t2 = Ticket('12345679', '2016-03-03', '20:00', 'Killer', c1, 'Sala 7')
    test_data = {
        "event_time": "20:00",
        "event_name": "Killer",
        "ticket_id": "12345678",
        "room_number": "Sala 7",
        "client":
            {
                "birth_date": "1985-01-23",
                "sex": "MALE",
                "first_name": "Romuald",
                "last_name": "Lechon"
            },

        "event_date": "2016-03-03"
    }

    assert json.loads(t1.get_ticket_data()) == test_data
    assert set(c1.get_tickets_ids()) == {'12345678', '12345679'}
    del t1
    assert c1.get_tickets_ids() == ['12345679']
    assert c1.can_watch_pegi(18)
    assert not c2.can_watch_pegi(18)


def test_task2():
    assert iterate_over_list(['1', '2', '3']) == [1, 3, 5]
    assert iterate_over_list(['a', 'b', 'c']) == ['', 'b', 'cc']


if __name__ == '__main__':
    test_task1()
    test_task2()
