from datetime import datetime
from json import dumps


##############
#   TASK 1   #
##############

#    SUBTASK 1
#
#    I assume that all data validation will be done on client site. Main
#    reason for this is lower server load.
#
#    SUBTASK 2
#
#    I assume that get_ticket_method return all data - including all_tickets
#    dictionary. Of course below method can be customize according to
#    requirements.
#
#    SUBTASK 3
#
#    I decided not to check pegi restriction. It keeps the method clean and
#    make it more elastic. Such a validation schould be done on fron-end site
#
#    SUBTASK 4
#
#    I decided to use decorators just for recruitment purpose. The simplest
#    method to provide client with appropriate interface is manual modification
#    of both classes. (We need to create dictionary in Client class and method
#    responsible for collecting ticket in the constructor of Client class


class Decorator_AddTicketToDictionaryInClientInstance:
    """ Add ticket_id value to dictionary in client instance """

    def __init__(self, Ticket):          
        self.Ticket = Ticket

    def __call__(self, *args, **kwargs): # On instance creation
        self.wrapped = self.Ticket(*args, **kwargs)
        self.wrapped.client.all_tickets.append(self.wrapped.ticket_id)
        return self.wrapped


class Decorator_AddDictionaryToEachInstance:
    """ Add dictionary '_all_tickets' to each client instance."""
    def __init__(self, Client):       
        self.Client = Client

    def __call__(self, *args, **kwargs): # On instance creation
        self.wrapped = self.Client(*args, **kwargs)
        self.wrapped.__dict__['all_tickets'] = []
        return self.wrapped


@Decorator_AddTicketToDictionaryInClientInstance
class Ticket(object):
    """ Class represent a single ticket object. Front-end is responsible for
    all data validation. Following data format are required:

    ticket_id:  int
    event_date: str 'YYYY-MM-DD'
    event_time: str 'HH-MM'
    event_name: str
    client: Client class instance
    room_number: str

    """
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
        """  Method is responsible for creating json object.

        :return: Json object
        """
        tmp_json = {}

        return dumps(
            self,
            default=lambda obj: obj.__dict__,
            indent=4
            )


@Decorator_AddDictionaryToEachInstance
class Client(object):
    """ Class represent a single Client object. Front-end is responsible for
    all data validation. Following data format are required:

    first_name: str
    last_name: str
    birth_date: 'YYYY-MM-DD'
    sex: str 'MALE' | 'FEMALE;

    """
    def __init__(
        self,         
        first_name,   # the first name of the client
        last_name,    # the last name of the client
        birth_date,   # the date whene the client born
        sex,          # the gender
    ):
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.sex = sex

    def can_watch_pegi(self, pegi, event_date):
        """ Method is responsible for client's age validation base on pegi
        restriction. Client must fulfill restriction before event date.

        Args:
            pegi: data validation on front-end site
            event_date: str 'YYYY-MM-DD'

        Return:
            True if client is old enough, else False
        """

        try:
            datetime.strptime(event_date, '%Y-%m-%d')   # check date format
        except ValueError:
            raise ValueError("Please use allowed data format: str 'YYYY-MM-DD'")
        else:
            min_born_year = int(event_date[:4]) - pegi
            min_born_date = str(min_born_year) + event_date[4:]
            return True if self.birth_date <= min_born_date else False

"""
# Simple tests

c1 = Client("Adam", "Kowalski", "2000-06-02", "MALE")
c2 = Client("Anna", "Zawadzka", "2000-06-01", "FEMALE")
c3 = Client("Dariusz", "Mielczyk", "2000-05-31", "MALE")
t1 = Ticket(1100000, "2016-07-03", "20:00", "Komapania braci", c1, "Sala 5")
t2 = Ticket(1100001, "2016-08-02", "16:30", "Szeregowiec Ryan", c1, "Sala 2")
t3 = Ticket(1111110, "2016-09-30", "21:00", "Zielona mila", c2, "Sala 10")

print(c1.all_tickets)
print(c2.all_tickets)
print(c3.all_tickets)
print(t1.get_ticket_data())
print(t2.get_ticket_data())
print(t3.get_ticket_data())
"""

##############
#   TASK 2   #
##############

# SUBTASK 1

def iterate_over_list(some_list):
    return [element + index for element, index in enumerate(some_list)]


# SUBTASK 2

def improved_iterate_over_list(some_list):
    return [(index + element
            if isinstance(element, int)
            else index * element)
            for index, element in enumerate(some_list)]

"""
# simple tests

L1 = [1, 2.9, 3, 4, 5]
L2 = ['a', 'b', 'c', 'd', 'e']
L3 = [1, 2, 3, 4, 5, 'a', 'b', 'c', 'd', 'e']
L4 = {1: 'a', 2: 'b'}

print(iterate_over_list(L1))
print(improved_iterate_over_list(L1))
print(improved_iterate_over_list(L2))
print(improved_iterate_over_list(L3))
print(improved_iterate_over_list(L4))
"""


##############
#   TASK 3   #
##############

# TABLE poi
#    COLUMN id SERIAL (primary_key)
#    COLUMN name TEXT
#    COLUMN location_city TEXT
#    COLUMN location_country TEXT
#    COLUMN latitude NUMERIC
#    COLUMN longitude NUMERIC
#
#    SELECT location_citym as city, count(*) as pois_count
#    FROM poi
#    GROUP BY location_city;
#
# SUBTASK 1
#
# 1. Create index on location_city column: 
#
#    CREATE INDEX poi_location_city_idndex
#    ON poi (location_city);

# 2. Create view or procedure (to save time for execution plan preparation)
#    Look at your execution plan. Check scan type. If not only index_scan
#    appears try this:
#
#    SET enable_seqscan = false;
#    SET enable_bitmapscan = false;
#
#    Check it again. Sometimes is is worth experimenting.
# 2. Use some cache software (redis, memcached) - first one is recommended
# 3. If your data set or load is huge you can consider some clustering and load
#    balancing tech.





