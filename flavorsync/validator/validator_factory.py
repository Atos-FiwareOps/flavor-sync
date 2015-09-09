from flavorsync.exceptions import UnsupportedMediaTypeError,\
    UnimplementedMethodError

class ValidatorFactory():
    def __init__(self, mimetype=None):
        self.mimetype = mimetype
    
    def createFlavorCollectionValidator(self):
        self._raise_error()
        
    def createFlavorModificationRequestValidator(self):
        self._raise_error()
    
    def createFlavorRequestValidator(self):
        self._raise_error()
    
    def createFlavorValidator(self):
        self._raise_error()
    
    def createInfrastructureRequestValidator(self):
        self._raise_error()
    
    def createInfrastructureValidator(self):
        self._raise_error()
    
    def _raise_error(self):
        if self.mimetype:
            raise UnsupportedMediaTypeError(self.mimetype.split(';')[0])
        else:
            raise UnimplementedMethodError()