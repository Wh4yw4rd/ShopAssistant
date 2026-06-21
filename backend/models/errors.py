class DatabaseStartupError(Exception):
    def __init__(self):
        message = "Unable to connect to database."
        super().__init__(message)


class DatabaseConnectionError(Exception):
    def __init__(self):
        message = "Unable to retrieve a database connection."
        super().__init__(message)


class DatabaseQueryError(Exception):
    def __init__(self, message):
        super().__init__(message)


class InvalidSession(Exception):
    def __init__(self):
        message = "No valid session was found."
        super().__init__(message)


class EmptyTransactionTable(Exception):
    def __init__(self):
        message = "No existing transactions are recorded."
        super().__init__(message)


class InvalidUser(Exception):
    def __init__(self):
        message = "No valid user was found."
        super().__init__(message)


class InvalidDateRange(Exception):
    def __init__(self):
        message = "Time range is invalid."
        super().__init__(message)


class AdminRequired(Exception):
    def __init__(self, message):
        super().__init__(message)

    
class APIConnectionError(Exception):
    def __init__(self, message):
        super().__init__(message)


class NameAlreadyExists(Exception):
    def __init__(self):
        message = "Name already in use."
        super().__init__(message)