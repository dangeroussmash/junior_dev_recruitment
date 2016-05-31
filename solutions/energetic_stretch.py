# -*- coding: utf-8 -*-
# Hello! Good luck!

##############
#   TASK 1   #
##############
import json
import datetime


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

    def get_ticket_data(self):
        json.dumps(
            {
                'ticket_id': self.ticket_id,
                'event_date': self.event_date,
                'event_time': self.event_time,
                'event_name': self.event_name,
                'client': {
                    'first_name': self.client.first_name,
                    'last_name': self.client.last_name,
                    'birth_date': self.client.birth_date,
                    'sex': self.client.sex,
                },
                'room_number': self.room_number
            },
            indent=4,
            separators=',',
        )


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
        self.birth_date = birth_date
        self.sex = sex

    def get_age(self):
        today = datetime.date.today()
        birth = datetime.datetime.strptime(self.birth_date, "%Y-%m-%d")
        return today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))

    def can_watch_pegi(self, rating):
        if rating in [3, 7, 12, 16, 18]:
            if self.get_age() > rating:
                return True
            else:
                return False
        else:
            return "Given rating for PEGI is wrong!"


##############
#   TASK 2   #
##############

# SUBTASK 1
# do it in pythonic way;
# it just adds the index to the list element on this index
# and return a new list;
# TIP: shorter is better;

some_list = ['a', 'b', 'c']
some_list2 = [1, 2, 3, 'a', 'b']


def iterate_over_list(data_list):
    return [x * i for x, i in enumerate(data_list)]

print(iterate_over_list(some_list2))

##############
#   TASK 3   #
##############

# SELECT location_city AS city, count(*) AS pois_count FROM poi GROUP BY location_city;

# To improve performance we can create an index on location_city like:

# CREATE INDEX poi_location_city_index ON poi(location_city);
