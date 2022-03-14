# Database
from db.MemoryDatabase import MemoryDatabase
# DAO's
from db.ReservationDAO import ReservationDAO
from db.UserDAO import UserDAO
from db.ParkingSpotDAO import ParkingSpotDAO
# Entities
from db.Reservation import Reservation
from db.User import User
from db.ParkingSpot import ParkingSpot
# Other
import json
from datetime import datetime


class BusinessLogic:
    def __init__(self):
        self.memory_database = MemoryDatabase()

        self.migrate()

        self.reservation_dao = ReservationDAO(self.memory_database)
        self.user_dao = UserDAO(self.memory_database)
        self.parking_spot_dao = ParkingSpotDAO(self.memory_database)

        self.seed()
    
    def migrate(self):
        """
        Create tables in DB.
        """
        self.memory_database.add_table('reservation')
        self.memory_database.add_table('parking_spot')
        self.memory_database.add_table('user')
    
    def seed(self):
        """
        Fill DB with some dummy data.
        """
        self.user_dao.insert(User(1, 'denis', 'denis@toogethr.com'))
        self.user_dao.insert(User(2, 'ted', 'ted@toogethr.com'))
        self.user_dao.insert(User(3, 'gerard', 'gdalmau@toogethr.com'))

        # 20th May 10:00 - 13:00
        self.reservation_dao.insert(
            Reservation(1, 1621497600, 1621508400, 1, 1)
        )
        # 20th May 14:00 - 16:00
        self.reservation_dao.insert(
            Reservation(2, 1621512000, 1621519200, 1, 1)
        )
        # 19th May 12:00 - 14:00
        self.reservation_dao.insert(
            Reservation(3, 1621418400, 1621425600, 2, 2)
        )

        self.parking_spot_dao.insert(ParkingSpot(1, 14.123, 46.123))
        self.parking_spot_dao.insert(ParkingSpot(2, 14.312, 46.321))
    
    
    def get_parking_spots_with_reservations(self):
        """
        Return the info about all the parking spots and all the reservations
        for each parking spot.
        """
        parking_spots = self.parking_spot_dao.get_all()

        result = []
        for parking_spot in parking_spots:
            booked_reservations = self.reservation_dao.get_by_parking_spot_id(
                parking_spot.id
            )
            # Magic of dynamically typed languages
            parking_spot.reservations = booked_reservations
            result.append(parking_spot)
        
        return BusinessLogic.to_json(result)

    def get_reservations_for_parking_spot(self, parking_spot_id):
        """
        Return all the reservations for specifi parking spot.
        """
        reservations = self.reservation_dao.get_by_parking_spot_id(
            parking_spot_id
        )

        return BusinessLogic.to_json(reservations)
    
    def get_reservation_by_user(self, user_id):
        """
        Return all the reservations for specific user.
        """
        reservations = self.reservation_dao.get_by_user_id(user_id)

        return BusinessLogic.to_json(reservations)
    
    def insert_reservation(self, reservation_json):
        new_reservation = BusinessLogic.deserialize_reservation(
            reservation_json
        )

        return self.reservation_dao.insert(new_reservation)
    
    def get_reservation(self, _id):
        """
        Return reservation with specific ID.
        """
        reservation = self.reservation_dao.get_by_id(_id)

        if reservation is not None:
            return BusinessLogic.to_json(reservation)

        return None
    
    def insert_reservation_request_valid(self, reservation_json):
        """
        Check if JSON request is valid by checking for all the required fields,
        if user exist and if reservation also exist.
        Return True if every check is True, else return False. 
        """
        if BusinessLogic.all_params(reservation_json):
            new_reservation = BusinessLogic.deserialize_reservation(
                reservation_json
            )

            if (
                self.user_exist(new_reservation.user_id)
                and self.parking_spot_exist(new_reservation.parking_spot_id)
            ):
                return True

        return False

    @staticmethod
    def all_params(
        reservation_json,
        required=('parking_spot_id', 'user_id', 'datetime_from', 'datetime_to'),
    ):
        """
        Check if all the required parameters are inside given
        JSON data structure.
        """
        return all(param in reservation_json for param in required)

    def user_exist(self, user_id):
        user = self.user_dao.get_by_id(user_id)

        return True if user is not None else False

    def parking_spot_exist(self, parking_spot_id):
        parking_spot = self.parking_spot_dao.get_by_id(parking_spot_id)

        return True if parking_spot is not None else False

    @staticmethod
    def deserialize_reservation(reservation_json):
        """
        Convert from JSON to Reservation object without ID.
        """
        parking_spot_id = reservation_json.get('parking_spot_id', None)
        user_id = reservation_json.get('user_id', None)
        datetime_from = reservation_json.get('datetime_from', None)
        datetime_to = reservation_json.get('datetime_to', None)

        return Reservation(
            None,
            datetime_from,
            datetime_to,
            user_id,
            parking_spot_id
        )

    @staticmethod
    def to_json(_object):
        return json.dumps({'data': _object}, default=lambda o: o.__dict__)

    def is_available(self, reservation_json):
        """
        Check if time for reservation is really available.
        """
        new_reservation = BusinessLogic.deserialize_reservation(
            reservation_json
        )

        booked_reservations = self.reservation_dao.get_by_parking_spot_id(
            new_reservation.parking_spot_id
        )

        for reservation in booked_reservations:
            if BusinessLogic.overlap(reservation, new_reservation):
                return False
        return True

    @staticmethod
    def overlap(booked, new):
        """
        Check if two Reservations overlap by time.
        """
        for f, s in ((booked, new), (new, booked)):
            if (
                f.datetime_from == s.datetime_from
                and f.datetime_to == s.datetime_to
            ):
                return True
            for time in (f.datetime_from, f.datetime_to):
                if s.datetime_from < time < s.datetime_to:
                    return True
        return False
