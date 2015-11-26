"""
Contains all exceptions used for the Threema gateway service.
"""
__all__ = (
    'GatewayError',
    'GatewayServerError',
    'IDError',
    'IDServerError',
    'KeyError',
    'KeyServerError',
    'ReceptionCapabilitiesError',
    'ReceptionCapabilitiesServerError',
    'CreditsServerError',
    'MessageError',
    'UnsupportedMimeTypeError',
    'MissingCapabilityError',
    'MessageServerError',
    'BlobError',
    'BlobServerError',
)


class GatewayError(Exception):
    """
    General error of this module. All other exceptions are derived from
    this class.
    """


class GatewayServerError(GatewayError):
    """
    The server has responded with an error code. All other server
    exceptions are derived from this class.

    Arguments:
        - `response`: An instance of a :class:`requests.Response`
          object.
    """
    status_description = {}

    def __init__(self, response):
        self.response = response

    def __str__(self):
        status_code = self.response.status_code

        # Return description for status code
        try:
            return self.status_description[status_code]
        except KeyError:
            return 'Unknown error, status code: {}'.format(status_code)


class IDError(GatewayError):
    """
    A problem before fetching a Threema ID occurred.
    """


class IDServerError(IDError, GatewayServerError):
    """
    The server has responded with an error code while looking up a
    Threema ID.
    """
    status_description = {
        400: 'Supplied hash invalid',
        401: 'API identity or secret incorrect',
        404: 'No matching Threema ID could be found',
        500: 'Temporary internal server error occurred'
    }


# noinspection PyShadowingBuiltins
class KeyError(GatewayError):
    """
    A problem with a key occurred.
    """


class KeyServerError(KeyError, GatewayServerError):
    """
    The server has responded with an error code while fetching a
    public key.
    """
    status_description = {
        401: 'API identity or secret incorrect',
        404: 'No matching Threema ID could be found',
        500: 'Temporary internal server error occurred'
    }


class ReceptionCapabilitiesError(GatewayError):
    """
    An invalid reception capability has been returned.
    """


class ReceptionCapabilitiesServerError(
    ReceptionCapabilitiesError, GatewayServerError
):
    """
    The server responded with an error code while fetching the reception
    capabilities of a Threema ID.
    """
    status_description = {
        401: 'API identity or secret incorrect',
        404: 'No matching Threema ID could be found',
        500: 'Temporary internal server error occurred'
    }


class CreditsServerError(GatewayServerError):
    """
    The server has responded with an error code while fetching the
    remaining credits.
    """
    status_description = {
        401: 'API identity or secret incorrect',
        500: 'Temporary internal server error occurred'
    }


class MessageError(GatewayError):
    """
    Indicates that a message is invalid. The server has not been
    contacted, yet.
    """


class UnsupportedMimeTypeError(MessageError):
    """
    Indicates that the supplied file or binary of a message has an
    unsupported mime type.
    """
    def __init__(self, mime_type):
        self.mime_type = mime_type

    def __str__(self):
        return 'Unsupported mime type: {}'.format(self.mime_type)


class MissingCapabilityError(MessageError):
    """
    A capability is missing to send a specific message type.
    """
    def __init__(self, missing_capabilities):
        self.missing_capabilities = missing_capabilities

    def __str__(self):
        return 'Missing capabilities: {}'.format(self.missing_capabilities)


class MessageServerError(MessageError, GatewayServerError):
    """
    The server has responded with an error code while sending a
    message.
    """
    status_description = {
        400: 'Recipient identity is invalid or the account is not setup for the '
             'requested mode',
        401: 'API identity or secret incorrect',
        402: 'Insufficient credits',
        404: 'Phone or email address could not be resolved to a Threema ID',
        413: 'Message too long',
        500: 'Temporary internal server error occurred'
    }


class BlobError(GatewayError):
    """
    Indicates that a blob is invalid. The server has not been contacted,
    yet.
    """


class BlobServerError(BlobError, GatewayServerError):
    """
    The server has responded with an error code while uploading or
    downloading a blob.
    """
    status_description = {
        400: 'Required parameters missing or blob is empty',
        401: 'API identity or secret incorrect',
        402: 'Insufficient credits',
        404: 'No matching blob found for the supplied ID',
        413: 'Blob too big',
        500: 'Temporary internal server error occurred'
    }