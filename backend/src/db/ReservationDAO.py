class ReservationDAO:
    def __init__(self, database):
        self.TABLE_NAME = 'reservation'
        self.database = database
    
    def get_by_id(self, reservation_id):
        return self.database.select(self.TABLE_NAME, reservation_id)
    
    def get_all(self):
        return self.database.select(self.TABLE_NAME, '*')
    
    def insert(self, reservation):
        return self.database.insert(self.TABLE_NAME, reservation)
    
    def get_by_parking_spot_id(self, parking_spot_id):
        reservations = self.database.select(
            self.TABLE_NAME,
            None,
            lambda x: x.parking_spot_id == parking_spot_id,
        )

        return reservations
    
    def get_by_user_id(self, user_id):
        reservations = self.database.select(
            self.TABLE_NAME,
            None,
            lambda x: x.user_id == user_id,
        )

        return reservations
