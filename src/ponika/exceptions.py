class TeltonikaApiException(Exception):
    def __init__(self, *args):
        super().__init__(*args)

        self.errors = args

    def __str__(self):
        return ', '.join([str(error) for error in self.errors])


class TeltonikaLoginException(TeltonikaApiException):
    def __init__(self, *args):
        super().__init__(*args)

        self.errors = ['The provided credentials are invalid.']

    def __str__(self):
        return ', '.join([str(error) for error in self.errors])
