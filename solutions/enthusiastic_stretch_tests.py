import json
import unittest
from enthusiastic_stretch import *


class TestClient(unittest.TestCase):

    def test_ticket_interface(self):
        client = Client('Tony', 'Stark', '2000-01-01', 'M')
        ticket1 = Ticket('8', '2016-06-21', '19:00', 'Ex Machina', client, '1')
        ticket2 = Ticket('2', '2016-02-05', '22:00', 'Avatar', client, '6')
        ticket3 = Ticket('4', '2016-08-05', '11:00', 'Rome + Juliet', client, '5')
        ticket4 = Ticket('12', '2016-08-04', '22:04', 'Freddy vs. Jason', client, '12')

        self.assertEqual(['2', '4', '8', '12'], client.by_ticket_id())

        self.assertEqual(['2', '8', '12', '4'], client.by_event_date())

        self.assertEqual(['4', '8', '2', '12'], client.by_event_time())

        self.assertEqual(['2', '8', '12', '4'], client.by_event_name())

        self.assertEqual(['8', '4', '2', '12'], client.by_room_number())


        with self.assertRaises(NameError):
            client.by_ticket_id(wrongvalue)

    def test_can_watch_pegi(self):
        client = Client('Tony', 'Stark', '2000-01-01', 'M')
        self.assertTrue(client.can_watch_pegi(7))
        self.assertFalse(client.can_watch_pegi(18))
        with self.assertRaises(ValueError):
            client.can_watch_pegi(21)


class TestTicket(unittest.TestCase):

    def test_get_ticket_data(self):
        client = Client('Tony', 'Stark', '2000-01-01', 'M')
        ticket = Ticket('8', '2016-06-21', '19:00', 'Ex Machina', client, '1')

        valid_data = json.dumps(
            ticket,
            default=lambda my_object: my_object.__dict__,
            indent=4,
            separators=(',', ': '),
        )

        self.assertEqual(valid_data, ticket.get_ticket_data())


class TestListIteration(unittest.TestCase):

    def test_iterate_over_list(self):
        list1 = [2, 3, 55, 12]
        list2 = ['w', 'r', 'test']
        list3 = [2, 41, 't', 5, 'k']
        list4 = [(2, 12), 2]

        self.assertEqual([2, 4, 57, 15], iterate_over_list(list1))
        self.assertEqual(['', 'r', 'testtest'], iterate_over_list(list2))
        self.assertEqual([2, 42, 'tt', 8, 'kkkk'], iterate_over_list(list3))
        with self.assertRaises(ValueError):
            iterate_over_list(list4)


if __name__ == '__main__':
    unittest.main()
