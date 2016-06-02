from datetime import datetime
import json
from operator import itemgetter
import time


# TASK 1
class Ticket(object):
    def __init__(
            self,
            ticket_id,  # the unique identifier of the ticket;
            event_date,  # the date of the event;
            event_time,  # the time when event occurs;
            event_name,  # the event name -> obvious one :);
            client,  # the INSTANCE of the client;
            room_number,  # the room number in which event happens;
    ):
        self.ticket_id = ticket_id
        self.event_date = event_date
        self.event_time = event_time
        self.event_name = event_name
        self.client = client
        self.room_number = room_number
        self.whole = {'ticket_id': int(ticket_id),    # dictionary which contains every ticket's attribute
                      # ticket_id and room_number changes from str to int to make sorting easier
                      'event_name': event_name,
                      'event_time': event_time,
                      'event_date': event_date,
                      'room_number': int(room_number)}
        self.client.tickets.append(self.whole)  # automatically adds every created ticket to its clients tickets list

# SUBTASK 2
    def get_ticket_data(self):
        return json.dumps(
            self,
            default=lambda my_object: my_object.__dict__,
            indent=4,
            separators=(',', ': '),
        )


# SUBTASK 1
class Client(object):
    def __init__(
            self,
            first_name,  # client's first name
            last_name,   # client's last name
            birth_date,  # the date of clients birth
            sex,  # client's sex
    ):
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.sex = sex
        self.tickets = []  # list which contains info about all clients tickets

# SUBTASK 3
    def can_watch_pegi(self, pegi):
        correct_pegi_list = [3, 7, 12, 16, 18]
        birth_date_as_date = time.strptime(self.birth_date, "%Y-%m-%d")  # reformats birthday string to more explicit
        today = datetime.today()
        if pegi in correct_pegi_list:  # checks if given pegi value is correct
            age = today.year - birth_date_as_date.tm_year - \
                    ((today.month, today.day) < (birth_date_as_date.tm_mon, birth_date_as_date.tm_mday))
            if age == pegi or age > pegi:
                return True
            else:
                return False
        else:
            raise ValueError('Wrong PEGI')

# SUBTASK 4

    def by_ticket_id(self, argument='ticket_id'):
        arguments_list = ['ticket_id', 'event_name', 'event_date', 'event_time', 'room_number']
        if argument in arguments_list:
            sort_list = sorted(self.tickets, key=itemgetter(argument))
            newlist = []
            for i in sort_list:
                newlist.append(str(i.get('ticket_id')))  # output list contains only ticket_id value as string
            return newlist
        else:
            raise ValueError('Key not allowed. Proper keys: %s.' % allowed_keys)

    def by_event_name(self):
        return self.by_ticket_id('event_name')

    def by_event_date(self):
        return self.by_ticket_id('event_date')

    def by_event_time(self):
        return self.by_ticket_id('event_time')

    def by_room_number(self):
        return self.by_ticket_id('room_number')


# TASK 2
    # Function checks whether the element in list is a string (then multiplies it by index value)
    # or int (then adds index value to it). Any other type of element raises ValueError.
def iterate_over_list(some_list):
    new_list = [element + some_list.index(element) if type(element) == int else element * some_list.index(element)
                if type(element) == str else None for element in some_list]
    if None in new_list:
        raise ValueError('Wrong value.')
    return new_list

# TASK 3

"SELECT location_city, COUNT(*) FROM poi GROUP BY location_city"

# SUBTASK 1
# To optimize database performance we should add index to location_city column.
