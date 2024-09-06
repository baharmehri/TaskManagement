from rest_framework.response import Response


class CustomResponse(Response):
    @classmethod
    def data_response(cls, data, message, meta=None, status=None):
        response_data = {
            'data': data,
            'message': message,
            'meta': meta
        }
        return cls(data=response_data, status=status)

    @classmethod
    def error_response(cls, error_message, status=None):
        response_data = {
            'error': error_message,
        }
        return cls(data=response_data, status=status)
