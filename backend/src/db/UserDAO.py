class UserDAO:
    def __init__(self, database):
        self.TABLE_NAME = 'user'
        self.database = database
    
    def get_by_id(self, _id):
        return self.database.select(self.TABLE_NAME, _id)
    
    def insert(self, user):
        return self.database.insert(self.TABLE_NAME, user)
