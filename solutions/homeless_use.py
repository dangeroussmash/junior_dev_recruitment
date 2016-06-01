# -*- coding: utf-8 -*-
import json
from datetime import datetime


##############
#   TASK 1   #
##############
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
        self.client.tickets.append(self.ticket_id)

    def get_ticket_data(self):
        ticket_data = self.__dict__
        ticket_data['client'] = self.client.__dict__
        return json.dumps(ticket_data)


class Client(object):
    def __init__(self, first_name, last_name, birth_date, sex):
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.sex = sex
        self.tickets = []

    def can_watch_pegi(self, pegi):
        try:
            if pegi in [3, 7, 12, 16, 18]:
                birth_date = datetime.strptime(self.birth_date, '%Y-%m-%d')
                current_date = datetime.today()
                if current_date.year - birth_date.year > pegi:
                    return True
                elif current_date.year - birth_date.year == pegi:
                    if (current_date.month, current_date.day) >= (birth_date.month, birth_date.day):
                        return True
                return False
            else:
                raise TypeError("Wrong pegi. Available pegi marks: 3, 7, 12, 16, 18.")
        except Exception as e:
            print e
            return False

    def get_ticket_ids(self):
        return self.tickets


client1 = Client('Jan', 'Nowak', '1980-03-18', 'MALE')
ticket1 = Ticket(1, '2016-07-10', '19:30', 'Batman', client1, 7)
ticket2 = Ticket(2, '2016-04-18', '17:30', 'Superman', client1, 5)
ticket3 = Ticket(3, '2016-05-14', '16:00', 'Spiderman', client1, 1)
print ticket1.get_ticket_data()
print client1.can_watch_pegi(16)
print client1.get_ticket_ids()


##############
#   TASK 2   #
##############
def iterate_over_list(some_list):
    try:
        return [element + i for i, element in enumerate(some_list)]
    except:
        return [element * i for i, element in enumerate(some_list)]

print iterate_over_list([10, 20, 30, 40, 50, 60])
print iterate_over_list(['a', 'b', 'c', 'd', 'e', 'f'])


##############
#   TASK 3   #
##############
# SELECT location_city AS city, COUNT(*) AS pois_count FROM poi GROUP BY location_city;

# SUBTASK 1:
# Add index on location_city
