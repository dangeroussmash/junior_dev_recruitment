# -*- coding: utf-8 -*-
import json
from datetime import date


##############
#   TASK 1   #
##############

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

        self.client.tickets.append(self)

    #  ModelSerializer would suit here better
    def get_ticket_data(self):
        ticket_data = self.__dict__
        ticket_data['client'] = self.client.as_dict()
        return json.dumps(ticket_data, indent=4)


class Client(object):
    def __init__(self, first_name, last_name, birth_date, sex):
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.sex = sex

        self.tickets = []

    def can_watch_pegi(self, age_mark):
        age = self.calculate_age()
        pegi_marks = [3, 7, 12, 16, 18]

        if age_mark not in pegi_marks:
            return 'This age mark is not correct PEGI mark'

        return age >= age_mark

    def calculate_age(self):
        today = date.today()
        age = (
            today.year - self.birth_date.year -
            ((today.month, today.day) < (
            self.birth_date.month, self.birth_date.day))
        )
        return age

    def get_ticket_ids(self):
        ids = [ticket.id for ticket in self.tickets]
        return ids

    def as_dict(self):
        return {
            'birth_date': self.birth_date,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'sex': self.sex
        }


##############
#   TASK 2   #
##############

def iterate_over_list(some_list):
    try:
        return [index + int(element) for index, element in enumerate(some_list)]
    except ValueError:
        return [index * element for index, element in enumerate(some_list)]


##############
#   TASK 3   #
##############

#  SELECT location_city AS city, count(1) AS pois_count FROM poi WHERE location_city IS NOT NULL GROUP BY location_city

#  SUBTASK 1
#  CREATE INDEX poi_location_city_idx ON poi (location_city)