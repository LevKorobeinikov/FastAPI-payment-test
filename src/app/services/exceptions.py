class UserNotFoundError(Exception):
    def __init__(self, message: str = 'User not found') -> None:
        super().__init__(message)


class AccountOwnershipError(Exception):
    def __init__(self, message: str = 'Account does not belong to this user') -> None:
        super().__init__(message)


class EmailAlreadyExistsError(Exception):
    def __init__(self, message: str = 'User with this email already exists') -> None:
        super().__init__(message)
