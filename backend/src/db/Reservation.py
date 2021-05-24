class Reservation():
    def __init__(self, id, dateTimeFrom, dateTimeTo, userId, parkingSpotId):
        self.id = id
        self.dateTimeFrom = dateTimeFrom
        self.dateTimeTo = dateTimeTo
        self.userId = userId
        self.parkingSpotId = parkingSpotId