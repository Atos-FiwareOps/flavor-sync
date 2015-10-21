from flavorsync import app
from flask import request
from flask import Response
from flavorsync.parser.parser_factory import ParserFactory

class UnimplementedMethodError(Exception):
    def __init__(self):
        Exception.__init__(self, "Uninplemented method")

class FlavorSyncError(Exception):
    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload
    
    def to_dict(self):
        rv = dict(self.payload or ())
        rv['error']= {"message" : self.message}
        return rv
    
    def super_class(self):
        return self.__class__

class InfrastructureAlreadyExistsError(FlavorSyncError):
    status_code = 409
    
    def __init__(self, infrastructure_id):
        message = "The infrastructure {0} already exists".format(infrastructure_id)
        super(InfrastructureAlreadyExistsError, self).__init__(message, self.status_code)

class InfrastructureBadRequestError(FlavorSyncError):
    status_code = 400
    
    def __init__(self):
        message = "The infrastructure is not well formed"
        super(InfrastructureBadRequestError, self).__init__(message, self.status_code)
        
class InfrastructureNotFoundError(FlavorSyncError):
    status_code = 404
    
    def __init__(self, infrastructure_id):
        message = "The infrastructure {0} does not exist".format(infrastructure_id)
        super(InfrastructureNotFoundError, self).__init__(message, self.status_code)

class FlavorNotFoundExceptionError(FlavorSyncError):
    status_code = 404
    
    def __init__(self, flavor_id):
        message = "The flavor {0} does not exist".format(flavor_id)
        super(FlavorNotFoundExceptionError, self).__init__(message, self.status_code)

class FlavorAlreadyExistsError(FlavorSyncError):
    status_code = 409
    
    def __init__(self, flavor_name):
        message = "The there is already a flavor named {0}".format(flavor_name)
        super(FlavorAlreadyExistsError, self).__init__(message, self.status_code)

class FlavorInfrastructureNotFoundError(FlavorSyncError):
    status_code = 409
    
    def __init__(self, infrastructure_name):
        message = "The node {0} does not exist".format(infrastructure_name)
        super(FlavorInfrastructureNotFoundError, self).__init__(message, self.status_code)

class UnpublishUnpromotedFlavorError(FlavorSyncError):
    status_code = 409
    
    def __init__(self):
        message = "A flavor cannot be unpublished or unpromoted"
        super(UnpublishUnpromotedFlavorError, self).__init__(message, self.status_code)

class FlavorBadRequestError(FlavorSyncError):
    status_code = 400
    
    def __init__(self):
        message = "The flavor request is not well formed"
        super(FlavorBadRequestError, self).__init__(message, self.status_code)

class PromotedNotPublicFlavorBadRequestError(FlavorSyncError):
    status_code = 400
    
    def __init__(self):
        message = "A flavor cannot be promoted and private"
        super(PromotedNotPublicFlavorBadRequestError, self).__init__(message, self.status_code)

class OpenStackConnectionError(FlavorSyncError):
    status_code = 502
    
    def __init__(self):
        message = "Cannot connet to Openstack infrastructure. It could happen "
        message += "because it is down, it is not reachable or credentials are "
        message += "wrong. Please check it"
        super(OpenStackConnectionError, self).__init__(message, self.status_code)

class UnsupportedMediaTypeError(FlavorSyncError):
    status_code = 415
    
    def __init__(self, content_type):
        if content_type:
            message = "Unrecognized content type '{0}'.".format(content_type)
            message += " Mustbe 'application/xml or 'application/json'"
        else:
            message = "Unrecognized content type. Mustbe 'application/xml'"
            message += " or 'application/json'"
        
        super(UnsupportedMediaTypeError, self).__init__(message, self.status_code)

@app.errorhandler(FlavorSyncError)
def handle_invalid_usage(error):
    mimetype = request.accept_mimetypes
    
    parser_factory = ParserFactory()
    parser = parser_factory.get_parser(mimetype, FlavorSyncError)
    
    response_body = parser.from_model(error)
    
    return Response(response_body, status=error.status_code, mimetype=mimetype[0][0])