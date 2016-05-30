import json
from datetime import datetime, date


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
        self.client.ticket_ids.append(ticket_id)

    def get_ticket_data(self):
        serializable_data = {key: val if not isinstance(val, Client)
                           else self.client.serialize_client()
                           for (key, val)in vars(self).iteritems()}
        return json.dumps(serializable_data, indent=4)

    def can_watch_pegi(self, age):
        year = int(datetime.strptime(self.client.birth_date, '%Y-%m-%d').year)
        client_age = date.today().year - year
        return client_age > age


class Client(object):
    ticket_ids = []

    def __init__(self, first_name, last_name, birth_date, sex):
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.sex = sex

    def serialize_client(self):
        return {prop: val for (prop, val) in vars(self).iteritems()}

    def get_ticket_ticket_ids(self):
        return self.ticket_ids


tst = Client('random', 'user', '1985-01-23', 'male')

ticket = Ticket(1, '23-23-95', '18:00', 'concert', tst, 2)
#print ticket.get_ticket_data()
#print ticket.can_watch_pegi(32)
#print tst.get_ticket_ticket_ids()

# TASK 2


def iterate_over_list(some_list):
    try:
        return [x + i for x, i in enumerate(some_list)]
    except TypeError:
        return [x * i for x, i in enumerate(some_list)]

_list = [1, 2, 3]
#print iterate_over_list(_list)
_list2 = ['a', 'b', 'c']
#print iterate_over_list(_list2)

#http://sqlfiddle.com/#!9/458cd4/2
# select location_city as 'City', count(*) as 'Count'
# from poi
# group by location_city

# Nalezy dodac index na kolumnie location_city