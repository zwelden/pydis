
class KeyValueStore:
    def __init__(self):
        self.db = {}
        # self.timeout_index = {}

    def process_command(self, command):
        pass
    
    def set_key(self, key, value, timeout=0):
        # if timeout set timeout value
        self.db[key] = {
            "val": value
        } 

    def get_key(self, key):
        if key in self.db:
            # check if expired, if so delete key and return None
            return self.db[key]
        
        return None  

    def delete_key(self, key):
        self.db.pop(key, None) 

    


