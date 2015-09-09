from flavorsync.database_manager import DatabaseManager
class AuthManager():
    def __init__(self):
        self.db_manager = DatabaseManager()
    
    def get_tenant_info(self):
        return self.db_manager.get_infrastructure()