from datetime import datetime
import json
from operator import itemgetter
import unittest
from enthusiastic_stretch import *


class TestClient(unittest.TestCase):

    def test_ticket_data_storing(self):
        client = Client('Paweł', 'Gaweł', '1994-03-11', 'M')
        ticket1 = Ticket('8', '2016-06-21', '19:00', 'Example event', client, '1')
        ticket2 = Ticket('2', '2016-02-05', '22:00', 'Aexample event', client, '6')
        ticket3 = Ticket('4', '2016-08-05', '11:00', 'Rexample event', client, '5')
        ticket4 = Ticket('12', '2016-08-04', '22:04', 'Fexample', client, '12')

        self.assertEqual(['2', '4', '8', '12'], client.by_ticket_id())

        self.assertEqual(['2', '8', '12', '4'], client.by_event_date())

        self.assertEqual(['4', '8', '2', '12'], client.by_event_time())

        self.assertEqual(['2', '8', '12', '4'], client.by_event_name())

        self.assertEqual(['8', '4', '2', '12'], client.by_room_number())


if __name__ == '__main__':
    unittest.main()