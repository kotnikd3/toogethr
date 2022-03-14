"""
Simulation of in-memory database.
"""


class MemoryDatabase:
    def __init__(self):
        self.tables = {}
    
    def add_table(self, table):
        if table not in self.tables:
            self.tables[table] = {'increment': 0, 'data': {}}
            return True
        return False
    
    def select(self, table, index=None, where=None):
        """
        Get data from specific name of the table.
        If index is '*', get all the data. Otherwise:
        if index has value (for example index='1'), get data that corresponds
        to that index. Otherwise, if where is lambda function, filter data with
        that function and return the filtered data.
        """
        def is_lambda(my_lambda):
            return callable(my_lambda) and my_lambda.__name__ == '<lambda>'
        
        if table in self.tables:
            if index == '*':
                return list(self.tables[table]['data'].values())
            if index is not None and index in self.tables[table]['data']:
                return self.tables[table]['data'][index]
            if where is not None and is_lambda(where):
                # TODO: Slow! Time complexity is O(n)!
                return list(filter(where, self.tables[table]['data'].values()))

        return None
    
    def insert(self, table, entity):
        """
        Auto increment index (integer) in the given table, set ID of the entity
        as this index, then insert given entity into the table
        and return the ID of the entity.
        """
        if table in self.tables:
            self.tables[table]['increment'] += 1
            entity.id = self.tables[table]['increment']
            self.tables[table]['data'][entity.id] = entity
            return entity.id

        return None
