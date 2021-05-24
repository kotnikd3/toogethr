class ReservationDAO():
    def __init__(self, database):
        self.TABLE_NAME = "reservation"
        self.database = database
    
    def getById(self, reservationId):
        return self.database.select(self.TABLE_NAME, reservationId)
    
    def getAll(self):
        return self.database.select(self.TABLE_NAME, "*")
    
    def insert(self, reservation):
        return self.database.insert(self.TABLE_NAME, reservation)
    
    def getByParkingSpotId(self, parkingSpotId):
        reservations = self.database.select(self.TABLE_NAME, None, lambda x: x.parkingSpotId == parkingSpotId)
        return reservations
    
    def getByUserId(self, userId):
        reservations = self.database.select(self.TABLE_NAME, None, lambda x: x.userId == userId)
        return reservations