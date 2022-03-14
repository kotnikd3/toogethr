import unittest
import json

from API import app
from service.BusinessLogic import BusinessLogic


BASE = 'http://localhost:5000'


class TestAPI(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client(self)

    def test_get_reservation_exist_status_code(self):
        response = self.client.get(BASE + '/reservations/1')

        self.assertEqual(response.status_code, 200)

    def test_get_reservation_exist_data(self):
        response = self.client.get(BASE + '/reservations/1').get_json()
        expected_response = ("{'data': {'id': 1, 'datetime_from': 1621497600, "
                             "'datetime_to': 1621508400, 'user_id': 1, "
                             "'parking_spot_id': 1}}")

        self.assertEqual(str(response), expected_response)
    
    def test_get_reservation_does_not_exist_status_code(self):
        response = self.client.get(BASE + '/reservations/66')

        self.assertEqual(response.status_code, 404)

    def test_get_parking_spots_with_reservation_status_code(self):
        response = self.client.get(BASE + '/parkingspots')

        self.assertEqual(response.status_code, 200)
    
    def test_get_parking_spots_with_reservation_data(self):
        response = self.client.get(BASE + '/parkingspots').get_json()
        expected_response = ("{'data': [{'id': 1, 'latitude': 14.123, "
                             "'longitude': 46.123, 'reservations': [{'id': 1, "
                             "'datetime_from': 1621497600, "
                             "'datetime_to': 1621508400, 'user_id': 1, "
                             "'parking_spot_id': 1}, {'id': 2, "
                             "'datetime_from': 1621512000, "
                             "'datetime_to': 1621519200, 'user_id': 1, "
                             "'parking_spot_id': 1}]}, {'id': 2, "
                             "'latitude': 14.312, 'longitude': 46.321, "
                             "'reservations': [{'id': 3, 'datetime_from': "
                             "1621418400, 'datetime_to': 1621425600, "
                             "'user_id': 2, 'parking_spot_id': 2}]}]}")

        self.assertEqual(str(response), expected_response)

    def test_get_reservation_for_user_dont_exist_status_code(self):
        response = self.client.get(BASE + '/users/66/reservations')

        self.assertEqual(response.status_code, 404)

    def test_get_reservation_for_user_exist_status_code(self):
        response = self.client.get(BASE + '/users/1/reservations')

        self.assertEqual(response.status_code, 200)

    def test_get_reservation_for_user_exist_data(self):
        response = self.client.get(BASE + '/users/1/reservations').get_json()
        expected_response = ("{'data': [{'id': 1, 'datetime_from': 1621497600, "
                             "'datetime_to': 1621508400, 'user_id': 1, "
                             "'parking_spot_id': 1}, {'id': 2, 'datetime_from':"
                             " 1621512000, 'datetime_to': 1621519200, "
                             "'user_id': 1, 'parking_spot_id': 1}]}")

        self.assertEqual(str(response), expected_response)

    def test_insert_reservation_data_ok_status_code(self):
        response = self.client.post(
            BASE + '/reservations',
            json={
                'datetime_from': 1621508400,  # Thu May 20 2021 11:00:00 GMT+0
                'datetime_to': 1621512000,  # Thu May 20 2021 12:00:00 GMT+0
                'user_id': 1,
                'parking_spot_id': 1,
            }
        )
        repr(response)

        self.assertEqual(response.status_code, 302)

    def test_insert_reservation_data_ok_data(self):
        response = self.client.post(
            BASE + '/reservations',
            json={
                'datetime_from': 1624190460,
                'datetime_to': 1624194060,
                'user_id': 1,
                'parking_spot_id': 1
            }
        ).get_json()

        self.assertIn('Reservation created with ID', str(response))

    def test_insert_reservation_missing_parameters_status_code(self):
        response = self.client.post(
            BASE + '/reservations',
            json={
                'datetime_to': 1621512000,  # Missing dateTimeFrom
                'user_id': 1,
                'parking_spot_id': 1
            }
        )
        self.assertEqual(response.status_code, 400)

    def test_insert_reservation_user_doesnt_exist(self):
        response = self.client.post(
            BASE + '/reservations',
            json={
                'datetime_from': 1621508400,
                'datetime_to': 1621512000,
                'user_id': 66,
                'parking_spot_id': 1
            }
        )

        self.assertEqual(response.status_code, 400)

    def test_insert_reservation_time_not_available(self):
        self.client.post(
            BASE + '/reservations',
            json={
                'datetime_from': 1626786000,  # Tue Jul 20 2021 13:00:00 GMT+0
                'datetime_to': 1626789600,  # Tue Jul 20 2021 14:00:00 GMT+0
                'user_id': 1,
                'parking_spot_id': 1
            }
        )

        response = self.client.post(
            BASE + '/reservations',
            json={
                'datetime_from': 1626789300,  # Tue Jul 20 2021 13:55:00 GMT+0
                'datetime_to': 1626792900,  # Tue Jul 20 2021 14:55:00 GMT+0
                'user_id': 1,
                'parking_spot_id': 1
            }
        )

        self.assertEqual(response.status_code, 400)

    def test_user_exist(self):
        business_logic = BusinessLogic()
        self.assertTrue(business_logic.user_exist(1))

    def test_parking_spot_exist(self):
        business_logic = BusinessLogic()
        self.assertTrue(business_logic.parking_spot_exist(1))

    def test_is_available(self):
        business_logic = BusinessLogic()
        # 1621508400: Thu May 20 2021 11:00:00 GMT+0000
        # 1621512000: Thu May 20 2021 12:00:00 GMT+0000
        reservation = ('{ "datetime_from" : 1621508400, "datetime_to" : '
                       '1621512000, "user_id" : 1, "parking_spot_id" : 1 }')
        self.assertTrue(business_logic.is_available(json.loads(reservation)))


if __name__ == "__main__":
    unittest.main()
