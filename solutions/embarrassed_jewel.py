##############
#   TASK 1   #
##############

import json
import datetime
from weakref import WeakSet


class WrongPegiNumber(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


def _parser(x):
    if isinstance(x, datetime.date):
        return str(x)
    if isinstance(x, set):
        return None
    return x.__dict__


class Ticket(object):
    # 2. WeakSet for all Ticket instances
    _instances = WeakSet()

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
        # 1. We can collect all ticket ids in set in Client instance
        self.client.tickets.add(ticket_id)
        # 2. or just keep all ticket instances in one static WeakSet
        Ticket._instances.add(self)

    def get_ticket_data(self):
        return json.dumps(self, default=_parser, indent=4)

    @classmethod
    def get_all_instances(cls):
        return list(Ticket._instances)


class Client(object):
    def __init__(self, first_name, last_name, birth_date, sex):
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.sex = sex
        # 1. set for all ticket ids for Client instance
        self.tickets = set()

    def can_watch_pegi(self, pegi):
        PEGI = [3, 7, 12, 16, 18]
        if pegi in PEGI:
            days = (datetime.date.today() - self.birth_date).days
            return (days / 365.25) >= pegi
        raise WrongPegiNumber

    # 1 possibility
    def get_tickets_ids(self):
        return list(self.tickets)

    # 2 possibility
    def get_tickets_ids_sec(self):
        result = list()
        for ticket in Ticket.get_all_instances():
            if ticket.client is self:
                result.append(ticket.ticket_id)
        return result


##############
#   TASK 2   #
##############

def iterate_over_list(some_list):
    return [j * i if isinstance(j, str) else i + int(j)
            for i, j in enumerate(some_list)]


##############
#   TASK 3   #
##############

"""
If we want to increase perfomance:
    we can add index on location_city
    we should use firstly 'where' statement then aggregate functions
    we should use count(1) instead of count(*)
    we can also create view or procedure if specific queries are often used
"""

"""
create index on poi(location_city);

select location_city, count(1) as pois_count from poi
where location_city is not null
group by location_city;
"""


##############
#   TESTS    #
##############

def generate_objects(how):
    import random
    clients = list()
    tickets = list()
    for i in range(how):
        clients.append(Client('test_name_{0}'.format(i),
                              'test_surname_{0}'.format(i),
                              datetime.date(1990 + i, 1 + (i % 12),
                                            1 + (i % 27)),
                              'M' if i % 3 != 0 else 'F'))
        tickets.append(Ticket(i, datetime.date.today(),
                              '17:4{0}'.format(i % 10),
                              'test_event_name_{0}'.format(i),
                              clients[random.randint(0, i)], i * 10))
    return tickets, clients


def test_get_ticket_data(tickets):
    for t in tickets:
        print t.get_ticket_data()
        print '\n==================\n'


def test_pegi(clients):
    import random
    for c in clients:
        pegi = random.randint(2, 20)
        try:
            age = (datetime.date.today() - c.birth_date).days / 365.25
            print '{0}\t{1}\t'.format(age, pegi), c.can_watch_pegi(pegi)
            print '\n==================\n'
        except WrongPegiNumber:
            print 'WRONG PEGI NUMBER!'


def test_get_ticket_ids_first(tickets, clients):
    for t, c in zip(tickets, clients):
        print c.get_tickets_ids()
        print '\n==================\n'


def test_get_ticket_ids_second(tickets, clients):
    for t, c in zip(tickets, clients):
        print c.get_tickets_ids_sec()
        print '\n==================\n'


if __name__ == '__main__':
    tc, cl = generate_objects(26)
    print '\n++++GET_TICKET_DATA TEST++++\n'
    test_get_ticket_data(tc)
    print '\n++++PEGI TEST++++\n'
    test_pegi(cl)
    print '\n++++GET_TICKETS_ID_FIRST TEST++++\n'
    test_get_ticket_ids_first(tc, cl)
    print '\n++++GET_TICKETS_ID_SECOND TEST++++\n'
    test_get_ticket_ids_second(tc, cl)
