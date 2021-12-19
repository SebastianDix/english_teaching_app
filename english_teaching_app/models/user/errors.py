#!/usr/bin/env python3
class UserError(Exception):
    def __init__(self,message):
        self.message = message

class UserNotFoundError(UserError):
    pass

class UserAlreadyRegisteredError(UserError):
    pass

class InvalidEmailError(UserError):
    pass

class IncorectPasswordError(UserError):
    pass
