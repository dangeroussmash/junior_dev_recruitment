import json
from datetime import date, time


##############
#   TASK 1   #
##############

class Ticket():

    def __init__(
        self,
        ticket_id,    # the unique identifier of the ticket;
        event_date,   # the date of the event;
        event_time,   # the time when event occurs;
        event,        # the INSTANCE of the event
        client,       # the INSTANCE of the client;
        room_number,  # the room number in which event happens;
    ):
        self.ticket_id = ticket_id
        self.event_date = event_date
        self.event_time = event_time
        self.event = event
        self.client = client
        self.room_number = room_number

        self.client.ticket_ids.append(self.ticket_id)

    def get_ticket_data(self):
        return json.dumps(self, indent=4, cls=CustomJSONEncoder)


class Event():

    def __init__(self, event_name, pegi):
        self.event_name = event_name
        # if wrong pegi is given set default(highest)
        self.pegi = pegi if pegi in [3, 7, 12, 16, 18] else 18


class Client():

    def __init__(self, first_name, last_name, birth_date, sex):
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.sex = sex
        self.ticket_ids = []

    def calculate_age(self):
        today = date.today()
        return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))

    def can_watch_pegi(self, event):
        return True if event.pegi <= self.calculate_age() else False


class CustomJSONEncoder(json.JSONEncoder):

    def default(self, obj):
        if (isinstance(obj, date) or isinstance(obj, time)):
            return obj.isoformat()
        elif (isinstance(obj, Ticket) or isinstance(obj, Client) or
              isinstance(obj, Event)):
            return obj.__dict__
        else:
            return super(DateTimeEncoder, self).default(obj)


##############
#   TASK 2   #
##############

# [1, 2, 3, 4, 'a', 'b'] -> [0, 2, 6, 12, 'aaaa', 'bbbbb']
def iterate_over_list(some_list):
    try:
        return [int(element) + i for i, element in enumerate(some_list)]
    except ValueError:
        return [element * i for i, element in enumerate(some_list)]


# [1, 2, 3, 4, 'a', 'b'] -> [1, 3, 5, 7, 'aaaa', 'bbbbb']
def alternative_iterate_over_list(some_list):
    return [element + i if isinstance(element, int) else
            element * i for i, element in enumerate(some_list)]


##############
#   TASK 3   #
##############

sql = """SELECT location_city as city, COUNT(location_city) as pois_count
         FROM poi
         GROUP BY location_city"""

# To improve performance you can create indexes on used columns from poi table


##############
#   TESTS    #
##############

if(__name__ == '__main__'):

    # Task 1
    client_01 = Client("Piotr", "Kowalski", date(2000, 10, 12), "MALE")
    movie_01 = Event("The Lion King", 7)
    movie_02 = Event("Saw", 18)
    ticket_01 = Ticket(98778, date(2016, 6, 2), time(15, 30),
                       movie_01, client_01, 15)
    ticket_02 = Ticket(98780, date(2016, 6, 15), time(21, 30),
                       movie_02, client_01, 20)

    print(ticket_01.get_ticket_data())
    print(client_01.can_watch_pegi(movie_01))
    print(client_01.can_watch_pegi(movie_02))
    print(client_01.ticket_ids)
    print()

    # Task2
    print(iterate_over_list([1, 2, 3, 4, 5]))
    print(alternative_iterate_over_list([1, 2, 3, 4, 5]))
    print(iterate_over_list(['a', 'b', 'c', 'd', 'e']))
    print(alternative_iterate_over_list(['a', 'b', 'c', 'd', 'e']))
    print(iterate_over_list([1, 2, 3, 4, 'a', 'b']))
    print(alternative_iterate_over_list([1, 2, 3, 4, 'a', 'b']))
