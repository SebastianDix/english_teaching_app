#!/usr/bin/env python3
import uuid
from dataclasses import dataclass, field
from typing import Dict
from models.model import Model
from common.utils import Utils
import models.user.errors as UserErrors

@dataclass
class User(Model):
    collection: str = field(init=False,default='users')
    email: str
    password: str
    firstname: str
    lastname: str
    _id: str = field(default_factory=lambda:uuid.uuid4().hex)

    @classmethod
    def find_by_email(cls,email:str) -> "User":
        try:
            return cls.find_one_by('email',email)
        except TypeError:
            raise UserErrors.UserNotFoundError('A user with this e-mail was not found.')

    @classmethod
    def is_login_valid(cls,email: str, password: str) -> bool:
        user = cls.find_by_email(email)

        if not Utils.check_hashed_password(password, user.password):
            raise UserErrors.IncorectPasswordError('Password seems to be incorrect')

        return True

    @classmethod
    def register_user(cls,email: str, password: str, firstname: str, lastname: str) -> bool:
        if not Utils.email_is_valid(email):
            raise UserErrors.InvalidEmailError('The e-mail does not have the right format')

        try:
            user = cls.find_by_email(email)
            raise UserErrors.UserAlreadyRegisteredError('The e-mail you used to register already exists.')
        except UserErrors.UserNotFoundError:
            User(email,Utils.hash_password(password),firstname,lastname).save_to_mongo()

        return True

    def json(self) -> Dict:
        return{
            '_id':self._id,
            'email':self.email,
            'password':self.password,
            'firstname':self.firstname,
            'lastname':self.lastname
        }

    def json_nopassword(self) -> Dict:
        return{
            '_id':self._id,
            'email':self.email,
            'firstname':self.firstname,
            'lastname':self.lastname
        }

