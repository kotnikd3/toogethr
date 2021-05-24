class ParkingSpotDAO():
    def __init__(self, database):
        self.TABLE_NAME = "parking_spot"
        self.database = database
    
    def getById(self, id):
        return self.database.select(self.TABLE_NAME, id)

    def getAll(self):
        return self.database.select(self.TABLE_NAME, "*")
    
    def insert(self, parkingSpace):
        return self.database.insert(self.TABLE_NAME, parkingSpace)