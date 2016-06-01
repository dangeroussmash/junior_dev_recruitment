import datetime, json, unittest
from breakable_monkey import Client, Ticket, iterate_over_list

# I didn't go deep with tests and I coverd only basic cases
class ClientTest(unittest.TestCase):

    def test_can_watch_pegi(self):
        bday = datetime.datetime(2013, 1, 29)
        client = Client('Carrol', 'Shelby', bday, 'MALE')
        self.assertTrue(client.can_watch_pegi(3))

        bday = datetime.datetime(2009, 5, 30)
        client = Client('Carrol', 'Shelby', bday, 'MALE')
        self.assertTrue(client.can_watch_pegi(7))

        bday = datetime.datetime(2004, 5, 30)
        client = Client('Carrol', 'Shelby', bday, 'MALE')
        self.assertTrue(client.can_watch_pegi(12))

        bday = datetime.datetime(2000, 5, 30)
        client = Client('Carrol', 'Shelby', bday, 'MALE')
        self.assertTrue(client.can_watch_pegi(16))

        bday = datetime.datetime(1998, 5, 31)
        client = Client('Carrol', 'Shelby', bday, 'MALE')
        self.assertTrue(client.can_watch_pegi(18))

    def test_can_watch_pegi_with_string(self):
        bday = datetime.datetime(2009, 5, 30)
        client = Client('Carrol', 'Shelby', bday, 'MALE')
        with self.assertRaises(ValueError):
            client.can_watch_pegi('a')

    def test_ticket_ids(self):
        bday = datetime.datetime(1989, 9, 29)
        client = Client('Carrol', 'Shelby', bday, 'MALE')
        date = datetime.datetime(2016, 6, 1, 23, 59, 59)
        event_date = date.strftime('%Y-%m-%d')
        event_time = date.strftime('%H:%M')
        ticket = Ticket(
            123,
            event_date,
            event_time,
            'ACDC Concert',
            client,
            'First row!'
        )
        ticket = Ticket(
            321,
            event_date,
            event_time,
            'ACDC Concert',
            client,
            'Last row!'
        )

        self.assertListEqual(client.ticket_ids, [123, 321])


class TicketTest(unittest.TestCase):
    
    def test_get_ticket_data_with_valid_input(self):
        bday = datetime.datetime(1989, 9, 29)
        client = Client('Carrol', 'Shelby', bday, 'MALE')

        date = datetime.datetime(2016, 6, 1, 23, 59, 59)
        event_date = date.strftime('%Y-%m-%d')
        event_time = date.strftime('%H:%M')
        ticket = Ticket(
            123,
            event_date,
            event_time,
            'ACDC Concert',
            client,
            'First row!'
        )

        parsed = json.loads(ticket.get_ticket_data())
        expected_parsed_json_output = {
            "event_time": "23:59",
            "event_name": "ACDC Concert",
            "room_number": "First row!",
            "client": 
                {
                    "birth_date": "1989-09-29",
                    "first_name": "Carrol",
                    "last_name": "Shelby",
                    "sex": "MALE",
                    "ticket_ids": [123]
                },
            "ticket_id": 123,
            "event_date": "2016-06-01"
            }
        self.assertDictEqual(parsed, expected_parsed_json_output)

class IterateOverListTest(unittest.TestCase):
    
    def test_iterate_over_list_with_numbers(self):
        a_list = [1, 2, 3]
        self.assertListEqual(iterate_over_list(a_list), [1, 3, 5])

    def test_iterate_over_list_with_letters(self):
        a_list = ['a', 'b', 'c']
        self.assertListEqual(iterate_over_list(a_list), ['', 'b', 'cc'])

    def test_iterate_over_list_with_letters_and_numbers(self):
        a_list = [1, 'b', 3]
        self.assertListEqual(iterate_over_list(a_list), [0, 'b', 6])

        a_list = [1, 'a', 2, 'b', 3, 'c']
        self.assertListEqual(
            iterate_over_list(a_list), 
            [0, 'a', 4, 'bbb', 12, 'ccccc']
        )


if __name__ == '__main__':
    unittest.main()
