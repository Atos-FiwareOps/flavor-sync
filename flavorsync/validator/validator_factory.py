from flavorsync.exceptions import UnsupportedMediaTypeError,\
    UnimplementedMethodError

class ValidatorFactory():
    def __init__(self, mimetype=None):
        self.mimetype = mimetype
    
    def create_exception_validator(self):
        self._raise_error()
    
    def create_flavor_collection_validator(self):
        self._raise_error()
        
    def create_flavor_modification_request_validator(self):
        self._raise_error()
    
    def create_flavor_request_validator(self):
        self._raise_error()
    
    def create_flavor_validator(self):
        self._raise_error()
    
    def create_infrastructure_request_validator(self):
        self._raise_error()
    
    def create_infrastructure_validator(self):
        self._raise_error()
    
    def _raise_error(self):
        if self.mimetype:
            raise UnsupportedMediaTypeError(self.mimetype.split(';')[0])
        else:
            raise UnimplementedMethodError()