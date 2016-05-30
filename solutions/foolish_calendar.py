# -*- coding: utf-8 -*-
from __future__ import print_function
import datetime
import json

##############
#   TASK 1   #
##############


class Ticket(object):
    """Modified class for task."""
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
        self.client.tickets.append(self)

    def get_ticket_data(self):
        return json.dumps(
            self,
            default=lambda obj: obj.__dict__,
            indent=4
        )


class Client(object):
    def __init__(self, first_name, last_name, birth_date, sex):
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.sex = sex
        self.tickets = []

    def can_watch_pegi(self, pegi):
        """Check if client can buy ticket based on PEGI.

        Method is expecting standard birth_date format: YYYY-MM-DD.
        :param pegi: Selected pegi marks: [3, 7, 12, 16, 18]
        :type pegi: int
        :returns: bool / str
        """
        if pegi in [3, 7, 12, 16, 18]:
            today = datetime.date.today()
            try:
                birth_datetime = datetime.datetime.strptime(self.birth_date, '%Y-%m-%d')
            except ValueError:
                return "Wrong birth_date format. Expecting YYYY-MM-DD on input."

            if today.year - birth_datetime.year >= pegi:
                return True
            else:
                return False
        else:
            return "Wrong PEGI mark!"

    def get_all_tickets_by_ids(self):
        """Return all associated tickets ids."""
        return [ticket.ticket_id for ticket in self.tickets]

# Examples:
import random

c = Client("Romuald", "Leon", "1999-06-23", "MALE")
c1 = Client("Romuald", "Leon", "1999-16-23", "MALE")
print(c.can_watch_pegi(2))
print(c.can_watch_pegi(3))
print(c.can_watch_pegi(18))
print(c1.can_watch_pegi(3))


def ticket_fabric():
    for x in range(100):
        Ticket(
            ticket_id=random.randint(10000, 20000),
            client=c,
            event_date='2016-{}-11'.format(
                random.randint(1, 12)
            ),
            event_time='{}:00'.format(
                random.randint(10, 22)
            ),
            event_name='The Killer 2',
            room_number="Sala {}".format(
                random.randint(1, 8)
            )
        )

ticket_fabric()
print(c.get_all_tickets_by_ids())
print(c1.get_all_tickets_by_ids())

##############
#   TASK 2   #
##############


def iterate_over_list(some_list):
    try:
        return [int(element) + index for index, element in enumerate(some_list)]
    except ValueError:
        return [element * index for index, element in enumerate(some_list)]

iterate_over_list([1, 2, 3])
iterate_over_list(['a', 'b', 'c'])


##############
#   TASK 3   #
##############


# COUNT(1) or COUNT(*) has the same performance;
# If we set COUNT(location_city) it will exclude NULL's from counting.
r"""
  SELECT location_city AS city, COUNT(1) pois_count FROM poi GROUP BY location_city;
"""

# To increase performance: simply add INDEX on location_city.
r"""
  CREATE INDEX poi_location_city_idx ON poi (location_city);
"""