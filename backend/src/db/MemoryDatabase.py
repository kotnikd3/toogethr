"""
Simulation of in-memory database.
"""

class MemoryDatabase():
    def __init__(self):
        self.tables = {}
    
    def addTable(self, table):
        if not table in self.tables:
            self.tables[table] = { "increment" : 0, "data" : {} }
            return True
        return False
    
    def select(self, table, index=None, where=None):
        """
        Get data from specific name of the table.
        If index is '*', get all the data. Otherwise:
        if index has value (for example index='1'), get data that corresponds to that index. Otherwise:
        if where is lambda function, filter data with that function and return the filtered data.
        TODO: method is very slow when using where!
        """
        def isLambda(myLambda):
            return callable(myLambda) and myLambda.__name__ == "<lambda>"
        
        if table in self.tables:
            if index == "*":
                return list(self.tables[table]["data"].values())
            if not index is None and index in self.tables[table]["data"]:
                return self.tables[table]["data"][index]
            if not where is None and isLambda(where):
                # Slow! Time complexity is O(n)!
                return list(filter(where, self.tables[table]["data"].values()))
        return None
    
    def insert(self, table, entity):
        """
        Auto increment index (integer) in the given table, set ID of the entity as this index, 
        then insert given entity into the table and return the ID of the entity.
        """
        if table in self.tables:
            self.tables[table]["increment"] += 1
            entity.id = self.tables[table]["increment"]
            self.tables[table]["data"][entity.id] = entity
            return entity.id
        return None