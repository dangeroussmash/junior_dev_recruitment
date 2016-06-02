##############
#   TASK 1   #
##############

import json
from datetime import datetime


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

    def get_ticket_data(self):
        def date_handler(obj):
            return obj.isoformat() if hasattr(obj, 'isoformat') else obj
        return json.dumps(self.__dict__, default=date_handler, indent=4)


class Client(object):
    def __init__(self, first_name, last_name, birth_date, sex):
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.sex = sex

    def can_watch_pegi(self, mark):
        if mark not in [3, 7, 12, 16, 18]:
            raise Exception("Wrong mark given")
        date_diff = datetime.now().date() - self.birth_date
        age = date_diff.days / 365.25
        return bool(age >= mark)

# SUBTASK 4: The cleanest solution I can think of is to aggregate ticket ids
# within client class attribute (as a set or list defined within client class constructor)
# and add/append to it ticket_id from every Ticket class instance.

##############
#   TASK 2   #
##############


# try/except would be cleaner, that one is shorter and faster in most cases
def iterate_over_list(some_list):
    return [(idx*el if isinstance(el, str) else idx+int(el))
            for idx, el in enumerate(some_list)]

##############
#   TASK 3   #
##############

query = "SELECT location_city, COUNT(1) total FROM poi GROUP BY location_city;"

# as in documentation: https://wiki.postgresql.org/wiki/Slow_Counting
improvement = "CREATE INDEX poi_location_city_index ON poi (location_city);"
