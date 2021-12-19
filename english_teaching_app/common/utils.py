#!/usr/bin/env python3
from common.database import Database
from typing import List
from passlib.hash import pbkdf2_sha512
import re

class Utils:
    @staticmethod
    def email_is_valid(email: str) -> bool:
        email_address_matcher = re.compile(r'^[\w_\.-]+@([\w_-]+\.)+[\w_-]+$')
        return True if email_address_matcher.match(email) else False

    @staticmethod
    def hash_password(password: str) -> str:
        return pbkdf2_sha512.encrypt(password)

    @staticmethod
    def check_hashed_password(password: str,hashed_password: str) -> bool:
        return pbkdf2_sha512.verify(password,hashed_password)
