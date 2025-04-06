import pypyodbc
class LibraryDB:
    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.conn = None
        self.cursor = None
    
    def connect(self):
        """Establish database connection"""
        if not self.conn:
            self.conn = pypyodbc.connect(self.connection_string)
            self.cursor = self.conn.cursor()
    
    def disconnect(self):
        """Close database connection"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None