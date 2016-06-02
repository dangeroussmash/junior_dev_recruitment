from datetime import datetime
import json
import weakref


# TASK 1

class Client(object):
    def __init__(
        self,
        first_name,
        last_name,
        birth_date,  # stored as datetime
        sex          # insist on two possible values
    ):
        if isinstance(birth_date, str):
            # let ValueError to be raised when wrong format
            birth_date = datetime.strptime(birth_date, '%Y-%m-%d')
        if sex not in {'MALE', 'FEMALE'}:
            raise ValueError('Wrong sex argument. Possible values: MALE, FEMALE')

        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.sex = sex
        self.reverse_tickets = weakref.WeakSet()  # prevents cyclic refs

    def get_ticket_ids(self):
        """
        Thanks to WeakSet when Ticket is going out of scope the Client drops
        reference to it automatically.
        """
        return [ticket.ticket_id for ticket in self.reverse_tickets]

    def can_watch_pegi(self, pegi_threshold):
        today = datetime.today()
        pegi_limit_date = today.replace(year=today.year - pegi_threshold)
        return self.birth_date < pegi_limit_date

    def to_representation(self):
        """Use this method to serialize only needed attributes"""
        return dict(
            birth_date=self.birth_date.strftime('%Y-%m-%d'),
            first_name=self.first_name,
            last_name=self.last_name,
            sex=self.sex
        )


class Ticket(object):
    def __init__(
        self,
        ticket_id,  # the unique identifier of the ticket;
        event_date,  # the date of the event;
        event_time,  # the time when event occurs;
        event_name,  # the event name -> obvious one :);
        client,  # the INSTANCE of the client;
        room_number,  # the room number in which event happens;
    ):
        self.ticket_id = ticket_id
        self.event_date = event_date
        self.event_time = event_time
        self.event_name = event_name
        self.client = client
        self.room_number = room_number
        self.client.reverse_tickets.add(self)

    def to_representation(self):
        return dict(
            event_time=self.event_time,
            event_name=self.event_name,
            room_number=self.room_number,
            client=self.client.to_representation(),
            ticket_id=self.ticket_id,
            event_date=self.event_date
        )

    def get_ticket_data(self):
        return json.dumps(self.to_representation())


# TASK 2

def iterate_over_list_task1(some_list):
    return [index + element for index, element in enumerate(some_list)]

# since there was ambiguity on subtask 1 assumed the worst case: mixed types list


def _iterate_over_list_task_2(some_list):
    for index, element in enumerate(some_list):
        if isinstance(element, int):
            yield element + index
        elif isinstance(element, str):
            yield element * index
        else:
            yield element


def iterate_over_list_task2(some_list):
    return [element for element in _iterate_over_list_task_2(some_list)]

# TASK 3

"""
SELECT location_city AS city, COUNT(*) as pois_count
FROM poi
GROUP BY location_city;
"""

"""
First thing when dealing with query performance i would confirm slowness with
profiler, look at query plan and consider possible solutions. In above case it
looks like simple index on location_city is sufficient.
"""


if __name__ == '__main__':
    # since typos can be lurking everywhere simple sanity checks should catch them
    import unittest

    class TestTasks(unittest.TestCase):
        def test_wrong_birth_date(self):
            wrong_date = '01-01-2015'
            err_msg = "time data '{}' does not match format '%Y-%m-%d'".format(wrong_date)
            # it seems that passing 'msg' kwarg to assertRaises is bugged :/
            with self.assertRaises(ValueError) as cm:
                Client('Snake', 'Blue', wrong_date, 'MALE')
            err = cm.exception
            self.assertEqual(str(err), err_msg)

        def test_wrong_sex(self):
            err_msg = 'Wrong sex argument. Possible values: MALE, FEMALE'
            with self.assertRaises(ValueError) as cm:
                Client('Snake', 'Blue', '2016-01-23', 'UNKNOWN')
            err = cm.exception
            self.assertEqual(str(err), err_msg)

        def test_can_watch_pegi(self):
            # test cannot watch
            unmature_client = Client('Dear', 'Dear', '2014-01-01', 'MALE')
            self.assertFalse(unmature_client.can_watch_pegi(3))

            # test for mature client
            mature_client = Client('Dear', 'Dear', '2010-01-01', 'MALE')
            self.assertTrue(mature_client.can_watch_pegi(3))

        def test_get_ticket_data(self):
            client = Client('Dear', 'Dear', '2010-01-01', 'MALE')
            ticket_1 = Ticket(
                1,                # id
                '2016-06-02',     # event_date
                '23:59',          # event_hour
                'Sprzedam opla',  # event_name
                client,           # client
                'Sala 7'          # room number
            )
            ticket_2 = Ticket(
                2,                # id
                '2016-06-02',     # event_date
                '22:59',          # event_hour
                'NopeNope',       # event_name
                client,           # client
                'Sala 7'          # room number
            )

            self.assertEqual(set(client.get_ticket_ids()), {1, 2})

            del ticket_2

            # client should be aware of deletion
            self.assertEqual(set(client.get_ticket_ids()), {1})

        def test_ticket_json_dump(self):
            client = Client('Dear', 'Dear', '2010-01-01', 'MALE')
            ticket_1 = Ticket(
                1,                # id
                '2016-06-02',     # event_date
                '23:59',          # event_hour
                'Sprzedam opla',  # event_name
                client,           # client
                'Sala 7'          # room number
            )

            self.assertEqual(
                json.loads(ticket_1.get_ticket_data()),
                {"event_time": "23:59",
                 "event_name": "Sprzedam opla",
                 "event_date": "2016-06-02",
                 "ticket_id": 1,
                 "room_number": "Sala 7",
                 "client": {
                     "first_name": "Dear",
                     "last_name": "Dear",
                     "sex": "MALE",
                     "birth_date": "2010-01-01"
                 }
                 }
            )

        def test_iterate_over_list(self):
            # subtask 1
            self.assertEqual(iterate_over_list_task1(range(3)), [0, 2, 4])

            # subtask 2
            self.assertEqual(iterate_over_list_task2([1, 'a', 2, 'b']), [1, 'a', 4, 'bbb'])


    unittest.main()
