"""
Custom exception to surface HTTP status codes
"""


class AppError(BaseException):
    def __init__(self, code, message):
        self.code = code
        self.message = message

    def __str__(self):
        return repr('%s - %s' % (self.code, self.message))