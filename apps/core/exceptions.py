from django.core.exceptions import ValidationError


class DuplicatedError(Exception):
    def __init__(self, message="Email or username duplicated"):
        self.message = message
        super().__init__(self.message)
        self.http_code = 400


class InvalidPassCode(Exception):
    def __init__(self, message="Pass code is invalid"):
        self.message = message
        super().__init__(self.message)
        self.http_code = 400
