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

class BusinessLogic():
    def __init__(self):
        self.memoryDatabase = MemoryDatabase()

        self.migrate()

        self.reservationDAO = ReservationDAO(self.memoryDatabase)
        self.userDAO = UserDAO(self.memoryDatabase)
        self.parkingSpotDAO = ParkingSpotDAO(self.memoryDatabase)

        self.seed()
    
    def migrate(self):
        """
        Create tables in DB.
        """
        self.memoryDatabase.addTable("reservation")
        self.memoryDatabase.addTable("parking_spot")
        self.memoryDatabase.addTable("user")
    
    def seed(self):
        """
        Fill DB with some dummy data.
        """
        self.userDAO.insert(User(1, "denis", "denis.kotnik@gmail.com"))
        self.userDAO.insert(User(2, "ted", "ted@toogethr.com.com"))
        self.userDAO.insert(User(3, "gerard", "gdalmau@toogethr.com"))

        # 20th May 10:00 - 13:00
        self.reservationDAO.insert(Reservation(1, 1621497600, 1621508400, 1, 1))
        # 20th May 14:00 - 16:00
        self.reservationDAO.insert(Reservation(2, 1621512000, 1621519200, 1, 1))
        # 19th May 12:00 - 14:00
        self.reservationDAO.insert(Reservation(3, 1621418400, 1621425600, 2, 2))

        self.parkingSpotDAO.insert(ParkingSpot(1, 14.123, 46.123))
        self.parkingSpotDAO.insert(ParkingSpot(2, 14.312, 46.321))
    
    
    def getParkingSpotsWithReservations(self):
        """
        Return the info about all the parking spots and all the reservations for each parking spot.
        """
        parkingSpots = self.parkingSpotDAO.getAll()

        result = []
        for parkingSpot in parkingSpots:
            bookedReservations = self.reservationDAO.getByParkingSpotId(parkingSpot.id)
            # Magic of dynamically typed languages :-)
            parkingSpot.reservations = bookedReservations
            result.append(parkingSpot)
        
        return self.toJSON(result)

    def getReservationsForParkingSpot(self, parkingSpotId):
        """
        Return all the reservations for specifi parking spot.
        """
        reservationsForParkingSpot = self.reservationDAO.getByParkingSpotId(parkingSpotId)
        return self.toJSON(reservationsForParkingSpot)
    
    def getReservationByUser(self, userId):
        """
        Return all the reservations for specific user.
        """
        reservations = self.reservationDAO.getByUserId(userId)
        return self.toJSON(reservations)

    
    def insertReservation(self, reservationJSON):
        newReservation = self.deserializeReservation(reservationJSON)
        return self.reservationDAO.insert(newReservation)
    
    def getReservation(self, id):
        """
        Return reservation with specific ID.
        """
        reservation = self.reservationDAO.getById(id)
        if not reservation is None:
            return self.toJSON(reservation)
        return None
    
    def insertReservationRequestValid(self, reservationJSON):
        """
        Check if JSON request is valid by checking for all the required fields, if user exist and if reservation also exist.
        Return True if every check is True, else return False. 
        """
        if self.allParams(reservationJSON):
            newReservation = self.deserializeReservation(reservationJSON)
            if self.userExist(newReservation.userId) and self.parkingSpotExist(newReservation.parkingSpotId):
                return True
        return False

    
    def allParams(self, reservationJSON, required=("parkingSpotId", "userId", "dateTimeFrom", "dateTimeTo")):
        """
        Check if all the required parameters are inside given JSON data structure.
        """
        return all(param in reservationJSON for param in required)

    def userExist(self, userId):
            user = self.userDAO.getById(userId)
            if not user is None:
                return True
            return False
    
    def parkingSpotExist(self, parkingSpotId):
        parkingSpot = self.parkingSpotDAO.getById(parkingSpotId)
        if not parkingSpot is None:
            return True
        return False

    def deserializeReservation(self, reservationJSON):
        """
        Convert from JSON to Reservation object without ID.
        """
        parkingSpotId = reservationJSON.get("parkingSpotId", None)
        userId = reservationJSON.get("userId", None)
        dateTimeFrom = reservationJSON.get("dateTimeFrom", None)
        dateTimeTo = reservationJSON.get("dateTimeTo", None)

        return Reservation(None, dateTimeFrom, dateTimeTo, userId, parkingSpotId)
    
    def toJSON(self, object):
        return json.dumps({"data" : object}, default=lambda o: o.__dict__)

    def isAvailable(self, reservationJSON):
        """
        Check if time for reservation is really available.
        """
        newReservation = self.deserializeReservation(reservationJSON)

        bookedReservations = self.reservationDAO.getByParkingSpotId(newReservation.parkingSpotId)

        for reservation in bookedReservations:
            if self.overlap(reservation, newReservation):
                return False
        return True
    
    def overlap(self, booked, new):
        """
        Check if two Reservations overlap by time.
        TODO: maybe encapsulate this logic into Reservation object?
        """
        for f,s in ((booked, new), (new, booked)):
            if (f.dateTimeFrom == s.dateTimeFrom and f.dateTimeTo == s.dateTimeTo):
                return True
            for time in (f.dateTimeFrom, f.dateTimeTo):
                if s.dateTimeFrom < time < s.dateTimeTo:
                    return True
        return False