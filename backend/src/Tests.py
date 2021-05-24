"""
Tests.
Author: Denis Kotnik, May 2021
Help: https://www.unixtimestamp.com/index.php
"""

import datetime
import unittest
import json

from API import app
from service.BusinessLogic import BusinessLogic

BASE = "http://127.0.0.1:5000"


class TestAPI(unittest.TestCase):
    def setUp(self):
        pass
    def setDown(self):
        pass

    def test_A_getReservationExistStatusCode(self):
        """
        Check status code 200 when asking for a reservation that exist.
        """
        client = app.test_client(self)
        response = client.get(BASE + "/reservations/1")
        self.assertEqual(response.status_code, 200)

    def test_B_getReservationExistData(self):
        """
        Check data when asking for a reservation that exist.
        """
        client = app.test_client(self)
        response = client.get(BASE + "/reservations/1").get_json()
        rightResponse = "{'data': {'id': 1, 'dateTimeFrom': 1621497600, 'dateTimeTo': 1621508400, 'userId': 1, 'parkingSpotId': 1}}"
        self.assertEqual(str(response), rightResponse)
    
    def test_C_getReservationDoesNotExistStatusCode(self):
        """
        Check status code 404 when asking for a reservation that does not exist.
        """
        client = app.test_client(self)
        response = client.get(BASE + "/reservations/66")
        self.assertEqual(response.status_code, 404)

    def test_D_getParkingSpotsWithReservationStatusCode(self):
        """
        Check status code 200 when asking for a parking spots with reservations.
        """
        client = app.test_client(self)
        response = client.get(BASE + "/parkingspots")
        self.assertEqual(response.status_code, 200)
    
    def test_E_getParkingSpotsWithReservationData(self):
        """
        Check data when asking for a reservation that exist.
        """
        client = app.test_client(self)
        response = client.get(BASE + "/parkingspots").get_json()
        rightResponse = "{'data': [{'id': 1, 'latitude': 14.123, 'longitude': 46.123, 'reservations': [{'id': 1, 'dateTimeFrom': 1621497600, 'dateTimeTo': 1621508400, 'userId': 1, 'parkingSpotId': 1}, {'id': 2, 'dateTimeFrom': 1621512000, 'dateTimeTo': 1621519200, 'userId': 1, 'parkingSpotId': 1}]}, {'id': 2, 'latitude': 14.312, 'longitude': 46.321, 'reservations': [{'id': 3, 'dateTimeFrom': 1621418400, 'dateTimeTo': 1621425600, 'userId': 2, 'parkingSpotId': 2}]}]}"
        self.assertEqual(str(response), rightResponse)

    def test_F_getReservationForUserUserDontExistStatusCode(self):
        """
        Check status code 404 when asking for a reservation for a user who does not exist.
        """
        client = app.test_client(self)
        response = client.get(BASE + "/users/66/reservations")
        self.assertEqual(response.status_code, 404)
    
    def test_G_getReservationForUserUseExistStatusCode(self):
        """
        Check status code 200 when asking for a reservations for a user who exist.
        """
        client = app.test_client(self)
        response = client.get(BASE + "/users/1/reservations")
        self.assertEqual(response.status_code, 200)
    
    def test_H_getReservationForUserUseExistData(self):
        """
        Check data when asking for a reservations for a user who exist.
        """
        client = app.test_client(self)
        response = client.get(BASE + "/users/1/reservations").get_json()
        rightResponse = "{'data': [{'id': 1, 'dateTimeFrom': 1621497600, 'dateTimeTo': 1621508400, 'userId': 1, 'parkingSpotId': 1}, {'id': 2, 'dateTimeFrom': 1621512000, 'dateTimeTo': 1621519200, 'userId': 1, 'parkingSpotId': 1}]}"
        self.assertEqual(str(response), rightResponse)
    
    def test_I_insertReservationDataOKStatusCode(self):
        """
        Check status code 200 when inserting a reservation.
        """
        client = app.test_client(self)
        # 1621508400: Thu May 20 2021 11:00:00 GMT+0000
        # 1621512000: Thu May 20 2021 12:00:00 GMT+0000
        response = client.post(BASE + '/reservations', json = { 'dateTimeFrom' : 1621508400, 'dateTimeTo' : 1621512000, 'userId' : 1, 'parkingSpotId' : 1 })
        self.assertEqual(response.status_code, 302)
    
    def test_J_insertReservationDataOKData(self):
        """
        Check data when inserting a reservation.
        """
        client = app.test_client(self)
        response = client.post(BASE + '/reservations', json = { 'dateTimeFrom' : 1624190460, 'dateTimeTo' : 1624194060, 'userId' : 1, 'parkingSpotId' : 1 }).get_json()
        rightResponse = "{'message': 'Reservation created with ID: 5'}"
        self.assertEqual(str(response), rightResponse)
    
    def test_K_insertReservationMissingParametersStatusCode(self):
        """
        Check status code 400 when inserting a reservation with missing parameters.
        """
        client = app.test_client(self)
        # Missing dateTimeFrom
        response = client.post(BASE + '/reservations', json = { 'dateTimeTo' : 1621512000, 'userId' : 1, 'parkingSpotId' : 1 })
        self.assertEqual(response.status_code, 400)

    def test_L_insertReservationUserDoesntExist(self):
        """
        Check status code 400 when inserting a reservation for a user who doesn not exist.
        """
        client = app.test_client(self)
        response = client.post(BASE + '/reservations', json = { 'dateTimeFrom' : 1621508400, 'dateTimeTo' : 1621512000, 'userId' : 66, 'parkingSpotId' : 1 })
        self.assertEqual(response.status_code, 400)

    def test_M_insertReservationTimeNotAvailable(self):
        """
        Check status code 400 when inserting a reservation for a time which is not available.
        """
        client = app.test_client(self)
        # 1626786000: Tue Jul 20 2021 13:00:00 GMT+0000
        # 1626789600: Tue Jul 20 2021 14:00:00 GMT+0000
        client.post(BASE + '/reservations', json = { 'dateTimeFrom' : 1626786000, 'dateTimeTo' : 1626789600, 'userId' : 1, 'parkingSpotId' : 1 })
        # 1626789300: Tue Jul 20 2021 13:55:00 GMT+0000
        # 1626792900: Tue Jul 20 2021 14:55:00 GMT+0000
        response = client.post(BASE + '/reservations', json = { 'dateTimeFrom' : 1626789300, 'dateTimeTo' : 1626792900, 'userId' : 1, 'parkingSpotId' : 1 })
        self.assertEqual(response.status_code, 400)
    
    def test_N_userExist(self):
        """
        Check if method userExist() return True, because user with ID already axist.
        """
        businessLogic = BusinessLogic()
        self.assertTrue(businessLogic.userExist(1))
    
    def test_O_parkingSpotExist(self):
        """
        Check if method parkingSpotExist() return True, because parking spot with ID already axist.
        """
        businessLogic = BusinessLogic()
        self.assertTrue(businessLogic.parkingSpotExist(1))

    def test_P_isAvailable(self):
        """
        Very important method which test the method which should tell if two dates overlap.
        The one who we test is already in DB, so it should return True.
        TODO: more tests!
        """
        businessLogic = BusinessLogic()
        # 1621508400: Thu May 20 2021 11:00:00 GMT+0000
        # 1621512000: Thu May 20 2021 12:00:00 GMT+0000
        reservation = '{ "dateTimeFrom" : 1621508400, "dateTimeTo" : 1621512000, "userId" : 1, "parkingSpotId" : 1 }'
        self.assertTrue(businessLogic.isAvailable(json.loads(reservation)))

if __name__ == "__main__":
    unittest.main()