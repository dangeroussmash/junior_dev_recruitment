# -*- coding: utf-8 -*-
# Hello! Good luck!
import json
import datetime
import time

print("""
##############
 # TASK 1  #
##############
""")
class Ticket(object):
	def __init__(
			self,
			ticket_id,
			event_date,
			event_time,
			event_name,
			client,
			room_number,
	):
		self.ticket_id = ticket_id
		self.event_date = event_date
		self.event_time = event_time
		self.event_name = event_name
		self.client = client
		self.room_number = room_number
		client.list_of_ids.append(ticket_id)

	def get_ticket_data(self):
		temp_dict = self.__dict__
		temp_dict['client'] = self.client.get_client_data()
		return json.dumps(temp_dict, indent=4)

class Client(object):

	def __init__(self, first_name, last_name, birth_date, sex):
		self.first_name = first_name
		self.last_name = last_name
		self.birth_date = birth_date
		self.sex = sex

		if any(char.isdigit() for char in first_name) or \
			any(char.isdigit() for char in last_name):
			raise TypeError("I believe your name shouldn't contain a number.")
		
		if isinstance(birth_date, str):
			try:
				time.strptime(birth_date, "%Y-%m-%d")
			except ValueError:
				raise TypeError("Your birth date format should be Y-M-D")

		self.list_of_ids = []

	def get_client_data(self):
		return {
			'first_name': self.first_name,
			'last_name': self.last_name,
			'birth_date': self.birth_date,
			'sex': self.sex,
		}

	def can_watch_pegi(self, restriction):
		now = str(datetime.date.today())
		now = [int(n) for n in now.split('-')]
		birth = str(self.birth_date)
		birth = [int(n) for n in birth.split('-')]
		age = (now[0] - birth[0] - ((birth[1], birth[2]) < (now[1], now[2])))
		age_marks = [3, 7, 12, 16, 18]
		
		if restriction not in age_marks:
			return """Given PEGI is incorrect. Available values are: 
					3, 7, 12, 16, 18"""

		return age >= restriction

	def get_ticket_ids(self, chosen_id=None):
		if chosen_id in self.list_of_ids:
			for bilet in bilety:
				return ("Info about ticket no.{}:".format(chosen_id)+
				"{a}, {b}, {c}".format(a=bilet.event_name,
										b=bilet.event_date,
										c=bilet.event_name,))

		return self.list_of_ids



klient = Client("Romuald", "Lechon", "2003-01-23", "MALE")
bilety = [
	Ticket("12345", "2015-09-10", "20:00", "The Killer", klient, "Sala 7"),
	Ticket("1495", "2015-09-10", "20:00", "The Killer", klient, "Sala 7"),
	Ticket("1245", "2015-09-10", "20:00", "The Killer", klient, "Sala 7"),
	Ticket("1892", "2015-09-10", "20:00", "The Killer", klient, "Sala 7"),
	Ticket("1445", "2015-09-10", "20:00", "The Killer", klient, "Sala 7"),
	]

print (bilety[0].get_ticket_data()) # SUBTASK 2
print (klient.can_watch_pegi(3)) # SUBTASK 3
print (klient.get_ticket_ids()) # SUBTASK 4 -> return all client tickets
print (klient.get_ticket_ids("1445")) # SUBTASK 4 -> return info about ticket

##############
#///TASK 1///#
##############

print("""
##############
 # TASK 2  #
##############
""")

def iterate_over_list(some_list):

	if all(type(n) is str for n in some_list):
		return [i*n for i,n in enumerate(some_list)]
	
	if (all(type(n) is int for n in some_list)) \
		or (all(type(n) is float for n in some_list)):
		return [i+n for i,n in enumerate(some_list)]
	
	raise ValueError

try:
	print (iterate_over_list([0,1,2,3]))
	print (iterate_over_list([0.7, 1.5, 2.4, 3.4]))
	print (iterate_over_list(['a','b','c','d']))
	print (iterate_over_list(['a','b','c','d',1]))
except ValueError:
	print ('Ups. We have an error here.')

##############
#///TASK 2///#
##############

##############
 # TASK 3  #
##############

# SELECT location_city AS city,COUNT(1) AS pois_count 
# FROM poi 
# GROUP BY location_city;

# If we want specifically number of pois for London the query is like:
# SELECT COUNT(*) 
# FROM poi WHERE location_city='London';

# To increase performance we create index, users can't see them and 
# this allows searching data more quickly:
# CREATE INDEX index ON poi(location_city);

##############
#///TASK 3///#
##############
