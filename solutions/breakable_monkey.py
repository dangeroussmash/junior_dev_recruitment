# -*- coding: utf-8 -*-

### PYTHON 3.4 ###

##############
#   TASK 1   #
##############

import json, datetime, time

def custom_serializer(python_object):
    """Custom serializer for datatypes not supported by JSON"""
    if isinstance(python_object, datetime.datetime):
        return python_object.strftime('%Y-%m-%d')
    elif isinstance(python_object, Client) or isinstance(python_object, Ticket):
        return python_object.__dict__
    raise TypeError


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
        self.birth_date = birth_date    # birthday stored as datetime object
        self.sex = sex                  # 'MALE' | 'FEMALE'
        # store ticket ids for the purpouse of TASK 1 - SUBTASK 4
        self.ticket_ids = []

    def can_watch_pegi(self, restricted_age):
        """Not restricting input to 3, 7, 12, 16, 18 so in case those values changes the function will still work"""
        today = datetime.datetime.today()
        try:
            past = today.replace(year=today.year - int(restricted_age))
        except ValueError:
            # in case we are changing years for a date like "2016-02-29"
            past = today.replace(year=today.year - int(restricted_age), day=today.day - 1)
        except TypeError:
            raise ValueError("Restricted Age variable must be an integer.")
        # if it's your birthday you still need to wait 1 day
        return past > self.birth_date


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

        # Send Ticket ID to Client object - the simplest solutions are the best, right?
        client.ticket_ids.append(self.ticket_id)
    
    def get_ticket_data(self):
        return json.dumps(self, default=custom_serializer)


##############
#   TASK 2   #
##############

def iterate_over_list(some_list):
    # Since description didn't require this, I skipped the case when given list is a mix of letters and numbers ie. [1, 'b', 3]
    try:
        return [int(element) + index for index, element in enumerate(some_list)]
    except ValueError:
        return [element * index for index, element in enumerate(some_list)]

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

sql = "SELECT location_city as city, COUNT(location_city) as poi_count FROM poi GROUP BY location_city"

# SUBTASK 1
# Assume that above query will be done quite frequently, additionally
# there will be also a query which will be filtering (WHERE) on location_city.
# What can we do to improve database performance?

"""

* We should add index(es) for poi table for columns that are most used.

* If above isn't enough, we can add backend cache layer like Redis to boost performance

"""

