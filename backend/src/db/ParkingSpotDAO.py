class ParkingSpotDAO:
    def __init__(self, database):
        self.TABLE_NAME = 'parking_spot'
        self.database = database
    
    def get_by_id(self, _id):
        return self.database.select(self.TABLE_NAME, _id)

    def get_all(self):
        return self.database.select(self.TABLE_NAME, '*')
    
    def insert(self, parking_space):
        return self.database.insert(self.TABLE_NAME, parking_space)
