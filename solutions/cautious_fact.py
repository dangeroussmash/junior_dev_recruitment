##############
#   TASK 1   #
##############
import json
import datetime

class Client():
    def __init__(
        self,
        first_name,
        last_name,
        birth_date,
        sex
        ):
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.sex = sex
    
    def can_watch_pegi(self):
        today = datetime.datetime.today()
        age = datetime.datetime.strptime(self.birth_date,  "%Y-%m-%d")
        age2 = (today.year - age.year - ((today.month, today.day)<(age.month, age.day)))
        if age2 >2 and age2 <7:
            return("Can watch PEGI 3")
        elif age2>6 and age2< 12:
            return("Can watch PEGI 7")
        elif age2>11 and age2<16:
            return("Can watch PEGI 12")
        elif age2 > 15 and age2< 18:
            return ("Can watch PEGI 16")
        elif age2> 17:
            return("Can watch PEGI 18")
        elif age2 <3: 
            return("Can't watch movies :(")
            
        
class Ticket(Client):
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
       return json.dumps({'event_time': self.event_time, 
       'event_name': self.event_name, 
       'room_number': self.room_number, 
       'client':{'birth_date': self.client.birth_date, 
       'first_name': self.client.first_name, 
       'last_name' : self.client.last_name, 
       'sex' : self.client.sex}, 
       'ticket_id' : self.ticket_id, 
       'event_date': self.event_date})
    

# SUBTASK 1
# Define the Client class with attributes:
# first_name, last_name, birth_date, sex

# SUBTASK 2
# define a method on Ticket: get_ticket_data, which returns dumped JSON object
# with all data on ticket, and all data on client;
# EXAMPLE:
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

# SUBTASK 3
# Write a method (name: can_watch_pegi ;)) on client which check if he is able
# to watch the movie - according to PEGI
# (https://pl.wikipedia.org/wiki/Pan_European_Game_Information)
# (yep, I know - PEGI is for games, but who cares) - assume following age
# marks: 3, 7, 12, 16, 18;
# Method should return True or False -> True means that client is older than
# restriction and can watch the movie;

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


##############
#   TASK 2   #
##############

# SUBTASK 1
# do it in pythonic way;
# it just adds the index to the list element on this index
# and return a new list;
# TIP: shorter is better;

def iterate_over_list(some_list):
    i = 0
    new_list = []
    for element in some_list:
        n_element = element * i
        new_list.append(n_element)
        i = i + 1

    return new_list

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

"""SELECT location_city, SUM(name) AS pois_count FROM poi""" 


# SUBTASK 1
# Assume that above query will be done quite frequently, additionally
# there will be also a query which will be filtering (WHERE) on location_city.
# What can we do to improve database performance?
"""
 We should split this one table into multiple tables, I would suggest  two more tables (sum of three)
First one with id and city name, second with id, and locations, third with id and longitude, and latitude
"""
